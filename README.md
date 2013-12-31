pycurl-win32
============

build pycurl for win32


because normal package download from pypi throw:

    ImportError: DLL load failed: The specified procedure could not be found.
    
I guess this maybe mismatch of openssl version, so I try to build with 1.0.0.t and replace with 0.9.8,
python throw this exception.

So I decided to link openssl staticly, and everything fine.

and I modify setup.py to include depend windows library and openssl, see setup.py source code for details.

    library_dirs.append(os.path.join(curl_dir, "lib"))
    extra_link_args.extend(["libeay32MD.lib", "ssleay32MD.lib", "advapi32.lib", "user32.lib"])
