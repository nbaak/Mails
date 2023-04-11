import email
import imaplib
import config


class MyMail():
    
    def __init__(self, mail):
        self._raw = mail
        self._from = mail['From']
        self._to = mail['To']
        self._subject = mail['Subject']
        self._date = mail['Date']
        
        self._content = self.get_content(mail)
        
    def get_content(self, mail):
        if mail.is_multipart():
            for part in mail.get_payload():
                if part.get_content_type() == 'text/plain':
                    return part.get_payload(decode=True).decode()
        else:
            if mail.get_content_type() == 'text/plain':
                return mail.get_payload(decode=True).decode()
            
    def show(self):
        return f"from: {self._from}\nto: {self._to}\nsubject: {self._subject}\n\n{self._content}\n----------------\n"



def get_emails():
    imap = imaplib.IMAP4_SSL(config.HOST)
    imap.login(config.MAILADDRES, config.PASSWORD)
    
    # select mailbox and search for emails
    imap.select(config.INBOX)
    _, data = imap.search(None, 'ALL')
    
    # iterate over email IDs and fetch data for each email
    for num in data[0].split():
        _, data = imap.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
    
        yield MyMail(msg)

    
    # close the connection
    imap.close()
    imap.logout()


def main():
    
    try:
        for mail in get_emails():
            print(mail.show())
        
    except Exception as e:
        print("wrong address or server")
        print(e)


if __name__ == "__main__":
    main()
