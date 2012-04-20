"""
Flask-Sendmail
----------

A Flask extension for sending email messages via a system's
built-in sendmail client.

Please refer to the online documentation for details.

Links
`````

* `documentation <http://packages.python.org/Flask-Sendmail>`_
* `development version
  <https://github.com/ajford/flask-sendmail/tarball/master#egg=Flask-Sendmail>`_
"""
from setuptools import setup


setup(
    name='Flask-Sendmail',
    version='0.1',
    url='http://github.com/ajford/flask-sendmail',
    license='BSD',
    author='Anthony Ford',
    author_email='ford.anthonyj@gmail.com',
    description='Flask extension for sendmail',
    long_description=__doc__,
    packages=['flask_sendmail'],
    test_suite='nose.collector',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
    ],
    tests_require=[
        'nose',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
