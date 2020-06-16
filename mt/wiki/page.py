import json as _js
import wikipedia as _w
import mt.base.path as _p

from . import home_dirpath
from .title import *


def page_id_dirpath(page_id):
    '''Retrieves the dirpath containing information about a page.
    
    Parameters
    ----------
    page_id : str
        page id

    Returns
    -------
    str
        local dirpath to the folder containing information about the page
    '''
    return _p.join(home_dirpath, 'page', page_id)


class Page(object):
    '''Wrapper of wikipedia.Page class which provides a caching mechanism.

    Parameters
    ----------
    page_title : str
        desired page title
    page_id : str
        desired page id
    cache_only : bool
        whether to restrict to our cache only or to use Wikipedia to resolve page attributes

    Attributes
    ----------
    page_id : str
        resolved page id
    wiki : wikipedia.WikipediaPage
        the remote instance wrapped by this instance
    dirpath : str
        path to the folder containing information about the page
    revision_id : int
        revision number
    url : str
        url to the Wikipedia page

    Notes
    -----
    The constructor must contain either page_id or page_title. In case both arugments are specified, we prioritise page_id.

    Raises
    ------
    ValueError
        for some errors in input arguments

    See Also
    --------
    wikipedia.page
        for constructing a page
    '''

    def __init__(self, page_title=None, page_id=None, cache_only=False):
        if page_title is not None and page_id is None: # use page_title
            self.page_id, self.wiki = as_page_id(page_title, cache_only=cache_only)
        else: # use page_id
            self.page_id = page_id
            self.wiki = None if cache_only else _p.page(pageid=page_id)

        self.dirpath = page_id_dirpath(self.page_id)
        _p.make_dirs(self.dirpath)

        self.sync_head()

        
    # ----- properties -----

    
    @property
    def content(self):
        '''Loads local page content and synchronises it with Wikipedia if allowed.'''
        if not hasattr(self, '_content'):
            filepath = _p.join(self.dirpath, 'content.json')

            if _p.exists(filepath):
                content = _js.load(open(filepath, 'r'))
                if content['revision_id'] != self.revision_id: # outdated content
                    if self.wiki is None:
                        raise ValueError("Unable to update the outdated content of page with id '{}'. Please disable 'cache_only'.".format(self.page_id))
                    content = {'revision_id': self.revision_id, 'content': self.wiki.content}
                    _js.dump(content, open(filepath, 'w'))
            else:
                content = {'revision_id': self.revision_id, 'content': self.wiki.content}
                _js.dump(content, open(filepath, 'w'))
                
            self._content = content['content']
        return self._content

    
    # ----- methods -----
            
    def sync_head(self):
        '''Loads local key attributes and synchronises them with Wikipedia if allowed.'''
        filepath = _p.join(self.dirpath, 'head.json')

        if _p.exists(filepath):
            head = _js.load(open(filepath, 'r'))
            dirty = False
            if self.wiki is not None and self.wiki.revision_id != head['revision_id']: # needs updating
                dirty = True
                head = {'revision_id': self.wiki.revision_id, 'url': self.wiki.url}                    
        else:
            if self.wiki is None:
                raise ValueError("Unable to find the head info for page with id '{}'".format(self.page_id))
            head = {'revision_id': self.wiki.revision_id, 'url': self.wiki.url}
            dirty = True

        self.revision_id = head['revision_id']
        self.url = head['url']

        if dirty:
            _js.dump(head, open(filepath, 'w'))
