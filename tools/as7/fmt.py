# -*- coding: utf-8 -*-
"""This book's fmt: the shared code in tools/sampler/fmt.py, run here.

The shared file is executed in this module's own namespace, so `__file__`
is this folder and the book's specs.py, titles.py and book.py are the
ones it imports. Edit tools/sampler/fmt.py, never this."""
import os as _os
_SHARED = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                        "sampler", "fmt.py")
exec(compile(open(_SHARED, encoding="utf-8").read(), _SHARED, "exec"))
