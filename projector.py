import os
import subprocess
import shutil
import signal

from glob import glob
from pprint import pprint

import telegram
import dotenv

from tqdm import tqdm

dotenv.load_dotenv()

chat_id = os.getenv("TELEGRAM_CHAT_ID")
token = os.getenv("TELEGRAM_TOKEN")
reminder = int(os.getenv("REMINDER"))
mod = int(os.getenv("MOD"))


is_interupted = False
bot = telegram.Bot(token=token)


def log(message):
    global bot

    print(f"{os.getpid()} {message}")
    # bot.send_message(chat_id=chat_id, text=message)


def graceful_exit(signum, frame):
    global is_interupted
    global bot

    is_interupted = True
    log("[INFO] Gracefully exiting...")


signal.signal(signal.SIGTERM, graceful_exit)
signal.signal(signal.SIGINT, graceful_exit)

with tqdm(sorted(glob("kindb/**/*.png", recursive=True))) as progress:
    for img_path in progress:

        if is_interupted:
            break

        iid = int(img_path.split("/")[-1].replace(".png", ""))
        if iid % mod != reminder:
            continue

        projection_path = img_path.replace(".png", ".npz")
        if os.path.exists(projection_path):
            continue

        log(f"[INFO] Projecting image {iid}...")

        projection_process = subprocess.run(
            ["tools/stylegan2-project.sh", img_path],
            timeout=600,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setpgrp)

        if projection_process.returncode != 0:
            log(
                f"[ERROR] Projection failed with STDERR: {projection_process.stderr}")
            continue

        shutil.copyfile("out/projected_w.npz", projection_path)


log(f"[INFO] Done.")
