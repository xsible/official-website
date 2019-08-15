import os
from io import BytesIO
import base64
import sys

from flask import Flask, render_template, escape, send_from_directory, request, jsonify
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from PIL import Image
import numpy as np
import cv2


sys.path.append('ssd_pytorch')
from ssd_pytorch.inference import run_inference
predict_simple = None


SAVE_DATA = False
INPUT_IMG_PATH = 'static/images/input/'
OUTPUT_IMG_PATH = 'static/images/output/'

def cv2_img_from_upload(req_file):
    req_file.stream.seek(0) # return to the start of the stream
    data = np.fromstring(req_file.stream.read(), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    img_converted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_converted

def base64_from_numpy_img(img):
    im = Image.fromarray(img.astype('uint8'))
    rawBytes = BytesIO()

    im.save(rawBytes, 'JPEG')
    rawBytes.seek(0)  # return to the start of the file

    base64img = base64.encodestring(rawBytes.read())
    return base64img.decode().replace('\n', '')

app = Flask(__name__, static_folder='static')

# Max file upload size will be 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def app_handle_413(err):
    return 'Attempted to upload file that was too large.', 413

@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

@app.route('/contact', methods = ['POST'])
def contact():
    return render_template('index.html', thankyou=request.form['name'])

@app.route('/')
def index():
    return render_template('index.html', message='using machine learning to locate accessible parking spots')

@app.route('/file-upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        sfname = secure_filename(file.filename)

        if SAVE_DATA:
            input_path = os.path.join(INPUT_IMG_PATH, sfname)
            file.save(input_path)

        input_img = cv2_img_from_upload(file)
        output_img, pts = predict_simple(input_img)

        if SAVE_DATA:
            output_path = os.path.join(OUTPUT_IMG_PATH, f"{sfname.split('.')[0]}-output.jpg")
            cv2.imwrite(output_path, output_img)

        return jsonify({
            'base64': base64_from_numpy_img(output_img)
        })

if __name__ == '__main__':
    if SAVE_DATA:
        if not os.path.exists(INPUT_IMG_PATH):
            os.makedirs(INPUT_IMG_PATH)
        if not os.path.exists(OUTPUT_IMG_PATH):
            os.makedirs(OUTPUT_IMG_PATH)

    predict_simple = run_inference('model/custom.pth', cuda=False)
    app.run(debug=True, port=5000)