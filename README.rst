===============
RecipeBook
===============

Conda recipes.


To build a package::

	docker run -ti continuumio/conda-ci-linux-64-python3.8
	sudo chown -R test_user: /opt/conda
	cd ~
	git clone https://github.com/domdfcoding/RecipeBook
	cd RecipeBook
	export ANACONDA_TOKEN=<token>
	python docker_build.py <package>
