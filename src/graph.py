# graph.py
#
# Copyright 2025 João Pastorello
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from pathlib import Path

import gi
try:
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib
except ImportError or ValueError as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

from matplotlib.backends.backend_gtk4cairo import \
    FigureCanvasGTK4Cairo as FigureCanvas
from matplotlib.figure import Figure

import matplotlib as mpl
import matplotlib.style as mstyle
import matplotlib.dates as mdates
import matplotlib.ticker as mtick


class Graph(FigureCanvas):
    __gtype_name__ = "Graph"

    def __init__(self):
        super().__init__()

        style = Adw.StyleManager.get_default()

        style.connect('notify::dark', self._on_theme_change)

        # The font is not being set currently
        # self._load_fonts()
        self.set_theme(style.get_dark())

        self._setup_figure()

    def _load_fonts(self):
        font_list = mpl.font_manager.findSystemFonts(fontpaths=None,
                                                     fontext='ttf')
        for font in font_list:
            try:
                mpl.font_manager.fontManager.addfont(font)
            except RuntimeError:
                print(f"Could not load {font}")

    def _setup_figure(self):
        self.figure = Figure(layout='constrained')
        self.figure.get_layout_engine().set(w_pad=0.2, h_pad=0.2)
        self._axis = self.figure.add_subplot()

    def _refresh(self):
        self._setup_figure()
        self._redraw()
        self.queue_resize()

    def _on_theme_change(self, style, _):
        self.set_theme(style.get_dark())
        self._refresh()

    def set_theme(self, dark):
        path = Path(GLib.get_system_data_dirs()[0],
                    "surveam", "surveam", 'styles')
        if (dark):
            file = Path(path, "adwaita-dark.mplstyle")
        else:
            file = Path(path, "adwaita.mplstyle")

        mstyle.use(file)

    def set_title(self, title):
        self.title = title

    def set_data(self, df):
        self.df = df

    def _redraw(self):
        self._axis.clear()

        for name in self.df.index.get_level_values("name").drop_duplicates():
            self._axis.plot(self.df.xs(name), label=name)

        self._axis.set_title(self.title)
        leg = self._axis.legend(loc="upper left")
        leg.set_in_layout(False)
        self._axis.set_ylabel('Popularity')

        self._axis.xaxis.set_major_locator(mdates.AutoDateLocator())
        self._axis.xaxis.set_minor_locator(mdates.MonthLocator())
        self._axis.xaxis.set_major_formatter(
            mdates.ConciseDateFormatter(self._axis.xaxis.get_major_locator()))
        self._axis.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0,
                                                                    xmax=1))
        self._axis.grid(True)

        self.draw()

    def update(self, title, df):
        self.set_title(title)
        self.set_data(df)

        self._redraw()

