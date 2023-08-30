from setuptools import setup, find_packages

setup(
    name='ARIXA',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Mohamed Ali',
    author_email='arixa.robotics@gmail.com',
    description='A Python library for controlling a robotic arm',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
