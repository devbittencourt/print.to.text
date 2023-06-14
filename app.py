from flask import Flask, request, jsonify, render_template
from keras_ocr import pipeline

app = Flask(__name__)

# Cria uma instância do pipeline fora da função para reutilização
pipeline_instance = pipeline.Pipeline()

@app.route('/', methods=['GET', 'POST'])
def process_image():
    if request.method == 'POST':
        # Verifica se foi fornecido o arquivo de imagem
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhum arquivo de imagem fornecido.'})

        image = request.files['image']
        
        # Lê a imagem a partir do arquivo
        image_data = image.read()

        # Utiliza o Keras-OCR pipeline para realizar a leitura da imagem e extrair o texto
        result = pipeline_instance.recognize(image_data)

        # Retorna o texto extraído como resposta em formato JSON
        return jsonify({'text': result})

    elif request.method == 'GET':
        # Retorna o conteúdo do arquivo 'index.html'
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
