from google_images_downloader import GoogleImagesDownloader, DEFAULT_DESTINATION, DEFAULT_LIMIT, \
    DEFAULT_RESIZE, DEFAULT_BROWSER, DEFAULT_FORMAT
import sys
import argparse
import os
import re


def get_arguments():
    argument_parser = argparse.ArgumentParser(
        description="Script to download images from a \"Google Images\" query",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    argument_parser.add_argument(
        "-q",
        "--query",
        help="Google Images query" + os.linesep +
             "example : google-images-downloader -q cat",
        required=True
    )

    argument_parser.add_argument(
        "-d",
        "--destination",
        help="download destination" + os.linesep +
             "example : google-images-downloader -d C:\\my\\download\\destination" + os.linesep +
             "(default: %(default)s)",
        default=DEFAULT_DESTINATION
    )

    argument_parser.add_argument(
        "-l",
        "--limit",
        help="maximum number of images downloaded" + os.linesep +
             "Google Images is returning ~600 images maximum" + os.linesep +
             "use a big number like 9999 to download every images" + os.linesep +
             "example : google-images-downloader -l 400" + os.linesep +
             "(default: %(default)s)",
        default=DEFAULT_LIMIT,
        type=int
    )

    argument_parser.add_argument(
        "-r",
        "--resize",
        help="resize downloaded images to specified dimension at format <width>x<height>" + os.linesep +
             "by default, images are not resized" + os.linesep +
             "example : google-images-downloader -r 256x256" + os.linesep +
             "(default: %(default)s)",
        default=DEFAULT_RESIZE,
    )

    argument_parser.add_argument(
        "-f",
        "--format",
        help="format download image to specified format" + os.linesep +
             "by default, images keep their default format" + os.linesep +
             "example : google-images-downloader -f PNG" + os.linesep +
             "(default: %(default)s)",
        default=DEFAULT_FORMAT,
        choices=["JPEG", "PNG"])

    argument_parser.add_argument(
        "-b",
        "--browser",
        help="specify browser to use for web scraping" + os.linesep +
             "example : google-images-downloader -b firefox" + os.linesep +
             "(default: %(default)s)",
        default=DEFAULT_BROWSER,
        choices=["chrome", "firefox"])

    argument_parser.add_argument(
        "-Q",
        "--quiet",
        help="disable program output" + os.linesep +
             "example : google-images-downloader -Q",
        action="count"
    )

    argument_parser.add_argument(
        "-D",
        "--debug",
        help="enable debug logs, disable progression bar and messages" + os.linesep +
             "example : google-images-downloader -D",
        action="count"
    )

    argument_parser.add_argument(
        "-s",
        "--show",
        help="show the browser by disabling headless option" + os.linesep +
             "useful for debugging" + os.linesep +
             "example : google-images-downloader -s",
        action="count"
    )

    return argument_parser.parse_args(sys.argv[1:])


def main():
    arguments = get_arguments()

    show = True if arguments.show else False

    downloader = GoogleImagesDownloader(browser=arguments.browser, show=show)

    downloader.init_arguments(arguments)

    resize = None

    if arguments.resize is not None:
        if re.match('^[0-9]+x[0-9]+$', arguments.resize) is None:
            raise Exception(f"Invalid size format" + os.linesep +
                            "Expected format example : 256x256")
        else:
            resize = [int(x) for x in arguments.resize.split("x")]

    downloader.download(arguments.query, destination=arguments.destination, limit=arguments.limit, resize=resize,
                        format=arguments.format)


if __name__ == "__main__":
    main()
