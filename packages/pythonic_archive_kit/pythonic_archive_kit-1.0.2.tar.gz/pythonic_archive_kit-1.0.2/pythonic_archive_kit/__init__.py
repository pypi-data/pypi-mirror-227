"""The Pythonic Archive Kit"""
__version__ = "1.0.2"

from . import mini_pak

try:
    from . import pak
except ImportError:
    pak = mini_pak
    print("WARNING: cryptography is not installed. PAK files will not be encrypted.", "To install cryptography, run `pip install cryptography`", sep="\n")
    
if pak is None:
    open = mini_pak.open_pak
    load = mini_pak.load_pak
    save = mini_pak.save_pak
else:
    open = pak.open_pak
    load = pak.load
    save = pak.save