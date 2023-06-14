import os
import cv2
import keras_ocr
from flask import Flask, request

# Configurar Flask
app = Flask(__name__)

# Definir rota para o endpoint
@app.route('/', methods=['POST'])
def extract_text():
    # Verificar se há um arquivo de imagem na requisição
    if 'image' not in request.files:
        return 'Nenhuma imagem encontrada', 400

    # Carregar o modelo OCR
    pipeline = keras_ocr.pipeline.Pipeline()

    # Ler a imagem e converter para RGB
    image = request.files['image'].read()
    image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Processar a imagem para extrair o texto
    images = [image]
    images = [tools.read(image) for image in images]
    predictions = pipeline.recognize(images)

    # Extrair o texto das predições
    text = [text for text in predictions[0][0] if text]

    return '\n'.join(text)

if __name__ == '__main__':
    # Desabilitar suporte a GPU
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    # Iniciar o servidor Flask
    app.run()
