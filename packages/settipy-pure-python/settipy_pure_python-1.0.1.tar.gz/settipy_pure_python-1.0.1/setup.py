import io

from setuptools import setup

with io.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='settipy_pure_python',
    author='Melvin Bijman',
    author_email='bijman.m.m@gmail.com',

    description='settings should be simple, boring and forget-able. With settipy it will be just that. Without dependencies pure python',
    long_description=long_description,
    long_description_content_type='text/markdown',

    version='1.0.1',
    py_modules=['settipy'],
    install_requires=[],
    license='MIT',

    url='https://github.com/Attumm/settipy_pure_python',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
