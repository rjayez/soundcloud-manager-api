from flask import Flask, jsonify, request
from flask_cors import CORS
import SoundcloudPlaylistCreator
import SoundcloudService
from SoundcloudService import client

app = Flask(__name__)
cors = CORS(app, resources={
    r"/playlists/*": {"origins": ["http://localhost:1234", "https://soundcloud-manager.netlify.app"]}})


@app.route('/')
def index():
    return "<h2>C'est mon api !</h2"


# @app.route('/me')
def me():
    values = client.get('/me')
    print(values)
    return jsonify(values)
    # return Flask.make_response("Success",)


@app.route('/playlists')
def getPlaylist():
    playlist_data = SoundcloudService.getPlaylist()
    return jsonify(playlist_data)


@app.route('/playlists/weekly/<int:week_number>', methods=['POST'])
def createWeeklyPlaylist(week_number):

    return SoundcloudPlaylistCreator.createPlaylist(week_number, request.args.get("year"))


@app.route('/test')
def test():
    # return SoundcloudService.testPlaylist()
    return ""


if __name__ == '__main__':
    app.run(debug=True, port=5000)
