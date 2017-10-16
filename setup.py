import os

from setuptools import setup, find_packages  # noqa, analysis:ignore

from smlgui import __version__

base_dir = os.path.dirname(__file__)

try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
    long_description = long_description.replace("\r", "")  # Do not forget this line
except OSError:
    print("Pandoc not found. Long_description conversion failure.")
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding="utf-8") as f:
        long_description = f.read()

setup(
    name='smlgui',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/akshaybabloo/SML-GUI',
    license='MIT',
    author='Akshay Raj Gollahalli',
    author_email='akshay@gollahalli.com',
    description='Data exporter for Spikes Markup Language (SML).',
    long_description=long_description,
    install_requires=['click', 'pyqt>=5.6', 'numpy>=1.10', 'pandas>=0.18', 'scikit-learn>=0.17'],
    scripts=['sml.sh', 'sml.cmd'],
    package_data={'smlgui': ['*.ui', '*.png']},
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Software Distribution',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Utilities'
    ]
)
