# Análisis de Datos Climáticos — UTN TUP 🌡️

**Trabajo Práctico: Gestión Colaborativa, Control de Versiones y Organización Empresarial**  
Cátedra: Organización Empresarial | Universidad Tecnológica Nacional — TUP a Distancia | Año 2026

---

## 👤 Integrante

| Integrante | Roles asumidos |
|------------|----------------|
| Leonardo Macre | P1 (Líder y Organizador) · P2 (Desarrollador Técnico) · P3 (Revisor y QA) |

> Trabajo desarrollado de forma individual. Leonardo Macre asumió los tres roles definidos en la consigna.

---

## 📌 Escenario Elegido

**Escenario A — Análisis de Datos Climáticos**

Se procesa un dataset de registros meteorológicos históricos mensuales (2020–2023) con variables de temperatura máxima, mínima, promedio y precipitaciones. El análisis genera indicadores estadísticos básicos y visualizaciones exportadas automáticamente.

---

## 📂 Estructura del Repositorio

```
repo-proyecto/
│
├── datos/
│   └── clima_historico.csv        # Dataset de temperaturas y precipitaciones (2020–2023)
│
├── scripts/
│   └── analisis_datos.py          # Script principal de análisis (Python 3)
│
├── resultados/
│   ├── grafico_temperaturas.png   # Evolución de temperaturas mensuales
│   ├── grafico_precipitaciones.png# Precipitaciones mensuales en barras
│   ├── grafico_comparacion_anual.png # Comparación anual de temperatura promedio
│   └── resumen_anual.csv          # Indicadores estadísticos por año
│
├── README.md
└── .gitignore
```

---

## 📊 Dataset Utilizado

**Archivo:** `datos/clima_historico.csv`  
**Período:** Enero 2020 — Diciembre 2023 (48 registros mensuales)  
**Variables:**

| Columna | Descripción | Unidad |
|---------|-------------|--------|
| `fecha` | Período mensual en formato AAAA-MM | — |
| `temperatura_max` | Temperatura máxima del mes | °C |
| `temperatura_min` | Temperatura mínima del mes | °C |
| `temperatura_promedio` | Temperatura promedio mensual | °C |
| `precipitacion_mm` | Total de precipitaciones del mes | mm |

> El dataset fue construido con datos simulados representativos del clima patagónico austral, con marcada variación estacional.

---

## ▶️ Cómo ejecutar el análisis

### Requisitos

```bash
pip install pandas matplotlib numpy
```

### En Google Colab

```python
# 1. Clonar el repositorio
!git clone https://github.com/leonardomacre/repo-proyecto.git
%cd repo-proyecto

# 2. Ejecutar el script
!python scripts/analisis_datos.py
```

### Localmente

```bash
git clone https://github.com/leonardomacre/repo-proyecto.git
cd repo-proyecto
python scripts/analisis_datos.py
```

Los gráficos y el resumen CSV se guardan automáticamente en la carpeta `/resultados`.

---

## 📋 Gestión del Proyecto (Jira)

Las tareas del proyecto se gestionan mediante Issues en Jira con el prefijo `PROY-`:

| Issue | Responsable | Descripción |
|-------|-------------|-------------|
| PROY-1 | Leonardo Macre (P1) | Inicialización del repositorio y estructura de carpetas |
| PROY-2 | Leonardo Macre (P2) | Desarrollo del script de análisis climático |
| PROY-3 | Leonardo Macre (P3) | Revisión de código, documentación y cierre de PR |

Cada commit referencia el Issue correspondiente siguiendo el formato de **Conventional Commits**:  
`PROY-N: <descripción en tiempo presente>`

---

## 🔒 Seguridad

- El Personal Access Token (PAT) nunca está expuesto en el código.
- El archivo `.gitignore` excluye archivos temporales, checkpoints y datos sensibles.
- Para autenticación en Colab: `!git push https://{TOKEN}@github.com/{USER}/{REPO}.git`

---

*UTN — Tecnicatura Universitaria en Programación — Organización Empresarial — 2026*
