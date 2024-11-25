from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path


class CustomInstallCommand(install):
    """Custom command to copy user configuration files."""
    def run(self):
        # Appeler l'installation standard
        super().run()

        # Répertoire utilisateur cible
        user_home = Path.home() / ".pysspfm"
        user_home.mkdir(exist_ok=True)

        # Répertoire contenant les fichiers à copier
        package_dir = Path(__file__).parent / "resources"
        if package_dir.exists():
            for file in package_dir.glob("*"):
                if file.suffix in [".json", ".toml"]:
                    self.copy_file(file, user_home / file.name)

    def copy_file(self, src, dst):
        """Copie un fichier du chemin source (src) au chemin destination (dst)."""
        self.announce(f"Copying {src} to {dst}", level=2)
        dst.write_bytes(src.read_bytes())

setup(
    name="PySSPFM",
    version='2024.11',
    license='GPL v3',
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        "numpy",
        "pandas",
        "openpyxl",
        "matplotlib",
        "Pillow",
        "scipy",
        "lmfit",
        "scikit-learn",
        "nanoscope",
        "pywin32; platform_system == 'Windows'",
    ],
    packages=find_packages(where='.', include=['PySSPFM*']),

    description="PySSPFM: A specialized tool for Switching Spectroscopy "
                "Piezoresponse Force Microscopy (SSPFM) data processing",

    url="https://github.com/CEA-MetroCarac/PySSPFM",
    author_email="hugovalloire@gmail.com",
    author="Hugo Valloire, Patrick Quemere",
    keywords="PySSPFM, SS-PFM, C-KPFM, switching-spectroscopy, PFM, AFM, "
             "piezoelectric, ferroelectric, image, hysteresis, nano-loop, "
             "piezoresponse, bruker, datacube, spm, python, python-library, "
             "data-processing, machine-learning, k-means, cross-correlation",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Environment :: Console',
    ],

    entry_points={
        'gui_scripts': [
            'PySSPFM = PySSPFM.gui.main:main',
        ]
    },

    cmdclass={"install": CustomInstallCommand},
)
