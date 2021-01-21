from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_jsglue import JSGlue
from werkzeug.utils import secure_filename
from PIL import Image
from base64 import b64encode, b64decode
import os

from imageoperations import upload_image, convert_image

from rq import Queue
from worker import conn

app = Flask(__name__)
jsglue = JSGlue(app)

q = Queue(connection=conn
          )  # create an RQ queue. Will be used for the uploadImage() function.

os.environ["MAX_FILE_SIZE"] = "20"

app.config['UPLOAD_FOLDER'] = '/tmp/'
# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5 # 5MB size limit for uploading files.


@app.route('/', methods=['GET', 'POST'])
def index(error=" "):
    if (request.method == 'POST'):
        error = request.form.get('error')

    return render_template('input.html',
                           maxFileSize=os.environ.get("MAX_FILE_SIZE"),
                           error=error)


@app.route('/upload', methods=['POST'])
def upload_file():
    if (request.method == 'POST'):
        if (is_base64(request.files.get('file'))):
            imgData = request.files.get('file')
        else:
            imgData = b64encode(request.files.get('file').read())

    # Start the upload as a background task in the Redis queue
    task = q.enqueue(upload_image, imgData)

    # create a dictionary with the ID of the task
    responseObject = {"status": "success", "data": {"taskID": task.get_id()}}
    # return the dictionary
    return jsonify(responseObject)

    # elif (request.form.get('type') == 'txt'):
    # outputtxt, errors = img2txt.main(str(inp['link']),
    #                                  str(request.form.get('mode')),
    #                                  int(request.form.get('num_cols')),
    #                                  int(request.form.get('scale')))

    #     # upload the converted text to paste.ee
    #     paste = Paste(outputtxt, private=False, desc=inp['link'], views=10)

    #     # raw and download links
    #     raw_link = paste['raw']
    #     dl_link = paste['download']

    #     # Reduce the size of the preview text so that it doesn't overflow
    #     font_size = int(request.form.get('num_cols')) / (
    #         100 * int(request.form.get('scale')))

    #     return render_template('result.html',
    #                            type='txt',
    #                            output_file=outputtxt,
    #                            raw_link=raw_link,
    #                            dl_link=dl_link,
    #                            size=font_size,
    #                            errors=errors)


@app.route('/tasks/<taskID>', methods=['GET'])
def get_status(taskID):
    task = q.fetch_job(taskID)

    # If such a job exists, return its info
    if (task):
        responseObject = {
            "success": "success",
            "data": {
                "taskID": task.get_id(),
                "taskStatus": task.get_status(),
                "taskResult": task.result
            }
        }

    else:
        responseObject = {"status": "error"}

    return responseObject


@app.route('/convert', methods=['POST'])
def convert_file():
    if (request.method == 'POST'):

        # Start the image conversion as a background task in the Redis Queue
        task = q.enqueue(convert_image, str(request.form.get('imglink')),
                         str(request.form.get('type')),
                         str(request.form.get('mode')),
                         str(request.form.get('bg')),
                         int(request.values.get('num_cols')),
                         int(request.values.get('scale')))

        # create a dictionary with the ID of the task
        responseObject = {
            "status": "success",
            "data": {
                "taskID": task.get_id()
            }
        }

        # return the dictionary
        return jsonify(responseObject)


def is_base64(file):
    try:
        return b64decode(file.encode('ascii')) == file
    except Exception:
        return False


@app.errorhandler(404)
def request_page_not_found(error):
    return 'File doesnt exist', 404


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
