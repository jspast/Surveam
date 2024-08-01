from gi.repository import Adw, Gio, Gtk, GObject

import numpy as np

from matplotlib.backends.backend_gtk4agg import \
    FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib as mpl
import matplotlib.pyplot as plt

style = Adw.StyleManager.get_default()

# Forces theme for testing
#style.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)

# Set correct colors for matplotlib based on the app's active theme
if (style.get_property("dark")):
    plt.style.use(['dark_background'])
    mpl.rcParams['axes.facecolor'] = ('#242424')
    mpl.rcParams['figure.facecolor'] = ('#242424')
else:
    mpl.rcParams['axes.facecolor'] = ('#fafafa')
    mpl.rcParams['figure.facecolor'] = ('#fafafa')


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

        # Exemplo para teste da interface:

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(title='Linux Version')
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2*np.pi*t)
        ax.plot(t, s)

        canvas = FigureCanvas(fig)
        self.chart_window.set_child(canvas)
