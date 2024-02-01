## Mercado-pago-simples-api

Esta aplicação foi criada com o objetivo de facilitar a vida de quem está aprendendo a programar, especialmente para aquelas pessoas que codificam pelo celular em muitos softwares. Muitas vezes, é necessário inserir as credenciais diretamente no aplicativo, o que pode ser perigoso. Portanto, esta API resolve esse problema para você.

## Instalação

Certifique-se de ter o Python e o pip instalados em seu sistema. Execute o seguinte comando para instalar as dependências necessárias:

```bash
pip install flask requests
```

## Configuração

1. Abra o arquivo `app.py` em seu editor de texto preferido.

2. Substitua o valor da variável `access_token` pelo seu Token de Acesso do MercadoPago. Você pode obtê-lo no [painel de desenvolvedor do MercadoPago](https://www.mercadopago.com/developers/pt-br/my-account/).

## Utilização

### Rota Padrão

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
  "qr_code_text": "codigo_copia_e_cola"
}
```

Exemplo de resposta de falha:

```json
{
  "status": "falha",
  "mensagem": "Falha ao processar o pagamento. Verifique os parâmetros fornecidos."
}
```

### Rota de Status de Pagamento

Para verificar o status de um pagamento, acesse a rota de status usando o conteúdo da chave `id_mercado_pago` gerada ao criar um pagamento:

```bash
GET /status?codigo=id_mercado_pago
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

### Verificações Adicionais

Além das verificações básicas, o código inclui algumas verificações adicionais para garantir a integridade e segurança das transações:

1. **Valor da Transação:**
   - Verifica se o valor da transação é numérico e maior que zero.

2. **Descrição:**
   - Garante que a descrição não esteja vazia.

3. **Destinatário (E-mail):**
   - Verifica se o destinatário é um endereço de e-mail válido.

4. **Outras Verificações:**
   - Inclui verificações adicionais para assegurar o correto processamento das transações.

Estas verificações são implementadas para fornecer uma experiência segura e eficaz ao utilizar a API.

## Executando a API

Certifique-se de executar a aplicação utilizando o comando:

```bash
python app.py
```

A API estará disponível em http://localhost:5000/.
``` 

Este README foi atualizado com as informações adicionais sobre as verificações implementadas no código para garantir um funcionamento seguro e eficiente da API.
