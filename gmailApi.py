from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
   
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX'], q="FROM:subscriptions@lists.juno.co.uk after:2021/12/25").execute()
    messages = results.get('messages', [])
    
    fileIdx = 0

    if not messages:
        print( "No messages found .")
    else:
        print("Message snippets:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            content = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
            subject = next(obj for obj in msg['payload']['headers'] if obj['name'] == 'Subject')
            messageSubject = ''
            if type(subject) == dict:
                messageSubject = subject['value']
            with open(f"message{fileIdx}.htm", 'w') as f:
                f.write(content)
            fileIdx = fileIdx + 1

if __name__ == '__main__':
    main()
