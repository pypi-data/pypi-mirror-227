"""
Library that makes it possible to work in a concise, algebraic way with
Python Imaging Library image objects.
"""
from __future__ import annotations
import doctest
import hashlib
import PIL.Image

class Image(PIL.Image.Image):
    """
    Derived class for :obj:`PIL.Image.Image` that is
    `hashable <https://docs.python.org/3/glossary.html#term-hashable>`__.
    When the :obj:`pillowcases.pillowcases` module is imported, the
    :obj:`PIL.Image.Image` class is redefined to refer to the
    :obj:`pillowcases.pillowcases.Image` class.

    >>> import pillowcases
    >>> i = PIL.Image.frombytes('RGBA', (2, 2), bytes([0]*16))
    >>> isinstance(i, pillowcases.Image)
    True

    Because instances of this derived class are
    `hashable <https://docs.python.org/3/glossary.html#term-hashable>`__,
    they can be added as elements to :obj:`set` objects and can be used
    as keys in :obj:`dict` objects.

    >>> j = PIL.Image.frombytes('RGBA', (2, 2), bytes([0]*16))
    >>> k = PIL.Image.frombytes('RGBA', (2, 2), bytes([255]*16))
    >>> len({i, j, k})
    2
    >>> d = {j: 1, k: 2}
    >>> d[k]
    2

    Compare the above to the default behavior of the :obj:`PIL.Image.Image`
    class, demonstrated below.

    >>> from importlib import reload
    >>> PIL.Image = reload(PIL.Image)
    >>> i = PIL.Image.frombytes('RGBA', (2, 2), bytes([0]*16))
    >>> j = PIL.Image.frombytes('RGBA', (2, 2), bytes([0]*16))
    >>> j = PIL.Image.frombytes('RGBA', (2, 2), bytes([255]*16))
    >>> len({i, j, k})
    Traceback (most recent call last):
        ...
    TypeError: unhashable type: 'Image'
    """
    def __hash__(self: Image) -> int:
        return int.from_bytes(hashlib.sha256(self.tobytes()).digest(), 'little')

PIL.Image.Image = Image # Replace class definition with that of derived class.

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
