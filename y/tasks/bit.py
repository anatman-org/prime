from pathlib import Path

from invoke import task


@task
def bits_update(ctx, bits, source):
    bitdir = Path(bits)
