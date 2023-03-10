import io
from PIL import Image
import requests
from rembg import remove
from flask_cors import CORS
import uuid
import os

from flask import Flask, request
app = Flask(__name__)
CORS(app)

@app.route('/remove_bg', methods=['POST'])

def predict():
    if request.method == 'POST':
        content = request.json
        image_url = content['image']
        image_data = requests.get(image_url).content
        image = Image.open(io.BytesIO(image_data))

        output = remove(image)
        filepath = f'static/{str(uuid.uuid4())}.png'

        # Create the necessary directories if they do not exist
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        output.save(filepath)

        return f'/{filepath}'


@app.route('/delete', methods=['POST'])
def remove_images():
    if request.method == 'POST': 
        password = request.json['password']
        if password == 'oranges4life':
            for root, dirs, files in os.walk('static'):
                for file in files:
                    os.remove(os.path.join(root, file))
            return 'Images removed!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
