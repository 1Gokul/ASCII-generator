from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import pyimgur
from base64 import b64encode
import img2img, img2txt
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
            inp = im._send_request('https://api.imgur.com/3/image', method='POST', params={'image': inputimg})
            print(inp['link'])
            if request.form.get('type') == 'img':
                outputimg = b64encode(img2img.main(str(inp['link']),
                            str(request.form.get('mode')),
                            str(request.form.get('background')),
                            int(request.form.get('num_cols')),
                            int(request.form.get('scale'))))


                out = im._send_request('https://api.imgur.com/3/image', method='POST', params={'image': outputimg})
                print(out['link'])
                outlink = out['link'].strip('https://i.imgur.com/')
                outlink = outlink.strip('.jpg')
                print(outlink)

                return render_template('result.html',
                                        type = 'img',
                                    output_file=outlink)
                # else:
                #     fname = os.path.splitext(filename)[0] + '.txt'
                #     img2txt.main(str("tmp/input/" + filename),
                #                 str("tmp/output/ASCII_" + fname),
                #                 str(request.form.get('mode')),
                #                 int(request.form.get('num_cols')),
                #                 int(request.form.get('scale')))
                #     outputfilename = "/tmp/output/ASCII_" + fname
                #     return render_template('result.html',
                #                             type = 'txt',
                #                         output_file=outputfilename)

            else:
                return render_template('input.html',
                                   error="Unsupported file format.")    
                        
def checkifimage(path_to_image):
    try:
        Image.open(path_to_image)
    except IOError:
        return False
    return True

                    


if __name__ == '__main__':
    app.run(debug=True)
