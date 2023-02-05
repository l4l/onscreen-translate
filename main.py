from sys import argv

import argparse
from PIL import Image
import pyocr
import pyocr.builders
import pyscreenshot
import argostranslate.package
import argostranslate.translate
import PySimpleGUI as sg

parser = argparse.ArgumentParser(description='Translate selected text.')
parser.add_argument('--box', metavar=('x', 'y', 'w', 'h'), type=int, nargs=4, help='left top/left bottom corners and width/height of translated box')
parser.add_argument('--src', metavar='src', type=str, nargs='?', help='source language to translate from')
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
    print("Not found language package for {} -> {}".format(args.src, args.dest))
    exit(1)

if package_to_install not in argostranslate.package.get_installed_packages():
    argostranslate.package.install_from_path(package_to_install.download())

# Translate
text = argostranslate.translate.translate(txt, args.src, args.dest)

sg.popup(text,
         title='onscreen-translate-py',
         auto_close=True,
         auto_close_duration=3,
         no_titlebar=True,
         keep_on_top=True,
         any_key_closes=True,
         button_type=sg.POPUP_BUTTONS_NO_BUTTONS)
