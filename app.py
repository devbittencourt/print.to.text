from flask import Flask, render_template, request
from PIL import ImageGrab, Image
import pytesseract
import base64

app = Flask(__name__)

caminho = r"C:\Program Files\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

def extract_text_from_image(img_path):
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    return text

@app.route('/', methods=['GET', 'POST'])
def show_image():
    if request.method == 'POST' and 'image_data' in request.form:
        image_data = request.form['image_data']
        img_data = base64.b64decode(image_data.split(',')[1])

        img_path = 'static/clipboard_image.png'
        with open(img_path, 'wb') as f:
            f.write(img_data)

        extracted_text = extract_text_from_image(img_path)
        return render_template('index.html', img_path=img_path, text=extracted_text)
    else:
        img = ImageGrab.grabclipboard()
        img_path = 'static/clipboard_image.png'

        if img is not None:
            img.save(img_path)
            extracted_text = extract_text_from_image(img_path)
            return render_template('index.html', img_path=img_path, text=extracted_text)
        else:
            return render_template('index.html', img_path=None, text=None)

if __name__ == '__main__':
    app.run()
