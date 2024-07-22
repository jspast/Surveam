from gi.repository import Adw, Gio, Gtk, GObject

import numpy as np

from matplotlib.backends.backend_gtk4agg import \
    FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib as mpl
import matplotlib.pyplot as plt

plt.style.use(['dark_background'])
mpl.rcParams['axes.facecolor'] = ('#242424')
mpl.rcParams['figure.facecolor'] = ('#242424')
mpl.rcParams['savefig.transparent'] = True


@Gtk.Template(resource_path='/io/github/jspast/SteamSurveyExplorer/ui/category_window.ui')
class CategoryWindow(Adw.Window):
    __gtype_name__ = 'CategoryWindow'

    chart_window = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(title='Linux Version')
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2*np.pi*t)
        ax.plot(t, s)

        canvas = FigureCanvas(fig)
        self.chart_window.set_child(canvas)
