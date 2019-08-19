from PIL import Image
import io
from moviepy.editor import VideoFileClip


def get_image_w_h(file):
    """Returns image's width and height

    :param file: path to image
    :return: (width, height) tuple
    """

    im = Image.open(file)
    return im.size


def get_video_w_h(file):
    """ Return video duration in int
    """
    vid = VideoFileClip(file)
    return vid.size


def get_video_duration(file):
    """ Return video duration in int
    """
    vid = VideoFileClip(file)
    result = int(vid.duration)
    return result


def get_image_thumb_bytes(file):
    """Returns image's thumbnail in form of byte array

    :param file: path to image
    :return: size and byte array
    """

    size = 90, 90

    im = Image.open(file)
    im = im.convert('RGB')
    im.thumbnail(get_image_w_h(file))
    stream = io.BytesIO()
    im.save(stream, "JPEG")

    return size[0], size[1], stream.getvalue()
