import os
from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Configuração da chave do OpenRouter via variável de ambiente
CHAVE_API = os.getenv('OPENROUTER_API_KEY')

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=CHAVE_API
)

# Definir o modelo a ser utilizado
MODELO = "openrouter/free"  # Substitua pelo modelo gratuito desejado no OpenRouter

@app.route('/', methods=['GET', 'POST'])
def index():
    pergunta = ""
    resposta = ""
    
    if request.method == 'POST':
        pergunta = request.form.get('pergunta', '')
        if pergunta.strip():
            try:
                completion = client.chat.completions.create(
                    model=MODELO,
                    messages=[
                        {"role": "user", "content": pergunta}
                    ]
                )
                resposta = completion.choices[0].message.content
            except Exception as e:
                resposta = f"Erro ao processar a pergunta: {str(e)}"
                
    return render_template('index.html', pergunta=pergunta, resposta=resposta)

if __name__ == '__main__':
    # Utiliza a porta definida pelo servidor de hospedagem (Render)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)