from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sys

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

PY3 = sys.version_info[0] == 3


class Attachment(object):
    """Encapsulates file attachment information.

    :param filename: filename of attachment
    :param content_type: file mimetype
    :param data: the raw file data
    :param disposition: content-disposition (if any)
    """

    def __init__(self, filename=None, content_type=None, data=None,
                 disposition=None, headers=None):
        self.filename = filename
        self.content_type = content_type or 'application/octet-stream'
        self.data = data
        self.disposition = disposition or 'attachment'
        self.headers = headers or {}


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


    def add_attachment(self,
                       filename=None,
                       content_type=None,
                       data=None,
                       disposition=None,
                       headers=None):
        """
        Adds an attachment to the message.

        :param filename: filename of attachment
        :param content_type: file mimetype
        :param data: the raw file data
        :param disposition: content-disposition (if any)
        """
        self.attachments.append(
            Attachment(filename, content_type, data, disposition, headers))

        return self

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
        attachments = self.attachments or []

        if len(attachments) == 0 and not self.html:
            # No HTML without attachments - plain text email
            msg = MIMEText(self.body, 'plain', self.charset)
        elif len(attachments) > 0 and not self.html:
            # No HTML with attachments means multipart
            msg = MIMEMultipart()
            msg.attach(MIMEText(self.body, 'plain', self.charset))
        else:
            msg = MIMEMultipart()
            alt = MIMEMultipart('alternative')
            alt.attach(self.html, 'html', self.charset)
            msg.attach(alt)

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

        # Attachments
        for attachment in attachments:
            f = MIMEBase(*attachment.content_type.split('/'))
            f.set_payload(attachment.data)
            encode_base64(f)

            filename = attachment.filename

            # TODO: Optional force filename to ASCII

            try:
                filename and filename.encode('ascii')
            except UnicodeEncodeError:
                if not PY3:
                    filename = filename.encode('utf-8')
                filename = ('UTF-8', '', filename)

            f.add_header('Content-Disposition',
                         attachment.disposition,
                         filename=filename)

            for k, v in attachment.headers.items():
                f.add_header(k, v)

            msg.attach(f)


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
