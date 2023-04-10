import email
import imaplib
import config


def get_emails():
    imap = imaplib.IMAP4_SSL(config.HOST)
    imap.login(config.MAILADDRES, config.PASSWORD)
    
    # select mailbox and search for emails
    imap.select('Inbox')
    _, data = imap.search(None, 'ALL')
    
    # iterate over email IDs and fetch data for each email
    for num in data[0].split():
        _, data = imap.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
    
        # print email headers
        print('From:', msg['From'])
        print('To:', msg['To'])
        print('Subject:', msg['Subject'])
        print('Date:', msg['Date'])
    
        # print email body if it's in plain text format
        if msg.is_multipart():
            for part in msg.get_payload():
                if part.get_content_type() == 'text/plain':
                    print('Body:', part.get_payload(decode=True).decode())
        else:
            if msg.get_content_type() == 'text/plain':
                print('Body:', msg.get_payload(decode=True).decode())

    
    # close the connection
    imap.close()
    imap.logout()


def main():
    
    try:
        get_emails()
        
    except Exception as e:
        print("wrong address or server")
        print(e)


if __name__ == "__main__":
    main()
