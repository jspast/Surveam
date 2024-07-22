from gi.repository import Adw, Gio, Gtk, GObject

@Gtk.Template(resource_path='/io/github/jspast/SteamSurveyExplorer/ui/main_window.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    search_bar_box = Gtk.Template.Child()
    windows_list = Gtk.Template.Child()

    def on_windows_version_expanded(self, widget, _):
        if (self.windows_version.get_property("expanded") == False):
            self.windows_label1.set_property("visible", True)
            self.windows_label2.set_property("visible", True)
            self.windows_label3.set_property("visible", True)
            self.windows_graph.set_property("visible", False)
        else:
            self.windows_label1.set_property("visible", False)
            self.windows_label2.set_property("visible", False)
            self.windows_label3.set_property("visible", False)
            self.windows_graph.set_property("visible", True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.windows_version = Adw.ExpanderRow()
        self.windows_list.append(self.windows_version)
        self.windows_version.set_property("title", "Linux Version")
        self.windows_version.set_property("title-lines", 1)

        self.windows_graph = Gtk.Button()
        self.windows_version.add_suffix(self.windows_graph)
        self.windows_graph.set_property("icon-name", "graph-symbolic")
        self.windows_graph.set_property("visible", False)
        self.windows_graph.set_property("has-frame", False)
        self.windows_graph.set_property("valign", "center")
        self.windows_graph.set_property("action-name", "app.category")

        self.windows_label3 = Gtk.Label(label='-1.89%')
        self.windows_version.add_suffix(self.windows_label3)
        self.windows_label3.set_property("width-chars", 7)
        self.windows_label3.set_property("halign", "end")
        self.windows_label3.set_property("css-classes", ["error"])

        self.windows_label2 = Gtk.Label(label='42.33%')
        self.windows_version.add_suffix(self.windows_label2)
        self.windows_label2.set_property("width-chars", 7)

        self.windows_label1 = Gtk.Label(label='"SteamOS Holo" 64 bit')
        self.windows_version.add_suffix(self.windows_label1)
        self.windows_label1.set_property("ellipsize", "end")

        for x in range(10):
            self.windows_version2 = Adw.ExpanderRow()
            self.windows_list.append(self.windows_version2)
            self.windows_version2.set_property("title", "System RAM")
            self.windows_version2.set_property("title-lines", 1)

        self.windows_version.connect("notify::expanded", self.on_windows_version_expanded)

        self.windows_frame = Gtk.Frame()
        self.windows_version.add_row(self.windows_frame)

        self.windows_tabela = Gtk.ColumnView()
        self.windows_frame.set_child(self.windows_tabela)
        self.windows_tabela.set_property("show-row-separators", True)

        self.windows_col1 = Gtk.ColumnViewColumn()
        self.windows_tabela.append_column(self.windows_col1)
        self.windows_col1.set_property("title", "Name")
        self.windows_col1.set_property("expand", True)

        self.windows_col2 = Gtk.ColumnViewColumn()
        self.windows_tabela.append_column(self.windows_col2)
        self.windows_col2.set_property("title", "Percentage")

        self.windows_col3 = Gtk.ColumnViewColumn()
        self.windows_tabela.append_column(self.windows_col3)
        self.windows_col3.set_property("title", "Change")

        # Create the data model
        self.data_model = Gio.ListStore(item_type=Distro)
        for name, distro_info in distros.items():
            self.data_model.append(Distro(name=name, percentage=distro_info[0], change=distro_info[1]))

        def model_func(_item):
            pass

        tree_model = Gtk.TreeListModel.new(self.data_model, False, True, model_func)
        tree_sorter = Gtk.TreeListRowSorter.new(self.windows_tabela.get_sorter())
        sorter_model = Gtk.SortListModel(model=tree_model, sorter=tree_sorter)
        selection = Gtk.SingleSelection.new(model=sorter_model)
        self.windows_tabela.set_model(model=selection)

        def _on_factory_setup_name(_factory, list_item):
            label = Gtk.Label(halign=Gtk.Align.START)
            label.set_selectable(True)
            list_item.set_child(label)

        def _on_factory_setup_percentage(_factory, list_item):
            label = Gtk.Label(halign=Gtk.Align.END)
            label.set_property("ellipsize", "end")
            label.set_selectable(True)
            list_item.set_child(label)

        def _on_factory_setup_change(_factory, list_item):
            label = Gtk.Label(halign=Gtk.Align.START)
            label.set_selectable(True)
            list_item.set_child(label)

        def _on_factory_bind(_factory, list_item, what):
            label_widget = list_item.get_child()
            distro = list_item.get_item().get_item()
            label = str(getattr(distro, what))
            label_widget.set_label(label)

            if (what == "change"):
                if (label[0] == "-"):
                    label_widget.set_property("css_classes", ["error"])
                elif (label[0] == "+"):
                    label_widget.set_property("css_classes", ["success"])


        factory1 = Gtk.SignalListItemFactory()
        factory2 = Gtk.SignalListItemFactory()
        factory3 = Gtk.SignalListItemFactory()

        factory1.connect("setup", _on_factory_setup_name)
        factory2.connect("setup", _on_factory_setup_percentage)
        factory3.connect("setup", _on_factory_setup_change)

        factory1.connect("bind", _on_factory_bind, "name")
        self.windows_col1.set_factory(factory1)

        factory2.connect("bind", _on_factory_bind, "percentage")
        self.windows_col2.set_factory(factory2)

        factory3.connect("bind", _on_factory_bind, "change")
        self.windows_col3.set_factory(factory3)

        # Custom Sorter is required because PyGObject doesn't currently support
        # Gtk.Expression: https://gitlab.gnome.org/GNOME/pygobject/-/issues/356

        def str_sorter(object_a, object_b, column) -> bool:
            a = getattr(object_a, column).lower()
            b = getattr(object_b, column).lower()
            return (a > b) - (a < b)

        def percentage_sorter(object_a, object_b, column) -> bool:
            print(object_a)
            a0 = getattr(object_a, column)
            b0 = getattr(object_b, column)

            return (a > b) - (a < b)

        self.windows_col1.set_sorter(Gtk.CustomSorter.new(str_sorter, "name"))
        """
        self.windows_col2.set_sorter(Gtk.CustomSorter.new(str_sorter, "percentage"))
        self.windows_col3.set_sorter(Gtk.CustomSorter.new(str_sorter, "change"))
        """

class Distro(GObject.Object):
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

distros = {
    '"SteamOS Holo" 64 bit': ("42.33%", "-1.89%"),
    '"Arch Linux" 64 bit': ("8.24%", "+0.58%"),
    'Ubuntu 22.04.4 LTS 64 bit': ("6.13%", "+0.59%")
}
