from flask import Flask, render_template, request
from PIL import ImageGrab, Image
import easyocr
import base64
import os

app = Flask(__name__)

def extract_text_from_image(img_path):
    reader = easyocr.Reader(['en'])
    img = Image.open(img_path)
    results = reader.readtext(img)
    text = ' '.join([result[1] for result in results])
    return text

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Lê a imagem enviada pelo usuário
        image_data = request.form['image']
        
        # Verifica se é uma imagem
        if image_data.startswith('data:image'):
            # Remove o prefixo "data:image/png;base64," para obter os dados da imagem
            image_data = image_data.replace('data:image/png;base64,', '')

            # Decodifica a string em base64 para obter os dados binários da imagem
            image_bytes = base64.b64decode(image_data)

            # Define o caminho de destino do arquivo
            upload_folder = 'static'
            filename = 'uploaded_image.png'
            destination = os.path.join(upload_folder, filename)

            # Salva a imagem no caminho de destino
            with open(destination, 'wb') as f:
                f.write(image_bytes)

            # Extrai o texto da imagem
            extracted_text = extract_text_from_image(destination)

            # Retorna uma mensagem de sucesso e o texto extraído
            return f'Imagem enviada com sucesso!\n\nTexto extraído:\n\n{extracted_text}'

    # Renderiza o template HTML
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
