from subprocess import PIPE,STDOUT,Popen


class Connection(object):
    """Handles connection to host."""

    def __init__(self, mail, max_emails=None):

        self.mail = mail
        self.app = self.mail.app
        self.suppress = self.mail.suppress
        self.max_emails = max_emails or self.mail.max_emails or 0
        self.fail_silently = self.mail.fail_silently

    def send(self,message):
        sm = Popen([self.mailer,self.mailer_flags], stdin=PIPE, stdout=PIPE,
                    stderr=STDOUT)
        sm.stdin.write(message.dump())
        sm.communicate()
        
        return sm.returncode
