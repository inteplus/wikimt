from mt.base import logger, home_dirpath as base_dirpath
import mt.base.path as _p
from .version import version as __version__


home_dirpath = _p.join(base_dirpath, 'wiki')


__all__ = ['logger', 'home_dirpath']
