from setuptools import setup

setup(
    name='CosmicaCLI',
    version='1.0',
    author='AS3PT1C',
    py_modules=['cosmica-package'],
    install_requires=[
        'eel',
    ],
    entry_points='''
        [console_scripts]
        cosmica=cosmica_package:main
    ''',
)
