#!/bin/bash
isort .
autopep8 --in-place --recursive .
npx prettier --write {**.md,**.yml,**.json}
flake8
