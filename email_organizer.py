import imapclient
import os

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('EMAIL_PASSWORD')


def organize_emails(old_folder, new_folder, search_keywords):
    '''
        old_folder: folder to retrieve emails
        new_folder: target folder to move emails
        search_keywords: iterable of keywords for filtering emails
    '''
    with imapclient.IMAPClient('imap.gmail.com', ssl=True) as imapObj:
        imapObj.login(EMAIL, PASSWORD)
        imapObj.select_folder(old_folder, readonly=True)
        if not imapObj.folder_exists(new_folder):
            imapObj.create_folder(new_folder)
        for keyword in search_keywords:
            move_emails(imapObj, new_folder, keyword)


def move_emails(imapObj, new_folder, search):
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
  organize_emails(old_folder='INBOX', new_folder='Git Related', search_keywords=['github', 'gitlab'])
  organize_emails(old_folder='INBOX', new_folder='Internship Related', search_keywords=['internship', 'job fair'])
  organize_emails(old_folder='INBOX', new_folder='ATH Móvil', search_keywords=['ath móvil'])
