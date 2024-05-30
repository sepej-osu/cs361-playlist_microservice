from flask import Flask
import sqlite3

app = Flask(__name__)

def create_db():
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS playlist(videoId)")
    con.close()

# playlist add
# TODO: change to a PUT
@app.route("/add/<string:song>")
def add_to_playlist(song):
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    cur.execute("INSERT INTO playlist VALUES (?)", (song,))
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

if __name__ == '__main__':
    create_db()
    app.run(debug=True)