from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import pyimgur
from base64 import b64encode
import img2img, img2txt
from pasteee import Paste
import os

app = Flask(__name__)

im = pyimgur.Imgur(os.environ.get("IMGUR_KEY"))

app.config['UPLOAD_FOLDER'] = '/tmp/'


@app.route('/')
def index():
    return render_template('input.html')


@app.route('/convert', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('input.html',
                                   error="Select an image first.")
        file = request.files['file']
        if file.filename == '':
            return render_template('input.html',
                                   error="Select an image first.")
        if file:
            inputimg = b64encode(file.read())
            inp = im._send_request('https://api.imgur.com/3/image',
                                   method='POST',
                                   params={'image': inputimg})
            print(inp['link'])
            if request.form.get('type') == 'img':
                outputimg, errors = img2img.main(
                    str(inp['link']), str(request.form.get('mode')),
                    str(request.form.get('background')),
                    int(request.form.get('num_cols')),
                    int(request.form.get('scale')))

                outimg = b64encode(outputimg)
                out = im._send_request('https://api.imgur.com/3/image',
                                       method='POST',
                                       params={'image': outputimg})
                print(out['link'])
                outlink = out['link'].replace('https://i.imgur.com/', '')
                outlink = outlink.replace('.jpg', '')
                print(outlink)
                return render_template('result.html',
                                       type='img',
                                       output_file=outlink,
                                       outimg=outimg,
                                       errors=errors)
            else:
                outputtxt, errors = img2txt.main(
                    str(inp['link']), str(request.form.get('mode')),
                    int(request.form.get('num_cols')),
                    int(request.form.get('scale')))

                                # upload the converted text to paste.ee
                paste = Paste(outputtxt, private=False, desc=inp['link'], views=10)

                # raw and download links
                raw_link = paste['raw']
                dl_link = paste['download']

                # Reduce the size of the preview text so that it doesn't overflow
                font_size = int(request.form.get('num_cols')) / (100 * int(request.form.get('scale')))

                return render_template('result.html',
                                       type='txt',
                                       output_file=outputtxt,
                                       raw_link=raw_link,
                                       dl_link=dl_link,
                                       size=font_size,
                                       errors=errors)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
