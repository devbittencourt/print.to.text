from flask import Flask, render_template
import cv2
import pytesseract

app = Flask(__name__)

def extract_text_from_image(img_path):
    img = cv2.imread(img_path)
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(grayscale_img)
    return text

@app.route('/')
def show_image():
    img_path = 'static/clipboard_image.png'

    extracted_text = extract_text_from_image(img_path)
    return render_template('index.html', img_path=img_path, text=extracted_text)

if __name__ == '__main__':
    app.run()
