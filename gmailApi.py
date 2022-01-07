from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from bs4 import BeautifulSoup
import base64
from SpotifyManager import SpotifyManager

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
sp = SpotifyManager()

def getMails():
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
        #for message in messages:
        #with messages[0] as message:
        message = messages[0]
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        content = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
        #subject = next(obj for obj in msg['payload']['headers'] if obj['name'] == 'Subject')
        #messageSubject = ''
        #if type(subject) == dict:
        #    messageSubject = subject['value']
        #with open(f"message{fileIdx}.htm", 'w') as f:
        #    f.write(content)
        scrapeMail(content)
        fileIdx = fileIdx + 1

def scrapeMail(mailContent):
    soup = BeautifulSoup(mailContent, 'html.parser')
    #FIND ALL THE ITEMS IN THE PAGE WITH A CLASS ATTRIBUTE OF 'TEXT'
    #AND STORE THE LIST AS A VARIABLE
    suggestions = soup.findAll('table', attrs={'class':'j-product'})
    for suggest in suggestions:
        titleDiv = suggest.find('div', attrs={'class', 'j-product-title'})
        artistDiv = suggest.find('div', attrs={'class', 'j-product-artist'})
        if(titleDiv is None or artistDiv is None): continue
        title = titleDiv.text
        artist = artistDiv.text
        res = sp.seach_album(artist, title)
        if not res: continue
        print(f"{artist} - {title}: " + res['external_urls']['spotify'])

        #print(f"{artist} - {title}")

    return

def main():
    getMails()

if __name__ == '__main__':
    main()
