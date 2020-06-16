import hashlib as _hl
import json as _js
import wikipedia as _w
import mt.base.path as _p

from . import home_dirpath


__all__ = ['page_title_filepath', 'register_page_title_to_id', 'as_page_id']


def page_title_filepath(page_title):
    '''Retrieves the filepath unique to a page title that contains the page id cache.
    
    Parameters
    ----------
    page_title : str
        page title

    Returns
    -------
    str
        the filepath
    '''
    dirpath = _p.join(home_dirpath, 'title_map')
    _p.make_dirs(dirpath)

    filepath = _hl.md5(page_title.encode()).hexdigest()+'.json'
    filepath = _p.join(dirpath, filepath)

    return filepath


def register_page_title_to_id(page_title, page_id):
    '''Registers an (page_title, page_id) entry.'''
    filepath = page_title_filepath(page_title)
    if _p.exists(filepath):
        old_page_id = _js.load(open(filepath, 'r'))
        if old_page_id == page_id:
            return # no need to register the same page id
    _js.dump(page_id, open(filepath, 'w'))


def as_page_id(page_title, cache_only=False):
    '''Converts a page title into a page id using our cache, checking Wikipedia if allowed.

    Parameters
    ----------
    page_title : str
        page title
    cache_only : bool
        whether to restrict to our cache only or to use Wikipedia to resolve the page id

    Returns
    -------
    page_id : str
        page id
    wiki : wikipedia.Page or None
        If cache_only is False, the wikipedia.Page instance. Otherwise None.

    Raises
    ------
    wikipedia.exceptions.PageError
        if no page is found
    '''

    if cache_only:
        filepath = page_title_filepath(page_title)
        local_page_id = _js.load(open(filepath, 'r')) if _p.exists(head_filepath) else None
        if not local_page_id:
            raise _w.exceptions.PageError("Page titled '{}' not found.".format(page_title), pageid=None)
        return local_page_id, None

    page = _w.page(page_title)
    page_id = page.pageid
    register_page_title_to_id(page_title, page_id)
    page_title2 = page.title
    if page_title != page_title2:
        register_page_title_to_id(page_title2, page_id)
    return page_id, page
