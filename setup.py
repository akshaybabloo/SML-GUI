from warnings import warn

try:
    from setuptools import setup, find_packages  # noqa, analysis:ignore
except ImportError:
    warn("unable to load setuptools. 'setup.py develop' will not work")
    pass
from distutils.core import setup

from SMLGUI import __version__

setup(
    name='SML-GUI',
    version=__version__,
    packages=find_packages(exclude=['tests', 'tests.*', 'docs']),
    url='https://github.com/akshaybabloo/SML-GUI',
    license='MIT',
    author='Akshay Raj Gollahalli',
    author_email='akshay@gollahalli.com',
    description='Data exporter for Spikes Markup Language (SML).',
    requires=['click', 'pyqt'],
    scripts=['sml.sh', 'sml.cmd'],
    package_data={'': ['*.ui']}
)
