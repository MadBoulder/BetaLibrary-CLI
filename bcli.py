from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog, yes_no_dialog, input_dialog, button_dialog, radiolist_dialog
import os

CONFIG_FILE = "config.txt"
# Actions
CREATE = 0
MODIFY = 1
DELETE = 2
EXIT = 3
#
ZONE = 0
SECTOR = 1

DATA = '/data'
ZONES = '/zones'
SEPARATOR = '/'


def cli_configured(config_filename):
    """
    """
    if not config_filename in os.listdir():
        return False
    return True


def load_configuration():
    """
    """

    if not cli_configured(CONFIG_FILE):
        configuration = yes_no_dialog(
            title='Configuration',
            text="BetaLibrary's path is not configured. Configure now?")

        text = input_dialog(
            title='Configuration',
            text="Please enter BetaLibrary's path: ")

        if text:
            with open("config.txt", 'w') as f:
                f.write(text)
            return text
    else:
        with open("config.txt", 'r') as f:
            return f.read()


def load_zones(path):
    
    return [d for d in next(os.walk(path+DATA+ZONES))[1]]

def load_sectors(zone, path):
    """
    """
    pass

def choose_action():
    """
    """
    return button_dialog(
        title = 'Options',
        text = 'What do you want to do?',
        buttons = [
            ('Create', 0),
            ('Modify', 1),
            ('Delete', 2),
            ('Exit', 3)
        ],
    )


def execute_action(action, path):
    if action == EXIT:
        return
    if action == CREATE:
        create(path)
    if action == MODIFY:
        modify(path)
    if action == DELETE:
        delete(path)


def create(path):
    """
    """
    create_type=button_dialog(
        title = 'Create',
        text = 'What do you want to create?',
        buttons = [
            ('Zone', 0),
            ('Sector', 1),
            ('Exit', 3)
        ],
    )

    if create_type == ZONE:
        create_zone(path)
    if create_type == SECTOR:
        create_sector(path)
    if create_type == EXIT:
        return


def create_zone(path):
    """
    """
    zone_name = input_dialog(
        title = 'Zone creation',
        text = "Name: ")
    zone_path = path+DATA+ZONES+SEPARATOR + zone_name.lower().replace(" ", "_").replace("-", "_")
    print(zone_name)
    os.mkdir(zone_path)
    # with open()


def create_sector(path):
    """
    """
    zones=load_zones(path)

    selected_zone=radiolist_dialog(
        values = [
            (zone, zone) for zone in zones
        ],
        title = 'Select Zone',
        text = 'Please select a zone (use tab to move to confirmation buttons):')


def modify(path):
    """
    """
    pass


def delete(path):
    """
    """
    delete_type=button_dialog(
        title = 'Delete',
        text = 'What do you want to delete?',
        buttons = [
             ('Zone', 0),
             ('Sector', 1),
             ('Exit', 3)
        ],
    )

    if delete_type == ZONE:
        delete_zone(path)
    if delete_type == SECTOR:
        delete_sector(path)
    if delete_type == EXIT:
        return

def delete_zone(path):
    """
    """
    pass

def delete_sector(path):
    """
    """
    pass


def main():
    """
    """
    path=load_configuration()

    if path is None:
        return

    execute_action(choose_action(), path)


if __name__ == "__main__":
    main()
