from setuptools import setup, find_packages

setup(
    name="pysspfm",
    version='2023.10',
    license='GPL v3',
    include_package_data=False,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        "os",
        "shutil",
        "collections",
        "time",
        "datetime",
        "tkinter",
        "numpy",
        "pandas",
        "matplotlib",
        "mpl_toolkits",
        "PIL",
        "scipy",
        "lmfit",
        "sklearn",
        "pywin32; platform_system == 'Windows'",
    ],
    packages=find_packages(where='.', include=['pyssfm*']),

    description="PySSPFM (A generic tool to SSPFM data processing)",

    url="https://github.com/CEA-MetroCarac/pysspfm",
    author_email="hugovalloire@gmail.com",
    author="Hugo Valloire",
    keywords="PySSPFM, SS-PFM, piezoelectric, ferroelectric, map, 1D, 2D, "
             "decomposition, Gaussian, Lorentzian, Pseudovoigt, GUI",
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
            'fitspy = fitspy.app.gui:fitspy_launcher',
        ]
    }

)
