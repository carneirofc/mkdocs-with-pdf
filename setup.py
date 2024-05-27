import io

from setuptools import find_packages, setup

setup(
    name='mkdocs-with-pdf-nightly',
    version='1.0.1',
    description='Generate a single PDF file from MkDocs repository nightly, a fork of the original project mkdocs-with-pdf',  # noqa E501
    long_description=io.open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    keywords='mkdocs pdf weasyprint mkdocs-with-pdf nightly',
    url='https://github.com/carneirofc/mkdocs-with-pdf',
    author='orzih',
    author_email='claudiofcarneiro@hotmail.com',
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'mkdocs>=1.1',
        'weasyprint>=0.44',
        'beautifulsoup4>=4.6.3',
        'libsass>=0.15'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.12'
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'with-pdf = mkdocs_with_pdf.plugin:WithPdfPlugin'
        ]
    }
)
