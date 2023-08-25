from setuptools import setup, Extension, find_packages

catdict = Extension(
    'catdict',
    sources = [
        'src/catdict_module.c',
        'src/catdict.c',
        'src/cd_long.c',
        'src/cd_unicode.c',
        'src/cd_list.c',
        'src/cd_set.c',
        'src/cd_float.c',
    ],
)

setup(
    name         = 'catdict',
    version      = '0.3.3',
    packages     = find_packages(),
    ext_modules  = [catdict],
    include_dirs = ['src'],
    description  = 'Python package providing categorical Dict class.',
    author       = 'Zhao Kunwang',
    author_email = 'clumsykundev@gmail.com',
    url          = 'https://github.com/clumsykun/catdict',
    download_url = 'https://github.com/clumsykun/catdict/archive/refs/tags/v0.1.tar.gz',
)
