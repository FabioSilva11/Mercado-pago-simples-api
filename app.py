from flask import Flask, request, jsonify
import mercadopago

app = Flask(__name__)

# Token de acesso do Mercado Pago
TOKEN_MERCADOPAGO = "SEU-ID-DO-MERCADO-PAGO"  # Substitua pelo seu token do Mercado Pago

sdk = mercadopago.SDK(TOKEN_MERCADOPAGO)

# Função para obter o status de um pagamento no Mercado Pago
def get_payment_status(payment_id):
    result = sdk.payment().get(payment_id)
    data = result["response"]["status"]
    return data

# Rota para criar um pagamento
@app.route('/')
def homepage():
    # Obter parâmetros da URL
    valor_da_transacao = request.args.get('valor')
    descricao = request.args.get('descricao')
    destinatario = request.args.get('destinatario')

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

    # Cria o pagamento usando o SDK do Mercado Pago
    result = sdk.payment().create(data)

    # Processa a resposta do Mercado Pago
    if result["status"] == 201:
        id_mercado_pago = result["response"]["id"]
        qr_code_base64 = result["response"]["point_of_interaction"]["transaction_data"]["qr_code_base64"]
        qr_code_text = result["response"]["point_of_interaction"]["transaction_data"]["qr_code"]

        # Constrói a resposta JSON
        resposta_json = {
            'mensagem': 'Pagamento criado com sucesso',
            'id_mercado_pago': id_mercado_pago,
            'qr_code_base64': qr_code_base64,
            'qr_code_text': qr_code_text
        }

        return jsonify(resposta_json)
    else:
        return jsonify(result)

# Rota para obter o status de um pagamento
@app.route('/status')
def payment_status():
    # Obter o parâmetro 'codigo' da URL
    codigo = request.args.get('codigo')

    # Verificar se o campo 'codigo' está presente
    if not codigo:
        return jsonify({'erro': 'Campo obrigatório ausente'})

    # Obter o status do pagamento usando a função get_payment_status
    status = get_payment_status(codigo)

    if status:
        # Construir a resposta com base no status do pagamento
        status_pagamento = {
            'status_pagamento': status
        }

        return jsonify(status_pagamento)
    else:
        return jsonify({'erro': 'Erro ao obter informações do pagamento'})

if __name__ == "__main__":
    app.run(debug=True)
            
