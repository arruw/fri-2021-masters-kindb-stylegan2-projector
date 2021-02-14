# Projecting KinDB to the StyleGAN2 latent space

## Requirements

## Steps
1. Clone this repository
```
$ git clone https://github.com/matjazmav/fri-2021-masters-kindb-stylegan2-projector.git
$ cd fri-2021-masters-kindb-stylegan2-projector/
```
2. Get submodules
```bash
$ git submodule update --init
```
3. Build StyleGAN2 Docker image
```bash
$ tools/stylegan2-build.sh
```
4. Set Google Drive credentials in file `creds.json`
5. Download KinDB dataset from Google Drive
```bash
$ python gdrive.py download 1llRI_7l2Ab2HHEWE5pckB3Q82AoMQ7tN kindb.zip
```
6. Extract zip
```bash
$ unzip kindb.zip -d kindb
```
7. Set `.env` file
```
TELEGRAM_TOKEN=<telegram token>
TELEGRAM_CHAT_ID=<telegram chat id>
REMINDER=0
MOD=2
```
8. Run projector
```bash
$ nohup python projector.py &
$ echo $! > nohup.pid
```