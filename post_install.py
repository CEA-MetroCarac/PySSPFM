"""
module description
"""

import os
from pathlib import Path


def post_install():
    """Copie les fichiers JSON et TOML dans le répertoire utilisateur
    après installation."""
    user_home = Path.home() / ".pysspfm"
    user_home.mkdir(exist_ok=True)  # Créer le répertoire s'il n'existe pas

    # Chemin vers le répertoire des fichiers à copier
    package_dir = Path(__file__).parent / "resources"
    if not package_dir.exists():
        return

    # Copier les fichiers JSON et TOML
    for file in package_dir.glob("*.json"):
        copy_file(file, user_home / file.name)
    for file in package_dir.glob("*.toml"):
        copy_file(file, user_home / file.name)


def copy_file(src, dst):
    """Copie un fichier du chemin source (src) au chemin destination (dst)."""
    print(f"Copying {src} to {dst}")
    dst.write_bytes(src.read_bytes())


if __name__ == "__main__":
    post_install()
