import base64
import json
import os

import pyimgur

import img2img
import img2txt
from pasteee import Paste


im = pyimgur.Imgur(os.environ.get("IMGUR_KEY"))


# Converts the image into and ASCII-fied image or text.
def convert_image(imglink, conv_type, mode, bg, num_cols, scale):

    if (conv_type == 'img'):
        convertedImage, errors = img2img.main(imglink, mode, bg, num_cols,
                                              scale)

        responseObject = upload_image(base64.b64encode(convertedImage))

    elif (conv_type == 'txt'):
        convertedText, errors = img2txt.main(imglink, mode, num_cols, scale)

        responseObject = upload_text(convertedText)

    else:
        responseObject = {
            "result": {
                'mainResult': "none",
                'raw': "none",
                'dl': "none"
            },
            "errors": "conv_type not specified!"
        }

    return responseObject


# Uploads the passed image file to Imgur anonymously. Returns the unique ID of the image.
def upload_image(imgToUpload):
    out = im._send_request('https://api.imgur.com/3/image',
                           method='POST',
                           params={'image': imgToUpload})

    downloadLink = out['link'].replace('https://i.imgur.com/',
                                       'https://imgur.com/download/')
    downloadLink = downloadLink.replace('.jpg', '')

    responseObject = {
        "result": {
            'mainResult': out['link'],
            'raw': out['link'],
            'dl': downloadLink
        },
        "errors": 'none'
    }

    return responseObject


# Uploads the passed text string to Paste.ee anonymously. Returns the unique ID of the paste.
def upload_text(textToUpload):

    # upload the converted text to paste.ee. Will get deleted after 10 views.
    out = Paste(textToUpload,
                private=False,
                desc="Pic2ASCII - Result",
                views=10)
    responseObject = {
        "result": {
            'mainResult': textToUpload,
            'raw': out['raw'],
            'dl': out['download']
        },
        "errors": 'none'
    }

    return responseObject
