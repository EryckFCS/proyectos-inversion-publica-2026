import re
from pathlib import Path


def clean_guide(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"File not found: {file_path}")
        return

    content = path.read_text()

    # 1. Remove Page Break characters
    content = content.replace("\f", "")

    # 2. Remove Graphic/Table/Map Index lines
    # Patterns like "Gráfico 1. ... 22" or just titles in lists
    # We look for lines that start with these words and are likely part of an index
    # (Checking for digits at the end is a good indicator of an index)
    lines = content.split("\n")
    cleaned_lines = []

    # Regex for noise: page numbers, specific URLs, legal headers
    noise_patterns = [
        re.compile(r"^Pág(ina)?\.?\s+\d+\s+de\s+\d+.*$", re.I),
        re.compile(r"^https?://edicioneslegales\.com\.ec/.*$", re.I),
        re.compile(r"^Todos los derechos reservados\.?.*$", re.I),
        re.compile(r"^Piense en el medio ambiente\..*$", re.I),
        re.compile(r"^Fiel Web.*Ediciones Legales.*$", re.I),
        # Remove literal graphic/map/table citations that look like index items
        # Usually they have a page number at the end
        re.compile(r"^(Gráfico|Mapa|Tabla)\s+\d+\..*\s+\d+$"),
        # Or just lines that are ONLY titles without content
        re.compile(r"^(Gráfico|Mapa|Tabla)\s+\d+\..*$"),
    ]

    for line in lines:
        is_noise = False
        # Do not remove if it's a section header or has actual article content
        if line.strip().startswith("##") or line.strip().startswith("Art."):
            cleaned_lines.append(line)
            continue

        for pattern in noise_patterns:
            if pattern.match(line.strip()):
                is_noise = True
                break

        if not is_noise:
            cleaned_lines.append(line)

    # Join and collapse multiple empty lines
    final_content = "\n".join(cleaned_lines)
    final_content = re.sub(r"\n{3,}", "\n\n", final_content)

    # Save back
    path.write_text(final_content)
    print(f"Cleanup complete for {file_path}")
    print(f"Original lines: {len(lines)} | Cleaned lines: {len(cleaned_lines)}")


if __name__ == "__main__":
    clean_guide("docs/activities/A1_Marco_Normativo/guia_cero_extraccion_raw.md")
