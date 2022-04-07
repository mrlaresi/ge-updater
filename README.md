# GE Updater

This is an utility tool built to check whether custom Proton implementation GloriousEggroll has a new release available on GitHub.

## Requirements

- Python installed on your computer (Tested on Python 3.10.2)
- Linux distribution
- Folder structure as shown in (Valve Proton GitHub)[https://github.com/ValveSoftware/Proton#install-proton-locally]

## Configuring the program

Program includes default `config.conf` file that can be customized as needed. 

Current customizations include:
- proton_location: location of compatibilitytools.d steam folder
- keep_old: whether old versions of GE are kept when updating

## Running

Program can be ran directly from terminal via 

`python ge_updater.py`

or by utilizing it's shebang

`./ge_updater`