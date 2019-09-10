from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog, yes_no_dialog, input_dialog, button_dialog, radiolist_dialog
import os
import json

CONFIG_FILE = "config.txt"
# Actions
CREATE = 0
MODIFY = 1
DELETE = 2
EXIT = 3
# Object sppecification
ZONE = 0
SECTOR = 1
# Betalibrary's path specifications
DATA = '/data'
ZONES = '/zones'
SECTORS = '/sectors'
SEPARATOR = '/'
# Special fields
NUMERICS = ['parkings', 'sectors', 'guides']
AUTOCOMPUTED = ['sector_data']
TEMPLATED_ZONE_CREATION = ['name', 'parkings', 'sectors', 'guides']


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
    """
    """
    return [d for d in next(os.walk(path+DATA+ZONES))[1]]


def load_sectors(zone, path):
    """
    """
    pass


def load_prefix(key):
    """
    """
    if key not in NUMERICS:
        return key
    return 'Number of ' + key


def try_parse(value_to_parse):
    """
    """
    try:
        return int(value_to_parse)
    except:
        return value_to_parse


def autocompute_fields(data):
    """
    """
    for sector in data['sectors']:
        sector['sector_data'] = '/sectors/' + \
            sector['name'].lower().replace(" ", "_").replace("-", "_")+'.txt'


def choose_action():
    """
    """
    return button_dialog(
        title='Options',
        text='What do you want to do?',
        buttons=[
            ('Create', 0),
            ('Modify', 1),
            ('Delete', 2),
            ('Exit', 3)
        ],
    )


def execute_action(action, path):
    """
    """
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
    create_type = button_dialog(
        title='Create',
        text='What do you want to create?',
        buttons=[
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
    creation_type = button_dialog(
        title='Create',
        text='How do you want to create the zone?',
        buttons=[
            ('Full', 0),
            ('Template', 1),
            ('Exit', 3)
        ],
    )

    data = {}
    with open('zone_template.txt') as json_file:
        data = json.load(json_file)

    if creation_type == 0:
        for data_key in data.keys():
            if data_key in AUTOCOMPUTED:
                continue
            field_value = input_dialog(
                title='Zone creation',
                text=load_prefix(data_key)+": ")
            if data_key in NUMERICS:
                content_array = []
                for i in range(int(field_value)):
                    content = {}
                    for sub_data_key in data[data_key][0].keys():
                        if sub_data_key in AUTOCOMPUTED:
                            continue
                        value = input_dialog(
                            title='Zone creation',
                            text=load_prefix(sub_data_key)+" "+str(i)+": ")
                        content[sub_data_key] = try_parse(value)
                    content_array += [content]
                data[data_key] = content_array
            else:
                data[data_key] = try_parse(field_value)
            autocompute_fields(data)
    elif creation_type == 1:
        for data_key in data.keys():
            if data_key not in TEMPLATED_ZONE_CREATION:
                continue
            field_value = input_dialog(
                title='Zone creation',
                text=load_prefix(data_key)+": ")
            if data_key in NUMERICS:
                content_array = []
                for i in range(int(field_value)):
                    content = {}
                    for sub_data_key in data[data_key][0].keys():
                        content[sub_data_key] = ""
                    content_array += [content]
                data[data_key] = content_array
            else:
                data[data_key] = try_parse(field_value)

    print(data)

    zone_path = path+DATA+ZONES+SEPARATOR + \
        data['name'].lower().replace(" ", "_").replace("-", "_")
    os.mkdir(zone_path)
    os.mkdir(zone_path + SECTORS)
    with open(zone_path + SEPARATOR + data['name'].lower().replace(" ", "_").replace("-", "_")+'.txt', 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))


def create_sector(path):
    """
    """
    zones = load_zones(path)

    selected_zone = radiolist_dialog(
        values=[
            (zone, zone) for zone in zones
        ],
        title='Select Zone',
        text='Please select a zone (use tab to move to confirmation buttons):')


def modify(path):
    """
    """
    pass


def delete(path):
    """
    """
    delete_type = button_dialog(
        title='Delete',
        text='What do you want to delete?',
        buttons=[
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
    path = load_configuration()

    if path is None:
        return

    execute_action(choose_action(), path)


if __name__ == "__main__":
    main()
