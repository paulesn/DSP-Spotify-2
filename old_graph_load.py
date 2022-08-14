with alive_bar(artists.shape[0] * 2) as bar:
    for (index, artist_row) in artists.iterrows():
        bar()  # update progress bar
        graph.add_node(artist_row['name'])  # create all artists as nodes

    i = 0
    max = str(artists.shape[0])

    for (index, artist_row) in artists.iterrows():
        i += 1
        print(f"execution {str(i)} of {max}")
        bar()  # update progress bar

        artist_id = artist_row['id']
        all_songs_of_this_artist = at[at['artist_id'] == artist_id]  # create a list with all songs of this artist
        print(f"songs of {artist_row.name}: {all_songs_of_this_artist.shape[0]}")

        for (index, track_row) in all_songs_of_this_artist.iterrows():
            print(f"current track: {track_row.track_id}")
            track_id = track_row['track_id']
            all_artists_of_song = at[at['track_id'] == track_id]  # create a list with all artists of this song

            print(f"cooperators of {track_row.track_id}: {all_artists_of_song.shape[0]}")

            for (index, cooperator) in all_artists_of_song.iterrows():
                #print("cooperator " + str(cooperator))
                #print("artist_id " + str(artist_id))
                if cooperator.artist_id == artist_id:
                    continue
                graph.add_edge(artist_id, cooperator.artist_id)