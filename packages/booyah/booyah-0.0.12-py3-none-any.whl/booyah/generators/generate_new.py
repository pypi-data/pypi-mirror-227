# First step, adding helper folder to sys path to be able to import functions
import os
import sys
import shutil
import argparse
import subprocess
import re

booyah_root = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from booyah.generators.helpers.io import print_error, print_success, prompt_override_file
from booyah.generators.helpers.system_check import current_dir_is_booyah_root, prompt_replace

import booyah.extensions.string
globals()['String'] = booyah.extensions.string.String

def main(args):
    """
    Handle commandline args to process creating new project
    """
    if current_dir_is_booyah_root():
        print_error('Already are or inside a booyah root project folder')
        return None
    parser = argparse.ArgumentParser(description='Creating New Booyah Project')
    parser.add_argument("project_name", help="The project name")
    args = parser.parse_args(args)
    if not args.project_name.strip():
        print_error('Please type the project name')
        return

    folder_name = String(args.project_name.strip()).underscore()
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    if os.path.exists(folder_path):
        response = input(f"The folder '{folder_path}' already exists. Are you sure you want to use this folder to create the project? (yes/no): ")
        if response.lower() != "yes":
            exit()
    copy_booyah_version(folder_path)
    create_project(folder_name)

def copy_booyah_version(target_folder):
    """
    Create .booyah_version file with the current booyah version (used to check if the folder is a booyah project)
    """
    target_file_path = os.path.join(target_folder, '.booyah_version')
    if prompt_replace(target_file_path):
        os.makedirs(target_folder, exist_ok=True)
        with open(target_file_path, "w") as file:
            file.write(get_booyah_version())

def get_booyah_version():
    try:
        output = subprocess.check_output(["pip", "show", "booyah"]).decode("utf-8")
        version_line = re.search(r"Version: (.+)", output)
        if version_line:
            return version_line.group(1)
        else:
            return 'booyah pip not found'
    except subprocess.CalledProcessError:
        return 'booyah pip not found'

def copy_folders_and_files(source_folder, destination_folder, config):
    for folder, content in config.items():
        source_folder_path = os.path.join(source_folder, folder)
        destination_folder_path = os.path.join(destination_folder, folder)

        # Create the destination folder if it doesn't exist
        os.makedirs(destination_folder_path, exist_ok=True)

        if isinstance(content, list):
            for file in content:
                source_file_path = os.path.join(source_folder_path, file)
                destination_file_path = os.path.join(destination_folder_path, file)

                # Copy the file from source to destination
                shutil.copy2(source_file_path, destination_file_path)
        elif isinstance(content, dict):
            copy_folders_and_files(source_folder_path, destination_folder_path, content)


def create_project(project_name):
    """
    Copy folders required to run a new booyah project
    """
    # Define project structure
    config = {
        'app': {
            'models': ['application_model.py'],
            'controllers': ['application_controller.py']
        },
        'config': ['routes.json', 'routes.py', '__init__.py'],
        'public': ['index.html'],
        'db': {'adapters': ['base_adapter.py', 'postgresql_adapter.py'] },
    }

    config2 = {
        'app': ['__init__.py'],
    }

    source_folder = os.path.realpath(os.path.join(booyah_root, 'generators', 'templates', 'generate_new'))
    destination_folder = project_name
    copy_folders_and_files(source_folder, destination_folder, config)
    copy_folders_and_files(source_folder, destination_folder, config2)
    shutil.copy(os.path.join(source_folder, 'env'), os.path.join(destination_folder, '.env'))
    shutil.copy(os.path.join(source_folder, 'application.py'), os.path.join(destination_folder, 'application.py'))
    shutil.copy(os.path.join(source_folder, '__init__.py'), os.path.join(destination_folder, '__init__.py'))

    print(f"Project '{project_name}' created successfully.")