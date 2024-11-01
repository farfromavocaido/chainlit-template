# get name of current git repo

import os
import subprocess

def get_repo_name():
    # get current directory
    current_dir = os.getcwd()
    # get git repo name
    repo_name = subprocess.check_output(["basename", current_dir])
    repo_name = repo_name.decode("utf-8").strip()
    print("Repo name: ", repo_name)
    return repo_name

get_repo_name()

# replace REPO_NAME in cloudbuild_temp.yaml with current repo name and save to cloudbuild.yaml
def replace_repo_name():
    repo_name = get_repo_name()
    with open("cloudbuild_temp.yaml", "r") as file:
        data = file.read()
        data = data.replace("REPO_NAME", repo_name)
    with open("cloudbuild.yaml", "w") as file:
        file.write(data)

# replace_repo_name()

# get $REPO_FULL_NAME
def get_repo_full_name():
    repo_name = get_repo_name()
    # get current directory
    current_dir = os.getcwd()
    # get git repo name
    repo_full_name = subprocess.check_output(["basename", current_dir])
    repo_full_name = repo_full_name.decode("utf-8").strip()
    print("Repo full name: ", repo_full_name)
    return repo_full_name

get_repo_full_name()