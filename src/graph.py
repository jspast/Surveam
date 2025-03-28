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
    from gi.repository import Adw, GLib, GObject
except ImportError or ValueError as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

import gio_pyio

import matplotlib as mpl
import matplotlib.style as mstyle
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt

from matplotlib.backends.backend_gtk4cairo import \
    FigureCanvasGTK4Cairo as FigureCanvas

LEGEND_POSITIONS = [
    "best",
    "upper right",
    "upper left",
    "lower left",
    "lower right",
    "center left",
    "center right",
    "lower center",
    "upper center",
    "center",
]


class Graph(FigureCanvas):
    __gtype_name__ = "Graph"

    def __init__(self):
        super().__init__()

        style = Adw.StyleManager.get_default()
        style.connect('notify::dark', self._on_theme_change)

        self._legend = True
        self._legend_position = LEGEND_POSITIONS[0]

        self._load_fonts()
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
        self.figure = plt.figure(layout='constrained')
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

    def set_items_visibility(self, items_visibility):
        self.items_visibility = items_visibility

    def _redraw(self):
        self._axis.clear()

        for name in self.df.index.get_level_values("name").drop_duplicates():
            if (self.filter_items):
                if (self.items_visibility[name]):
                    self._axis.plot(self.df.xs(name), label=name)
            else:
                self._axis.plot(self.df.xs(name), label=name)

        self._axis.set_title(self.title)

        self._handles = self._axis.get_legend_handles_labels()[0]
        self.update_legend()

        self._axis.set_ylabel('Popularity')

        self._axis.xaxis.set_major_locator(mdates.AutoDateLocator())
        self._axis.xaxis.set_minor_locator(mdates.MonthLocator())
        self._axis.xaxis.set_major_formatter(
            mdates.ConciseDateFormatter(self._axis.xaxis.get_major_locator()))
        self._axis.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0,
                                                                    xmax=1))
        self._axis.grid(True)

        self.draw()

    def update(self, title, df, items_visibility):
        self.set_title(title)
        self.set_data(df)
        self.set_items_visibility(items_visibility)

        self._redraw()

    def update_item_visibility(self, items_visibility):
        self.set_items_visibility(items_visibility)

        self._redraw()

    def update_legend(self) -> None:
        """Update the legend or hide if not used."""
        if self._legend and self._handles:
            leg = self._axis.legend(
                handles=self._handles,
                loc=self._legend_position,
                frameon=True,
                reverse=True,
            )
            leg.set_in_layout(False)
            self.queue_draw()
            return
        legend = self._axis.get_legend()
        if legend is not None:
            legend.remove()
        self.queue_draw()

    @GObject.Property(type=bool, default=False)
    def filter_items(self) -> bool:
        """Whether or not, the legend is visible."""
        return self._filter_items

    @filter_items.setter
    def filter_items(self, filter_items: bool) -> None:
        self._filter_items = filter_items
        self._redraw()

    @GObject.Property(type=bool, default=True)
    def legend(self) -> bool:
        """Whether or not, the legend is visible."""
        return self._legend

    @legend.setter
    def legend(self, legend: bool) -> None:
        self._legend = legend
        self.update_legend()

    @GObject.Property(type=int, default=0)
    def legend_position(self) -> int:
        """Legend Position (see `LEGEND_POSITIONS`)."""
        return LEGEND_POSITIONS.index(self._legend_position)

    @legend_position.setter
    def legend_position(self, legend_position: int) -> None:
        self._legend_position = LEGEND_POSITIONS[legend_position]
        self.update_legend()

    @GObject.Property(type=str)
    def title(self) -> str:
        """Figure title."""
        return self._axis.get_title()

    @title.setter
    def title(self, title: str) -> None:
        self._axis.set_title(title, picker=True).id = "title"
        self.queue_draw()

    @GObject.Property(type=str)
    def bottom_label(self) -> str:
        """Label of the bottom axis."""
        return self._axis.get_xlabel()

    @bottom_label.setter
    def bottom_label(self, label: str) -> None:
        self._axis.set_xlabel(label, picker=True).id = "bottom_label"
        self.queue_draw()

    @GObject.Property(type=str)
    def left_label(self) -> str:
        """Label of the left axis."""
        return self._axis.get_ylabel()

    @left_label.setter
    def left_label(self, label: str) -> None:
        self._axis.set_ylabel(label, picker=True).id = "left_label"
        self.queue_draw()

    @GObject.Property(type=float)
    def min_bottom(self) -> float:
        """Lower limit for the bottom axis."""
        return self._axis.get_xlim()[0]

    @min_bottom.setter
    def min_bottom(self, value: float) -> None:
        self._axis.set_xlim(value, None)
        self.queue_draw()

    @GObject.Property(type=float)
    def max_bottom(self) -> float:
        """Upper limit for the bottom axis."""
        return self._axis.get_xlim()[1]

    @max_bottom.setter
    def max_bottom(self, value: float) -> None:
        self._axis.set_xlim(None, value)
        self.queue_draw()
