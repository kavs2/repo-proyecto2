"""
PROY-2: Script de Análisis de Datos Climáticos
================================================
Cátedra: Organización Empresarial - UTN TUP
Escenario A: Análisis de Datos Climáticos
Autor: P2 - Desarrollador Técnico (Rol: Paco)

Descripción:
    Este script procesa datos climáticos históricos mensuales (temperatura máxima,
    mínima, promedio y precipitaciones) para una ciudad del sur de Argentina,
    calculando indicadores estadísticos básicos y generando visualizaciones
    exportadas automáticamente a la carpeta /resultados.

Uso en Google Colab:
    1. Clonar el repositorio con git clone.
    2. Ejecutar: !python scripts/analisis_datos.py
    3. Los resultados se guardan en la carpeta /resultados.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# ──────────────────────────────────────────────
# 1. CONFIGURACIÓN DE RUTAS (relativas al repo)
# ──────────────────────────────────────────────
# Se usan rutas relativas para garantizar la reproducibilidad en cualquier
# entorno (local, Google Colab, CI) sin necesidad de modificar el código.
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS_DIR   = os.path.join(BASE_DIR, "datos")
RESULT_DIR  = os.path.join(BASE_DIR, "resultados")

# Crear carpeta de resultados si no existe (no se versiona su contenido generado)
os.makedirs(RESULT_DIR, exist_ok=True)

# ──────────────────────────────────────────────
# 2. CARGA DE DATOS
# ──────────────────────────────────────────────
ruta_csv = os.path.join(DATOS_DIR, "clima_historico.csv")

# parse_dates convierte la columna 'fecha' a tipo datetime automáticamente,
# lo que habilita operaciones temporales (resample, groupby por año/mes, etc.)
df = pd.read_csv(ruta_csv, parse_dates=["fecha"])

print("=" * 60)
print("ANÁLISIS DE DATOS CLIMÁTICOS — UTN TUP")
print("=" * 60)
print(f"\nDataset cargado: {len(df)} registros mensuales")
print(f"Período: {df['fecha'].min().strftime('%b %Y')} → {df['fecha'].max().strftime('%b %Y')}")
print(f"Columnas: {list(df.columns)}\n")

# ──────────────────────────────────────────────
# 3. CÁLCULO DE INDICADORES ESTADÍSTICOS
# ──────────────────────────────────────────────
# Se calculan los indicadores solicitados en el Escenario A del TP:
# temperatura promedio, máxima, mínima y promedio de precipitaciones.

temp_promedio_global   = df["temperatura_promedio"].mean()
temp_maxima_global     = df["temperatura_max"].max()
temp_minima_global     = df["temperatura_min"].min()
precip_promedio_global = df["precipitacion_mm"].mean()
precip_total_anual     = df.groupby(df["fecha"].dt.year)["precipitacion_mm"].sum()

print("─" * 60)
print("INDICADORES ESTADÍSTICOS GLOBALES")
print("─" * 60)
print(f"  Temperatura promedio global : {temp_promedio_global:.2f} °C")
print(f"  Temperatura máxima registrada: {temp_maxima_global:.1f} °C")
print(f"  Temperatura mínima registrada: {temp_minima_global:.1f} °C")
print(f"  Precipitación promedio mensual: {precip_promedio_global:.1f} mm")
print()

# Agrupación anual para detectar tendencias año a año
df["anio"] = df["fecha"].dt.year
resumen_anual = df.groupby("anio").agg(
    temp_max    = ("temperatura_max",     "max"),
    temp_min    = ("temperatura_min",     "min"),
    temp_prom   = ("temperatura_promedio","mean"),
    precip_prom = ("precipitacion_mm",    "mean"),
    precip_total= ("precipitacion_mm",    "sum")
).reset_index()

print("─" * 60)
print("RESUMEN ANUAL")
print("─" * 60)
print(resumen_anual.to_string(index=False))
print()

# ──────────────────────────────────────────────
# 4. GENERACIÓN DE GRÁFICOS
# ──────────────────────────────────────────────
# Se utiliza un estilo limpio para mejorar la legibilidad de los gráficos
# destinados al informe técnico.
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150
})

# ── Gráfico 1: Evolución de temperaturas en el tiempo ──
fig1, ax1 = plt.subplots(figsize=(12, 5))

ax1.fill_between(df["fecha"], df["temperatura_min"], df["temperatura_max"],
                 alpha=0.15, color="#2196F3", label="Rango Mín–Máx")
ax1.plot(df["fecha"], df["temperatura_promedio"], color="#1565C0",
         linewidth=2, marker="o", markersize=3, label="Temp. Promedio (°C)")
ax1.plot(df["fecha"], df["temperatura_max"], color="#E53935",
         linewidth=1, linestyle="--", alpha=0.7, label="Temp. Máxima (°C)")
ax1.plot(df["fecha"], df["temperatura_min"], color="#43A047",
         linewidth=1, linestyle="--", alpha=0.7, label="Temp. Mínima (°C)")

ax1.axhline(temp_promedio_global, color="#1565C0", linestyle=":",
            linewidth=1.2, alpha=0.5, label=f"Media global ({temp_promedio_global:.1f}°C)")

ax1.set_title("Evolución de Temperaturas Mensuales (2020–2023)",
              fontsize=14, fontweight="bold", pad=12)
ax1.set_xlabel("Fecha", fontsize=11)
ax1.set_ylabel("Temperatura (°C)", fontsize=11)
ax1.legend(fontsize=9, loc="upper right")
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax1.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

ruta_g1 = os.path.join(RESULT_DIR, "grafico_temperaturas.png")
fig1.savefig(ruta_g1, bbox_inches="tight")
print(f"[✓] Gráfico 1 guardado: {ruta_g1}")

# ── Gráfico 2: Precipitaciones mensuales (barras) ──
fig2, ax2 = plt.subplots(figsize=(12, 4))

colores = ["#1E88E5" if x >= precip_promedio_global else "#90CAF9"
           for x in df["precipitacion_mm"]]
bars = ax2.bar(df["fecha"], df["precipitacion_mm"],
               width=20, color=colores, edgecolor="none", align="center")
ax2.axhline(precip_promedio_global, color="#E53935", linestyle="--",
            linewidth=1.5, label=f"Promedio ({precip_promedio_global:.1f} mm)")

ax2.set_title("Precipitaciones Mensuales (2020–2023)",
              fontsize=14, fontweight="bold", pad=12)
ax2.set_xlabel("Fecha", fontsize=11)
ax2.set_ylabel("Precipitación (mm)", fontsize=11)
ax2.legend(fontsize=9)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax2.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

ruta_g2 = os.path.join(RESULT_DIR, "grafico_precipitaciones.png")
fig2.savefig(ruta_g2, bbox_inches="tight")
print(f"[✓] Gráfico 2 guardado: {ruta_g2}")

# ── Gráfico 3: Temperatura promedio anual (barras comparativas) ──
fig3, ax3 = plt.subplots(figsize=(7, 4))

colores_anio = ["#1565C0", "#1976D2", "#1E88E5", "#2196F3"]
bars3 = ax3.bar(resumen_anual["anio"].astype(str),
                resumen_anual["temp_prom"],
                color=colores_anio, edgecolor="none", width=0.5)

# Anotar el valor sobre cada barra
for bar, val in zip(bars3, resumen_anual["temp_prom"]):
    ax3.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.15,
             f"{val:.1f}°C", ha="center", va="bottom", fontsize=10, fontweight="bold")

ax3.set_title("Temperatura Promedio Anual (2020–2023)",
              fontsize=13, fontweight="bold", pad=10)
ax3.set_xlabel("Año", fontsize=11)
ax3.set_ylabel("Temperatura promedio (°C)", fontsize=11)
ax3.set_ylim(0, resumen_anual["temp_prom"].max() + 3)
ax3.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

ruta_g3 = os.path.join(RESULT_DIR, "grafico_comparacion_anual.png")
fig3.savefig(ruta_g3, bbox_inches="tight")
print(f"[✓] Gráfico 3 guardado: {ruta_g3}")

# ──────────────────────────────────────────────
# 5. EXPORTACIÓN DE RESUMEN A CSV
# ──────────────────────────────────────────────
# Se exporta el resumen anual en formato CSV para referencia y auditoría.
ruta_resumen = os.path.join(RESULT_DIR, "resumen_anual.csv")
resumen_anual.to_csv(ruta_resumen, index=False, encoding="utf-8")
print(f"[✓] Resumen anual exportado: {ruta_resumen}")

print("\n" + "=" * 60)
print("Análisis completado exitosamente.")
print("=" * 60)
