import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw

from .window import MainWindow

class SteamSurveyExplorerApplication(Adw.Application):
    """The main application singleton class."""

    win = None

    def __init__(self):
        super().__init__(application_id='io.github.jspast.SteamSurveyExplorer',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.connect("shutdown", self.on_shutdown)
        self.win

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = MainWindow(application=self)
        self.win.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Gtk.Builder.new_from_resource(
            '/io/github/jspast/SteamSurveyExplorer/ui/about_dialog.ui'
        ).get_object('about')
        about.present(self.props.active_window)

    def on_shutdown(self, app):
        # Handle application shutdown
        self.win.close_files()

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
    app = SteamSurveyExplorerApplication()
    return app.run(sys.argv)

