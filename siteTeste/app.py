from flask import Flask, request, send_file, render_template
from google.cloud import texttospeech
import os

app = Flask(__name__)

# Configurar as credenciais da API do Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/miche/ProjectsIA/TxtToSpch/vlc/youtube-voz-49b5c180f006.json"

# Instanciar o cliente de Text-to-Speech
client = texttospeech.TextToSpeechClient()

# Dicionário de vozes e gêneros
voices = {
    "pt-BR-Wavenet-A": texttospeech.SsmlVoiceGender.MALE,
    "pt-BR-Wavenet-B": texttospeech.SsmlVoiceGender.MALE,
    "pt-BR-Wavenet-C": texttospeech.SsmlVoiceGender.FEMALE,
    "pt-BR-Wavenet-D": texttospeech.SsmlVoiceGender.FEMALE
}

# Configurar o diretório de upload
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    text = request.form['text']
    voice_name = request.form['voice']
    rate = float(request.form['rate'])
    pitch = float(request.form['pitch'])

    # Definir o texto a ser sintetizado usando SSML
    ssml_text = f"""
    <speak>
        <p>{text}</p>
    </speak>
    """

    # Configurar a solicitação com o texto, voz e parâmetros de áudio
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        name=voice_name,
        ssml_gender=voices[voice_name]
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=rate,
        pitch=pitch
    )

    # Realizar a síntese de texto para fala
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Salvar o arquivo de áudio resultante
    audio_file = 'exemplo.mp3'
    with open(audio_file, "wb") as out:
        out.write(response.audio_content)

    return send_file(audio_file, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Ler o conteúdo do arquivo
        with open(filepath, 'r') as f:
            text = f.read()
        
        # Processar o texto como antes (pode incluir chamada para função de síntese)
        return f'File uploaded and content: {text}'

if __name__ == '__main__':
    app.run(debug=True)
