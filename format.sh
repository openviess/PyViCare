#!/bin/bash
autopep8 --in-place --recursive .
npx prettier --write {**.md,**.yml}
flake8 --ignore=E501,W503
