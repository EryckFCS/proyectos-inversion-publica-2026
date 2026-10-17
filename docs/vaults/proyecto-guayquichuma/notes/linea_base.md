
## Respuesta directa

Las dos tareas se resuelven. Para la concentración de fuentes necesitas un protocolo de contraste por indicador y una fuente primaria para cada bloque. Para los gráficos, ya generé seis figuras a partir de un CSV y un script reproducible.

## Cómo resolver la concentración de fuentes

**Regla de trabajo.** Cada indicador crítico necesita una fuente primaria y el PDOT como fuente secundaria. Si ambas coinciden, el dato queda como Contrastada. Si difieren, se reporta el valor de la fuente primaria y se documenta la diferencia con el PDOT.

**Fuentes primarias localizadas por bloque:**

- Minería: la agencia de control minero entrega cartografía digital de las áreas mineras de una provincia o sector, mediante reporte gráfico catastral. Tiene también un geoportal del catastro minero. Las 7 concesiones y las 1.222,84 ha se contrastan con esta entrega. [controlminero.gob](https://controlminero.gob.ec/entrega-de-mapas-y-reportes-graficos-catastrales/)
- Educación: el ministerio publica los registros de matrícula de inicio y fin de año en CSV y XLSX. Con ellos puedes verificar las 2 escuelas y los 8 estudiantes, y resolver el desfase con los 38 menores de 15 años. [datosabiertos.gob](https://www.datosabiertos.gob.ec/dataset/?organization=ministerio-de-educacion)
- Salud: el ministerio mantiene un portal de datos abiertos  y el INEC enlaza las estadísticas del RDACAA, el registro de atenciones ambulatorias. Con esa base puedes confirmar las 107, 52 y 35 atenciones y revisar los códigos de diabetes. [salud.gob](https://www.salud.gob.ec/datos-abiertos-2/)
- Población, vivienda, hogares y NBI: la consulta directa a REDATAM del Censo 2022 y 2010. Es la prioridad, porque ahí se resuelven la discrepancia entre 128 hogares y 117 viviendas, el 62,39% frente al 64,2% y los 383 habitantes de 2010.
- Agua y electricidad: la autoridad del agua para concesiones y caudales, y la empresa distribuidora para cobertura. No busqué sus portales, así que ubica el canal de solicitud antes de comprometerte con esas filas.

**Vía formal si no hay datos públicos.** Presenta un oficio de solicitud de información a la entidad. Para minería, el trámite de reporte gráfico catastral existe como servicio. Citarías el documento recibido como comunicación oficial. [controlminero.gob](https://controlminero.gob.ec/entrega-de-mapas-y-reportes-graficos-catastrales/)

**Registro de contraste.** Agrega una tabla de contraste con indicador, valor PDOT, valor fuente primaria, diferencia y decisión. Así la discrepancia queda visible y defendible, no oculta.

## Cómo quedaría la condición del dato

Reemplaza la columna única por dos:

- **Origen:** Reportada en PDOT, Contrastada con fuente primaria, Calculada o Declarada.
- **Calidad:** Consistente, Con discrepancia documentada o Sin contraste posible.

Eso corrige también el uso de «Verificada» y de «Inconsistente» que señalé antes.

## Gráficos de la línea base

Sí se puede condensar. Generé seis figuras desde el CSV: estructura etaria, servicios y conectividad, NBI frente a comparadores, ocupación por rama, presión sobre el territorio y composición vial. Usan fondo blanco, un solo color institucional, resolución de 300 dpi, fuente al pie y rutas relativas. Los valores salen de la ficha , así que heredan sus limitaciones hasta que hagas el contraste.

Tres criterios para elegir qué graficar:

- Grafica solo comparaciones o composiciones. La densidad o las coordenadas no ganan nada con un gráfico.
- Mantén el valor impreso en cada barra, porque con 293 habitantes los conteos importan.
- No grafiques los indicadores marcados con discrepancia hasta resolverlos, o márcalos visualmente.

## Script reproducible

Guárdalo junto a `datos/linea_base.csv`. El CSV tiene las columnas `panel, titulo, etiqueta, valor, unidad, fuente`. Para agregar un gráfico solo añades filas con un nuevo `panel`.

```python
from pathlib import Path
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
ENTRADA = RAIZ / "datos" / "linea_base.csv"
SALIDA = RAIZ / "figuras"
COLUMNAS = {"panel", "titulo", "etiqueta", "valor", "unidad", "fuente"}
COLOR = "#1F3A5F"

def cargar(ruta: Path) -> pd.DataFrame:
    if not ruta.exists():
        sys.exit(f"No existe el archivo de entrada: {ruta}")
    df = pd.read_csv(ruta, encoding="utf-8")
    faltan = COLUMNAS - set(df.columns)
    if faltan:
        sys.exit(f"Columnas ausentes: {sorted(faltan)}")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    sucias = df[df["valor"].isna()]
    if not sucias.empty:
        print(f"Aviso: {len(sucias)} filas sin valor numerico, se omiten.")
    return df.dropna(subset=["valor"])

def graficar(g: pd.DataFrame, destino: Path) -> None:
    g = g.sort_values("valor")
    unidad = g["unidad"].iloc[0]
    fuentes = "; ".join(sorted(g["fuente"].unique()))
    fig, ax = plt.subplots(figsize=(8, 0.6 * len(g) + 1.8), facecolor="white")
    ax.set_facecolor("white")
    ax.barh(g["etiqueta"], g["valor"], color=COLOR, height=0.6)
    tope = g["valor"].max()
    for y, v in enumerate(g["valor"]):
        txt = f"{v:,.2f}".rstrip("0").rstrip(".")
        ax.text(v + tope * 0.01, y, txt + (" %" if unidad == "%" else f" {unidad}"),
                va="center", fontsize=9)
    ax.set_xlim(0, tope * 1.18)
    ax.set_title(g["titulo"].iloc[0], loc="left", fontsize=11, fontweight="bold")
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.set_xlabel(unidad)
    fig.text(0.01, 0.01, f"Fuente: {fuentes}. Elaboracion propia.", fontsize=7, color="#555555")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(destino, dpi=300)
    plt.close(fig)

def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    df = cargar(ENTRADA)
    for panel, g in df.groupby("panel", sort=False):
        try:
            graficar(g, SALIDA / f"{panel}.png")
            print(f"OK {panel}")
        except Exception as e:
            print(f"Fallo en {panel}: {e}")

if __name__ == "__main__":
    main()
```

## Riesgo técnico

Un gráfico con datos sin contrastar proyecta más certeza que una tabla con notas. Antes de insertar las figuras en el PDF, completa el contraste de las filas con discrepancia. En Quarto, referencia las figuras con `{#fig-...}` y deja la fuente en el pie de cada una.
