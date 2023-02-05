from sys import argv
from textwrap import wrap

import argparse
from PIL import Image
import pyocr
import pyocr.builders
import pyscreenshot
import argostranslate.package
import argostranslate.translate
import gi

gi.require_version("Gtk", "3.0")

has_layer_shell = False
try:
    gi.require_version("GtkLayerShell", "0.1")
    has_layer_shell = True
except:
    pass

from gi.repository import Gtk, Gdk, GLib, GtkLayerShell

parser = argparse.ArgumentParser(description='Translate selected text.')
parser.add_argument('--box', metavar=('x', 'y', 'w', 'h'), type=int, nargs=4, help='left top/left bottom corners and width/height of translated box')
parser.add_argument('--src', metavar='src', type=str, required=True, help='source language to translate from')
parser.add_argument('--dest', metavar='dest', action='store', type=str, default='en', help='destination language to translate to')

args = parser.parse_args()


[x, y, dx, dy] = args.box
img = pyscreenshot.grab(bbox=(x, y, x + dx, y + dy))

tool = pyocr.get_available_tools()[0]
txt = tool.image_to_string(
    img,
    lang='eng',
    builder=pyocr.builders.TextBuilder()
)

# newlines are not handled properly so just join all the lines
txt = ' '.join([line.strip() for line in txt.split('\n')])

argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == args.src and x.to_code == args.dest, available_packages
    )
)
if package_to_install is None:
    print('Not found language package for {} -> {}'.format(args.src, args.dest))
    exit(1)

if package_to_install not in argostranslate.package.get_installed_packages():
    print('Installing package: {}'.format(package_to_install))
    argostranslate.package.install_from_path(package_to_install.download())

text = argostranslate.translate.translate(txt, args.src, args.dest)
text = '\n'.join(wrap(text, 60))

win = Gtk.Window(title='onscreen-translate-py')
Gtk.Widget.set_opacity(win, 0.95)
win.set_type_hint(Gdk.WindowTypeHint.TOOLTIP)

if has_layer_shell:
    GtkLayerShell.init_for_window(win)
    GtkLayerShell.auto_exclusive_zone_enable(win)
    GtkLayerShell.set_layer(win, GtkLayerShell.Layer.OVERLAY)

label = Gtk.Label(label=text)
label.set_margin_top(40)
label.set_margin_bottom(40)
label.set_margin_start(40)
label.set_margin_end(40)
win.add(label)

win.connect("destroy", Gtk.main_quit)
win.show_all()

GLib.timeout_add(3000, Gtk.Window.destroy, win)

Gtk.main()
