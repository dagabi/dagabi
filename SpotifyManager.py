import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyManager:
    def __init__(self):
        _clientId = '27e67fa550724feea9966aadf22e1e48'
        _clientSecret = 'f807223c41114ee59353c7dda031a15d'
        self._sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=_clientId, client_secret=_clientSecret))
    
    def seach_album(self, artist, album):
        _sp = self._sp
        res = _sp.search(f"{album} artist:{artist}", type='album')
        if not res:
            return None
        
        result = res['albums']['items']
        if(not result): return None

        result = result[0]

        if not result: return None

        return result

        #for idx, track in enumerate(res['albums']['items']):
        #    print(idx, track['external_urls']['spotify'])
        #return

#tester
if(__name__ == '__main__'):
    sp = SpotifyManager()
    sp.seach_album("Prince", "Purple Rain")
                                                        