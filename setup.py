from distutils.core import setup
from SMLGUI import __version__

setup(
    name='SML-GUI',
    version=__version__,
    packages=['SMLGUI'],
    url='https://github.com/akshaybabloo/SML-GUI',
    license='MIT',
    author='Akshay Raj Gollahalli',
    author_email='akshay@gollahalli.com',
    description='Data exporter for Spikes Markup Language (SML).'
)
