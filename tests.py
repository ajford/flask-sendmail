import unittest
import mailbox

from email import encoders

from flask import Flask, g
from flask_sendmail import Mail, Message, BadHeaderError

class TestCase(unittest.TestCase):
    
    TESTING = True
    DEFAULT_MAIL_SENDER = "support@example.com"

    def setUp(self):
        
        self.app = Flask(__name__)
        self.app.config.from_object(self)

        self.assertTrue(self.app.testing)

        self.mail = Mail(self.app)

        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

class TestMessage(TestCase):

    def test_initialize(self):

        msg = Message(subject="subject",
                      recipients=['to@example.com'])

        self.assertEqual(msg.sender, "support@example.com")
        self.assertEqual(msg.recipients, ['to@example.com'])

    def test_recipients_properly_initialized(self):

        msg = Message(subject="subject")
        self.assertEqual(msg.recipients, [])

        msg2 = Message(subject="subject")
        msg2.add_recipient("somebody@example.com")
        self.assertEqual(len(msg2.recipients), 1)

    #def test_sendto_properly_set(self):
        #msg = Message(subject="subject", recipients=["somebody@example.com"],
                       #cc=["cc@example.com"], bcc=["bcc@example.com"])
        #self.assertEqual(len(msg.send_to), 3)
        #msg.add_recipient("cc@example.com")
        #self.assertEqual(len(msg.send_to), 3)

    def test_add_recipient(self):

        msg = Message("testing")
        msg.add_recipient("to@example.com")

        self.assertEqual(msg.recipients, ["to@example.com"])


    def test_sender_as_tuple(self):

        msg = Message(subject="testing",
                      sender=("tester", "tester@example.com"),
                      body="test")

        msg_str = msg.dump()
        self.assertTrue("From: tester <tester@example.com>" in str(msg_str))

    
    def test_reply_to(self):

        msg = Message(subject="testing",
                      recipients=["to@example.com"],
                      sender="spammer <spammer@example.com>",
                      reply_to="somebody <somebody@example.com>",
                      body="testing")

        msg_str = msg.dump()
        self.assertTrue("Reply-To: somebody <somebody@example.com>" in str(msg_str))

    def test_send_without_sender(self):

        del self.app.config['DEFAULT_MAIL_SENDER']

        msg = Message(subject="testing",
                      recipients=["to@example.com"],
                      body="testing")

        self.assertRaises(AssertionError, self.mail.send, msg)

    def test_send_without_recipients(self):

        msg = Message(subject="testing",
                      recipients=[],
                      body="testing")

        self.assertRaises(AssertionError, self.mail.send, msg)

    def test_send_without_body(self):

        msg = Message(subject="testing",
                      recipients=["to@example.com"])

        self.assertRaises(AssertionError, self.mail.send, msg)

    #def test_normal_send(self):
        #"""
        #This will not actually send a message unless the mail server
        #is set up. The error will be logged but test should still
        #pass.
        #"""
#
        #self.app.config['TESTING'] = False
        #self.mail.init_app(self.app)
#
        #with self.mail.record_messages() as outbox:
#
            #msg = Message(subject="testing",
                          #recipients=["to@example.com"],
                          #body="testing")
#
            #self.mail.send(msg)
#
            #self.assertEqual(len(outbox), 1)
#
        #self.app.config['TESTING'] = True

    def test_bcc(self):

        msg = Message(subject="testing",
                      recipients=["to@example.com"],
                      body="testing",
                      bcc=["tosomeoneelse@example.com"])

        msg_str = msg.dump()
        self.assertTrue("Bcc: tosomeoneelse@example.com" in str(msg_str))

    def test_cc(self):

        msg = Message(subject="testing",
                      recipients=["to@example.com"],
                      body="testing",
                      cc=["tosomeoneelse@example.com"])

        msg_str = msg.dump()
        self.assertTrue("Cc: tosomeoneelse@example.com" in str(msg_str))
 
