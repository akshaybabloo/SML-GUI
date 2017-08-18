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
    requires=['click', 'pyqt>5.6', 'numpy>=1.10'],
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
