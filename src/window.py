from gi.repository import Adw, Gio, Gtk, GObject

from .category_window import CategoryWindow

from .load_data import *

from io import StringIO

class Item(GObject.Object):
    def __init__(self, name, percentage, change):
        super().__init__()

        self._name = name
        self._percentage = percentage
        self._change = change

    @GObject.Property(type=str)
    def name(self) -> str:
        return self._name

    @GObject.Property(type=str)
    def percentage(self) -> str:
        return self._percentage

    @GObject.Property(type=str)
    def change(self) -> str:
        return self._change

@Gtk.Template(resource_path='/io/github/jspast/SteamSurveyExplorer/ui/category_box.ui')
class CategoryBox(Gtk.ListBox):
    __gtype_name__ = 'Category'

    expander_row = Gtk.Template.Child()
    item_name_label = Gtk.Template.Child()
    item_percentage_label = Gtk.Template.Child()

    column_view = Gtk.Template.Child()
    name_column = Gtk.Template.Child()
    percentage_column = Gtk.Template.Child()
    change_column = Gtk.Template.Child()

    name_factory = Gtk.SignalListItemFactory()
    percentage_factory = Gtk.SignalListItemFactory()
    change_factory = Gtk.SignalListItemFactory()

    def __init__(self, category_name, item_name, item_percentage):
        super().__init__()

        self.expander_row.set_property("title", category_name)
        self.item_name_label.set_property("label", item_name)
        self.item_percentage_label.set_property("label", item_percentage)

        self.setup_column_view()

    def setup_column_view(self):
        super().__init__()

        def model_func(_item):
            pass

        self.store = Gio.ListStore(item_type=Item)
        tree_model = Gtk.TreeListModel.new(self.store, False, True, model_func)
        tree_sorter = Gtk.TreeListRowSorter.new(self.column_view.get_sorter())
        sorter_model = Gtk.SortListModel(model=tree_model, sorter=tree_sorter)
        selection = Gtk.NoSelection.new(model=sorter_model)
        self.column_view.set_model(model=selection)

        def _on_factory_setup_name(_factory, list_item):
            label = Gtk.Label(halign=Gtk.Align.START)
            label.set_selectable(True)
            list_item.set_child(label)

        def _on_factory_setup_percentage(_factory, list_item):
            label = Gtk.Label(halign=Gtk.Align.END)
            label.set_property("ellipsize", "end")
            label.set_property("css_classes", ["monospace"])
            label.set_selectable(True)
            list_item.set_child(label)

        def _on_factory_setup_change(_factory, list_item):
            label = Gtk.Label(halign=Gtk.Align.END)
            label.set_property("css_classes", ["monospace"])
            label.set_selectable(True)
            list_item.set_child(label)

        def _on_factory_bind(_factory, list_item, what):
            label_widget = list_item.get_child()
            item = list_item.get_item().get_item()
            label = str(getattr(item, what))
            label_widget.set_label(label)

            if what == "change":
                if label[0] == "-":
                    label_widget.set_property("css_classes", ["error", "monospace"])
                elif label[0] == "+":
                    label_widget.set_property("css_classes", ["success", "monospace"])

        self.name_factory.connect("setup", _on_factory_setup_name)
        self.percentage_factory.connect("setup", _on_factory_setup_percentage)
        self.change_factory.connect("setup", _on_factory_setup_change)

        self.name_factory.connect("bind", _on_factory_bind, "name")
        self.name_column.set_factory(self.name_factory)

        self.percentage_factory.connect("bind", _on_factory_bind, "percentage")
        self.percentage_column.set_factory(self.percentage_factory)

        self.change_factory.connect("bind", _on_factory_bind, "change")
        self.change_column.set_factory(self.change_factory)

    def populate_column_view(self, list):
        super().__init__()

        for name, percentage, change in list:
            self.store.append(Item(name, percentage, change))

    @Gtk.Template.Callback()
    def on_category_action(self, *args):
        category_win = CategoryWindow()
        category_win.present()

@Gtk.Template(resource_path='/io/github/jspast/SteamSurveyExplorer/ui/main_window.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    search_bar_box = Gtk.Template.Child()
    windows_list = Gtk.Template.Child()
    combined_list = Gtk.Template.Child()
    linux_list = Gtk.Template.Child()
    mac_list = Gtk.Template.Child()
    stack = Gtk.Template.Child()

    def open_file_dialog(self, action, _):
        # Create a new file selection dialog, using the "open" mode
        native = Gtk.FileDialog()
        native.open(self, None, self.on_open_response)

    def on_open_response(self, dialog, result):
        file = dialog.open_finish(result)
        # If the user selected a file...
        if file is not None:
            # ... open it
            self.open_file(file)

    def open_file(self, file):
        file.load_contents_async(None, self.open_file_complete)

    def open_file_complete(self, file, result):
        contents = file.load_contents_finish(result)
        if not contents[0]:
            path = file.peek_path()
            print(f"Unable to open {path}: {contents[1]}")

        csv_string = contents[1].decode('utf-8')
        csv_file_like = StringIO(csv_string)

        db = open_database()
        load_data(db, csv_file_like)
        close_database(db)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        open_action = Gio.SimpleAction(name="open-csv")
        open_action.connect("activate", self.open_file_dialog)
        self.add_action(open_action)

        self.settings = Gio.Settings(schema_id="io.github.jspast.SteamSurveyExplorer")
        self.settings.bind("window-width", self, "default-width",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("window-height", self, "default-height",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("window-maximized", self, "maximized",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("platform-page", self.stack, "visible-child-name",
                           Gio.SettingsBindFlags.DEFAULT)

        # Exemplo para teste da interface:
        db = open_database()

        combined_categories = get_categories(db, 'c', 2407)
        for category in combined_categories:
            box = CategoryBox(category[0], category[1][0][0], category[1][0][1])
            self.combined_list.append(box)
            box.populate_column_view(category[1])

        windows_categories = get_categories(db, 'w', 2407)
        for category in windows_categories:
            box = CategoryBox(category[0], category[1][0][0], category[1][0][1])
            self.windows_list.append(box)
            box.populate_column_view(category[1])

        linux_categories = get_categories(db, 'l', 2407)
        for category in linux_categories:
            box = CategoryBox(category[0], category[1][0][0], category[1][0][1])
            self.linux_list.append(box)
            box.populate_column_view(category[1])

        mac_categories = get_categories(db, 'm', 2407)
        for category in mac_categories:
            box = CategoryBox(category[0], category[1][0][0], category[1][0][1])
            self.mac_list.append(box)
            box.populate_column_view(category[1])

