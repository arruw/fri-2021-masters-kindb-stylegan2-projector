# Projecting KinDB to the StyleGAN2 latent space

## Requirements

## Steps
1. Set Google Drive credentials
2. Download KinDB dataset from Google Drive
```bash
python gdrive.py download 1llRI_7l2Ab2HHEWE5pckB3Q82AoMQ7tN kindb.zip
```
3. Extract zip
```bash
unzip kindb.zip -d kindb
```
4. Set `.env` file
```
TELEGRAM_TOKEN=<telegram token>
TELEGRAM_CHAT_ID=<telegram chat id>
REMINDER=0
MOD=2
```
5. Run projector
```bash
nohup python projector.py &
```