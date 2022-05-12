from flask import Flask, Response, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

app = Flask(__name__, template_folder='templates')

#CONFIGURAÇÔES DO BANCO
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/barbearia-dados'

db = SQLAlchemy(app)



#======================================
# CRIANDO MAPEAMENTO COM  AS TABELAS NO BANCO MYSQL 
class Serviços(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(50))
    tipo = db.Column(db.String(100))
    preço = db.Column(db.String(100))

    #================================
	#TESTANDO COM UM METODO DIFERENTE
    def __init__(self, nome, tipo, preço):
        self.nome = nome
        self.tipo = tipo
        self.preço = preço
        

#CRIANDO ROTA PARA templates html

@app.route('/')
def index():
    serviços = Serviços.query.all()
    return render_template( 'index.html', serviços=serviços)



#CRIANDO ROTA  PARA abrir empresa

@app.route('/cadastrar', methods=['GET','POST'])
def cadstrar():
    if request.method == 'POST':
        serviços = Serviços(request.form['nome'], request.form['tipo'], request.form['preço'])
        db.session.add(serviços)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastrarServico.html')


#==============================
#CRIANDO ROTA PARA VOLTAR AO ('/')

@app.route('/')
def voltar():
    return render_template('index.html')


#============================
#CRIANDO ROTA  PARA baixar empresa

@app.route('/excluir/<int:id>')
def excluir(id):
    serviços = Serviços.query.get(id)
    db.session.delete(serviços)
    db.session.commit()
    return redirect(url_for('index'))
    

#============================
#CRIANDO ROTA  PARA editar empresa

@app.route('/atualizar/<int:id>' , methods=['GET', 'POST'])
def atualizar(id):
    serviços = Serviços.query.get(id)
    if request.method == 'POST':
        serviços.nome  = request.form['nome']
        serviços.tipo  = request.form['tipo']
        serviços.preço  = request.form['preço']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('atualizarServico.html', serviços=serviços)


#========================================
#rodar servidor
if __name__ == '__main__':
	app.run(debug=True, port=3000)