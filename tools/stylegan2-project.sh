#!/bin/bash

TARGET=$1

STYLEGAN_PATH="submodules/stylegan2-ada-pytorch"
IMAGE="stylegan2-ada-pytorch:latest"

CMD="python $STYLEGAN_PATH/projector.py --outdir=out --target=$TARGET --save-video=False --network=https://nvlabs-fi-cdn.nvidia.com/stylegan2-ada-pytorch/pretrained/ffhq.pkl"

rm -rf ./out/
docker run --shm-size=2g --gpus all --rm -v `pwd`:/scratch --user $(id -u):$(id -g) --workdir=/scratch -e HOME=/scratch $IMAGE $CMD