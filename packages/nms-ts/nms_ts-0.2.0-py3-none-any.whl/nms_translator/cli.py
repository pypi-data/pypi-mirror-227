import click
from nms_translator import __version__

LORE_PATH = "~/nms_lore.txt"


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
    import os
    from nms_translator.grabber import grab_screen
    from nms_translator.textract import extract_from_file
    from nms_translator.translator import translate

    screen = grab_screen()
    encoded_str = extract_from_file(screen)
    final = translate(encoded_str)
    write_mode = "a"
    if not os.path.isfile(LORE_PATH):
        write_mode = "w"
    with open(LORE_PATH, write_mode) as f:
        f.write(f"{final}\n")


cli.add_command(ts)

if __name__ == "__main__":
    cli()
