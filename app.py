from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Token de acesso do Mercado Pago
access_token = "SUA-API-KEY-DO-MERCADO-PAGO"

# Rota padrão
@app.route('/')
def homepage():
    # Obter parâmetros da URL
    valor_da_transacao = request.args.get('valor')
    descricao = request.args.get('descricao')
    destinatario = request.args.get('destinatario')

# Verificar se os parâmetros obrigatórios estão presentes
    if not valor_da_transacao or not descricao or not destinatario:
        return jsonify({'erro': 'Parâmetros obrigatórios ausentes'})

    # Verificar se o valor da transação é numérico e maior que zero
    try:
        valor_da_transacao = float(valor_da_transacao)
        if valor_da_transacao <= 0:
            raise ValueError
    except ValueError:
        return jsonify({'erro': 'O valor da transação deve ser numérico e maior que zero'})

    # Verificar se a descrição não está vazia
    if not descricao:
        return jsonify({'erro': 'A descrição não pode estar vazia'})

    # Verificar se o destinatário é um e-mail válido
    if '@' not in destinatario or '.' not in destinatario:
        return jsonify({'erro': 'O destinatário deve ser um endereço de e-mail válido'})

    # Verificar se o valor da transação é numérico
    try:
        valor_da_transacao = float(valor_da_transacao)
    except ValueError:
        return jsonify({'erro': 'O valor da transação deve ser numérico'})

    # URL da API do MercadoPago
    url = "https://api.mercadopago.com/v1/payments"

    # Prepara os dados JSON para a solicitação de pagamento
    data = {
        "transaction_amount": float(valor_da_transacao),
        "description": descricao,
        "payment_method_id": "pix",
        "payer": {
            "email": destinatario,
            "first_name": destinatario  # Substitua pelo nome do pagador
        }
    }

    # Configura os cabeçalhos da solicitação
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }

    # Faz a solicitação POST para a API do MercadoPago
    response = requests.post(url, json=data, headers=headers)

    # Processa a resposta da API do MercadoPago
    if response.status_code == 201:
        resposta_mercado_pago = response.json()
        id = resposta_mercado_pago.get('id')
        qr_code_base64 = resposta_mercado_pago.get('point_of_interaction', {}).get('transaction_data', {}).get('qr_code_base64')
        qr_code_text = resposta_mercado_pago.get('point_of_interaction', {}).get('transaction_data', {}).get('qr_code')

        # Adicione as informações processadas à resposta da sua API
        resposta_json = {
            'mensagem': 'Pagamento criado com sucesso',
            'id_mercado_pago': id,
            'qr_code_base64': qr_code_base64,
            'qr_code_text': qr_code_text
        }

        return jsonify(resposta_json)
    else:
        return jsonify(response.json())

# Rota para status de pagamento
@app.route('/status')
def payment():
    # Obter o parâmetro 'codigo' da URL
    codigo = request.args.get('codigo')

    # Verificar se o campo 'codigo' está presente
    if not codigo:
        return jsonify({'erro': 'Campo obrigatório ausente'})

    # URL da API do Mercado Pago para obter informações do pagamento
    url = f"https://api.mercadopago.com/v1/payments/{codigo}"

    # Configura os cabeçalhos da solicitação
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    # Faz a solicitação GET para a API do Mercado Pago
    response = requests.get(url, headers=headers)

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Processa a resposta da API do Mercado Pago
        response_json = response.json()
        status_pagamento = response_json.get('status')
        return jsonify({'status_pagamento': status_pagamento})
    else:
        return jsonify({'erro': 'Erro ao obter informações do pagamento'})

# Rodar a nossa API
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
