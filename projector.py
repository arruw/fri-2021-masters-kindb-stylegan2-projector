import os
import subprocess
import shutil
import signal
import dotenv

from glob import glob
from tqdm import tqdm
from datetime import datetime

dotenv.load_dotenv()

reminder = int(os.getenv("REMINDER"))
mod = int(os.getenv("MOD"))

is_interupted = False


def graceful_exit(signum, frame):
    global is_interupted
    is_interupted = True
    print(f"{datetime.now()} [INFO] Gracefully exiting...")


signal.signal(signal.SIGTERM, graceful_exit)
signal.signal(signal.SIGINT, graceful_exit)


def get_iid(img_path):
    return int(img_path.split("/")[-1].replace(".png", ""))


def npz_exists(img_path):
    return os.path.exists(img_path.replace(".png", ".npz"))


raw_images = glob(".cache/kindb/**/*.png", recursive=True)
raw_images = filter(lambda p: get_iid(p) % mod == reminder, raw_images)
raw_images = filter(lambda p: not npz_exists(p), raw_images)
raw_images = sorted(list(raw_images))

with tqdm(raw_images) as progress:
    for img_path in progress:

        if is_interupted:
            break

        progress.set_description(
            desc=f"{datetime.now()} [INFO] Projecting image {img_path}...", refresh=True)

        projection_process = subprocess.run(
            ["tools/stylegan2-project.sh", img_path],
            timeout=600,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setpgrp)

        if projection_process.returncode != 0:
            progress.set_description(
                desc=f"{datetime.now()} [ERROR] Projection failed with STDERR: {projection_process.stderr}", refresh=True)
            continue

        shutil.copyfile("out/projected_w.npz",
                        img_path.replace(".png", ".npz"))


print(f"[INFO] Done.")
