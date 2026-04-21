import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Cargar categorías desde JSON
def cargar_categorias(path="data/listado_categorias.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

        if isinstance(data, dict) and "categorias" in data:
            return data["categorias"]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Formato de categorías no válido")


#Construir string para el prompt
def construir_categorias_prompt(categorias):
    return "\n".join(
        [f"{c['codigo']} - {c['categoria']}" for c in categorias]
    )


#Validar código devuelto
def validar_codigo(codigo, categorias):
    codigos_validos = {c["codigo"] for c in categorias}
    return codigo if codigo in codigos_validos else "99"


def clasificar(texto, categorias):
    if not texto or texto.strip() == "":
        return None

    categorias_prompt = construir_categorias_prompt(categorias)

    prompt = f"""
Eres un clasificador de respuestas de encuestas de transporte.

TAREA:
Clasifica la siguiente respuesta en UNA SOLA categoría.

IMPORTANTE:
- Ignora palabras como: "gracias", "aunque no está mal", "por favor"
- Corrige errores tipográficos (ej: "menosgente" -> "menos gente")
- Devuelve SOLO el código (ej: 02), sin texto adicional

CATEGORÍAS:
{categorias_prompt}

RESPUESTA:
"{texto}"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        result = response.choices[0].message.content.strip()

        # limpieza extra
        result = result.replace('"', '').replace("'", "").strip()
        result = result.split()[0]  # por si devuelve "02 algo"

        result = validar_codigo(result, categorias)

        return result

    except Exception as e:
        print(f"Error clasificando: {texto} -> {e}")
        return None