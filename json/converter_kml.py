import xml.etree.ElementTree as ET
import json
import re

arquivo_kml = "PAA  RDP  SLN  SPD  ASO  CHQ.kml"

ns = {
    "kml": "http://www.opengis.net/kml/2.2"
}

tree = ET.parse(arquivo_kml)
root = tree.getroot()

sites = {}

for folder in root.findall(".//kml:Folder", ns):

    cidade_tag = folder.find("kml:name", ns)
    cidade = cidade_tag.text.strip() if cidade_tag is not None else "NÃO INFORMADA"

    for placemark in folder.findall("kml:Placemark", ns):

        nome_tag = placemark.find("kml:name", ns)

        if nome_tag is None:
            continue

        nome_original = nome_tag.text.strip()

        codigo = re.search(
            r"(SI[A-Z]{2,}\d+[A-Z]*|AMR\d+|SUM\d+)",
            nome_original.upper()
        )

        if codigo:
            codigo = codigo.group(0)
        else:
            codigo = nome_original.upper()

        desc_tag = placemark.find("kml:description", ns)
        descricao = ""

        if desc_tag is not None and desc_tag.text:
            descricao = desc_tag.text

            descricao = re.sub(r"<br\s*/?>", "\n", descricao)
            descricao = re.sub(r"<[^>]+>", "", descricao)
            descricao = descricao.strip()

        coord_tag = placemark.find(".//kml:coordinates", ns)

        latitude = ""
        longitude = ""

        if coord_tag is not None:

            coords = coord_tag.text.strip()

            partes = coords.split(",")

            if len(partes) >= 2:
                longitude = partes[0]
                latitude = partes[1]

        sites[codigo] = {
            "nome_original": nome_original,
            "cidade": cidade,
            "latitude": latitude,
            "longitude": longitude,
            "descricao": descricao
        }

with open("sites.json", "w", encoding="utf-8") as f:
    json.dump(
        sites,
        f,
        ensure_ascii=False,
        indent=4
    )

print(f"{len(sites)} sites exportados.")