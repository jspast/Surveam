# window.py
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

import gi
try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw
except ImportError or ValueError as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

from .graph import Graph


@Gtk.Template(resource_path='/io/github/jspast/Surveam/window.ui')
class Window(Adw.ApplicationWindow):
    __gtype_name__ = 'Window'

    title = Gtk.Template.Child()

    graph = Gtk.Template.Child()

    platform_dropdown = Gtk.Template.Child()
    category_dropdown = Gtk.Template.Child()
    start_date_dropdown = Gtk.Template.Child()
    end_date_dropdown = Gtk.Template.Child()
    items_wrapbox = Gtk.Template.Child()
    items_switch = Gtk.Template.Child()

    legend_switch = Gtk.Template.Child()

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)

        self.data = data

        self.platform_dropdown.connect('notify::selected-item',
                                       self._on_platform_selected)

        self.category_dropdown.connect('notify::selected-item',
                                       self._on_category_selected)

        self._connect_date_dropdowns()
        self._populate_platform_dropdown()

        self.legend_switch.set_active(True)

    def _connect_date_dropdowns(self):
        self.start_date_signal = self.start_date_dropdown.connect(
                                    'notify::selected-item',
                                    self._on_start_date_selected)

        self.end_date_signal = self.end_date_dropdown.connect(
                                    'notify::selected-item',
                                    self._on_end_date_selected)

    def _disconnect_date_dropdowns(self):
        self.start_date_dropdown.disconnect(self.start_date_signal)
        self.end_date_dropdown.disconnect(self.end_date_signal)

    def _populate_platform_dropdown(self):
        self.platform_list = Gtk.StringList.new(self.data.get_platforms())
        self.platform_dropdown.set_model(self.platform_list)

    def _on_platform_selected(self, dropdown, _):
        self.selected_platform = dropdown.get_selected_item().get_string()
        self.title.set_subtitle(self.selected_platform)

        self._populate_category_dropdown()

    def _populate_category_dropdown(self):
        self.category_list = Gtk.StringList.new(
                              self.data.get_categories(self.selected_platform))
        self.category_dropdown.set_model(self.category_list)

    def _on_category_selected(self, dropdown, _):
        self.selected_category = dropdown.get_selected_item().get_string()
        self.title.set_title(self.selected_category)

        self._populate_date_dropdowns()

    def _populate_date_dropdowns(self):
        self._disconnect_date_dropdowns()

        self.dates = self.data.get_dates(self.selected_platform,
                                         self.selected_category)
        self.start_date_list = Gtk.StringList.new(self.dates[:-1])
        self.end_date_list = Gtk.StringList.new(self.dates[1:])
        self.start_date_dropdown.set_model(self.start_date_list)
        self.start_date_dropdown.set_selected(0)
        self.end_date_dropdown.set_model(self.end_date_list)
        self.end_date_dropdown.set_selected(- 1
                                            + self.end_date_list.get_n_items())

        self.start_date = self.dates[self.start_date_dropdown.get_selected()]
        self.end_date = self.dates[self.end_date_dropdown.get_selected() + 1]

        self._connect_date_dropdowns()
        self._update_graph()

    def _on_start_date_selected(self, dropdown, _):
        start_date_num = dropdown.get_selected()

        # In this case, this is faster than
        # dropdown.get_selected_item().get_string():
        self.start_date = self.dates[start_date_num]

        end_date_offset = (1 + start_date_num - len(self.dates)
                           + self.end_date_list.get_n_items())

        if (end_date_offset >= 0):
            self.end_date_list.splice(0, end_date_offset)
        else:
            self.end_date_list.splice(0, 0, self.dates[start_date_num + 1:
                                                       start_date_num + 1
                                                       - end_date_offset])
        self._update_graph()

    def _on_end_date_selected(self, dropdown, _):
        end_date_num = dropdown.get_selected()

        # In this case, this is faster than
        # self.dates[end_date_num + ...]:
        self.end_date = dropdown.get_selected_item().get_string()

        start_date_list_size = self.start_date_list.get_n_items()
        end_date_list_size = self.end_date_list.get_n_items()

        start_date_offset = (end_date_num
                             + len(self.dates)
                             - end_date_list_size
                             - start_date_list_size)

        if (start_date_offset <= 0):
            self.start_date_list.splice(start_date_list_size
                                        + start_date_offset,
                                        - start_date_offset)
        else:
            self.start_date_list.splice(start_date_list_size, 0,
                                        self.dates[start_date_list_size:
                                                   start_date_list_size
                                                   + start_date_offset])

        self._update_graph()

    def _update_graph(self):

        self.graph_data = self.data.get_category_data(self.selected_platform,
                                                      self.selected_category,
                                                      self.start_date,
                                                      self.end_date)

        self._update_items()

        self.graph.update(self.selected_category,
                          self.graph_data,
                          self.items_visibility)

    def _on_item_toggled(self, button):
        self.items_visibility[button.get_label()] = button.get_active()
        self.graph.update_item_visibility(self.items_visibility)

    @staticmethod
    def _remove_children(box):
        while (box.get_first_child()):
            box.remove(box.get_first_child())

    def _clear_items(self):
        Window._remove_children(self.items_wrapbox)

    def _add_items(self):
        items = self.data.get_item_names(self.graph_data)
        for item in items:
            button = Gtk.ToggleButton(label=item, active=True)
            button.set_can_shrink(True)
            button.connect('toggled', self._on_item_toggled)
            self.items_wrapbox.prepend(button)

        self.items_visibility = {item: True for item in items}

    def _update_items(self):
        self._clear_items()
        self._add_items()
