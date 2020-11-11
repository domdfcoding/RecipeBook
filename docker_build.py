#!/usr/bin/env python

# Don't run this outside of docker
import getpass
import os
import sys

if not getpass.getuser() == "test_user":
	raise NameError("Refusing to run when outside of a Docker container")

ANACONDA_TOKEN = os.environ.get("ANACONDA_TOKEN", '')

if not ANACONDA_TOKEN:
	raise ValueError("ANACONDA_TOKEN unset.")

# Not writeable in Anaconda's own docker image 🙄
os.system("sudo chown -R test_user: /opt/conda/pkgs")

root_dir = os.getcwd()

for recipe in sys.argv[1:]:
	os.chdir(recipe)

	CHANNELS = []

	if os.path.isfile("CHANNELS"):
		with open("CHANNELS") as fp:
			CHANNELS = fp.readlines()

	command = f"conda build . "
	for channel in CHANNELS:
		command += f"-c {channel} "

	os.system(command)

	os.chdir(root_dir)
