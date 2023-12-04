from pathlib import Path
from datetime import datetime
import platform

import xxhash
from invoke import task
from slugify import slugify


HOSTNAME = platform.node()


try:
    from reflink import reflink as file_copy
    import reflink.error
except ModuleNotFoundError:
    print(
        "NO REFLINK, TRY export PYTHONPATH=${HOME}/.local/lib/python3.12/site-packages"
    )
    exit(1)
    # from shutil import copy2 as file_copy

now = datetime.now

EXCLUDE = ["bits", "snap", "tmp", "lfs"]


@task
def bits_update(ctx, bitbase):
    bitdir = Path(bitbase)

    if not (bitdir / "bits").is_dir():
        (bitdir / "bits").mkdir()

    index_file = bitdir / f"bits/{HOSTNAME}-{slugify(str(bitdir))}-{now():%Y%m%d}.idx"

    with index_file.open("a") as index:
        for toplevel in bitdir.glob("*"):
            if toplevel.name not in EXCLUDE and toplevel.is_dir():
                for file in toplevel.rglob("*"):
                    if not file.is_file():
                        continue

                    xxh = xxhash.xxh64(file.open("rb").read())

                    xxh_hex = xxh.hexdigest()

                    xxh_path = (
                        (bitdir / "bits") / xxh_hex[:2] / xxh_hex[2:4] / xxh_hex[4:]
                    )

                    file_name = str(file)

                    if xxh_path.exists():
                        print(
                            f"{now():%Y%m%d:%H%M%S} HERE {xxh_path} {file_name}",
                            file=index,
                            flush=True,
                        )
                    else:
                        print(
                            f"{now():%Y%m%d:%H%M%S} LINK {xxh_path} {file_name}",
                            file=index,
                            flush=True,
                        )

                        if not xxh_path.parent.exists():
                            xxh_path.parent.mkdir(parents=True)

                    try:
                        file_copy(file_name, str(xxh_path))
                    except (reflink.error.ReflinkImpossibleError, OSError):
                        print(
                            f"{now():%Y%m%d:%H%M%S} SKIP {xxh_path} {file_name}",
                            file=index,
                            flush=True,
                        )


@task
def bits_copyto(ctx, bitbase, destination):
    EXCLUDE = ["bits", "snap", "tmp"]
    bitdir = Path(bitbase)

    bits = bitdir / "bits"

    if not bits.is_dir():
        print("ERROR, no bits dir")

    print(f"rsync -avzHP {str(bits)}/ {destination}/")
