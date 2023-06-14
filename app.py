from flask import Flask, request, jsonify
from keras_ocr import pipeline
import os
import base64
from PIL import Image
import io

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

app = Flask(__name__)
ocr_pipeline = pipeline.Pipeline()

@app.route('/')
def process_image():
    image_file = request.files['image']

    if image_file is None:
        return jsonify({'error': 'Image data not provided'})

    # Lê a imagem a partir do arquivo
    image = Image.open(image_file)

    # Realiza a leitura da imagem usando OCR
    result = ocr_pipeline.recognize([image])

    # Extrai o texto detectado
    text = result[0]['text']

    # Retorna o texto como resposta em formato JSON
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run()
