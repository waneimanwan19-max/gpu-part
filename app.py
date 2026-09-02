from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT * FROM gpu;"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("home.html", results=results)


@app.route('/gpu/<int:gpu_id>')
def gpu_page(gpu_id):
    db = get_db()
    cursor = db.cursor()
    sql = "JOIN performance ON performance.gpu_id=gpu.gpu_id JOIN game ON performance.game_id=game.game_id WHERE gpu.gpu_id = ?;"
    cursor.execute(sql)
    results = cursor.fetchall()
    return  render_template("gpu.html", results=results) 


    
  
 
if __name__ == "__main__": 
    app.run(debug=True)