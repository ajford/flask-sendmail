"""
    flask_sendmail
    ~~~~~~~~~~~~~~

    Module provides an interface to the system's sendmail client.

    It's based heavily off of Flask-Mail (written by danjac),
    and owes a majority of its code to it.

    It's also designed to be a nearly complete drop-in replacement
    for Flask-Mail.

    :copyright: (c) 2012 by Anthony Ford.
    :license: None, see LICENSE for more details.
"""

from .mail import Mail
from .message import Message, BadHeaderError
