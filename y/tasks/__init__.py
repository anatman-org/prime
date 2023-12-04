from pathlib import Path
from datetime import datetime
from invoke import task

FRAMERATE = 6

WORKDIR = Path("/work")
PLAYDIR = WORKDIR / "play"
CLIPDIR = WORKDIR / "clips"

BACKUP_DESTINATION = "meru:/data/vajra/"

now = datetime.now


@task
def clips_build(ctx):

    for p in PLAYDIR.glob("*"):
        print(f"Working {p}")

        if p.is_dir():

            infiles = f"{str(p)}/*.png"
            outfile = f"{str(CLIPDIR)}/{p.name}.mp4"

            if Path(outfile).exists():
                print(f"{outfile} exists")
                continue

            ctx.run(
                f"""ffmpeg \
                -framerate {FRAMERATE} \
                -pattern_type glob -i '{infiles}' \
                -vf scale=1920:1080 -preset slow -crf 18 \
                {outfile}""",
                warn=True,
            )


@task
def work_backup(ctx):

    ctx.run(
        f"""rsync \
        -avzHP \
        --exclude .snap --exclude tmp \
        {str(WORKDIR)}/ \
        {BACKUP_DESTINATION}"""
    )

@task
def frames2_vid(ctx, framebase):
    from slugify import slugify

    OUTPUT = slugify(framebase) + '.mp4'

    # https://superuser.com/a/891478
    # FFMPEG = f"ffmpeg -framerate 6 -pattern_type glob -i '{framebase}' -vf 'scale=(iw*sar)*min(1920/(iw*sar)\\,1280/ih):ih*min(1920/(iw*sar)\\,1280/ih), pad=1920:1280:(1920-iw*min(1920/iw\\,1280/ih))/2:(1280-ih*min(1920/iw\\,1280/ih))/2' /work/clips/{OUTPUT}"
    FFMPEG = f"ffmpeg -framerate 6 -pattern_type glob -i '{framebase}' -vf 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2' /work/clips/{OUTPUT}"
    print(FFMPEG)
    ctx.run(FFMPEG)

@task 
def vid2_frames(ctx, vid):
    from slugify import slugify
    OUTPUT = '/work/frames/' + slugify(vid) + '-%08d.png'
    FFMPEG = f"ffmpeg -i {vid} -vf 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2' '{OUTPUT}'"
    print(FFMPEG)
    ctx.run(FFMPEG)


@task
def bits_update(ctx, bitbase):
    import xxhash

    try:
        from reflink import reflink as file_copy
        import reflink.error
    except ModuleNotFoundError:
        print(
            "NO REFLINK, TRY export PYTHONPATH=$HOME/.local/lib/python3.12/site-packages"
        )
        return
        from shutil import copy2 as file_copy

    EXCLUDE = ["bits", "snap", "tmp"]
    bitdir = Path(bitbase)

    if not (bitdir / "bits").is_dir():
        (bitdir / "bits").mkdir()

    index_file = bitdir / f"bits/{now():%Y%m%d}.idx"

    with index_file.open("a") as index:

        for toplevel in bitdir.glob("*"):

            if toplevel.name not in EXCLUDE and toplevel.is_dir():

                print(toplevel)

                for file in toplevel.rglob("*"):
                    if not file.is_file():
                        continue

                    xxh = xxhash.xxh64(file.open("rb").read())

                    xxh_hex = xxh.hexdigest()

                    xxh_path = (
                        (bitdir / "bits") / xxh_hex[:2] / xxh_hex[2:4] / (xxh_hex[4:] + file.suffix)
                    )

                    if xxh_path.exists():
                        print(
                            f"{now():%Y%m%d:%H%M%S} HERE {xxh_path} {str(file)}",
                            file=index,
                            flush=True,
                        )
                    else:
                        print(
                            f"{now():%Y%m%d:%H%M%S} LINK {xxh_path} {str(file)}",
                            file=index,
                            flush=True,
                        )

                        if not xxh_path.parent.exists():
                            xxh_path.parent.mkdir(parents=True)

                    try:
                        file_copy(str(file), str(xxh_path))
                    except (reflink.error.ReflinkImpossibleError, OSError):
                        print(
                            f"{now():%Y%m%d:%H%M%S} SKIP {xxh_path} {str(file)}",
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
