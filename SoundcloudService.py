import soundcloud
from Config import config
import os

client_id = os.environ['SOUNDCLOUD_CLIENT_ID']
client_secret = os.environ['SOUNDCLOUD_CLIENT_SECRET']
username = os.environ['SOUNDCLOUD_USERNAME']
password = os.environ['SOUNDCLOUD_PASSWORD']

client = None


def get_client():
    if client is not None:
        return client
    else:
        return load_client()


def load_client():
    global client
    client = soundcloud.Client(client_id=client_id,
                               grant_type="authorization_code",
                               redirect_uri="https://soundcloud-manager.netlify.app")

    print(client.authorize_url())

    return client

    # client = soundcloud.Client(client_id=client_id,
    #                            grant_type="authorization_code",
    #                            redirect_uri="https://soundcloud-manager.netlify.app",
    #                            code=code)

def connnection(code):
    global client
    # client = soundcloud.Client()
    # client.exchange_token(code)
    client = soundcloud.Client(client_id=client_id,
                               client_secret=client_secret,
                               redirect_uri="https://soundcloud-manager.netlify.app")

    print(client.authorize_url())

    access_token, expires, scope, refresh_token = client.exchange_token(code)
    print(access_token)
    print(expires)
    print(scope)
    print(refresh_token)

    return access_token


def get_for_path(path):
    get_client().get(path)

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


def get_activities(limit):
    return get_client().get('/me/activities', limit=limit)


def get_activities_with_cursor(limit, cursor):
    return get_client().get('/me/activities', limit=limit, cursor=cursor)


def post_playlist(list_id, numero_semaine, titre):
    if len(list_id) > 0:
        get_client().post('/playlists', playlist={
            'title': '%s %s' % (titre, numero_semaine),
            'tracks': list_id,
            'sharing': 'private'})
    else:
        print("La liste \"%s\" est vide" % titre)


def testPlaylist():
    activities = get_client().get('/me/activities')
    print(activities)
    return ''
