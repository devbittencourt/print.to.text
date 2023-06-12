from flask import Flask, render_template
from PIL import ImageGrab, Image
import pytesseract

app = Flask(__name__)


def extract_text_from_image(img_path):
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    return text

@app.route('/')
def show_image():
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
