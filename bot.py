import json
import os
import re

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

# ==========================
# TOKEN DO BOT
# ==========================

TOKEN = "8553475552:AAFnFo0TbsOkX5yzx-2eaZRhD6m9PUMeaFE"

# ==========================
# BANCO EM MEMÓRIA
# ==========================

sites = {}

# ==========================
# CARREGAR TODOS OS JSONS
# ==========================

def carregar_todos_json():

    sites.clear()

    pasta = "json"

    if not os.path.exists(pasta):
        print(f"Pasta '{pasta}' não encontrada.")
        return

    total = 0

    for arquivo in os.listdir(pasta):

        if not arquivo.lower().endswith(".json"):
            continue

        caminho = os.path.join(pasta, arquivo)

        try:

            with open(
                caminho,
                "r",
                encoding="utf-8"
            ) as f:

                dados = json.load(f)

            for codigo, info in dados.items():

                codigo = codigo.upper().strip()

                sites[codigo] = {
                    "descricao": info.get(
                        "descricao",
                        ""
                    ),
                    "lat": str(
                        info.get(
                            "latitude",
                            ""
                        )
                    ),
                    "lon": str(
                        info.get(
                            "longitude",
                            ""
                        )
                    ),
                    "cidade": info.get(
                        "cidade",
                        ""
                    ),
                    "arquivo": arquivo
                }

            print(
                f"{arquivo} -> {len(dados)} sites"
            )

            total += len(dados)

        except Exception as erro:

            print(
                f"Erro em {arquivo}: {erro}"
            )

    print()
    print(f"Total carregado: {total} sites")
    print()

# ==========================
# START
# ==========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🤖 Bot de Consulta de Sites\n\n"
        "Digite o nome do site.\n\n"
        "Exemplos:\n"
        "SIAMR01\n"
        "SISTB01\n"
        "SISUM01"
    )

# ==========================
# CONSULTA
# ==========================

async def consultar(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    texto = update.message.text

    if not texto:
        return

    pesquisa = texto.upper().strip()

    match = re.search(
        r"[A-Z]{2,}\d+[A-Z]*",
        pesquisa
    )

    if match:
        pesquisa = match.group(0)

    if pesquisa in sites:

        info = sites[pesquisa]

        descricao = info["descricao"]

# transforma qualquer bloco grande de espaços em quebra de linha
        descricao = re.sub(r"\s{4,}", "\n", descricao)

# remove linhas vazias repetidas
        descricao = re.sub(r"\n+", "\n", descricao)

        descricao = descricao.strip()

        resposta = f"""📍 {pesquisa}

🏙 Cidade: {info.get('cidade', '')}

🌎 Latitude: {info['lat']}
🌎 Longitude: {info['lon']}

📂 Arquivo:
{info['arquivo']}

📝 Informações:

{descricao}

🔗 Google Maps:
https://maps.google.com/?q={info['lat']},{info['lon']}
"""

        await update.message.reply_text(
            resposta[:4000]
        )

        return

    # busca parcial
    resultados = []


    # ======================
    # BUSCA PARCIAL
    # ======================

    resultados = []

    for site in sites:

        if pesquisa in site:
            resultados.append(site)

    if resultados:

        resultados.sort()

        resposta = (
            "❓ Site não encontrado exatamente.\n\n"
            "Possíveis resultados:\n\n"
        )

        resposta += "\n".join(
            resultados[:50]
        )

        await update.message.reply_text(
            resposta
        )

        return

    await update.message.reply_text(
        "❌ Site não encontrado."
    )

# ==========================
# MAIN
# ==========================

def main():

    carregar_todos_json()

    app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT &
            ~filters.COMMAND,
            consultar
        )
    )

    print("Bot iniciado...")

    app.run_polling()

# ==========================

if __name__ == "__main__":
    main()