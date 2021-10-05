"""
about format_dt, utcnow functions and TimestampStyle type hint are
The MIT License (MIT)
Copyright (c) 2015-present Rapptz
https://github.com/Rapptz/discord.py
"""
from __future__ import annotations

import datetime
from collections.abc import Generator
from typing import TYPE_CHECKING, Literal, TypeVar

if TYPE_CHECKING:
    from typing import Optional, Union


__all__ = (
    'YAML_DUMP_CONFIG',
    'split_line',
    'get_unique_list',
    'maybe_int',
    'TimestampStyle',
    'format_dt',
    'docstring_updater',
    'utcnow',
)


YAML_DUMP_CONFIG = {
    'encoding': 'utf8',
    'allow_unicode': True,
    'default_flow_style': False
}


T = TypeVar('T')


def split_line(string: str, num: int)-> Generator[str]:
    string, num = str(string), int(num)
    if len(string) <= num:
        yield string
        return
    str1, str2 = string[:num], string[num:]
    str1_split = str1.splitlines(keepends=True)
    if len(str1_split) > 1:
        str1 = ''.join(str1_split[:-1])
        str2 = str1_split[-1] + str2
    yield str1
    if len(str2) > num:
        yield from split_line(str2, num)
    else:
        yield str2


def get_unique_list(
        not_unique_list: list,
        *,
        need_flatten: bool= False
)-> list:
    if need_flatten:
        not_unique_list = sum(not_unique_list, [])
    return_list = []
    for element in not_unique_list:
        if element not in return_list:
            return_list.append(element)
    return return_list


TimestampStyle = Literal['f', 'F', 'd', 'D', 't', 'T', 'R']


def format_dt(
        dt: datetime.datetime,
        /,
        style: Optional[TimestampStyle] = None
)-> str:
    """
    A helper function to format a :class:`datetime.datetime`
    for presentation within Discord.

    This allows for a locale-independent way of presenting data using
    Discord specific Markdown.

    +-------------+----------------------------+-----------------+
    |    Style    |       Example Output       |   Description   |
    +=============+============================+=================+
    | t           | 22:57                      | Short Time      |
    +-------------+----------------------------+-----------------+
    | T           | 22:57:58                   | Long Time       |
    +-------------+----------------------------+-----------------+
    | d           | 17/05/2016                 | Short Date      |
    +-------------+----------------------------+-----------------+
    | D           | 17 May 2016                | Long Date       |
    +-------------+----------------------------+-----------------+
    | f (default) | 17 May 2016 22:57          | Short Date Time |
    +-------------+----------------------------+-----------------+
    | F           | Tuesday, 17 May 2016 22:57 | Long Date Time  |
    +-------------+----------------------------+-----------------+
    | R           | 5 years ago                | Relative Time   |
    +-------------+----------------------------+-----------------+

    Note that the exact output depends on the user's locale setting
    in the client.
    The example output presented is using the ``en-GB`` locale.

    .. versionadded:: 2.0

    Parameters
    -----------
    dt: :class:`datetime.datetime`
        The datetime to format.
    style: :class:`str`
        The style to format the datetime with.

    Returns
    --------
    :class:`str`
        The formatted string.
    """
    if style is None:
        return f'<t:{int(dt.timestamp())}>'
    return f'<t:{int(dt.timestamp())}:{style}>'


def docstring_updater(doc):
    def deco(func):
        func.__doc__ += doc
        return func
    return deco


def maybe_int(obj: T)-> Union[int, T]:
    try:
        return int(obj)
    except Exception:
        return obj


def utcnow() -> datetime.datetime:
    """A helper function to return an aware UTC datetime representing the current time.
    This should be preferred to :meth:`datetime.datetime.utcnow` since it is an aware
    datetime, compared to the naive datetime in the standard library.
    .. versionadded:: 2.0
    Returns
    --------
    :class:`datetime.datetime`
        The current aware datetime in UTC.
    """
    return datetime.datetime.now(datetime.timezone.utc)
