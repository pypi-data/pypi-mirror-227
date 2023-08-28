# video.py

import os
import multiprocessing
from typing import Union, Optional, List, Tuple, Iterable
from pathlib import Path
from functools import partial

import numpy as np
from PIL import Image

from pyvideo import Video

from ascii_art.image import (
    image_to_ascii_art_html, html_to_image, pillow_to_numpy,
    load_image, load_html, save_html, save_image
)

__all__ = [
    "video_to_ascii_art_html",
    "video_ascii_art",
    "htmls_to_video",
    "htmls_to_images",
    "save_htmls",
    "save_images",
    "load_images",
    "load_htmls"
]

FPS = 60

def save_htmls(htmls: Iterable[str], path: Union[str, Path]) -> List[str]:
    """
    Saves the HTML data to the saving path.

    :param htmls: The HTML strings.
    :param path: The saving path.

    :return: The file paths.
    """

    location = os.path.split(path)[0]

    if location:
        os.makedirs(location, exist_ok=True)
    # end if

    pool = multiprocessing.Pool()

    paths = [str(Path(path) / Path(f"{i}.html")) for i in range(len(list(htmls)))]

    pool.map(save_html, [(html, file) for html, file in zip(htmls, paths)])

    return paths
# end save_html

def load_htmls(path: Union[str, Path]) -> List[str]:
    """
    Loads the HTML data from the path.

    :param path: The saving path.

    :return: The HTML string.
    """

    pool = multiprocessing.Pool()

    return pool.map(
        load_html,
        [path for path in os.listdir(path) if path.endswith(".html")]
    )
# end load_html

def save_images(
        images: Iterable[Union[Image.Image, np.ndarray]],
        path: Union[str, Path],
        extension: Optional[str] = "png"
) -> List[str]:
    """
    Saves the image data to the saving path.

    :param images: The image objects.
    :param path: The saving path.
    :param extension: The type of file extension.

    :return: The file paths.
    """

    location = os.path.split(path)[0]

    if location:
        os.makedirs(location, exist_ok=True)
    # end if

    pool = multiprocessing.Pool()

    paths = [str(Path(path) / Path(f"{i}.{extension}")) for i in range(len(list(images)))]

    pool.map(save_image, [(html, file) for html, file in zip(images, paths)])

    return paths
# end save_image

def load_images(
        path: Union[str, Path], extensions: Iterable[str] = None
) -> List[Union[Image.Image, np.ndarray]]:
    """
    Loads the image data from the path.

    :param path: The saving path.
    :param extensions: The file extensions to load.

    :return: The image object.
    """

    pool = multiprocessing.Pool()

    return pool.map(
        load_image,
        [
            path for path in os.listdir(path)
            if (
                (extensions is None) or
                any(extension == path[-len(extension):] for extension in extensions)
            )
        ]
    )
# end load_image

def video_to_ascii_art_html(
        video: Video,
        lines: Optional[int] = None,
        color: Optional[bool] = None
) -> List[str]:
    """
    Generates an HTML string of ASCII art from a source pillow image object.

    :param video: The source video object or file path.
    :param lines: The amount of lines in the html string.
    :param color: The value to color the html.

    :return: The HTML string.
    """

    pool = multiprocessing.Pool()

    return pool.map(
        partial(image_to_ascii_art_html, lines=lines, color=color),
        video.fps
    )
# end image_to_ascii_art_html_file

def htmls_to_images(
        htmls: List[str],
        size: Optional[Tuple[int, int]] = None,
        quality: Optional[int] = None,
        brightness_factor: Optional[float] = None,
        color_factor: Optional[float] = None
) -> List[np.ndarray]:
    """
    Generates an image from the html.

    :param htmls: The HTML string.
    :param size: The size to crop the image to.
    :param quality: The quality of the image.
    :param brightness_factor: The brightness factor to scale the image.
    :param color_factor: The color factor to scale the image.

    :return: The generated image object.
    """

    pool = multiprocessing.Pool()

    return pool.map(
        partial(
            html_to_image,
            size=size, quality=quality,
            brightness_factor=brightness_factor,
            color_factor=color_factor
        ),
        htmls
    )
# end htmls_to_images

def htmls_to_video(
        htmls: List[str],
        fps: float,
        size: Optional[Tuple[int, int]] = None,
        quality: Optional[int] = None,
        brightness_factor: Optional[float] = None,
        color_factor: Optional[float] = None
) -> Video:
    """
    Generates an image from the html.

    :param htmls: The HTML string.
    :param fps: The fps for the video.
    :param size: The size to crop the image to.
    :param quality: The quality of the image.
    :param brightness_factor: The brightness factor to scale the image.
    :param color_factor: The color factor to scale the image.

    :return: The generated image object.
    """

    if fps is None:
        fps = FPS
    # end if

    frames = htmls_to_images(
        htmls=htmls,
        size=size, quality=quality,
        brightness_factor=brightness_factor,
        color_factor=color_factor
    )

    return Video(
        frames=frames,
        width=frames[0].shape[0],
        height=frames[0].shape[1],
        fps=fps,
        length=len(frames)
    )
# end htmls_to_video

def video_ascii_art(
        video: Optional[Union[str, Path, Video]] = None,
        htmls: Optional[Union[Union[str, Path], List[str]]] = None,
        lines: Optional[int] = None,
        color: Optional[bool] = None,
        quality: Optional[int] = None,
        fps: Optional[float] = None,
        brightness_factor: Optional[float] = None,
        color_factor: Optional[float] = None,
        html_destination: Optional[Union[str, Path]] = None,
        video_destination: Optional[Union[str, Path]] = None,
) -> None:
    """
    Generate an ASCII ark image from a source image or HTML file.

    :param video: The source video object or file path.
    :param htmls: The html file path or data.
    :param lines: The amount of lines in the html string.
    :param color: The value to color the html.
    :param fps: The fps for the video.
    :param quality: The quality of the image.
    :param brightness_factor: The brightness factor to scale the image.
    :param color_factor: The color factor to scale the image.
    :param html_destination: The path to save the html data in.
    :param video_destination: The path to save the generated video data in.
    """

    if (video, htmls) == (None, None):
        raise ValueError("At least one of html or video must be defined.")
    # end if

    if fps is None:
        fps = FPS
    # end if

    if htmls is None:
        if isinstance(video, (str, Path)):
            if Path(str(video)).is_file():
                video = Video.load(video)

            else:
                images = load_images(video)

                video = Video(
                    frames=[pillow_to_numpy(image) for image in images],
                    width=images[0].width,
                    height=images[0].height,
                    length=len(images),
                    fps=fps
                )
            # end if
        # end if

        htmls = video_to_ascii_art_html(
            video=video, lines=lines, color=color
        )
    # end if

    if isinstance(htmls, Path) or (isinstance(htmls, (str, Path)) and Path(htmls).exists()):
        htmls = load_htmls(htmls)
    # end if

    art_video = htmls_to_video(
        htmls=htmls,
        quality=quality,
        brightness_factor=brightness_factor,
        color_factor=color_factor,
        size=(video.width, video.height),
        fps=fps
    )

    if html_destination is not None:
        save_htmls(htmls=htmls, path=html_destination)
    # end if

    if video_destination is not None:
        art_video.save(video_destination)
    # end if
# end ascii_art