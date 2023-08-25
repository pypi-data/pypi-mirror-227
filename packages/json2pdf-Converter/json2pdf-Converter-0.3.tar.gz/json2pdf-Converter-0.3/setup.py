from setuptools import setup, find_packages

setup(
    name='json2pdf-Converter',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'jinja2',
        'pdfkit',
        'PyPDF2'
    ],
    tests_require=['pytest'],
    # Other metadata (author, description, etc.)
)
