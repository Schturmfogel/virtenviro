from setuptools import setup, find_packages
import os
import virtenviro


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache License, Version 2.0',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
]

setup(
    author="Kamo Petrosyan",
    author_email="kamo@haikson.com",
    name='virtenviro',
    version=virtenviro.__version__,
    description='Open source content management system (CMS) based on the django framework.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    url='https://www.virtenviro.com/',
    license='Apache License, Version 2.0',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.7',
        'django-mptt>=0.6.1',
        'pytils',
        'lxml',
        'Pillow>=2.5.3',
        'sorl-thumbnail',
        'django-filebrowser-no-grappelli>=3.5.7',
    ],
    packages=find_packages(exclude=["samplesite", "samplesite.*"]),
    include_package_data=True,
    zip_safe=False,
)