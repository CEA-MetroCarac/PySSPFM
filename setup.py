from setuptools import setup, find_packages

setup(
    name="PySSPFM",
    version='2023.10',
    license='GPL v3',
    include_package_data=False,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "lmfit",
        "scikit-learn",
        "pywin32; platform_system == 'Windows'",
    ],
    packages=find_packages(where='.', include=['PySSPFM*']),

    description="PySSPFM (A specific tool to perform Switching Spectroscopy Piezoresponse Force Microscopy (SSPFM) data processing)",

    url="https://github.com/CEA-MetroCarac/PySSPFM",
    author_email="hugovalloire@gmail.com",
    author="Hugo Valloire",
    keywords="PySSPFM, Switching Spectroscopy, SSPFM, PFM, piezoelectric, ferroelectric, map, hysteresis, "
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
            'PySSPFM = PySSPFM.gui.main',
        ]
    }

)
