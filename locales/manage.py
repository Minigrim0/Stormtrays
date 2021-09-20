import sys

command = sys.argv[1]
app = sys.argv[2]


def maketrans():
    pass


def compiletrans():
    pass


def addapp():
    pass


availabe_commands = {
    "maketrans": ,
    "compiletrans": ,
    "addapp": 
}

if command not in availabe_commands:
    raise NotImplementedError(f"command {command} not found !")

if command == availabe_commands[0]:
    # Make the messages for all the locales
    pass
elif command == availabe_commands[0]:
    # Make the messages for all the locales
    pass
elif command == availabe_commands[3]:
    # Make the messages for all the locales
    pass

print(command, app)

exec = "usr/lib/python3.9/Tools/i18n/pygettext.py -d quit_menu -o locales/quit_menu.pot UI/menus/quit.py"
