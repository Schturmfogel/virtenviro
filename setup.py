from distutils.core import setup
from setuptools import find_packages, setup

EXCLUDE_FROM_PACKAGES = []


def get_version(major=0, minor=0, build=0, release_type='b', release_build=0):
    return '%s.%s.%s.%s.%s' % (major, minor, build, release_type, release_build)


setup(
    name='virtenviro',
    version=get_version(
        major=0,
        minor=5,
        build=9,
        release_type='b',
        release_build=1
    ),
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    url='https://github.com/Haikson/virtenviro',
    license='GPL3',
    author='Kamo Petrosyan',
    author_email='kamo@haikson.com',
    description='Open source content management system (CMS) based on the django framework.',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: CMS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    requires=['django']
)