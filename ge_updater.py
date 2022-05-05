#!/usr/bin/python
import requests
from os import scandir, remove, rmdir
import configparser
import tarfile
from shutil import copyfileobj
from pathlib import Path

git_api = "https://api.github.com"
repo = "/repos/gloriouseggroll/proton-ge-custom"
latest = "/releases/latest"
config = configparser.ConfigParser()
config.read("config.conf")
proton_path = f"{str(Path.home())}{config['proton']['proton_location']}"


def fetch_already_installed():
	"""Finds already installed versions of GE
	
	Return: returns all GEProton versions found
	"""

	subfolders = [file.name for file in scandir(proton_path) if file.is_dir() and "proton" in file.name.lower()]
	subfolders.sort()
	return subfolders


def fetch_latest():
	"""Fetches latest release of GloriousEggroll
	
	Return: json result from GitHub API
	"""

	response = requests.get(f"{git_api}{repo}{latest}")
	return response.json()


def download_tarball(url, tag_name):
	"""Downloads a tarball file from given url
	
	url: location of the tarball
	tag_name: name of the git release
	Return: filepath to the downloaded file
	"""
	
	with requests.get(url, stream=True) as response:
		response.raise_for_status()
		tar_file = f"{tag_name}.tar.gz"
		print("Downloading GloriousEggroll, this might take a while...")
		with open(tar_file, "wb") as file:
			# Using shutil instead of file.write prevents the entire ~400mb file from being downloaded to RAM memory
			copyfileobj(response.raw, file)
		return tar_file


def extract_tar(file):
	"""Extracts a downloaded tarball file to proton folder and 
	deletes the tarball afterwards
	
	file: filepath to the tarball
	"""
	
	print("Extracting")
	tar = tarfile.open(file, "r:gz")
	tar.extractall(proton_path)
	tar.close()
	remove(file)


def remove_old_versions(proton_installs):
	"""Removes ALL old versions of GE
	
	"""
	for proton in proton_installs[0:-1]:
		rmdir(f"{proton_path}/{proton}")


def install_glorious_eggroll(result):
	"""Installs the tarball found from the release
	
	result: json object of GitHub API request
	"""
	
	tar_url = result['assets'][1]['browser_download_url']
	filepath_for_tar = download_tarball(tar_url, result['tag_name'])
	extract_tar(filepath_for_tar)

def verify_user_yes_no(question):
	print(question)
	while True:
		user_input = input("(y/n)? >").lower()
		if user_input == "y":
			return True
		elif user_input == "n":
			return False
		print("Invalid input, please type 'y' or 'n'.")


def main():
	result = fetch_latest()
	versions = fetch_already_installed()
	newest_version = versions[-1]
	tag_name = result['tag_name']
	if tag_name != newest_version:
		print(f"No new version of GloriousEggroll was found.\r\n Newest installed version is {newest_version}, latest available version was {tag_name}.")
		exit(0)

	is_install = verify_user_yes_no(f"New version of Proton was found. Do you want to install {tag_name}?")
	if is_install:
		install_glorious_eggroll(result)
		if config['proton']['keep_old'] == 'False':
			is_remove = verify_user_yes_no(f"Warning: Program is set to delete ALL old installs of proton. All other versions except {tag_name} will be removed. Do you accept this?")
			if is_remove:
				remove_old_versions(versions)
			exit(0)

if __name__ == '__main__':
	main()