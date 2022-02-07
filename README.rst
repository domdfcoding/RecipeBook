===============
RecipeBook
===============

Conda recipes.


To build a package::

	docker run --rm -ti continuumio/conda-ci-linux-64-python3.9
	cd ~
	git clone https://github.com/domdfcoding/RecipeBook
	cd RecipeBook
	export ANACONDA_TOKEN=<token>
	python docker_build.py <package>
