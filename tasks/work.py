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
