# qr.py

import tempfile

from PIL import Image
import qrcode
from pyzbar.pyzbar import decode as extract

__all__ = [
    "encode",
    "decode",
    "extract"
]

def encode(data: bytes) -> Image:
    """
    Encodes the data into an image of a qr code.

    :param data: The source data to encode.

    :return: The image object with the qr code.
    """

    file = tempfile.TemporaryFile()

    file.close()

    qrcode.make(data).save(file.name)

    return Image.open(file.name)
# end encode

def decode(data: Image.Image) -> bytes:
    """
    Decodes the qr code in the image to a string.

    :param data: The data of the qr code image.

    :return: The extracted data from the qr code.
    """

    restored = []

    for shape in extract(data):
        restored.append(shape.data)
    # end for

    return b"".join(restored)
# end decode