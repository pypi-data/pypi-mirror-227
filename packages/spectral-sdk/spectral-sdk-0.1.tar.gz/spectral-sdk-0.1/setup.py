from setuptools import setup, find_packages

setup(
    name='spectral-sdk',  # Name of your package
    version='0.1',  # Version number
    # Automatically discover all packages and subpackages. Alternatively, you can specify the package names.
    packages=find_packages(),
    install_requires=[
        'cloudpickle>=2.2.1',
        'ezkl>=1.11.5',
        'numpy>=1.25.2',
        'onnx>=1.14.0',
        'torch>=2.0.1',
        'requests>=2.31.0',
        'web3>=6.9.0'
    ],
    author='Spectral Finance',
    author_email='maciej@spectral.finance',
    description='Spectral SDK allows you to participate in the challenges and competitions on Spectral Finance platform.',
    # You can use a README file to provide a longer description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # If using a markdown README file
    # Link to the source code or the project website
    url='https://github.com/Spectral-Finance/spectral-ai-sdk',
    classifiers=[
        'License :: OSI Approved :: MIT License',  # Example license
        # Specify which python versions your package works on
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    # Optionally include package data
    # This will include any non-python files specified in your MANIFEST.in
    include_package_data=True,
    keywords='machine learning ai data science web3',
    entry_points={
        'console_scripts': [  # This allows creating command-line scripts from your package's functions
            # This will create a command-line script named 'myscript' which will execute 'myfunction' from 'mymodule' in 'mypackage'
            'myscript=mypackage.mymodule:myfunction',
        ],
    },
    python_requires='>=3.7',  # Minimum python version
)
