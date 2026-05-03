# Algoritmos Python

Esta carpeta contiene scripts sencillos para apoyar la verificación comunitaria documental.

Los scripts están pensados para trabajar con matrices donde cada fila representa un documento y cada columna representa una pregunta de verificación.

## Archivo principal

`verificador_matriz.py`

## Qué hace

El script permite

1. Leer una matriz en CSV
2. Revisar las nueve preguntas clave
3. Detectar contradicciones básicas
4. Detectar información insuficiente
5. Detectar requisitos pendientes
6. Generar un reporte en Markdown

## Estados reconocidos

SÍ

NO CONSTA

PENDIENTE

?

N/A

También reconoce versiones sin tilde como SI.

## Uso básico

Desde la carpeta del repositorio

```bash
python algoritmos_python/verificador_matriz.py plantillas/matriz_vacia.csv reporte_verificacion.md
```

## Advertencia

Este script no reemplaza análisis jurídico.

Este script no decide si un proyecto es legal o ilegal.

Este script ayuda a ordenar señales documentales para que la comunidad pueda formular preguntas y solicitar aclaraciones.
