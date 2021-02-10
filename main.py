from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_jsglue import JSGlue
from werkzeug.utils import secure_filename
from PIL import Image
from base64 import b64encode, b64decode
import os

from imageoperations import upload_image, convert_image

app = Flask(__name__)
jsglue = JSGlue(app)

os.environ["MAX_FILE_SIZE"] = "20"
app.config['UPLOAD_FOLDER'] = '/tmp/'


@app.route('/', methods=['GET', 'POST'])
def index(error=" "):
    if (request.method == 'POST'):
        error = request.form.get('error')

    return render_template('input.html',
                           maxFileSize=os.environ.get("MAX_FILE_SIZE"),
                           error=error)


@app.route('/convert', methods=['POST'])
def convert_file():
    if (request.method == 'POST'):
        # Start the image conversion as a background task in the Redis Queue
        responseObject = convert_image(request.files['image'],
                         str(request.form.get('type')),
                         str(request.form.get('mode')),
                         str(request.form.get('bg')),
                         int(request.values.get('num_cols')),
                         int(request.values.get('scale')))

        
        # return the dictionary
        return responseObject


@app.errorhandler(404)
def request_page_not_found(error):
    return '404', 404


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
