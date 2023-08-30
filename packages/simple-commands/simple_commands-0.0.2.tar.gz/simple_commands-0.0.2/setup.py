from setuptools import setup, find_packages

setup(
    name='simple_commands',
    version='0.0.2',
    description='simple_commands',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        'numpy',
        'Pillow',
        'opencv-python',
        'pytz'
    ],
)
