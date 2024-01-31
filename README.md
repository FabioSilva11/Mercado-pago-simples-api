# Mercado-pago-simples-api
Essa app foi criada com o intuito de facilitar a vida de quem está aprendendo a programar agora especialmente para as pessoas que codificam pelo celular em muitos softwares é necessário colocar o as credenciais diretamente no aplicativo o que pode ser perigoso então essa pi resolve esse problema para você

Este é um guia completo para utilizar a API de Pagamentos MercadoPago. Siga as instruções abaixo para integração bem-sucedida.

### Instalação

Certifique-se de ter o Python e o pip instalados em seu sistema. Execute o seguinte comando para instalar as dependências necessárias:

```bash
pip install flask requests
```

### Configuração

1. Abra o arquivo `app.py` em seu editor de texto preferido.

2. Substitua o valor da variável `access_token` pelo seu Token de Acesso do MercadoPago. Você pode obter isso no [painel de desenvolvedor do MercadoPago](https://www.mercadopago.com/developers/pt-br/my-account/).

### Utilização

#### Rota Padrão

Para criar um pagamento, acesse a rota padrão:

```bash
GET /?valor=<valor>&descricao=<descricao>&destinatario=<destinatario>
```

- `valor`: Valor da transação (numérico).
- `descricao`: Descrição da transação.
- `destinatario`: E-mail do destinatário.

Exemplo:

```bash
GET /?valor=100&descricao=Compra%20Online&destinatario=destinatario@email.com
```

A resposta incluirá um QR Code e informações relevantes sobre a transação.

Exemplo de resposta bem-sucedida:

```json
{
  "mensagem": "Pagamento criado com sucesso",
  "id_mercado_pago": "123456789",
  "qr_code_base64": "base64_encoded_qr_code",
  "qr_code_text": "qr_code_text"
}
```

Exemplo de resposta de falha:

```json
{
  "status": "falha",
  "mensagem": "Falha ao processar o pagamento. Verifique os parâmetros fornecidos."
}
```

#### Rota de Status de Pagamento

Para verificar o status de um pagamento, acesse a rota de status use o conteúdo da chave id_mercado_pago gerada ao criar um pagamento:

```bash
GET /status?codigo= id_mercado_pago
```

- `codigo`: Código do pagamento.

Exemplo:

```bash
GET /status?codigo=123456789
```

A resposta incluirá o status atual do pagamento.

Exemplo de resposta bem-sucedida:

```json
{
  "status_pagamento": "aprovado"
}
```

Exemplo de resposta de erro:

```json
{
  "erro": "Erro ao obter informações do pagamento"
}
```

Certifique-se de adaptar as rotas conforme necessário para a integração bem-sucedida em seu aplicativo.
