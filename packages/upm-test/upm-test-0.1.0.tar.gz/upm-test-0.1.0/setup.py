from setuptools import setup, find_packages

setup(
    name='upm-test',
    version='0.1.0',
    author='Akeem King',
    author_email='akeemtlking@email.com',
    description='A short description of your package',
    long_description='A longer description of your package',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='your, keywords, here',
    install_requires=[
        # List your dependencies here
    ],
    python_requires='>=3.6',
)