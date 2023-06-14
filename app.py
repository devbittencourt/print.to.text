from flask import Flask, request, jsonify
from keras_ocr import pipeline

app = Flask(__name__)
ocr_pipeline = pipeline.Pipeline()

@app.route('/', methods=['POST'])
def process_image():
    image_base64 = request.form.get('image')

    # Realiza a leitura da imagem usando OCR
    result = ocr_pipeline.recognize([image_base64])

    # Extrai o texto detectado
    text = result[0]['text']

    # Retorna o texto como resposta em formato JSON
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run()
