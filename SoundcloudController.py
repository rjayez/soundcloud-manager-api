from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import SoundcloudPlaylistCreator
import SoundcloudService

# from SoundcloudService import client

app = Flask(__name__)
cors = CORS(app, resources={
    r"/playlists/*": {"origins": ["http://localhost:3214", "https://soundcloud-manager.netlify.app"]},
    r"/authentication/*": {"origins": ["http://localhost:3214", "https://soundcloud-manager.netlify.app"]},
    r"/authorization/*": {"origins": ["http://localhost:3214", "https://soundcloud-manager.netlify.app"]},
    r"/check-authent/*": {"origins": ["http://localhost:3214", "https://soundcloud-manager.netlify.app"]},
})


@app.route('/')
def index():
    return "<h2>C'est mon api !</h2"


@app.route('/me')
def me():
    code = request.args.get("code")
    SoundcloudService.connnection(code)
    values = SoundcloudService.get_client().get("/me")
    print(values.obj)
    return jsonify(values.obj)
    # return Flask.make_response("Success",)


@app.route('/check-authent')
def check_authentifcation():
    try:
        SoundcloudService.get_client().get("/me")
        return {"isAuthenticated": True}
    except Exception as ex:
        return {"isAuthenticated": False}


@app.route('/authorization')
def authorization():
    return SoundcloudService.get_client().authorize_url()


@app.route('/authentication')
def authentication():
    code = request.args.get("code")
    if code is None:
        abort(400, "code request parameters is required")
        # raise Exception("code request parameters is required")

    SoundcloudService.connnection(code)
    return "Success authentication"


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
    return "Coucou"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
