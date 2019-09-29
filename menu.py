
from easy_widgets import * 
import json 
import os
import sys
import subprocess

Application.init()

conf = None
try:
    f = None
    try:
        f = open("%s/menu.json" % os.getcwd())
    except:
        f = open("%s/.config/menu.json" % os.environ["HOME"])
    conf = json.loads(f.read())
    f.close()
except FileNotFoundError:
    print("Please make ~/.config/menu.json to set up your menu. You can see example of config in repository of this project on GitHub, just visit github.com/fantastic001/curses-menu.")
    exit(1)

def execute_process(x, params):
    item, menu = params
    subprocess.call(item["path"])
    menu.show()

def create_menu(title, items):
    menu = Menu(title)
    for item in items:
        if item["type"] == "submenu":
            submenu = create_menu(item["title"], item["items"])
            submenu.addOption("Back", lambda x, p: menu.show())
            menu.addOption(item["title"], lambda x, p: submenu.show())
        elif item["type"] == "executable":
            menu.addOption(item["title"], execute_process, params=[item, menu])
        else:
            print("Wrong item type: %s" % item["type"])
            exit(1)
    return menu

menu = create_menu("Main menu", conf["items"])
menu.show()
Application.run()
