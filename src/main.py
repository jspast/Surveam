# main.py
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
    gi.require_version('Adw', '1')
    from gi.repository import Gio, Adw
except ImportError or ValueError as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

from .window import Window
from .data import Data


class Application(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.jspast.Surveam',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.connect("shutdown", self.on_shutdown)

        self.data = Data()
        self.data.load_from_original_csvs()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = Window(application=self, data=self.data)
        win.present()

    def on_shutdown(self, app):
        pass

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(application_name='Surveam',
                                application_icon='io.github.jspast.Surveam',
                                developer_name='João Pastorello',
                                version='1.0.0',
                                developers=['João Pastorello'],
                                copyright='© 2025 João Pastorello')
        # Translators: Replace "translator-credits" with your name/username,
        # and optionally an email or URL.
        about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = Application()
    return app.run(sys.argv)
