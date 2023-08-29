from setuptools import setup, find_packages

VERSION = '1.0.2'
DESCRIPTION = 'TEKO Translator Package'

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='teko-multi-lang',
    version='1.0.2',
    description='Teko translator tool',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(exclude=('tests', )),
    include_package_data=True,
    author='Thanh Nguyen',
    author_email='danthanh92@gmail.com',
    keywords=['Teko', 'Teko Translator tools'],
    url='https://git.teko.vn/common-utilities/sample/language-package',
    download_url='https://pypi.org/project/teko-multi-lang/'
)

install_requires = [
    'requests',
    'cachetools'
]


if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
