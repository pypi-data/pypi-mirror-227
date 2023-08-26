from setuptools import setup

setup(
    name='ediwheel',
    version='0.1.2',
    description='AdHoc Ediwheel XML API port to Python',
    url='https://github.com/mrztti/python-ediwheel',
    author='M.Ranzetti',
    author_email='maloranzetti@gmail.com',
    license_files='LICENSE',
    packages=['ediwheel'],
    package_dir={'ediwheel': 'ediwheel'},
    install_requires=['jinja2',
                      'requests'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)