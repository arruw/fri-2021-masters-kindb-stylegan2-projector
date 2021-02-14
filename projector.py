import os
import subprocess
import shutil
import signal
import dotenv

from glob import glob
from tqdm import tqdm

dotenv.load_dotenv()

reminder = int(os.getenv("REMINDER"))
mod = int(os.getenv("MOD"))

is_interupted = False


def graceful_exit(signum, frame):
    global is_interupted
    is_interupted = True
    print("[INFO] Gracefully exiting...")


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

        print(f"[INFO] Projecting image {img_path}...")

        projection_process = subprocess.run(
            ["tools/stylegan2-project.sh", img_path],
            timeout=600,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setpgrp)

        if projection_process.returncode != 0:
            print(
                f"[ERROR] Projection failed with STDERR: {projection_process.stderr}")
            continue

        shutil.copyfile("out/projected_w.npz",
                        img_path.replace(".png", ".npz"))


print(f"[INFO] Done.")
