from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates') # objeto da classe flask que será a main

# config persitencia de dados sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.sqlite3'
db = SQLAlchemy(app)

class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    artist = db.Column(db.String(150), nullable=False)
    link = db.Column(db.String(350), nullable=False)
    
    def __init__(self, name, artist, link):
        self.name = name
        self.artist = artist
        self.link = link
    
    
    
@app.route('/') # rota (endpoints do site)
def index(): # a função da rota
    musics = Music.query.all()
    return render_template('index.html', musics=musics) # renderizando o template


@app.route('/newmusic', methods=['POST', 'GET'])
def newmusic():
    # verificando o método que chega
    if request.method == 'POST':
        # recebdo os dados do form
        music = Music(
            request.form['name'],
            request.form['artist'],
            request.form['link']
           
        )
        
        db.session.add(music) # adicionando ao banco
        db.session.commit()
        return redirect('/#Playlist')
    return render_template('newmusic.html')



@app.route('/editmusic/<id>', methods=['POST', 'GET'])
def editmusic(id):
    music = Music.query.get(id)
    if request.method == 'POST':
        music.name = request.form['name']
        music.artist = request.form['artist']
        music.link = request.form['link']
        
        # adicionando ao banco
        db.session.commit()
        return redirect('/#Playlist')
    return render_template('editmusic.html', music=music)


@app.route('/deletemusic/<id>')
def deletemusic(id):
    music = Music.query.get(id)
    db.session.delete(music)
    db.session.commit()
        


# teste de chamada para rodar a função main app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=False) # debbug para desenvolvimento
