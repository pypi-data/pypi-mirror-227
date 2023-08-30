from setuptools import setup, find_packages

setup(
    name='light-distribution-analysis',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
        'matplotlib'
    ],
    author='Viktor Veselov',
    author_email='lipovkaviktor@yahoo.com',
    description='Analyze the flux of images based on wavelength and frequency'
)
