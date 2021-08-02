#!/bin/bash

echo -n "Which version do you want to publish? (Format: x.y) "
read new_tag

rm -rf ./dist
git tag $new_tag

python setup.py sdist bdist_wheel
twine upload dist/*
git push --tags