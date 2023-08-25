"""IPFS HTTP Client for Python

Install
-------

.. code-block:: bash

    pip install ipfs-http-client-sdk

Quickstart
----------

>>> from ipfs_http_client_sdk import Ipfs
>>> ipfs = Ipfs()
>>> result = ipfs.cat({
...     "cid": "Qmc5gCcjYypU7y28oCALwfSvxCBskLuPKWpK4qpterKC7z",
...     "ipfsProvider": "https://ipfs.io"
... })
>>> print(result.decode().strip())
Hello World!

Contact Us
----------
Join our `discord <https://discord.polywrap.io>`__ and ask your questions right away!
"""
from .wrap import *

__all__ = [
    # SDK
    "Ipfs",
    # Types
    "IpfsCatOptions",
    "IpfsAddOptions",
    "IpfsResolveOptions",
    "IpfsResolveResult",
    "IpfsAddResult",
    "IpfsFileEntry",
    "IpfsDirectoryEntry",
    "IpfsBlob",
    # Args
    "IpfsModuleArgsCat",
    "IpfsModuleArgsResolve",
    "IpfsModuleArgsAddFile",
    "IpfsModuleArgsAddDir",
    "IpfsModuleArgsAddBlob",
]
