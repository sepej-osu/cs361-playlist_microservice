from flask import Flask
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def create_db():
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS playlist(videoId TEXT, played INTEGER DEFAULT 0)")
    con.close()

# playlist add
# TODO: change to a PUT
@app.route("/add/<string:song>")
def add_to_playlist(song):
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    cur.execute("INSERT INTO playlist VALUES (?, ?)", (song, 0,))
    con.commit()
    con.close()
    return song + " added"

# playlist remove
@app.route("/remove/<string:song>")
def remove_from_playlist(song):
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    cur = cur.execute('DELETE FROM playlist WHERE videoId = ?;', (song,))
    con.commit()
    con.close()
    return song + " removed"

@app.route("/current_song")
def current_song():
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    cur.execute('SELECT videoId FROM playlist WHERE played = 0 LIMIT 1;')
    song = cur.fetchone()
    con.close()
    print(song)
    if song is None:
        return "None"
    else:
        return song[0]
    
@app.route("/next_songs")
def next_songs():
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    cur.execute('SELECT videoId FROM playlist WHERE played = 0 LIMIT 1 OFFSET 1;')
    songs = cur.fetchall()
    if not songs:
        cur.execute('SELECT videoId FROM playlist LIMIT 1;')
        song = cur.fetchone()
        con.close()
        if song is None:
            return "None"
        else:
            return song[0]
    else:
        con.close()
        return ', '.join([song[0] for song in songs])

@app.route("/mark_song_played/<string:song>")
def mark_song_played(song):
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    cur.execute('UPDATE playlist SET played = 1 WHERE videoId = ?;', (song,))
    con.commit()
    con.close()
    return song + " played"

@app.route("/reset_playlist")
def reset_playlist():
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    cur.execute("UPDATE playlist SET played = 0")
    con.commit()
    con.close()
    return "All songs reset to unplayed"

@app.route("/seed")
def seed():
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    cur.execute("INSERT INTO playlist VALUES (?, ?)", ('9nEp5px9LyQ', 0,))
    cur.execute("INSERT INTO playlist VALUES (?, ?)", ('gPwGcy8mBl4', 0,))
    cur.execute("INSERT INTO playlist VALUES (?, ?)", ('2tq1iv6GKys', 0,))
    cur.execute("INSERT INTO playlist VALUES (?, ?)", ('GhqubYAM2W4', 0,))
    cur.execute("INSERT INTO playlist VALUES (?, ?)", ('tArdmbr_znI', 0,))
    cur.execute("INSERT INTO playlist VALUES (?, ?)", ('I2sS6Y_uh4s', 0,))
    con.commit()
    con.close()
    return "seeds added"

if __name__ == '__main__':
    create_db()
    app.run(debug=False, port=5002)