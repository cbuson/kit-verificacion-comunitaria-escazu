import sys
from pathlib import Path
from typing import Dict, List

import pandas as pd


CRITERIOS = {
    "1": "Ubicación justificada",
    "2": "Estudios ambientales suficientes",
    "3": "Licencia ambiental o concepto equivalente",
    "4": "Plan de manejo ambiental",
    "5": "Permisos ambientales específicos",
    "6": "Participación pública informada",
    "7": "Consulta previa cuando aplique",
    "8": "Viabilidad aprobada",
    "9": "Autoridad ambiental clara",
}


def normalizar_estado(valor: object) -> str:
    if pd.isna(valor):
        return ""

    texto = str(valor).strip().upper()

    equivalencias = {
        "SÍ": "SÍ",
        "SI": "SÍ",
        "NO": "NO CONSTA",
        "NO CONSTA": "NO CONSTA",
        "PENDIENTE": "PENDIENTE",
        "?": "?",
        "N/A": "N/A",
        "NA": "N/A",
        "": "",
    }

    return equivalencias.get(texto, texto)


def validar_columnas(df: pd.DataFrame) -> None:
    if "Documento" not in df.columns:
        raise ValueError("La matriz debe tener una columna llamada Documento.")

    faltantes = [criterio for criterio in CRITERIOS if criterio not in df.columns]

    if faltantes:
        raise ValueError(f"Faltan columnas de criterios: {', '.join(faltantes)}")


def analizar_criterio(df: pd.DataFrame, criterio: str) -> Dict[str, object]:
    estados = [normalizar_estado(valor) for valor in df[criterio].tolist()]
    documentos = df["Documento"].astype(str).tolist()

    pares = list(zip(documentos, estados))

    estados_relevantes = {estado for estado in estados if estado not in {"", "N/A"}}

    contradiccion = False
    informacion_insuficiente = False
    pendiente = False

    if "SÍ" in estados_relevantes and (
        "NO CONSTA" in estados_relevantes or "PENDIENTE" in estados_relevantes
    ):
        contradiccion = True

    if estados_relevantes == {"?"}:
        informacion_insuficiente = True

    if "PENDIENTE" in estados_relevantes:
        pendiente = True

    return {
        "criterio": criterio,
        "nombre": CRITERIOS[criterio],
        "pares": pares,
        "estados_relevantes": sorted(estados_relevantes),
        "contradiccion": contradiccion,
        "informacion_insuficiente": informacion_insuficiente,
        "pendiente": pendiente,
    }


def analizar_matriz(df: pd.DataFrame) -> List[Dict[str, object]]:
    validar_columnas(df)
    return [analizar_criterio(df, criterio) for criterio in CRITERIOS]


def construir_reporte(resultados: List[Dict[str, object]], archivo_origen: str) -> str:
    lineas = []

    lineas.append("# Reporte preliminar de verificación documental")
    lineas.append("")
    lineas.append(f"Archivo analizado: `{archivo_origen}`")
    lineas.append("")
    lineas.append("Este reporte es una ayuda de organización documental.")
    lineas.append("")
    lineas.append("No sustituye asesoría jurídica ni decisión de autoridad competente.")
    lineas.append("")
    lineas.append("## Resumen")
    lineas.append("")

    contradicciones = [r for r in resultados if r["contradiccion"]]
    insuficiencias = [r for r in resultados if r["informacion_insuficiente"]]
    pendientes = [r for r in resultados if r["pendiente"]]

    lineas.append(f"Contradicciones documentales detectadas: {len(contradicciones)}")
    lineas.append("")
    lineas.append(f"Alertas de información insuficiente: {len(insuficiencias)}")
    lineas.append("")
    lineas.append(f"Criterios con requisitos pendientes: {len(pendientes)}")
    lineas.append("")

    lineas.append("## Detalle por criterio")
    lineas.append("")

    for resultado in resultados:
        criterio = resultado["criterio"]
        nombre = resultado["nombre"]

        lineas.append(f"### Criterio {criterio}. {nombre}")
        lineas.append("")

        estados = ", ".join(resultado["estados_relevantes"]) or "Sin información"
        lineas.append(f"Estados encontrados: {estados}")
        lineas.append("")

        if resultado["contradiccion"]:
            lineas.append("Alerta: contradicción documental que requiere aclaración institucional.")
            lineas.append("")

        if resultado["informacion_insuficiente"]:
            lineas.append("Alerta: información insuficiente. No se afirma ocultamiento sin prueba. Se solicita aclaración.")
            lineas.append("")

        if resultado["pendiente"]:
            lineas.append("Alerta: existe información marcada como pendiente.")
            lineas.append("")

        lineas.append("| Documento | Estado |")
        lineas.append("|---|---|")

        for documento, estado in resultado["pares"]:
            estado_visible = estado or ""
            lineas.append(f"| {documento} | {estado_visible} |")

        lineas.append("")

    lineas.append("## Recomendación prudente")
    lineas.append("")
    lineas.append("Cuando existan contradicciones, ausencias o requisitos pendientes, la comunidad puede solicitar aclaración formal a la autoridad competente.")
    lineas.append("")
    lineas.append("El principio central es verificar sin acusar sin prueba.")
    lineas.append("")

    return "\n".join(lineas)


def main() -> None:
    if len(sys.argv) != 3:
        print("Uso: python verificador_matriz.py entrada.csv salida.md")
        sys.exit(1)

    entrada = Path(sys.argv[1])
    salida = Path(sys.argv[2])

    if not entrada.exists():
        print(f"No se encontró el archivo de entrada: {entrada}")
        sys.exit(1)

    try:
        df = pd.read_csv(entrada)
        resultados = analizar_matriz(df)
        reporte = construir_reporte(resultados, str(entrada))
        salida.write_text(reporte, encoding="utf-8")
        print(f"Reporte creado correctamente: {salida}")

    except Exception as error:
        print(f"Error al procesar la matriz: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
