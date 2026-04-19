import fitz
from pathlib import Path
import json
import hashlib


def extract_images_from_pdf(pdf_path, output_dir, doc_id):
    doc = fitz.open(pdf_path)
    path_obj = Path(output_dir) / doc_id
    path_obj.mkdir(parents=True, exist_ok=True)

    seen_hashes = set()
    unique_count = 0

    print(f"Harvesting unique images from {doc_id}...")

    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Compute hash to detect duplicates (logos, footers, etc.)
            img_hash = hashlib.sha256(image_bytes).hexdigest()

            if img_hash in seen_hashes:
                continue

            seen_hashes.add(img_hash)
            unique_count += 1

            # Extension handling
            image_ext = base_image["ext"]
            img_filename = (
                f"{doc_id}_page{page_index + 1}_img{img_index + 1}.{image_ext}"
            )

            with open(path_obj / img_filename, "wb") as f:
                f.write(image_bytes)

    print(f"  Total images found: {len(image_list) * len(doc)} (est.)")
    print(f"  Unique images saved: {unique_count}")
    return unique_count


def run_harvesting(metadata_path, base_raw_dir, output_root):
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    summary = {}
    for item in metadata.get("library", []):
        pdf_path = Path(base_raw_dir) / item["path"]
        if pdf_path.exists():
            count = extract_images_from_pdf(pdf_path, output_root, item["id"])
            summary[item["id"]] = count

    print("\n--- Harvesting Summary ---")
    for doc_id, count in summary.items():
        print(f"{doc_id}: {count} unique images")


if __name__ == "__main__":
    run_harvesting(
        "data/raw/marco_normativo/metadata.json",
        "data/raw/marco_normativo",
        "data/processed/images",
    )
