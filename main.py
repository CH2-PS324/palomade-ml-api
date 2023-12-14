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

# Set Allowed Extension for Upload File
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Load Model
app.config['MODEL_BONGKAHAN'] = 'models/bongkahan/model_bongkahan_v2.h5'
app.config['MODEL_BRONDOLAN'] = 'models/brondolan/model-brondolan.h5'
app.config['MODEL_NON_SAWIT'] = 'models/deteksi-sawit/model-nonsawit_v2.h5'

# Assign to variable
model_non_sawit = load_model(app.config['MODEL_NON_SAWIT'], compile=False)
model_bongkahan = load_model(app.config['MODEL_BONGKAHAN'], compile=False)
model_brondolan = load_model(app.config['MODEL_BRONDOLAN'], compile=False)

# Function to check allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
           
# Route Index
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': {
            'code': 200,
            'message': 'Model Palomade',
            'teamName': 'CH2-PS324'
        }
    }), 200

# Route Predict
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        reqImage = request.files['image'] # Get Image Files
        reqType = request.form['type'] # Get Type of Scan : bongkahan or brondolan
        if reqImage and allowed_file(reqImage.filename):
            filename = secure_filename(reqImage.filename)
            reqImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img = Image.open(image_path).convert("RGB")
            img = img.resize((150, 150))
            x = tf_image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = x / 255
            detect_non_sawit = model_non_sawit.predict(x)[0][0] # Predict Non Sawit
            # Check if Sawit
            if(detect_non_sawit > 0.5):
                # Check if Bongkahan
                if(reqType == "bongkahan"):
                    detect_bongkahan = model_bongkahan.predict(x)[0][0] # Predict Bongkahan
                    # if sawit bongkahan mentah
                    if(detect_bongkahan > 0.5):
                        return jsonify({
                            'status': {
                                'code': 200,
                                'message': 'Success predicting',
                                'data': { 'classType': 'Bongkahan Sawit Mentah', 'precentase': int(detect_bongkahan * 100) },
                            }
                        }), 200
                    # if sawit bongkahan matang
                    else:
                        return jsonify({
                            'status': {
                                'code': 200,
                                'message': 'Success predicting',
                                'data': { 'classType': 'Bongkahan Sawit Matang', 'precentase': (100 - int(detect_bongkahan * 100)) },
                            }
                        }), 200
                # Check if brondolan
                elif(reqType == "brondolan"):
                    detect_brondolan = model_brondolan.predict(x)[0][0] # predict brondolan
                    # if sawit brondolan mentah
                    if(detect_brondolan > 0.5):
                        return jsonify({
                            'status': {
                                'code': 200,
                                'message': 'Success predicting',
                                'data': { 'classType': 'Brondolan Sawit Mentah', 'precentase': int(detect_brondolan * 100) },
                            }
                        }), 200
                    # if sawit brondolan matang
                    else:
                        return jsonify({
                            'status': {
                                'code': 200,
                                'message': 'Success predicting',
                                'data': { 'classType': 'Brondolan Sawit Matang', 'precentase': (100 - int(detect_brondolan * 100)) },
                            }
                        }), 200
                # Check if not bongkahan or brondolan
                else:
                    return jsonify({
                        'status': {
                            'code': 400,
                            'message': 'Invalid type of scan. Please choose bongkahan or brondolan.'
                        }
                    }), 400
            # non sawit
            else:
                return jsonify({
                    'status': {
                        'code': 200,
                        'message': 'Success predicting',
                        'data': { 'classType': 'Bukan Sawit', 'precentase': (100 - int(detect_non_sawit * 100)) },
                    }
                }), 200
        # if not allowed file
        else:
            return jsonify({
                'status': {
                    'code': 400,
                    'message': 'Invalid file format. Please upload a JPG, JPEG, or PNG image.'
                }
            }), 400
    # if not POST method
    else:
        return jsonify({
            'status': {
                'code': 405,
                'message': 'Method not allowed'
            }
        }), 405

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))