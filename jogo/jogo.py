import Kwargs as Kwargs
from flask import Flask, render_template, session, url_for, redirect, flash, request
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.testing import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import*

SECRET_KEY = 'projeto2'

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jogo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Status(db.Model):
    __tablename__ = "Status"
    idStatus = db.Column(db.Integer(), primary_key=True)
    vidaMax = db.Column(db.Integer())
    vidaAtual = db.Column(db.Integer())
    forca = db.Column(db.Integer())
    resistencia = db.Column(db.Integer())
    inteligencia = db.Column(db.Integer())
    velocidade = db.Column(db.Integer())
    iniciativa = db.Column(db.Integer())
    sorte = db.Column(db.Integer())
    tamInventario = db.Column(db.Integer())
    def __init__(self, **kwargs):
        super().__init__(**Kwargs)
        self.vidaMax = kwargs.pop('vidaMax')
        self.vidaAtual = kwargs.pop('vidaAtual')
        self.forca = kwargs.pop('forca')
        self.resistencia = kwargs.pop('resistencia')
        self.inteligencia = kwargs.pop('inteligencia')
        self.velocidade = kwargs.pop('velocidade')
        self.iniciativa = kwargs.pop('iniciativa')
        self.sorte = kwargs.pop('sorte')
        self.tamInventario = kwargs.pop('tamInventario')

class Classe(db.Model):
    idClasse = db.Column(db.Integer(), primary_key=True)
    nomeClasse = db.Column(db.String())
    idStatus = db.Column(db.Integer(), ForeignKey('Status.idStatus'))
    descricao = db.Column(db.String())
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nomeClasse = kwargs.pop('nomeClasse')
        self.idStatus = kwargs.pop('idStatus')
        self.descricao = kwargs.pop('descricao')

class Raca(db.Model):
    idRaca = db.Column(db.Integer(), primary_key=True)
    nomeRaca = db.Column(db.String())
    idStatus = db.Column(db.Integer(), ForeignKey('Status.idStatus'))
    descricao = db.Column(db.String())
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nomeRaca = kwargs.pop('nomeRaca')
        self.idStatus = kwargs.pop('idStatus')
        self.descricao = kwargs.pop('descricao')

class Personagem(db.Model):


class Pessoa(db.Model):
    __tablename__ = "Pessoa"
    login = db.Column(db.String(), primary_key=True)
    nomePessoa = db.Column(db.String())
    tipo = db.Column(db.Integer())
    senha = db.Column(db.String(128))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login = kwargs.pop('login')
        self.nomePessoa = kwargs.pop('nomePessoa')
        self.tipo = kwargs.pop('tipo')
        self.senha = generate_password_hash(kwargs.pop('senha'))

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

    def __repr__(self):
        return '<User {}>'.format(self.login)

class Eleicao(db.Model):
    __tablename__ = "Eleicao"
    idEleicao = db.Column(db.Integer, primary_key=True)
    eleicao = db.Column(db.String())
    dataInicio = db.Column(db.String())
    dataFinal = db.Column(db.String())
    statusEleicao = db.Column(db.Integer())
    apuracao = db.Column(db.Integer())
    login = db.Column(db.String(),ForeignKey('Pessoa.login'))
    pessoa = relationship(Pessoa)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.eleicao =  kwargs.pop('eleicao')
        self.dataInicio = (str(datetime.now())).split('.')[0]
        self.dataFinal = '0'
        self.statusEleicao = 0
        self.apuracao = 0
        self.login =  kwargs.pop('login')

class Eleitor(db.Model):
    __tablename__ = "Eleitor"
    statusVoto = db.Column(db.Integer())
    idEleicao = db.Column(db.Integer(), ForeignKey('Eleicao.idEleicao'), primary_key=True)
    eleicao = relationship(Eleicao)
    login = db.Column(db.String(),ForeignKey('Pessoa.login'),primary_key=True)
    pessoa = relationship(Pessoa)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.statusVoto = 0
        self.idEleicao =  kwargs.pop('idEleicao')
        self.login =  kwargs.pop('login')

class Pergunta(db.Model):
    __tablename__ = "Pergunta"
    idPergunta = db.Column(db.Integer, primary_key=True)
    pergunta = db.Column(db.String())
    numMinResposta = db.Column(db.Integer())
    numMaxResposta = db.Column(db.Integer())
    idEleicao = db.Column(db.Integer(), ForeignKey('Eleicao.idEleicao'))
    eleicao = relationship(Eleicao)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pergunta = kwargs.pop('pergunta')
        self.numMinResposta = kwargs.pop('numMinResposta')
        self.numMaxResposta = kwargs.pop('numMaxResposta')
        self.idEleicao = kwargs.pop('idEleicao')

class Resposta(db.Model):
    __tablename__ = "Resposta"
    idResposta = db.Column(db.Integer, primary_key=True)
    resposta = db.Column(db.String())
    contadorResposta = db.Column(db.Integer())
    idPergunta = db.Column(db.Integer(), ForeignKey('Pergunta.idPergunta'), primary_key=True)
    perg = relationship(Pergunta)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resposta = kwargs.pop('resposta')
        self.contadorResposta = 0
        self.idPergunta = kwargs.pop('idPergunta')