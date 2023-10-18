from y.play.images import ImageStatic, ImageGlobSequence, ImageGlobCarousel, ImageGlobRandom, ImageNull, VideoStatic

STAGE_SEQUENCE_GLOB = "media/marks*.png"
STAGE_IMAGE = ImageGlobCarousel(glob=STAGE_SEQUENCE_GLOB, autoincrement=False)

# BACK_SEQUENCE_GLOB = "media/back/*.png"
# BACK_SEQUENCE_GLOB_INDEX = 0
# BACK_IMAGE = ImageGlobRandom( glob=BACK_SEQUENCE_GLOB, index=BACK_SEQUENCE_GLOB_INDEX)
# BACK_IMAGE = ImageGlobCarousel(glob=STAGE_SEQUENCE_GLOB, autoincrement=False)

# BACK_IMAGE = ImageNull()
# BACK_IMAGE = ImageStatic(file="media/background.png")

BACK_IMAGE = VideoStatic(file="copy/Observing the Sun [5518376507001].mp4")

FNAME_TEMPLATE = "out/{now:%Y%m%d}/{now:%Y%m%d-%H%M%S-%f}.png"

DASH_SCREEN = 2
PLAY_SCREEN = 1

PLAY_FULLSCREEN = True
DASH_FULLSCREEN = True

CAMERA = 1
CAMERA_SLEEP = 0.5


DEBUG = True
if DEBUG:
    DASH_SCREEN = 0
    PLAY_SCREEN = 0

    PLAY_FULLSCREEN = False
    DASH_FULLSCREEN = False

    CAMERA = 0
