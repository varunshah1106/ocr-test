import os
import logging
import json
import pytesseract
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify, render_template

from ocr import VisionApi

app = Flask(__name__)
_VERSION = 1  # API version


@app.route('/')
def main():
    return render_template('index.html')

"""
<form role="form" method="POST" id="post-form" action="{{ url_for('ocr') }}" enctype=multipart/form-data>
  <div class="form-group">
    <input type="file" class="form-control input-lg" name="image_url" placeholder="Upload your image" required></center>
  </div>
  <input type="submit" class="btn btn-lg btn-block btn-success boom" id="search">Submit!</input>
</form>
"""

@app.route('/ocr/', methods=["POST"])
def ocr():
    image = request.files['file']
    response = VisionApi().detect_text(image.read())[0]
    print response['textAnnotations'][0]['description']
    #print response[0]['textAnnotations'][0]['description'][0]
    """try:
        url = request.json['image_url']
        if 'jpg' in url:
            output = process_image(url)
            return jsonify({"output": output})
        else:
            return jsonify({"error": "only .jpg files, please"})
    except:
        return jsonify(
            {"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}"}
        )"""
    pytesseract.image_to_string(image.open())
    return render_template('index.html', result=response['textAnnotations'][0]['description'])


@app.errorhandler(500)
def internal_error(error):
    print str(error)  # ghetto logging


@app.errorhandler(404)
def not_found_error(error):
    print str(error)

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
