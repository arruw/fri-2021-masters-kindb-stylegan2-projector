#!/bin/bash

STYLEGAN_PATH="submodules/stylegan2-ada-pytorch"
IMAGE="stylegan2-ada-pytorch:latest"

docker build --tag $IMAGE $STYLEGAN_PATH