from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog, yes_no_dialog, input_dialog, button_dialog, radiolist_dialog

import os
import json
import re
import unicodedata

from constants import *

def cli_configured(config_filename):
    """
    Check if a config file exists. This file should
    point to BetaLibrary's directory
    """
    if not config_filename in os.listdir():
        return False
    return True


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.

    Source: https://github.com/django/django/blob/master/django/utils/text.py
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '_', value)


def load_configuration():
    """
    Load or load and configure BetaLibrary's project directory
    """
    if not cli_configured(CONFIG_FILE):
        configuration = yes_no_dialog(
            title='Configuration',
            text="BetaLibrary's path is not configured. Configure now?")

        text = input_dialog(
            title='Configuration',
            text="Please enter BetaLibrary's path: ")

        if text:
            with open("config.txt", 'w', encoding='utf-8') as f:
                f.write(text)
            return text
    else:
        with open("config.txt", 'r', encoding='utf-8') as f:
            return f.read()


def load_zones(path):
    """
    Load all bouldering zones
    """
    return [d for d in next(os.walk(path+DATA+ZONES))[1]]


def load_sectors(zone, path):
    """
    Load the sectors of a bouldering zone
    """
    return [d for d in next(os.walk(path+DATA+ZONES+SEPARATOR+zone+SECTORS))[2]]


def load_prefix(key):
    """
    Define the prefix that should be shown
    in the dialog for the current key
    """
    if key not in NUMERICS:
        return key
    return 'Number of ' + key


def try_parse(value_to_parse):
    """
    Try to parse the value to a number. If this
    fails, keep the original type
    """
    try:
        return float(value_to_parse)
    except:
        return value_to_parse


def autocompute_fields(data):
    """
    Automatic computation of data fields from the
    rest of input data
    """
    for sector in data['sectors']:
        sector['sector_data'] = '/sectors/' + \
            slugify(sector['name'], False).lower() + '.txt'


def choose_action():
    """
    Select which action to perform
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
    Execute the selected action
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
    Create action
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
    Create a new zone
    """
    creation_type = button_dialog(
        title='Create',
        text='How do you want to create the zone?',
        buttons=[
            ('Empty template (only structure)', 0),
            ('Structure and data', 1),
            ('Exit', 3)
        ],
    )

    data = {}
    with open('zone_template.txt', encoding='utf-8') as json_file:
        data = json.load(json_file)

    if creation_type == EXIT:
        return
    # Create zone with all the data
    elif creation_type == 1:
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
    # Create only zone template
    elif creation_type == 0:
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

    # Create zone
    zone_path = path+DATA+ZONES+SEPARATOR + \
        slugify(data['name'], False).lower()
    os.mkdir(zone_path)
    os.mkdir(zone_path + SECTORS)
    # Load sector template
    sector_data = {}
    with open('sector_template.txt', encoding='utf-8') as json_file:
        sector_data = json.load(json_file)
    # Add sectors
    for num, sector in enumerate(data['sectors']):
        # if a sector data file name has been provided, create the file
        if sector['sector_data']:
            with open(zone_path + slugify(sector['sector_data'], False), 'w', encoding='utf-8') as f:
                f.write(json.dumps(sector_data, indent=4, sort_keys=True))
        elif sector['name']:
            sector['sector_data'] = SECTORS + SEPARATOR + \
                slugify(sector['name'], False)+'.txt'
            with open(zone_path + slugify(sector['sector_data'], False), 'w', encoding='utf-8') as f:
                f.write(json.dumps(sector_data, indent=4, sort_keys=True))
        else:
            sector['sector_data'] = SECTORS + \
                SEPARATOR + 'sector_' + str(num) + '.txt'
            with open(zone_path + sector['sector_data'], 'w', encoding='utf-8') as f:
                f.write(json.dumps(sector_data, indent=4, sort_keys=True))
    # Add zone data
    with open(zone_path + SEPARATOR + slugify(data['name'], False).lower()+'.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))


def create_sector(path):
    """
    Create a new sector
    """
    zones = load_zones(path)

    selected_zone = radiolist_dialog(
        values=[
            (zone, zone) for zone in zones
        ],
        title='Select Zone',
        text='Please select a zone (use enter to select tab to move to confirmation buttons):')


def modify(path):
    """
    Modify action
    """
    pass


def delete(path):
    """
    Delete action
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
    Deletes a zone
    """
    zones = load_zones(path)

    selected_zone = radiolist_dialog(
        values=[
            (zone, zone) for zone in zones
        ],
        title='Select Zone',
        text='Please select a zone to delete (use tab to move to confirmation buttons):')


def delete_sector(path):
    """
    Delectes a sector from a zone
    """
    zones = load_zones(path)

    selected_zone = radiolist_dialog(
        values=[
            (zone, zone) for zone in zones
        ],
        title='Select Zone',
        text='Please select a zone (use tab to move to confirmation buttons):')
    sectors = load_sectors(selected_zone, path)

    selected_sector = radiolist_dialog(
        # Remove extension by slicing
        values=[
            (sector, sector[:-4]) for sector in sectors
        ],
        title='Select Sector',
        text='Please select a sector to delete (use tab to move to confirmation buttons):')

    # TODO: Replace by an easier selector dialog
    sure = radiolist_dialog(
        values=[
            (True, "Yes"),
            (False, "No")
        ],
        title='Select Sector',
        text='Are you sure you want to delete '+selected_sector[:-4]+' from '+selected_zone+'?')

    if sure:
        os.remove(path+DATA+ZONES+SEPARATOR+selected_zone+SECTORS+SEPARATOR+selected_sector)


def main():
    """
    Main entry point of the cli. Loads project path
    and asks user for an action
    """
    path = load_configuration()
    if path is None:
        return

    execute_action(choose_action(), path)


if __name__ == "__main__":
    main()
