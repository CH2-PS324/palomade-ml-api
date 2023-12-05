import os
import numpy as np
from PIL import Image
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as tf_image

load_dotenv()
app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

app.config['MODEL_SAWIT'] = 'models/model_bongkahan_v2.h5'
# app.config['MODEL_SAWIT_2'] = 'models/model_bongkahan_v2.h5'



model_sawit = load_model(app.config['MODEL_SAWIT'], compile=False)
# model_sawit_2 = load_model(app.config['MODEL_SAWIT_2'], compile=False)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
           
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': {
            'code': 200,
            'message': 'Hello World!'
        }
    }), 200

@app.route('/predict', methods=['POST'])
def predict_bongkahan():
    if request.method == 'POST':
        reqImage = request.files['image']
        if reqImage and allowed_file(reqImage.filename):
            filename = secure_filename(reqImage.filename)
            reqImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img = Image.open(image_path).convert("RGB")
            img = img.resize((150, 150))
            x = tf_image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = x / 255
            result = model_sawit.predict(x)[0][0]
            # result2 = model_sawit_2.predict(x)[0][0]
            if(result > 0.5):
                return jsonify({
                    'status': {
                        'code': 200,
                        'message': 'Success predicting',
                        'data': { 'class': 'Mentah', 'precentase': int(result * 100) },
                        # 'data2': { 'class': 'Mentah', 'precentase': int(result2 * 100) }
                    }
                }), 200
            else:
                return jsonify({
                    'status': {
                        'code': 200,
                        'message': 'Success predicting',
                        'data': { 'class': 'Matang', 'precentase': (100 - int(result * 100)) },
                        # 'data2': { 'class': 'Matang', 'precentase': (100 - int(result2 * 100)) }
                    }
                }), 200
        else:
            return jsonify({
                'status': {
                    'code': 400,
                    'message': 'Invalid file format. Please upload a JPG, JPEG, or PNG image.'
                }
            }), 400
    else:
        return jsonify({
            'status': {
                'code': 405,
                'message': 'Method not allowed'
            }
        }), 405

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))