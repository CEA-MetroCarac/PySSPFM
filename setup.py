from setuptools import setup, find_packages

setup(
    name="PySSPFM",
    version='2024.03',
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
    }

)
