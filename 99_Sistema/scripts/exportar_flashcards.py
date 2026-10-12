#!/usr/bin/env python3
"""Exporta las flashcards de la bóveda a un archivo TSV importable en Anki.

Busca en cada nota la sección "## Flashcards" y toma las líneas con el formato
`frente :: reverso` (también acepta `:::`, el formato bidireccional del plugin
Spaced Repetition de Obsidian).

Uso (desde la raíz de la bóveda):
    python 99_Sistema/scripts/exportar_flashcards.py
    python 99_Sistema/scripts/exportar_flashcards.py --nivel A1 --salida flashcards_A1.tsv

En Anki: Archivo → Importar → elegir el .tsv (separador: tabulador; la 3.ª columna son etiquetas).
"""
import argparse
import re
from pathlib import Path

import boveda as bv

CARPETAS = ["20_Conocimiento", "30_Curriculum", "40_Clases", "50_Cursos"]


def extraer_tarjetas(texto):
    tarjetas = []
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    dentro = False
    for linea in texto.splitlines():
        if linea.startswith("## "):
            dentro = linea[3:].strip().lower() == "flashcards"
            continue
        if dentro and "::" in linea:
            frente, reverso = re.split(r":{2,3}", linea, maxsplit=1)
            frente, reverso = frente.strip(" -"), reverso.strip()
            if frente and reverso:
                tarjetas.append((frente, reverso))
    return tarjetas


def etiqueta(texto):
    return re.sub(r"\s+", "_", texto.strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--boveda", default=str(Path(__file__).resolve().parents[2]), help="Raíz de la bóveda")
    parser.add_argument("--nivel", help="Exportar solo un nivel (A0, A1, A2, B1, B2, tutor)")
    parser.add_argument("--salida", default="flashcards.tsv", help="Archivo de salida")
    args = parser.parse_args()

    boveda = Path(args.boveda)
    filas = []
    for carpeta in CARPETAS:
        for nota in sorted((boveda / carpeta).rglob("*.md")):
            texto = nota.read_text(encoding="utf-8")
            props, _ = bv.separar(texto)
            niveles = bv.como_lista(props.get("nivel"))
            if args.nivel and args.nivel not in niveles:
                continue
            tags = [f"nivel_{n}" for n in niveles]
            if props.get("area"):
                tags.append(f"area_{props['area']}")
            tags.append(f"nota_{etiqueta(nota.stem)}")
            for frente, reverso in extraer_tarjetas(texto):
                filas.append("\t".join([frente, reverso, " ".join(tags)]))

    Path(args.salida).write_text("\n".join(filas) + ("\n" if filas else ""), encoding="utf-8")
    print(f"{len(filas)} flashcards exportadas a {args.salida}")


if __name__ == "__main__":
    main()
