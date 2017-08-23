import logging
import sys

import click
from PyQt5 import QtWidgets

from smlgui import __version__
from smlgui.ui import Home
from smlgui.utility import is_windows, load_stylesheet, get_sml_conf

conf = get_sml_conf()


@click.command()
@click.option('--debug', is_flag=True, help="Verbose logging. Defaults to 0, add 1 for verbose logging.")
@click.option('--version', '-v', is_flag=True, help="Show the version number.")
def main(debug, version):
    """
    Runs the main app, if ``--debug=1`` a more verbose logging is shown.

    Parameters
    ----------
    version
    debug
    """
    global conf

    if debug:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d [%(threadName)s]: %('
                                   'message)s')
    elif version:
        click.echo("Version " + __version__)
        sys.exit()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    if is_windows():
        import ctypes
        my_app_id = 'gollahalli.sml_gui.' + __version__
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    app = QtWidgets.QApplication(sys.argv)
    window = Home()

    if conf['DEFAULT']['dark_mode'] == "true":
        app.setStyleSheet(load_stylesheet())
    else:
        app.setStyleSheet("")

    sys.exit(app.exec_())
