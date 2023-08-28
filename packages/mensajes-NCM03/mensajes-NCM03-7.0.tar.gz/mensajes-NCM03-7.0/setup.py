from setuptools import setup, find_packages

setup(
    name= 'mensajes-NCM03',
    version='7.0',
    description='un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Noelia',
    author_email='Hola@Noelia.dev',
    url='https://www.noelia.dev',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='Tests',
    install_requires=[paquete.strip()
                        for paquete in open ("requirements.txt").readlines()],
    
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities' 
    ]
)

