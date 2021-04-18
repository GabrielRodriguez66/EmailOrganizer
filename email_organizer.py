import imapclient
import os


class IMAPClient:
    def __init__(self, email, password, imap_server):
        self.email = email
        self.password = password
        self.imap_server = imap_server

    def organize_emails(self, old_folder, new_folder, search_keywords):
        '''
            old_folder: folder to retrieve emails
            new_folder: target folder to move emails
            search_keywords: iterable of keywords for filtering emails
        '''
        with imapclient.IMAPClient(self.imap_server, ssl=True) as imapObj:
            imapObj.login(self.email, self.password)
            imapObj.select_folder(old_folder, readonly=True)
            if not imapObj.folder_exists(new_folder):
                imapObj.create_folder(new_folder)
            for keyword in search_keywords:
                self.__move_emails(imapObj, new_folder, keyword)


    def __move_emails(self, imapObj, new_folder, search):
        '''
            imapObj: imapClient instance
            new_folder: target folder to move emails
            search: search keyword to filter emails
        '''
        ids = imapObj.gmail_search(search)
        if len(ids) > 0:
            print(f'Moving {len(ids)} emails related to {search}')
            imapObj.move(messages=ids, folder=new_folder)
            print(f'All emails moved to {new_folder} successfully')


if __name__ == '__main__':
    client = IMAPClient(email=os.environ.get('EMAIL'), password=os.environ.get('EMAIL_PWD'), imap_server="imap.gmail.com")
    client.organize_emails(old_folder='INBOX', new_folder='Git Related', search_keywords=['github', 'gitlab'])
    client.organize_emails(old_folder='INBOX', new_folder='Internship Related', search_keywords=['internship', 'job fair'])
    client.organize_emails(old_folder='INBOX', new_folder='ATH Móvil', search_keywords=['ath móvil'])
