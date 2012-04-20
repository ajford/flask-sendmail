from .message import Message
from .connection import Connection


class Mail(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes your mail settings from app.config

        Can be used to set up Mail at configuration time

        :param app: Flask application instance
        """

        self.debug = app.config.get('MAIL_DEBUG', app.debug)
        self.mailer = app.config.get('MAIL_MAILER', '/usr/sbin/sendmail')
        self.mailer_flags = app.config.get('MAIL_MAILER_FLAGS', '-t')
        self.suppress = app.config.get('MAIL_SUPPRESS_SEND', False)
        self.fail_silently = app.config.get('MAIL_FAIL_SILENTLY', True)
        self.max_emails = None
        self.suppress = self.suppress or app.testing
        self.app = app

        #register extension with app
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['sendmail'] = self

    def send(self, message):
        """
        Sends message through system's sendmail client.

        :param message: Mail Message instance
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

        return Connection(self, max_emails)
