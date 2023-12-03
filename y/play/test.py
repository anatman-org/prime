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


def list_ports():
    import cv2

    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while (
        len(non_working_ports) < 6
    ):  # if there are more than 5 non working ports stop the testing.
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." % dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print(
                    "Port %s is working and reads images (%s x %s)" % (dev_port, h, w)
                )
                working_ports.append(dev_port)
            else:
                print(
                    "Port %s for camera ( %s x %s) is present but does not reads."
                    % (dev_port, h, w)
                )
                available_ports.append(dev_port)
        dev_port += 1
    return available_ports, working_ports, non_working_ports


def config_test():
    from config import BACK

    print(BACK)


if __name__ == "__main__":
    list_ports()

    # config_test()
