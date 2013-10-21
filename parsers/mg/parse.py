# -*- coding: utf-8 -*-
import csvkit
from collections import defaultdict
import json

# Estrutura
# Despesa (1) -> Função de Governo (2) -> Unidade Orçamentaria (3) ->
# Projeto (4) -> Elemento (5) -> Item (6)-> Credor (7)

dados = csvkit.CSVKitDictReader(open("raw/despesa_dados.csv", 'r'), encoding='iso-8859-1');
meta = csvkit.CSVKitDictReader(open("raw/despesa_metadados.csv", 'r'), encoding='iso-8859-1');
meses = ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ']

def nested_defaultdict():
    return defaultdict(dict)

def parsemeta(niveis):
    meta_dict = {}
    for n in niveis:
        meta_dict[n] = { 'nivel' : n, 'cat' : {} }
    for i in meta:
        if i['NR_NIVEL'] in niveis:
            meta_dict[i['NR_NIVEL']]['cat'][i['CD_METADADOS']] = { 'nome' : i['DS_NOME_ESTRUTURA'], 'dados' : [], 'mes' : {} }
    return meta_dict

def extract(meta_dict):
    for i in dados:
        for m in meta_dict:
            if i['CD_METADADOS'] in meta_dict[m]['cat']:
                mes = meses[int(i['CD_MENSAL'])-1]
                #meta_dict[i['CD_METADADOS']]['dados'].append(i)
                if mes not in meta_dict[m]['cat'][i['CD_METADADOS']]['mes']:
                    meta_dict[m]['cat'][i['CD_METADADOS']]['mes'][mes] = { 'total' : float(i['NR_VALOR2']) }
                else:
                    meta_dict[m]['cat'][i['CD_METADADOS']]['mes'][mes]['total'] += float(i['NR_VALOR2'])
    return meta_dict

def reorder(meta_dict):
    rd = defaultdict(nested_defaultdict)
    for nivel in meta_dict:
        for cat in meta_dict[nivel]['cat']:
            for mes in meta_dict[nivel]['cat'][cat]['mes']:
                rd[mes][nivel][meta_dict[nivel]['cat'][cat]['nome'].strip()] = meta_dict[nivel]['cat'][cat]['mes'][mes]
    return rd

def consistencia():
    for i in meta:
        if i['CD_METADADOS'].index(i['CD_PAI']) != 0:
            print 'Duh!'


print 'Parsing...'
a = parsemeta(['1','2','3'])
print 'Extracting...'
a = extract(a)
print 'Reordering...'
b = reorder(a)
print 'Saving...'
c = json.dumps(b, indent=4)
d = open('resultado.json', 'w')
d.write(c)
d.close()