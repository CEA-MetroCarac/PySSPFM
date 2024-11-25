"""
Create settings and parameters folder
"""

from pathlib import Path


def post_install():
    """Copy JSON and TOML files to the user directory after installation."""
    user_home = Path.home() / ".pysspfm"
    # Create the directory if it doesn't exist
    user_home.mkdir(exist_ok=True)

    # Path to the directory containing the files to copy
    for folder in ["PySSPFM", r"PySSPFM/data_processing", r"PySSPFM/toolbox"]:
        package_dir = Path(__file__).parent / folder
        if not package_dir.exists():
            return

        # Copy JSON and TOML files
        for file in package_dir.glob("*.json"):
            if file.name == "examples_settings.json":
                pass
            elif file.name == "default_settings.json":
                copy_file(file, user_home / "pysspfm.json")
            else:
                copy_file(file, user_home / file.name)
        for file in package_dir.glob("*.toml"):
            copy_file(file, user_home / file.name)


def copy_file(src, dst):
    """Copy a file from the source path (src) to the destination path (dst)."""
    print(f"Copying {src} to {dst}")
    dst.write_bytes(src.read_bytes())


if __name__ == "__main__":
    post_install()
