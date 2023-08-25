#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Misc API routes
"""

from __future__ import annotations
from meerschaum.utils.typing import Optional

def get_mrsm_version(self, **kw) -> Optional[str]:
    """

    Parameters
    ----------
    **kw :
        

    Returns
    -------
    type
        

    """
    from meerschaum.config.static import _static_config
    try:
        j = self.get(
            _static_config()['api']['endpoints']['version'] + '/mrsm',
            use_token = True,
            **kw
        ).json()
    except Exception as e:
        return None
    if isinstance(j, dict) and 'detail' in j:
        return None
    return j

def get_chaining_status(self, **kw) -> Optional[bool]:
    """

    Parameters
    ----------
    **kw :
        

    Returns
    -------
    type
        

    """
    from meerschaum.config.static import _static_config
    try:
        response = self.get(
            _static_config()['api']['endpoints']['chaining'],
            use_token = True,
            **kw
        )
        if not response:
            return None
    except Exception as e:
        return None

    return response.json()
