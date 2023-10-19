#!/usr/bin/env python


def list_screens():

    import pyglet
    from y.play import log

    display = pyglet.canvas.get_display()
    screens = display.get_screens()

    for idx, screen in enumerate(screens):
        print(
            f"{idx} Screen at {screen.display} at {screen.x} {screen.y} with {screen.width}x{screen.height}"
        )


def mat_files():

    mat = y.play.mat.MatWindow()

    index = mat.fname_list.index("out/20230926/20230926-213703-920051.png")
    print(index, len(mat.fname_list))


def video_dump():
    import pyglet
    from PIL import Image
    import numpy as np

    import av

    container = av.open("out/20230927.mp4")
    container.streams.video[0].thread_type = "AUTO"  # Go faster!

    columns = []
    for frame in container.decode(video=0):

        print(frame)
        array = frame.to_ndarray(format="rgb24")

        # Collapse down to a column.
        column = array.mean(axis=1)

        # Convert to bytes, as the `mean` turned our array into floats.
        column = column.clip(0, 255).astype("uint8")

        # Get us in the right shape for the `hstack` below.
        column = column.reshape(-1, 1, 3)

        columns.append(column)

    # Close the file, free memory
    container.close()

    full_array = np.hstack(columns)
    full_img = Image.fromarray(full_array, "RGB")
    full_img = full_img.resize((800, 200))
    full_img.save("out/20230927.jpg", quality=85)


def config_test():
    from config import BACK

    for x in BACK._filelist:
        print(x)


if __name__ == "__main__":
    # list_screens()

    config_test()
