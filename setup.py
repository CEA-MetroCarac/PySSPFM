import os
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.install import install
from distutils.cmd import Command


class CustomInstallCommand(install):
    """Custom command to handle post-install tasks."""
    def run(self):
        # Call the standard installation process
        super().run()

        # Target user directory
        user_home = Path.home() / ".pysspfm"
        user_home.mkdir(exist_ok=True)

        # Directory containing the files to copy
        package_dir = Path(__file__).parent / "resources"
        if package_dir.exists():
            for file in package_dir.glob("*"):
                if file.suffix in [".json", ".toml"]:
                    self.copy_file(file, user_home / file.name)

        # Execute the post_install.py script
        post_install_script = Path(__file__).parent / "post_install.py"
        if post_install_script.exists():
            self.announce(f"Executing {post_install_script}...", level=2)
            os.system(f"{os.sys.executable} {post_install_script}")
        else:
            self.announce("No post_install.py script found.", level=2)

    def copy_file(self, src, dst):
        """Copy a file from the source path (src) to the destination
        path (dst)."""
        self.announce(f"Copying {src} to {dst}", level=2)
        dst.write_bytes(src.read_bytes())


class RunPostInstallScript(Command):
    """Custom command to execute the post_install.py script."""
    description = "Run the post_install.py script."
    user_options = []  # Add options if necessary

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        post_install_script = Path(__file__).parent / "post_install.py"
        if post_install_script.exists():
            self.announce(f"Executing {post_install_script}...", level=2)
            os.system(f"{os.sys.executable} {post_install_script}")
        else:
            self.announce(f"Script {post_install_script} not found.", level=2)


setup(
    name="PySSPFM",
    version='2024.12',
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

    cmdclass={
        "install": CustomInstallCommand,
        "run_post_install": RunPostInstallScript,
    },
)
