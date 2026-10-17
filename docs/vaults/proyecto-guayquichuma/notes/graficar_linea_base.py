
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
COLOR, COLOR_REF = "#1F3A5F", "#9AA5B1"

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
    colores = [COLOR] * len(g)
    fig, ax = plt.subplots(figsize=(8, 0.6 * len(g) + 1.8), facecolor="white")
    ax.set_facecolor("white")
    ax.barh(g["etiqueta"], g["valor"], color=colores, height=0.6)
    tope = g["valor"].max()
    for y, v in enumerate(g["valor"]):
        ax.text(v + tope * 0.01, y, f"{v:,.2f}".rstrip("0").rstrip(".") + (" %" if unidad == "%" else f" {unidad}"),
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
        destino = SALIDA / f"{panel}.png"
        try:
            graficar(g, destino)
            print(f"OK {destino.name}")
        except Exception as e:
            print(f"Fallo en {panel}: {e}")

if __name__ == "__main__":
    main()
