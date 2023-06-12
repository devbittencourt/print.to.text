from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import cv2
import pytesseract

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def extract_text_from_image(img_path):
    try:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError("Failed to load image")
        
        grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(grayscale_img)
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def show_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', error='No image selected.')
        
        image_file = request.files['image']
        if image_file.filename == '':
            return render_template('index.html', error='No image selected.')
        
        # Save the uploaded image to the UPLOAD_FOLDER
        filename = secure_filename(image_file.filename)
        img_path = app.config['UPLOAD_FOLDER'] + '/' + filename
        image_file.save(img_path)
        
        extracted_text = extract_text_from_image(img_path)
        return render_template('index.html', img_path=img_path, text=extracted_text)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
