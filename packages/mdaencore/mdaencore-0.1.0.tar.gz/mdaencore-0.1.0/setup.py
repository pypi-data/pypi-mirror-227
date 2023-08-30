"""
mdaencore
Ensemble overlap comparison software for molecular data.
"""
import os
import sys
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import numpy as np
import platform

sys.path.append(os.path.dirname(__file__))

import versioneer

short_description = "Ensemble overlap comparison software for molecular data.".strip().split("\n")[0]

# from https://github.com/pytest-dev/pytest-runner#conditional-requirement
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

try:
    with open("README.md", "r") as handle:
        long_description = handle.read()
except:
    long_description = "\n".join(short_description[2:])


def extensions(debug=False, use_cython=True):
    encore_compile_args = ['-std=c99', '-funroll-loops', '-fsigned-zeros']

    cython_linetrace = bool(os.environ.get('CYTHON_TRACE_NOGIL', False))

    define_macros = []
    if debug:
        encore_compile_args.extend(['-Wall', '-pedantic'])
        define_macros.extend([('DEBUG', '1')])

    # encore is sensitive to floating point accuracy, especially on non-x86
    # to avoid reducing optimisations on everything, we make a set of compile
    # args specific to encore
    if platform.machine() == 'aarch64' or platform.machine() == 'ppc64le':
        encore_compile_args.append('-O1')
    else:
        encore_compile_args.append('-O3')

    include_dirs = [np.get_include()]

    mathlib = [] if os.name == 'nt' else ['m']

    encore_utils = Extension('mdaencore.cutils',
                             sources=['mdaencore/cutils.pyx'],
                             include_dirs=include_dirs,
                             define_macros=define_macros,
                             extra_compile_args=encore_compile_args,
                             )

    ap_clustering = Extension('mdaencore.clustering.affinityprop',
                              sources=['mdaencore/clustering/affinityprop.pyx',
                                       'mdaencore/clustering/src/ap.c'],
                              include_dirs=include_dirs+['mdaencore/clustering/include'],
                              libraries=mathlib,
                              define_macros=define_macros,
                              extra_compile_args=encore_compile_args)

    spe_dimred = Extension('mdaencore.dimensionality_reduction.stochasticproxembed',
                           sources=['mdaencore/dimensionality_reduction/stochasticproxembed.pyx',
                                    'mdaencore/dimensionality_reduction/src/spe.c'],
                           include_dirs=include_dirs+['mdaencore/dimensionality_reduction/include'],
                           libraries=mathlib,
                           define_macros=define_macros,
                           extra_compile_args=encore_compile_args)

    pre_exts = [encore_utils, ap_clustering, spe_dimred]

    cython_generated = []

    extensions = cythonize(
        pre_exts,
        annotate=False,
        compiler_directives={'linetrace': cython_linetrace,
                             'embedsignature': False,
                             'language_level': '3'},
    )

    if cython_linetrace:
        print("Cython coverage will be enabled")

    for pre_ext, post_ext in zip(pre_exts, extensions):
        for source in post_ext.sources:
            if source not in pre_ext.sources:
                cython_generated.append(source)

    return extensions, cython_generated


exts, cythonfiles = extensions()

setup(
    # Self-descriptive entries which should always be present
    name='mdaencore',
    author='MDAnalysis',
    author_email='mdanalysis@numfocus.org',
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='GNU Public License v2+',

    # Which Python importable modules should be included when your package is installed
    # Handled automatically by setuptools. Use 'exclude' to prevent some specific
    # subpackage(s) from being added, if needed
    packages=find_packages(),

    # Optional include package data to ship with your package
    # Customize MANIFEST.in if the general case does not suit your needs
    # Comment out this line to prevent the files from being packaged with your software
    include_package_data=True,
    python_requires=">=3.9",          # Python version restrictions
    # Allows `setup.py test` to work correctly with pytest
    setup_requires=[] + pytest_runner,
    # Required packages, pulls from pip if needed
    # do not use for Conda deployment
    install_requires=[
        "mdanalysis>=2.0.0",
    ],
    # Additional entries you may want simply uncomment the lines you want and fill in the data
    # url='mdaencore.readthedocs.io/en/latest/',  # Website
    # platforms=['Linux',
    #            'Mac OS-X',
    #            'Unix',
    #            'Windows'],            # Valid platforms your code works on, adjust to your flavor

    # Manual control if final package is compressible or not, set False to prevent the .egg from being made
    # zip_safe=False,

    extras_require={
        "test": [
            "pytest>=6.0",
            "pytest-xdist>=2.5",
            "pytest-cov>=3.0",
        ],
        "doc": [
            "sphinx",
            "sphinx_rtd_theme",
        ]
    },
    ext_modules=exts,
)
