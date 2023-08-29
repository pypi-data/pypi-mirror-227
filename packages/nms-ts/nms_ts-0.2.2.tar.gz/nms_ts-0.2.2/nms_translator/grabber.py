"""
Tool for grabbing screenshot
"""


def grab_screen(xres: int = 1920, yres: int = 1080) -> str:
    from PIL import ImageGrab
    from tempfile import mkstemp

    _, temp_filename = mkstemp(suffix=".png")
    img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
    img.save(temp_filename)
    return temp_filename
