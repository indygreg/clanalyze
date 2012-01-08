from distutils.core import setup

setup(
    name='Clanalyze',
    version='0.0.1',
    author='Gregory Szorc',
    author_email='gregory.szorc@gmail.com',
    packages=['clanalyze', 'clanalyze.test'],
    scripts=[],
    url='https://github.com/indygreg/clanalyze',
    license='LICENSE.txt',
    description='C language analyzer.',
    long_description=open('README.rst').read(),
)
