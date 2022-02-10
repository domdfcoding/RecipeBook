#!/usr/bin/env python

# Don't run this outside of docker

# stdlib
import getpass
import os
import pathlib
import sys
from itertools import chain

if not getpass.getuser() == "test_user":
	raise NameError("Refusing to run when outside of a Docker container")

ANACONDA_TOKEN = os.environ.get("ANACONDA_TOKEN", '')

if not ANACONDA_TOKEN:
	raise ValueError("ANACONDA_TOKEN unset.")

output_dir = pathlib.Path("/home/test_user/conda-bld/noarch")
opt_output_dir = pathlib.Path("/opt/conda/conda-bld/noarch")

# Not writeable in Anaconda's own docker image 🙄
os.system("sudo chown -R test_user: /opt/conda/pkgs")

root_dir = os.getcwd()

for recipe in sys.argv[1:]:
	recipe = recipe.strip("/")
	os.chdir(recipe)

	CHANNELS = []

	if os.path.isfile("CHANNELS"):
		with open("CHANNELS") as fp:
			CHANNELS = fp.readlines()

	command = f"conda build . "
	for channel in CHANNELS:
		command += f"-c {channel} "

	os.system(command)

	for filename in chain.from_iterable(d.glob(f"{recipe}-*.tar.bz2") for d in (output_dir, opt_output_dir)):
		print(filename)
		print("Deploying to Anaconda.org...")
		ret = os.system(f"anaconda -t $ANACONDA_TOKEN upload {filename}")
		if ret == 0:
			"Successfully deployed to Anaconda.org."
			break
		else:
			raise OSError(f"Anaconda upload exited with non-zero code {ret}")
	else:
		raise FileNotFoundError(f"No matching files for {output_dir / f'{recipe}-*.tar.bz2'}")

	os.chdir(root_dir)
