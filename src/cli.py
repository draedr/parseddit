import os
import click
from parseddit import parseddit, options
from version import __version__

@click.command(epilog="Code available at https://github.com/draedr/reddit-img-parse")
@click.version_option(version=__version__, prog_name="reddit-img-parse", message="%(prog)s version %(version)s")
@click.argument('url')
@click.option('--output_folder', default=os.path.expanduser("~/Desktop"), help='Output folder for downloaded images (A new folder will be created inside of it). By deafult, the current working directory will be used.')
@click.option('--overwrite', is_flag=True, help='Overwrites download folder if already exists by deleting it first. Default is False.')
@click.option('--foldername', default='', help='Name of the folder created in output_folder where the images will be saved.')
def run(url, output_folder, overwrite, foldername):
    """A python script to download images from a Reddit post with a gallery.
    
    URL must be the link to page url, not the image url or something else.
    Example: https://www.reddit.com/r/wholesomememes/comments/1x2y3z/this_is_a_test_post/
    """
    opt = options(url, output_folder, overwrite, foldername)
    parser = parseddit(url, opt)
    parser.parse()

if __name__ == "__main__":
    run()