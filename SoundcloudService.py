import soundcloud
from Config import config
import os

client_id = os.environ['SOUNDCLOUD_CLIENT_ID']
client_secret = os.environ['SOUNDCLOUD_CLIENT_SECRET']
username = os.environ['SOUNDCLOUD_USERNAME']
password = os.environ['SOUNDCLOUD_PASSWORD']

client = soundcloud.Client(client_id=client_id,
                           client_secret=client_secret,
                           username=username,
                           password=password)


def getPlaylist():
    playlists = client.get('me/playlists')
    data = []
    for playlist in playlists:
        data.append(getPlaylistData(playlist))

    return data


def getPlaylistData(playlist):
    data = {"titre": playlist.title,
            "url_image": playlist.artwork_url,
            "uri": playlist.uri,
            "nb": len(playlist.tracks),
            "key": playlist.id
            }
    return data


def deletePlaylist(playlistId):
    response = client.delete('/playlists/' + str(playlistId))
    print(response)


def testPlaylist():
    activities = client.get('/me/activities')
    print(activities)
    return ''
