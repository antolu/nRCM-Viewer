from setuptools import setup
from os import path
import pyqt5ac


# generate PyQt UI modules
try:
    # compile pyqt files
    HERE = path.split(path.abspath(__file__))[0]
    pyqt5ac.main(
        uicOptions='--from-imports', force=False, initPackage=True,
        ioPaths=[
            [path.join(HERE, 'resources/ui/*.ui'),
             path.join(HERE,
                       'nrcm_viewer/generated/%%FILENAME%%_ui.py')],
            [path.join(HERE, 'resources/*.qrc'),
             path.join(HERE, 'nrcm_viewer/generated/%%FILENAME%%_rc.py')]
        ]
    )
except (PermissionError, OSError):
    pass


setup()
