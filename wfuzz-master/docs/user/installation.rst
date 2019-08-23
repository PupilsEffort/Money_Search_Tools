Installation
==================================

Pip install Wfuzz
--------------------

To install WFuzz using `pip <https://pip.pypa.io>`_ ::

    $ pip install wfuzz

Get the Source Code
-------------------

Wfuzz is actively developed on 
`GitHub <https://github.com/xmendez/wfuzz>`_.

You can either clone the public repository::

    $ git clone git://github.com/xmendez/wfuzz.git

Or download last `release <https://github.com/xmendez/wfuzz/releases/latest>_`.

Once you have a copy of the source, you can embed it in your own Python
package, or install it into your site-packages easily::

    $ python setup.py install


Dependencies
-----------

Wfuzz uses:

* `pycurl <http://pycurl.sourceforge.net/>`_ library to perform HTTP requests.
* `pyparsing <https://github.com/pyparsing/pyparsing>`_ library to create filter's grammars.
* `JSON.miniy (C) Gerald Storer <https://github.com/getify/JSON.minify/blob/master/minify_json.py>`_ to read json recipes.
* `chardet <https://chardet.github.io/>`_ to detect dictionaries encoding.
* `coloroma <https://github.com/tartley/colorama/>`_ to support ANSI escape characters in Windows.

Installation issues
===================

Pycurl on MacOS
--------------------------

Wfuzz uses pycurl as HTTP library. You might get errors like the listed below when running Wfuzz::

    pycurl: libcurl link-time ssl backend (openssl) is different from compile-time ssl backend (none/other)

Or::

    pycurl: libcurl link-time ssl backend (none/other) is different from compile-time ssl backend (openssl)

This is due to the fact that, MacOS might need some tweaks before pycurl is installed correctly:

#. First you need to install OpenSSL via Homebrew::

    $ brew install openssl

#. Curl is normally already installed in MacOs, but to be sure it uses OpenSSL, we need to install it using brew::

    $ brew install curl-openssl

#. Curl is installed keg-only by brew. This means that is installed but not linked. Therefore, we need to instruct pip to use the recently installed curl before installing pycurl. We can do this permanently by changing our bash_profile::

    $ echo 'export PATH="/usr/local/opt/curl-openssl/bin:$PATH"' >> ~/.bash_profile

#. Or temporary in the current shell::

    $ export PATH="/usr/local/opt/curl-openssl/bin:$PATH"

#. Then, we need to install pycurl as follows::

    $ PYCURL_SSL_LIBRARY=openssl LDFLAGS="-L/usr/local/opt/openssl/lib" CPPFLAGS="-I/usr/local/opt/openssl/include" pip install --no-cache-dir pycurl

#. Finally, if we re-install or execute wfuzz again it should work correctly.

Pycurl on Windows
-----------------

Install pycurl matching your python version from https://pypi.org/project/pycurl/#files

PyCurl SSL bug
--------------

If you experience errors when using Wfuzz against SSL sites, it could be because an old know issue:

http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=515200

Briefly, pycurl is built against libcurl3-gnutls, which does not work with a number of web sites. Pycurl fails with the following error message::

   pycurl.error: (35, 'gnutls_handshake() failed: A TLS packet with unexpected length was received.')

Verifying the problem
^^^^^^^^^^^^^^^^^^^^^

* Pycurl linked against gnutls::

    $ python
    >>> import pycurl
    >>> pycurl.version
    libcurl/7.21.3 GnuTLS/2.8.6 zlib/1.2.3.4 libidn/1.18'

* Pycurl linked against openssl::

    $ python
    >>> import pycurl
    >>> pycurl.version
    'libcurl/7.21.3 OpenSSL/0.9.8o zlib/1.2.3.4 libidn/1.18'

Installing pycurl openssl flavour
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In newer Ubuntu versions, you can install libcurl openssl flavour::

    $ sudo apt install libcurl4-openssl-dev
    $ sudo pip3 install --upgrade wfuzz 

Installing pycurl against openssl
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Alternatively, it can be done manually:

1. sudo apt-get install build-essential fakeroot dpkg-dev
2. mkdir ~/python-pycurl-openssl
3. cd ~/python-pycurl-openssl
4. sudo apt-get source python-pycurl
5. sudo apt-get build-dep python-pycurl
6. sudo apt-get install libcurl4-openssl-dev
7. sudo dpkg-source -x pycurl_7.19.0-3build1.dsc
8. cd pycurl-7.19.0
9. edit debian/control file and replace all instances of “libcurl4-gnutls-dev” with “libcurl4-openssl-dev”
10. sudo PYCURL_SSL_LIBRARY=openssl dpkg-buildpackage -rfakeroot -b
11. sudo dpkg -i ../python-pycurl_7.19.0-3build1_i386.deb

If there is still the error::

    ImportError?: No module named bottle

Check this http://stackoverflow.com/questions/9122200/importerror-no-module-named-bottle
