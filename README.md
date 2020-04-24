# BetaLibrary-CLI
Command line interface for modifying or updating Betalibrary's internal data

## Setup

1. Clone the repo in the desired root folder: `$ git clone https://github.com/MadBoulder/BetaLibrary-CLI`
2. Install dependencies. It is recomended to install everything in a [virtual environment](https://virtualenv.pypa.io/en/latest/). After cloning the repository you can install the required packages with: `$ pip install -r /path/to/requirements.txt`)
3. Run the tool with: `$ python bcli.py`

## Supported operations

Currently, the tool supports:

1. Creating the empty template (only adds structure - folders and files) for a new zone.
2. Deleting a sector.

## Future work:

1. Enable installation as a system wide CLI that can be called from anywhere in the system.
2. Add support for all management operations (Create, Edit, Delete for zones and sectors).
