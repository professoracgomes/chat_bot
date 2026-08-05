from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

CHAVE_API = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=CHAVE_API
)

MODELO = "openrouter/free"


@app.route("/", methods=["GET", "POST"])
def index():

    pergunta = ""
    resposta = ""
    erro = ""

    if request.method == "POST":

        pergunta = request.form.get("pergunta", "").strip()

        if not pergunta:
            erro = "Digite uma pergunta antes de enviar."

        elif not CHAVE_API:
            erro = "A variável OPENROUTER_API_KEY não foi configurada."

        else:
            try:
                resultado = client.chat.completions.create(
                    model=MODELO,
                    messages=[
                        {
                            "role": "user",
                            "content": pergunta
                        }
                    ]
                )

                resposta = resultado.choices[0].message.content

            except Exception as e:
                erro = f"Não foi possível consultar a IA: {e}"

    return render_template(
        "index.html",
        pergunta=pergunta,
        resposta=resposta,
        erro=erro
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True
    )