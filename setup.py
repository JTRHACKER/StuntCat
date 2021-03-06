import sys

import os

from setuptools import setup, find_packages

from stuntcat import __version__


here = os.path.abspath(os.path.dirname(__file__))

name = "stuntcat"


from io import open


with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

freeze_cmds = ["bdist_dmg", "bdist_msi", 'build_exe', 'bdist_mac']

if any(x in sys.argv for x in freeze_cmds):
    from cx_Freeze import setup, Executable

    import cx_Freeze.hooks

    if not hasattr(cx_Freeze.hooks, 'load_pymunk'):
        def load_pymunk(finder, module):

            """The chipmunk.dll or .dylib or .so is included in the package.
               But it is not found by cx_Freeze, so we include it.
            """

            import pymunk

            finder.IncludeFiles(pymunk.chipmunk_path,
                                os.path.join(os.path.basename(pymunk.chipmunk_path)),
                                copyDependentFiles=False)


        cx_Freeze.hooks.load_pymunk = load_pymunk

    if not hasattr(cx_Freeze.hooks, 'load_pycparser'):
        def load_pycparser(finder, module):

            """ These files are missing which causes
                permission denied issues on windows when they are regenerated.
            """

            finder.IncludeModule("pycparser.lextab")
            finder.IncludeModule("pycparser.yacctab")


        cx_Freeze.hooks.load_pycparser = load_pycparser

    # Dependencies are automatically detected, but it might need fine tuning.

    build_exe_options = {
        "packages": [
            "os", "pygame", "sys", "typing", "random", "pyscroll", "pytmx", "thorpy", "pymunk"
        ],
        "excludes": ["tkinter"],
    }

    # GUI applications require a different base on Windows (the default is for a
    # console application).

    base = None

    if sys.platform.startswith("win"):
        base = "Win32GUI"

    options = {
        "build_exe": build_exe_options
    }

    executables = [Executable("run_game.py", base=base)]

    print("options, executables, base", options, executables, base)

else:
    options = {}

    executables = []

setup(
    name=name,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: pygame',
        'Topic :: Games/Entertainment :: Arcade',
    ],
    license='LGPL',
    author='JTR3',
    author_email='0450400@gmail.com',
    maintainer='the cult of kosmos',
    maintainer_email='0450400@gmail.com',
    description='The cult of kosmos secret project.',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    options=options,
    executables=executables,
    package_dir={'the cult of kosmos': 'jtr3'},
    packages=find_packages(),
    # package_data={'stuntcat': []},
    url='the cult of kosmos.com',
    install_requires=[
        "pygame",
        "pyscroll",
        "pytmx",
        "thorpy",
        "pymunk>=5.4.2",
    ],
    version=__version__,
    extras_require={
        ':python_version < "3.5"': [
            'typing',
        ],
    },
    entry_points={
        'console_scripts': [
            'stuntcat=stuntcat.cli:main',
        ],
    },
)
