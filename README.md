# Projecting KinDB to the StyleGAN2 latent space

## Requirements

* Docker
* [NVIDIA Container Runtime](https://github.com/NVIDIA/nvidia-container-runtime)
* Conda (see [./conda-env.yml](./conda-env.yml))
* NVIDIA GPU, NVIDIA drivers (see [NVlabs/stylegan2-ada-pytorch](https://github.com/NVlabs/stylegan2-ada-pytorch))

## Steps
* Clone this repository
```
$ git clone https://github.com/matjazmav/fri-2021-masters-kindb-stylegan2-projector.git
$ cd fri-2021-masters-kindb-stylegan2-projector/
$ git submodule update --init
```

* Build StyleGAN2 Docker image
```bash
$ tools/stylegan2-build.sh
```

* Create Conda env
```bash
$ conda env create -f conda-env.yml
```

* Set Google Drive credentials in file `creds.json`
* Download KinDB dataset from Google Drive
```bash
$ python gdrive.py download 1llRI_7l2Ab2HHEWE5pckB3Q82AoMQ7tN kindb.zip
$ unzip kindb.zip -d kindb
```

* Set `.env` file
```
REMINDER=0
MOD=2
```

* Run projector
```bash
$ nohup python projector.py &
$ echo $! > nohup.pid
```