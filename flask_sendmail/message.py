from email.mime.text import MIMEText
import sys

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class BadHeaderError(Exception):
    pass


class Message(object):
    """
    Encapsulates an email message.

    :param subject: email subject header
    :param recipients: list of email addresses
    :param body: plain text message
    :param html: HTML message
    :param sender: email sender address, or **DEFAULT_MAIL_SENDER** by default
    :param cc: CC list
    :param bcc: BCC list
    :param attachments: list of Attachment instances
    :param reply_to: reply-to address
    :param charset: used to set MIMEText _charset
    """

    def __init__(self, subject, recipients=None, body=None, html=None,
                sender=None, cc=None, bcc=None, attachments=None,
                reply_to=None, charset=None):

        if sender is None:
            app = stack.top.app
            sender = app.config.get("DEFAULT_MAIL_SENDER")

        self.subject = subject
        self.sender = sender
        self.body = body
        self.html = html
        self.charset = charset
        self.cc = cc
        self.bcc = bcc
        self.reply_to = reply_to

        if recipients is None:
            recipients = []

        self.recipients = list(recipients)

        if attachments is None:
            attachments = []

        self.attachments = attachments

    def add_recipient(self, recipient):
        """
        Adds another recipient to the message.

        :param recipient: email address.
        """

        self.recipients.append(recipient)

    def is_bad_headers(self):
        """
        Checks for bad headers i.e. newlines in subject, sender or recipients.
        """

        reply_to = self.reply_to or ''
        for val in [self.subject, self.sender, reply_to] + self.recipients:
            for c in '\r\n':
                if c in val:
                    return True
        return False

    def dump(self):
        if self.html:
            msg = MIMEText(self.html, 'html', self.charset)
        elif self.body:
            msg = MIMEText(self.body, 'plain', self.charset)

        if isinstance(self.sender, tuple):
            # sender can be tuple of (name, address)
            self.sender = "%s <%s>" % self.sender

        msg['Subject'] = self.subject
        msg['To'] = ', '.join(self.recipients)
        msg['From'] = self.sender
        if self.cc:
            if hasattr(self.cc, '__iter__'):
                msg['Cc'] = ', '.join(self.cc)
            else:
                msg['Cc'] = self.cc
        if self.bcc:
            if hasattr(self.bcc, '__iter__'):
                msg['Bcc'] = ', '.join(self.bcc)
            else:
                msg['Bcc'] = self.bcc
        if self.reply_to:
            msg['Reply-To'] = self.reply_to

        msg_str = msg.as_string()
        if sys.version_info >= (3,0) and isinstance(msg_str, str):
            return msg_str.encode(self.charset or 'utf-8')
        else:
            return msg_str

    def send(self, connection):
        """
        Verifies and sends the message.

        :param connection: Connection instance
        """

        assert self.recipients, "No recipients have been added"
        assert self.body or self.html, "No body or HTML has been set"
        assert self.sender, "No sender address has been set"

        if self.is_bad_headers():
            raise BadHeaderError

        connection.send(self)
