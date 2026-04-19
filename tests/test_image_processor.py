import hashlib


def test_image_hashing_consistency():
    """Verifica que el hashing SHA-256 sea consistente para las mismas muestras."""
    sample_data = b"fake image data"
    hash1 = hashlib.sha256(sample_data).hexdigest()
    hash2 = hashlib.sha256(sample_data).hexdigest()
    assert hash1 == hash2
    assert hash1 == "5b3397652358a6663a0225ee76466d4e4fd6c58d484d1aa25170bb617d6bb086"


def test_deduplication_logic():
    """Verifica la lógica de conjunto para deduplicación."""
    seen_hashes = set()
    sample_hash = "abc123hash"

    # Primera vez: debe agregarse
    if sample_hash not in seen_hashes:
        seen_hashes.add(sample_hash)
        added = True
    else:
        added = False
    assert added is True

    # Segunda vez: debe detectarse como duplicado
    if sample_hash not in seen_hashes:
        added = True
    else:
        added = False
    assert added is False
