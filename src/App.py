import email
import imaplib
import config


class MyMail():
    
    def __init__(self, mail, num):
        self._raw = mail
        self._from = mail['From']
        self._to = mail['To']
        self._subject = mail['Subject']
        self._date = mail['Date']
        self.num = num
        
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
        return f"Num: {self.num}\nfrom: {self._from}\nto: {self._to}\nsubject: {self._subject}\n\n{self._content}\n----------------\n"


def get_emails(imap):
    # select mailbox and search for emails
    imap.select(config.INBOX)
    _, data = imap.search(None, 'ALL')
    
    # iterate over email IDs and fetch data for each email
    for num in data[0].split():
        _, data = imap.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
    
        yield MyMail(msg, num)
    
    # close the connection
    imap.close()
    imap.logout()


def delete(imap, message_id:bytes|list[bytes], empty_folder=False):
    if type(message_id) == bytes:
        print("delete: ", message_id)
        imap.store(message_id, '+FLAGS', '\\Deleted')
        
    elif type(message_id) == list and len(message_id) > 0:
        message_id_list = message_id
        for message_id in message_id_list:
            print('delete: ', message_id)
            imap.store(message_id, '+FLAGS', '\\Deleted')
    else:
        return None
    
    
    # permanently remove deleted emails from mailbox
    if empty_folder:
        imap.expunge()

def main():
    
    try:
        imap = imaplib.IMAP4_SSL(config.HOST)
        imap.login(config.MAILADDRES, config.PASSWORD)
        
        dtl = []
        for mail in get_emails(imap):
            print(mail.show())
            
            # if mail.num == b'2':
                # delete(imap, mail.num)
                # dtl.append(mail.num)
        
        print("delete test list")   
        delete(imap, dtl)
        
    except Exception as e:
        print("wrong address or server")
        print(e)


if __name__ == "__main__":
    main()
