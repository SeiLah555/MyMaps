import json
import os
import re

PASTA = "."

for arquivo in os.listdir(PASTA):

    if not arquivo.endswith(".json"):
        continue

    print(f"Limpando {arquivo}")

    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    for site in dados.values():

        descricao = site.get("descricao", "")

        # substitui vários espaços por apenas 1
        descricao = re.sub(r"[ \t]+", " ", descricao)

        # remove espaços antes/depois de quebra de linha
        descricao = re.sub(r" *\n *", "\n", descricao)

        # remove mais de duas linhas vazias
        descricao = re.sub(r"\n{3,}", "\n\n", descricao)

        descricao = descricao.strip()

        site["descricao"] = descricao

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(
            dados,
            f,
            ensure_ascii=False,
            indent=4
        )

print("Finalizado!")