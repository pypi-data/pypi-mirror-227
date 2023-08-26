from setuptools import setup, find_packages
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='texere',
    version='1.0.2',
    description='A Python package for text removal and edge marking from images',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='MOHD MINHAL',
    author_email='mohdminhal.001@gmail.com',
    url='https://github.com/MohdMinhal/texere',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python-headless',
        'Pillow',
        'keras-ocr'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
