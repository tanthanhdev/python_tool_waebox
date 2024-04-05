# python_tool_waebox

## Only Linux Usage

I. Setup environment

- python3 -m venv venv
- source venv/bin/activate
- pip3 install -m requirements.txt

II. Configuration

- Copy [settings.json.example] into new file [settings.json] and configure it

- Create new folder uploads in the root directory: /uploads

III. Initial database

- python3 services/init_db.py

IV. Run tool

- python3 main.py

## Helps

1. Collect installed lib into requirements.txt

- pip3 freeze > requirements.txt

2. Update latest modules

- pip3 install -e .