# -*- coding: utf-8 -*-
import json, random
from flask import Flask, render_template

app = Flask(__name__)

meses = ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ']
START = chr(3) # Caracter ASCII que inicia o conteudo
END = '\n\n'

def thermalprint(texto):
    return START + texto + END

def simulate(texto):    
    return render_template('fake.html', texto=texto)

def formata(valor):
    val = " {0:.1f}".format(valor/100000000) + ' bilhoes'
    if valor < 100000000: 
        val = " {0:.1f}".format(valor/1000000) + ' milhoes'
    if valor < 1000000: 
        val = " {0:.1f}".format(valor/1000) + ' mil'
    return val

def extrato(mes):
    orca = json.loads(open('data/despesas_2012.json', 'r').read())
    total = 0.0;
    texto = START
    texto += '========== HACKATHON =========\n'
    texto += '        GOVERNO DE MINAS       \n'
    texto += '==== DESPESAS - '+meses[mes-1] +'/2012 ====\n'
    for i in orca[0]['cat']:
        full = 0
        texto += orca[0]['cat'][i]['nome'].strip()
        for g in orca[0]['cat'][i]['dados']:
            if g['CD_MENSAL'] == str(mes):
                valor = float(g['NR_VALOR'])
                val = formata(valor)
                texto += val
                full = 1
                total += valor
        if full != 1:
            texto += '  ---'
        texto += '\n'

    texto += '\n'
    texto += 'TOTAL:' + formata(total)
    texto += '\n========= HACKATHON =========\n'
    return texto

@app.route('/')
def index():
    return None

@app.route('/lipsum')
def lipsum():
    return  thermalprint('lorem ipsum sic dolor')

@app.route('/raw/<texto>')
@app.route('/raw/<texto>/<fake>')
def raw(texto='Hello World!', fake=False):
    if fake:
        return simulate(texto)
    return thermalprint(texto)

@app.route('/mg/despesas/<mes>')
@app.route('/mg/despesas/<mes>/<fake>')
def despesas(mes='RND', fake=False):
    if mes == 'RND':
        mes = meses[random.randint(0,11)]
    texto = extrato(meses.index(mes)+1)
    if fake:
        return simulate(texto)
    return thermalprint(texto)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')