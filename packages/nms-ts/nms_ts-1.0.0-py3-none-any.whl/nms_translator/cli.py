import click
from pathlib import Path
from nms_translator import __version__

LORE_PATH = Path().home() / "nms_lore.txt"


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "-x", "--xres", type=click.INT, help="Your display's X resolution", default=1920
)
@click.option(
    "-y", "--yres", type=click.INT, help="Your display's Y resolution", default=1080
)
def ts(xres: int, yres: int):
    from nms_translator.grabber import grab_screen
    from nms_translator.textract import extract_from_file
    from nms_translator.translator import translate

    screen = grab_screen()
    encoded_str = extract_from_file(screen)
    final = translate(encoded_str)
    with open(LORE_PATH, "a+") as f:
        f.write(f"{final}\n")


cli.add_command(ts)

if __name__ == "__main__":
    cli()
