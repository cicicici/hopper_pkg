.PHONY : install build uninstall clean

PROJECT ?= hopper

build:
	python setup.py build

install:
	python setup.py install

uninstall: clean
	pip uninstall -y $(PROJECT)

clean:
	rm -rf build $(PROJECT).egg-info dist

