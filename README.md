# 🧠 Codificador automático de respuestas abiertas (Survey Coding AI)

Este proyecto implementa un sistema automático de codificación de respuestas abiertas en encuestas de satisfacción, utilizando modelos de lenguaje (LLMs) a través de la API de OpenAI.

El objetivo es transformar respuestas textuales libres a una clasificación estructurada basada en un listado cerrado de categorías previamente definido.

``` text 

codificador_respuestas_abiertas/
│
├── src/
│   ├── main.py                # Script principal
│   ├── db_conexion.py                  # Conexión y operaciones SQL
│   ├── classifier.py          # Lógica de clasificación (prompt + API)
│
│
├── data/
│   ├── listado_categorias.json        # Listado cerrado de categorías
│
│
├── .env                       # Variables sensibles
├── requirements.txt
└── README.md
```
## 🗂️ Categorías

Las categorías están definidas en:

`data/listado_categorias.json`


| Código | Categoría |
|--------|----------|
| C01 | Puntualidad (retrasos, horarios incumplidos) |
| C02 | Frecuencia insuficiente |
| C03 | Precio alto |
| C04 | Limpieza |
| C05 | Comodidad (asientos, espacio, etc.) |
| C06 | Atención del personal |
| C07 | Información / claridad de horarios |
| C08 | Seguridad |
| C09 | Accesibilidad (PMR, carritos, etc.) |
| C10 | Cobertura de rutas |
| C11 | App / web / tecnología |
| C12 | Masificación / demasiada gente |
| C13 | Climatización (frío/calor) |
| C14 | Ruido |
| C15 | Ninguna mejora / todo bien / NS |

## 🗄️ Estructura recomendada de base de datos

Tabla principal:

```
CREATE TABLE encuesta_transporte (

    id INT PRIMARY KEY,
    mejoras1 NVARCHAR(255),
    mejoras2 NVARCHAR(255),
    mejoras3 NVARCHAR(255),
    mejoras4 NVARCHAR(255),
    mejoras5 NVARCHAR(255),

    codigo_mejoras1 NVARCHAR(3),
    codigo_mejoras2 NVARCHAR(3),
    codigo_mejoras3 NVARCHAR(3),
    codigo_mejoras4 NVARCHAR(3),
    codigo_mejoras5 NVARCHAR(3)
);
```

## 🔄 Flujo de procesamiento

- Se obtienen filas desde la base de datos

- Para cada fila:
    - Se recorren las columnas mejoras1...5
    - Si no están codificadas:
    - Se envía el texto al clasificador
    - Se obtiene un código (C01...C15)
    - Se actualiza la base de datos



## 🧠 Lógica de clasificación

El sistema utiliza un modelo de OpenAI (gpt-4.1-mini) con un prompt diseñado para:

- Corregir errores tipográficos
- Ignorar ruido ("gracias", "todo bien", etc.)
- Clasificar en una única categoría
- Devolver únicamente el código (ej: C07)


## ⚙️ Requisitos

- Python 3.9+
- SQL Server
- Driver ODBC 17 para SQL Server
- API Key de OpenAI

Instalar dependencias:

`pip install -r requirements.txt`

## 💡 Nota final

Este proyecto convierte texto libre en datos estructurados listos para análisis (BI, dashboards, etc.). Es especialmente útil para explotar preguntas abiertas en encuestas sin necesidad de codificación manual.