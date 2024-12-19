from setuptools import setup, find_packages

setup(
    name='parsnorm',  # The name of your package
    version='0.1.0',  # Initial version
    description='Text Normalization Tool for Persian Speech Dataset Creation',
    long_description=open('README.md').read(),  # Read the README for a detailed description
    long_description_content_type='text/markdown',  # Use markdown for the long description
    author='Saeedreza Zouashkiani',  # Replace with your name or the name of your team
    author_email='saeedzou2012@gmail.com',  # Replace with your email address
    url='https://github.com/saeedzou/ParsNorm',  # Replace with your GitHub URL
    packages=find_packages(where='parsnorm'),  # Automatically find the packages in your project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[  # List the external dependencies
        'hazm',  # Example dependencies
        'parsinorm',
    ],
    python_requires='>=3.6',
)
