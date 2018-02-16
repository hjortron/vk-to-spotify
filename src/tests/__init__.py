import json

import spotipy
import spotipy.util as util


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
                                    track['name']))


if __name__ == '__main__':
    with open("playlist.json", 'r') as json_file:
        datastore = json.load(json_file)
        print(datastore)
    # username = 'a_hjortron'
    # scope = 'user-library-read'
    # util.prompt_for_user_token(
    #     username, scope, client_id='d7ac3652ccaf4584a09a27757e2f6820',
    #     client_secret='fa6314d67ecb4acaa8c0837f17d0efb9', redirect_uri='127.0.0.1')
    # token = util.prompt_for_user_token(username)
    #
    # if token:
    #     sp = spotipy.Spotify(auth=token)
    #     playlists = sp.user_playlists(username)
    #     for playlist in playlists['items']:
    #         if playlist['owner']['id'] == username:
    #             print(playlist['name'])
    #             print('  total tracks', playlist['tracks']['total'])
    #             results = sp.user_playlist(username, playlist['id'],
    #                                        fields="tracks,next")
    #             tracks = results['tracks']
    #             show_tracks(tracks)
    #             while tracks['next']:
    #                 tracks = sp.next(tracks)
    #                 show_tracks(tracks)
    # else:
    #     print("Can't get token for", username)
