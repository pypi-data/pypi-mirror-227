"""The Pythonic Archive Kit"""
__version__ = "1.0.4"

from . import mini_pak

try:
    from . import pak
except ImportError:
    pak = mini_pak
    print(
        "WARNING: cryptography is not installed. PAK files will not be encrypted.", 
        "To install cryptography, run `pip install cryptography`", 
        sep="\n"
        )
    
open = pak.open_pak
load = pak.load_pak
save = pak.save_pak