from gi.repository import Adw, Gio, Gtk, GObject, GLib

import threading

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
            label.set_property("ellipsize", "middle")
            label.set_selectable(True)
            list_item.set_child(label)

        def _on_factory_setup_percentage(_factory, list_item):
            label = Gtk.Label(halign=Gtk.Align.END)
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

        def str_sorter(object_a, object_b, column) -> bool:
            a = getattr(object_a, column).lower()
            b = getattr(object_b, column).lower()
            return (a > b) - (a < b)

        def percent_to_int(string):
            return int(string[:-1].replace('.', ''))

        def percent_sorter(object_a, object_b, column) -> bool:
            a = percent_to_int(getattr(object_a, column))
            b = percent_to_int(getattr(object_b, column))
            return (a > b) - (a < b)

        self.name_factory.connect("setup", _on_factory_setup_name)
        self.percentage_factory.connect("setup", _on_factory_setup_percentage)
        self.change_factory.connect("setup", _on_factory_setup_change)

        self.name_factory.connect("bind", _on_factory_bind, "name")
        self.name_column.set_factory(self.name_factory)
        self.name_column.set_sorter(Gtk.CustomSorter.new(str_sorter, "name"))

        self.percentage_factory.connect("bind", _on_factory_bind, "percentage")
        self.percentage_column.set_factory(self.percentage_factory)
        self.percentage_column.set_sorter(Gtk.CustomSorter.new(percent_sorter, "percentage"))

        self.change_factory.connect("bind", _on_factory_bind, "change")
        self.change_column.set_factory(self.change_factory)
        self.change_column.set_sorter(Gtk.CustomSorter.new(percent_sorter, "change"))

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

    stack = Gtk.Template.Child()

    date_dropdown = Gtk.Template.Child()

    windows_list = Gtk.Template.Child()
    combined_list = Gtk.Template.Child()
    linux_list = Gtk.Template.Child()
    mac_list = Gtk.Template.Child()

    db = open_database()

    moment = int()

    loaded_pages = [False, False, False, False]

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

        load_data(self.db, csv_file_like)
        self.populate_date_dropdown()

        if self.date_dropdown.get_selected() == None:
            self.date_dropdown.set_selected(0)

    def populate_date_dropdown(self):
        moment_strings = Gtk.StringList()
        self.date_dropdown.props.model = moment_strings

        moments = get_moments(self.db)
        for moment in moments:
            #pos = self.db.search_id("moment", moment, Moment.id, sizeof(Moment))
            #record = self.db.get_record("moment", pos, sizeof(Moment))
            #month = self.db.get_record_field_int_value(record, Moment.month, False)
            #year = 2000 + self.db.get_record_field_int_value(record, Moment.year, False)
            moment_strings.append(str(moment))

    def on_date_selected(self, dropdown, _pspec):
        # Selected Gtk.StringObject
        selected = self.date_dropdown.props.selected_item

        if selected is not None:
            self.moment = int(selected.props.string)
            self.loaded_pages = [False, False, False, False]
            self.populate_platform()

    def on_page_changed(self, stack, _pspec):
        self.populate_platform()

    def populate_platform(self):
        platform = self.stack.get_visible_child_name()[0].lower()

        if platform == 'c' and self.loaded_pages[0] == False:
            list = self.combined_list
            self.loaded_pages[0] = True
        elif platform == 'w' and self.loaded_pages[1] == False:
            list = self.windows_list
            self.loaded_pages[1] = True
        elif platform == 'l' and self.loaded_pages[2] == False:
            list = self.linux_list
            self.loaded_pages[2] = True
        elif platform == 'm' and self.loaded_pages[3] == False:
            list = self.mac_list
            self.loaded_pages[3] = True
        else:
            return

        # Clear existing items
        child = list.get_first_child()
        while child != None:
            list.remove(child)
            child = list.get_first_child()

        spinner = Gtk.Spinner()
        spinner.set_property("height-request", 32)
        list.append(spinner)
        spinner.start()

        threading.Thread(target=self.fetch_and_process_categories, args=(platform, list)).start()

    def fetch_and_process_categories(self, platform, list):
        # Fetch categories from the database
        categories = get_categories(self.db, platform, self.moment)

        # Update the UI with the categories
        GLib.idle_add(self.update_ui, categories, list)

    def update_ui(self, categories, list):

        child = list.get_first_child()
        list.remove(child)

        if categories == []:
            no_data = Adw.StatusPage()
            no_data.set_title("No Results Found")
            no_data.set_description("Try a different search or survey date")
            list.append(no_data)

        else:
            for category in categories:
                box = CategoryBox(category[0], category[1][0][0], category[1][0][1])
                list.append(box)
                box.populate_column_view(category[1])

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

        self.date_dropdown.connect('notify::selected-item', self.on_date_selected)

        self.stack.connect('notify::visible-child-name', self.on_page_changed)

        self.populate_date_dropdown()

