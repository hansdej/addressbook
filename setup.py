# !/usr/bin/env python


# https://packaging.python.org/
#
# https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/

from distutils.core import setup
setup(
    name='addressbook',
    packages=['src/addressbook'],
    version='0.0.1',
    description='An addressbook created for educational purposes.',
    author='J (Hans) de Jonge',
    license='GPLv3',
    author_email='j.dejonge@gmail.com',
    url='https://github.com/hansdej/addressbook',
    keywords=['educational', 'addressbook', 'person data' ]
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
    ],
)
