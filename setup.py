#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et
#
#   setup.py build -c mingw32
#
#   pip wheel --global-option build_ext --global-option --compiler=mingw32 .
#

"""Setup script for the PycURL module distribution."""

PACKAGE = "pycurl"
PY_PACKAGE = "curl"
VERSION = "7.43.0"

import os
import sys
from distutils.core import setup
from distutils.extension import Extension

if sys.version.find('AMD64') >= 0:
    LIBCURL_PATH = 'mingw64'
    MINGW_PATH   = 'C:/msys64/mingw64'
else:
    LIBCURL_PATH = 'mingw32'
    MINGW_PATH   = 'C:/msys64/mingw32'

setup_args = dict(
    name=PACKAGE,
    version=VERSION,
    description='PycURL -- A Python Interface To The cURL library',
    long_description='''\
PycURL -- A Python Interface To The cURL library
================================================

PycURL is a Python interface to `libcurl`_, the multiprotocol file
transfer library. Similarly to the urllib_ Python module,
PycURL can be used to fetch objects identified by a URL from a Python program.
Beyond simple fetches however PycURL exposes most of the functionality of
libcurl, including:

- Speed - libcurl is very fast and PycURL, being a thin wrapper above
  libcurl, is very fast as well. PycURL `was benchmarked`_ to be several
  times faster than requests_.
- Features including multiple protocol support, SSL, authentication and
  proxy options. PycURL supports most of libcurl's callbacks.
- Multi_ and share_ interfaces.
- Sockets used for network operations, permitting integration of PycURL
  into the application's I/O loop (e.g., using Tornado_).

.. _was benchmarked: http://stackoverflow.com/questions/15461995/python-requests-vs-pycurl-performance
.. _requests: http://python-requests.org/
.. _Multi: http://curl.haxx.se/libcurl/c/libcurl-multi.html
.. _share: http://curl.haxx.se/libcurl/c/libcurl-share.html
.. _Tornado: http://www.tornadoweb.org/


Requirements
------------

- Python 2.6, 2.7 or 3.1 through 3.5.
- libcurl 7.19.0 or better.


Installation
------------

Download source and binary distributions from `PyPI`_ or `Bintray`_.
Binary wheels are now available for 32 and 64 bit Windows versions.

Please see `the installation documentation`_ for installation instructions.

.. _PyPI: https://pypi.python.org/pypi/pycurl
.. _Bintray: https://dl.bintray.com/pycurl/pycurl/
.. _the installation documentation: http://pycurl.io/docs/latest/install.html


Documentation
-------------

Documentation for the most recent PycURL release is available on
`PycURL website <http://pycurl.io/docs/latest/>`_.


Support
-------

For support questions please use `curl-and-python mailing list`_.
`Mailing list archives`_ are available for your perusal as well.

Although not an official support venue, `Stack Overflow`_ has been
popular with some PycURL users.

Bugs can be reported `via GitHub`_. Please use GitHub only for bug
reports and direct questions to our mailing list instead.

.. _curl-and-python mailing list: http://cool.haxx.se/mailman/listinfo/curl-and-python
.. _Stack Overflow: http://stackoverflow.com/questions/tagged/pycurl
.. _Mailing list archives: http://curl.haxx.se/mail/list.cgi?list=curl-and-python
.. _via GitHub: https://github.com/pycurl/pycurl/issues


License
-------

PycURL is dual licensed under the LGPL and an MIT/X derivative license
based on the libcurl license. The complete text of the licenses is available
in COPYING-LGPL_ and COPYING-MIT_ files in the source distribution.

.. _libcurl: http://curl.haxx.se/libcurl/
.. _urllib: http://docs.python.org/library/urllib.html
.. _COPYING-LGPL: https://raw.githubusercontent.com/pycurl/pycurl/master/COPYING-LGPL
.. _COPYING-MIT: https://raw.githubusercontent.com/pycurl/pycurl/master/COPYING-MIT
''',
    author="Kjetil Jacobsen, Markus F.X.J. Oberhumer, Oleg Pudeyev",
    author_email="kjetilja at gmail.com, markus at oberhumer.com, oleg at bsdpower.com",
    maintainer="Oleg Pudeyev",
    maintainer_email="oleg@bsdpower.com",
    url="http://pycurl.io/",
    license="LGPL/MIT",
    keywords=['curl', 'libcurl', 'urllib', 'wget', 'download', 'file transfer',
        'http', 'www'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: File Transfer Protocol (FTP)',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=[PY_PACKAGE],
    package_dir={ PY_PACKAGE: os.path.join('python', 'curl') },
)

if __name__ == "__main__":
    sources = [
        os.path.join("src", "docstrings.c"),
        os.path.join("src", "easy.c"),
        os.path.join("src", "module.c"),
        os.path.join("src", "multi.c"),
        os.path.join("src", "oscompat.c"),
        os.path.join("src", "pythoncompat.c"),
        os.path.join("src", "share.c"),
        os.path.join("src", "stringcompat.c"),
        os.path.join("src", "threadsupport.c"),
    ]
    depends = [
        os.path.join("src", "pycurl.h"),
    ]
    ext = Extension(
        name                = PACKAGE,
        sources             = sources,
        depends             = depends,
        include_dirs        = [
            os.path.realpath(os.path.join(LIBCURL_PATH, 'include')),
            os.path.realpath(os.path.join(MINGW_PATH, 'include')),
        ],
        define_macros       = [
            ('HAVE_CURL_SSL',1),
            ('HAVE_CURL_OPENSSL',1),
            ('CURL_STATICLIB',1),
        ],
        library_dirs        = [os.path.realpath(os.path.join(LIBCURL_PATH, 'lib'))],
        extra_objects       = [
            os.path.realpath(os.path.join(LIBCURL_PATH, 'lib', 'libcurl_ssl.a')),
            os.path.realpath(os.path.join(MINGW_PATH, 'lib', 'libssl.a')),
            os.path.realpath(os.path.join(MINGW_PATH, 'lib', 'libcrypto.a')),
            os.path.realpath(os.path.join(MINGW_PATH, 'lib', 'libz.a')),
        ],
        libraries           = [
	        'ws2_32',
	        'gdi32',
	        'wldap32',
        ],
        extra_compile_args  = [],
        extra_link_args     = ['-static-libgcc'],
    )

    setup_args['ext_modules'] = [ext]
    setup(**setup_args)

