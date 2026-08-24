from flask import Flask, render_template_string, request

app = Flask(__name__)

FORM_HTML = """
<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mapa de Inteligência</title>
    <style>
        :root {
            color-scheme: light;
            font-family: Georgia, "Times New Roman", serif;
            color: #1d2b2a;
            background: #f3efe7;
        }
        body {
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            padding: 2rem;
            box-sizing: border-box;
        }
        main {
            width: min(100%, 42rem);
            background: #fffdf8;
            border: 1px solid #d9d0c1;
            padding: clamp(1.5rem, 5vw, 3rem);
            box-sizing: border-box;
            box-shadow: 0 1rem 3rem rgb(52 45 33 / 10%);
        }
        h1 { margin-top: 0; font-size: clamp(2rem, 6vw, 3.25rem); }
        p { line-height: 1.6; }
        label { display: block; margin: 1.25rem 0 0.4rem; font-weight: 700; }
        input, textarea, button {
            width: 100%;
            box-sizing: border-box;
            font: inherit;
            padding: 0.8rem;
            border: 1px solid #a9b5ad;
            border-radius: 0.25rem;
        }
        textarea { min-height: 8rem; resize: vertical; }
        button {
            margin-top: 1.5rem;
            background: #1d5b52;
            color: white;
            border-color: #1d5b52;
            cursor: pointer;
        }
        button:hover { background: #16483f; }
        .success {
            border-left: 4px solid #1d5b52;
            padding: 0.75rem 1rem;
            background: #e5f0e9;
        }
    </style>
</head>
<body>
<main>
    <h1>Mapa de Inteligência</h1>
    <p>Registre uma ideia, observação ou hipótese para organizar sua análise.</p>
    {% if submitted %}
    <p class="success" role="status">Resposta registrada com sucesso.</p>
    {% endif %}
    <form method="post">
        <label for="nome">Nome</label>
        <input id="nome" name="nome" autocomplete="name" required>

        <label for="tema">Tema</label>
        <input id="tema" name="tema" required>

        <label for="observacao">Observação</label>
        <textarea id="observacao" name="observacao" required></textarea>

        <button type="submit">Enviar resposta</button>
    </form>
</main>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    submitted = request.method == "POST"
    return render_template_string(FORM_HTML, submitted=submitted)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
