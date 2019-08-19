from pathlib import Path

""" Constants sharing from configuration data files """


class DefaultValues:
    BASE_DIR = Path(__file__).parent
    txt = str(BASE_DIR.joinpath('resources/textfile.txt'))
    gif = str(BASE_DIR.joinpath('resources/giphy.gif'))
    video = str(BASE_DIR.joinpath('resources/big.mp4'))
    jpg = BASE_DIR.joinpath('resources/small.jpg')
    json = str(BASE_DIR.joinpath('resources/emoji-db.json'))
    downloads = str(BASE_DIR.joinpath('resources/downloads/'))
    txt_loaded = str(BASE_DIR.joinpath('resources/downloads/textfile.txt'))
    gif_loaded = str(BASE_DIR.joinpath('resources/downloads/giphy.gif'))
    video_loaded = str(BASE_DIR.joinpath('resources/downloads/big.mp4'))
    jpg_loaded = BASE_DIR.joinpath('resources/downloads/small.jpg')
