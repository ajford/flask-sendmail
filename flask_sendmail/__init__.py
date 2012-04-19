"""
Module provides an interface to the system's sendmail client.

It's based heavily off of Flask-Mail (originaly by danjac),
and owes a majority of its code to him.

"""
from flask.ext.sendmail.message import Message
from flask.ext.sendmail.connection import Connection

class Mailer(object):

    def __init__(self,app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes your mail settings from app.config

        Can be used to set up the Mailer at configuration time

        :param app: Flask application instance
        """

        self.debug = app.config.get('MAIL_DEBUG',app.debug)
        self.mailer = app.config.get('MAIL_MAILER','/usr/sbin/sendmail')
        self.mailer_flags = app.config.get('MAIL_MAILER_FLAGS','-t')
        self.suppress = app.config.get('MAIL_SUPPRESS_SEND', False)
        self.fail_silently = app.config.get('MAIL_FAIL_SILENTLY', True)

        self.suppress = self.suppress or app.testing
        self.app = app

        #register extenshion with app
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['sendmail'] = self

    def send(self,message):
        """
        Sends message through system's sendmail client.

        :param message: Mailer Message instance
        """

        with self.connect() as connection:
            message.send(connection)

    def send_message(self, *args, **kwargs):
        """
        Shortcut for send(msg).

        Takes same arguments as Message constructor.
        """

        self.send(Message(*args, **kwargs))

    def connect(self, max_emails=None):
        """
        Opens a connection to the system's sendmail client.
        """

        return Connection(self, max_email)
