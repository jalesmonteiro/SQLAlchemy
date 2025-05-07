from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, Usuario

engine = create_engine('sqlite:///exemplo.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route("/<int:pag>")
def inicio(pag):
    limite = 3
    qtd = session.query(Usuario).count()
    usuarios = session.query(Usuario).offset((pag-1)*limite).limit(limite).all()
    return render_template('index.html', pag=pag, limite=limite, qtd=qtd, usuarios=usuarios)

if __name__ == "__main__":
    app.run(debug=True)