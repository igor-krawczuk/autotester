import pytest
from unittest.mock import MagicMock,patch

from autotester.MailNotificator import MailNotificator
from autotester.abstractions import *

@pytest.fixture(autouse=True)
def no_stmplib(monkeypatch):
    monkeypatch.setattr("smtplib.SMTP", MagicMock())


@pytest.fixture(scope="function")
def notif(monkeypatch):
    monkeypatch.setattr("smtplib.SMTP", MagicMock())
    target_mail = "igor@me.com"
    server = "seerver.com"
    port = "80"
    fromaddr = "asdasd@moh.com"
    password =" nope"
    yield MailNotificator(target_mail, server,port, fromaddr,password)

class Test_MailNotificator:
    def test_init(self):
        pass
    
    def test_send(self,notif):
        body= "body"
        subject="sub"
        notif.send(body,subject)

    def test_done(self,notif):
        notif.done
