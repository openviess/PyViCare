#!/bin/bash

set -e

LAST_TAG=$(git tag --sort=-version:refname | head -1)

echo -n "Which version do you want to publish? (Last: $LAST_TAG) "
read new_tag

rm -rf ./dist
git fetch
git checkout master
git reset --hard origin/master
git tag $new_tag

python setup.py sdist bdist_wheel
twine upload dist/*
git push --tags