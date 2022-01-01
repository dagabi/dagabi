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
    results = service.users().messages().list(userId='me',labelIds = ['INBOX'], q="FROM:subscriptions@lists.juno.co.uk").execute()
    messages = results.get('messages', [])
    

    if not messages:
        print( "No messages found.")
    else:
        print("Message snippets:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print(base64.b64decode(msg['payload']['body']['data'].encode('utf8')).decode('utf8'))

if __name__ == '__main__':
    main()
