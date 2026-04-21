from db_conexion import fetch_rows, update_codigo
from classifier import clasificar, cargar_categorias

COLUMNAS_MEJORAS = [
    ("mejoras1", "codigo_mejoras1"),
    ("mejoras2", "codigo_mejoras2"),
    ("mejoras3", "codigo_mejoras3"),
    ("mejoras4", "codigo_mejoras4"),
    ("mejoras5", "codigo_mejoras5"),
]


def procesar():
    rows = fetch_rows()
    categorias = cargar_categorias()  

    for row in rows:
        row_id = row["id"]

        print(f"\nProcesando ID: {row_id}")

        for col_mejora, col_codigo in COLUMNAS_MEJORAS:
            texto = row.get(col_mejora)

         
            if row.get(col_codigo) is not None:
                continue

            if texto and texto.strip():
                print(f" - {col_mejora}: {texto}")

                codigo = clasificar(texto, categorias)  

                if codigo:
                    print(f"   → Código: {codigo}")
                    update_codigo(row_id, col_codigo, codigo)
                else:
                    print("   → Error, no clasificado")

            else:
                continue


if __name__ == "__main__":
    procesar()