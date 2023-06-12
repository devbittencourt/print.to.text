from flask import Flask, render_template, request
import cv2
import pytesseract

app = Flask(__name__)

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
        image_file = request.files['image']
        img_path = 'static/' + image_file.filename
        image_file.save(img_path)

        extracted_text = extract_text_from_image(img_path)
        return render_template('index.html', img_path=img_path, text=extracted_text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
