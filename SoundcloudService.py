import soundcloud
from Config import config
import os

client_id = os.environ['SOUNDCLOUD_CLIENT_ID']
client_secret = os.environ['SOUNDCLOUD_CLIENT_SECRET']
username = os.environ['SOUNDCLOUD_USERNAME']
password = os.environ['SOUNDCLOUD_PASSWORD']

client = None


# client = soundcloud.Client(client_id=client_id,
#                            client_secret=client_secret,
#                            username=username,
#                            password=password)


def get_client():
    if client is not None:
        return client
    else:
        return load_client()


def load_client():
    global client
    client = soundcloud.Client(client_id=client_id,
                               client_secret=client_secret,
                               username=username,
                               password=password)
    return client


def getPlaylist():
    playlists = get_client().get('me/playlists')
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
    response = get_client().delete('/playlists/' + str(playlistId))
    print(response)


def testPlaylist():
    activities = get_client().get('/me/activities')
    print(activities)
    return ''
