NMS Lore Translator
===

With the Echoes update, No Man's Sky introduced some dialogue written in binary. I created this tool so that I could easily grab the screen, extract the binary text, and then convert it to UTF-8 characters. It will then append each new bit of lore to a file in your home folder.

Caveats
---

This was only tested on Ubuntu 23.04 with a screen resolution of 1920x1080 and the game running in full screen. It should, theoretically, work on any OS with the Tesseract OCR library installed, but it has not at all been tested and I take no responsibilites for this.

Installation
---

You can either clone this repository and then run `poetry build && pip3 install --user dist/nms_translator-<version>-py3-none-any.whl` or you can install from PyPi with just `pip3 install --user nms-ts`