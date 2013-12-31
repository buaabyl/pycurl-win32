pycurl-win32
============

build pycurl for win32


because normal package download from pypi throw:

    ImportError: DLL load failed: The specified procedure could not be found.
    
I guess this maybe mismatch of openssl version, so I try to build with 1.0.0.t and replace with 0.9.8,
python throw this exception.

So I decided to link openssl staticly, and everything fine.
