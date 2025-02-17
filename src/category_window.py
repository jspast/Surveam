from gi.repository import Adw, Gio, Gtk, GObject

@Gtk.Template(resource_path='/io/github/jspast/SteamSurveyExplorer/ui/category_window.ui')
class CategoryWindow(Adw.Window):
    __gtype_name__ = 'CategoryWindow'

    stack = Gtk.Template.Child()
    chart_window = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings(schema_id="io.github.jspast.SteamSurveyExplorer")
        self.settings.bind("category-window-width", self, "default-width",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("category-window-height", self, "default-height",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("category-window-maximized", self, "maximized",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("category-chart-page", self.stack, "visible-child-name",
                           Gio.SettingsBindFlags.DEFAULT)

        # ToDo: Implementar gráfico
