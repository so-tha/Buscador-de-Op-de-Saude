from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import chardet

app = Flask(__name__)
CORS(app)

def detectar_codificacao(arquivo):
    with open(arquivo, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def carregar_operadoras():
    caminho_csv = '/home/yaythai/Documentos/teste-nivelamento/interface/back-end/assets/Relatorio_cadop.csv'   
    try:
        encoding = detectar_codificacao(caminho_csv)
        dataframe = pd.read_csv(caminho_csv, sep=';', encoding=encoding)
        dataframe.columns = [col.lower().replace(' ', '_') for col in dataframe.columns]
        
        dataframe = dataframe.fillna('')

        for col in ['razao_social', 'nome_fantasia', 'modalidade', 'cidade']:
            dataframe[col] = dataframe[col].astype(str).str.strip()

        return dataframe.to_dict(orient='records')
    
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return []

operadoras = carregar_operadoras()

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify({"results": []}), 200

    results = []
    for op in operadoras:
        score = 0
        razao_social = op.get('razao_social', '').lower()
        nome_fantasia = op.get('nome_fantasia', '').lower()
        registro_ans = str(op.get('registro_ans', '')).lower()
        cnpj = str(op.get('cnpj', '')).lower()
        modalidade = str(op.get('modalidade', '')).lower()
        cidade = str(op.get('cidade', '')).lower()
        uf = str(op.get('uf', '')).lower()

        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

        if query in razao_social:
            score += 3
        if query in nome_fantasia:
            score += 2
        if query in registro_ans:
            score += 4
        if query in cnpj_limpo:
            score += 4
        if query in modalidade:
            score += 1
        if query in cidade:
            score += 1
        if query in uf:
            score += 1
        if score > 0:
 
            formatted_cnpj = cnpj_limpo
            if len(cnpj_limpo) == 14:
                formatted_cnpj = f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"

            results.append({
                "id": registro_ans,
                "Razao_Social": razao_social.upper(),
                "Nome_Fantasia": nome_fantasia.title(),
                "Registro_ANS": registro_ans,
                "CNPJ": formatted_cnpj,
                "Modalidade": modalidade.title(),
                "Cidade": cidade.title(),
                "UF": uf.upper(),
                "Relevancia": score
            })

    results = sorted(results, key=lambda x: x['Relevancia'], reverse=True)
    return jsonify({"results": results[:20]})

if __name__ == '__main__':
    app.run(debug=True)
