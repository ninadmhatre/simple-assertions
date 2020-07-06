#!/usr/bin/env bash

export PYTHONPATH=$PWD

cd tests || exit 1

echo "running tests"
python -m unittest discover

echo "running coverage"
coverage run -m unittest discover
