Flask-Sendmail
======================================

.. module:: flask-mail

Emailing users is essential in most web applications. For most cases, you can
easily use SMTP, and in those cases, `Flask-Mail`_ is perfect. In other cases,
you can only use your system's ``sendmail`` client.

The **Flask-Sendmail** extension provides a simple interface to your system's
sendmail client from within your `Flask`_ application and gives you ability to 
send messages from your views and scripts.

Source code and issue tracking are at `GitHub`_.

Installing Flask-Sendmail
-------------------------

Install with **pip** and **easy_install**::

    pip install Flask-Sendmail

or download the latest version from version control::

    git clone https://github.com/ajford/flask-sendmail.git
    cd flask-sendmail
    python setup.py install

If you are using **virtualenv**, it is assumed that you are installing
flask-mail in the same virtualenv as your Flask application(s).

Configuring Flask-Sendmail
--------------------------

**Flask-Sendmail** is configured through the standard Flask config API. These are the available
options (each is explained later in the documentation):

* **MAIL_MAILER** : default **'/usr/sbin/sendmail'**

* **MAIL_MAILER_FLAGS** : default **'-t'**

* **MAIL_DEBUG** : default **app.debug**

* **DEFAULT_MAIL_SENDER** : default **None**

* **DEFAULT_MAX_EMAILS** : default **None**

* **MAIL_FAIL_SILENTLY** : default **True**
  
* **MAIL_SUPPRESS_SEND** : default **False**

In addition the standard Flask ``TESTING`` configuration option is used by
**Flask-Sendmail** in unit tests (see below).

Emails are managed through a ``Mail`` instance::

    from flask import Flask
    from flask.ext.sendmail import Mail

    app = Flask(__name__)
    mail = Mail(app)

Alternatively you can set up your ``Mail`` instance later at configuration time,
using the **init_app** method::

    mail = Mail()

    app = Flask(__name__)
    mail.init_app(app)


Sending messages
----------------

To send a message first create a ``Message`` instance::

    from flask.ext.sendmail import Message

    @app.route("/")
    def index():

        msg = Message("Hello",
                      sender="from@example.com",
                      recipients=["to@example.com"])
       
You can set the recipient emails immediately, or individually::

    msg.recipients = ["you@example.com"]
    msg.add_recipient("somebodyelse@example.com")

If you have set ``DEFAULT_MAIL_SENDER`` you don't need to set the message
sender explicity, as it will use this configuration value by default::

    msg = Message("Hello",
                  recipients=["to@example.com"])

If the ``sender`` is a two-element tuple, this will be split into name
and address::

    msg = Message("Hello",
                  sender=("Me", "me@example.com"))

    assert msg.sender == "Me <me@example.com>"

The message can contain a body and/or HTML::

    msg.body = "testing"
    msg.html = "<b>testing</b>"

Finally, to send the message, you use the ``Mail`` instance configured with your
Flask application::

    mail.send(msg)

If the setting **MAIL_FAIL_SILENTLY** is **True**, and the connection fails (for
example, the mail server cannot be found at that hostname) then no error will be
raised, although of course no emails will be sent either.


Bulk emails
-----------

While `Flask-Mail`_ supports bulk emailing, **Flask-Sendmail** does not yet
support it. If anyone has any suggestions on achieving bulk email support,
please pull a request on `Github`_.

**Flask-Sendmail** does take the ``max_email`` argument in an effort to mantain
drop-in compatibility


Attachments
-----------

Attachments are planned for a future release.

Unit tests and suppressing emails
---------------------------------

When you are sending messages inside of unit tests, or in a development
environment, it's useful to be able to suppress email sending.

If the setting ``TESTING`` is set to ``True``, emails will be
suppressed. Calling ``send()`` on your messages will not result in 
any messages being actually sent.

Alternatively outside a testing environment you can set ``MAIL_SUPPRESS_SEND``
to **False**. This will have the same effect.

Header injection
----------------

To prevent `header injection <http://www.nyphp.org/PHundamentals/8_Preventing-Email-Header-Injection>`_,
attempts to send a message with newlines in the subject, sender or recipient
addresses will result in a ``BadHeaderError``.


API
---

.. module:: flask_sendmail
 
.. autoclass:: Mail
   :members: send, connect, send_message

.. autoclass:: Connection
   :members: send, send_message

.. autoclass:: Message
   :members: attach, add_recipient

.. _Flask: http://flask.pocoo.org
.. _Flask-Mail: http://packages.python.org/Flask-Mail/
.. _GitHub: http://github.com/ajford/flask-sendmail
