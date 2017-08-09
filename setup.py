from setuptools import setup, find_packages  # noqa, analysis:ignore

from smlgui import __version__

setup(
    name='smlgui',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/akshaybabloo/SML-GUI',
    license='MIT',
    author='Akshay Raj Gollahalli',
    author_email='akshay@gollahalli.com',
    description='Data exporter for Spikes Markup Language (SML).',
    requires=['click', 'pyqt'],
    scripts=['sml.sh', 'sml.cmd'],
    package_data={'smlgui': ['*.ui', '*.png']},
    include_package_data=True
)
