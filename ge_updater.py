#!/usr/bin/python
import requests
from os import scandir, remove
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
	
	Return: returns the newest install of GE found
	"""

	subfolders = [file.name for file in scandir(proton_path) if file.is_dir() and "proton" in file.name.lower()]
	subfolders.sort()
	return subfolders[-1]


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


def remove_old_versions():
	"""Removes old versions of GE
	
	"""
	
	raise NotImplementedError


def install_glorious_eggroll(result):
	"""Installs the tarball found from the release
	
	result: json object of GitHub API request
	"""
	
	tar_url = result['assets'][1]['browser_download_url']
	filepath_for_tar = download_tarball(tar_url, result['tag_name'])
	if config['proton']['keep_old'] == 'False':
		remove_old_versions()
	extract_tar(filepath_for_tar)
	

def main():
	result = fetch_latest()
	newest_version = fetch_already_installed()
	tag_name = result['tag_name']
	if tag_name == newest_version:
		print(f"No new version of GloriousEggroll was found.\r\n Newest installed version is {newest_version}, latest available version was {tag_name}.")
		exit(0)

	print(f"New version of Proton was found. Do you want to install {tag_name}?")
	while(True):
		user_input = input("(y/n)? >")
		if "y" == user_input.lower():
			install_glorious_eggroll(result)
			exit(0)
		if "n" == user_input.lower():
			exit(0)
		print("Invalid input, please type 'y' or 'n'.")


if __name__ == '__main__':
	main()