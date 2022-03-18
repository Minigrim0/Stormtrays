import os
import sys
import json
import shutil
import subprocess

command = sys.argv[1]


def makeTrans():
    """Creates the POT files and the po files from the code"""
    with open("locales/settings.json") as settings_file:
        settings = json.load(settings_file)
        apps = settings["apps"]
        langs = settings["langs"]

    files = [file for _, file in apps.items()]
    full_command = ["/usr/lib/python3.9/Tools/i18n/pygettext.py", "-d", "stormtrays", "-o", "locales/stormtrays.pot"]
    full_command.extend(files)
    subprocess.run(full_command, check=True)

    for lang in langs:
        if os.path.exists(f"locales/{lang}/LC_MESSAGES/stormtrays.po"):
            subprocess.run(
                [
                    "/usr/bin/msgmerge", "-vU", f"locales/{lang}/LC_MESSAGES/stormtrays.po", "locales/stormtrays.pot"
                ],
                check=True
            )
        else:
            shutil.copy("locales/stormtrays.pot", f"locales/{lang}/LC_MESSAGES/stormtrays.po")


def compileTrans():
    """Compiles all the po files into mo files"""
    with open("locales/settings.json") as settings_file:
        settings = json.load(settings_file)
        langs = settings["langs"]

    for lang in langs:
        full_command = [
            "/usr/bin/msgfmt", "-o", f"locales/{lang}/LC_MESSAGES/stormtrays.mo", f"locales/{lang}/LC_MESSAGES/stormtrays.po"
        ]
        subprocess.run(full_command, check=True)


def addApp():
    """Adds an app to be translated"""
    if len(sys.argv) < 4:
        raise RuntimeError("Missing parameters for command addapp")
    app = sys.argv[2]
    path = sys.argv[3]

    with open("locales/settings.json", "r") as settings_file:
        data = json.load(settings_file)
        data["apps"][app] = path
    with open("locales/settings.json", "w") as settings_file:
        json.dump(data, settings_file, indent=4)


availabe_commands = {
    "maketrans": makeTrans,
    "compiletrans": compileTrans,
    "addapp": addApp
}

if command not in availabe_commands:
    raise NotImplementedError(f"command {command} not found !")

availabe_commands[command]()