
# Telegram Bot

Este projeto é um bot do Telegram desenvolvido com o objetivo de auxiliar no processo de aplicação da vaga para o time **FURIA**. A solução foi projetada para ser simples, eficiente e de alto desempenho.

## 🚀 Tecnologias e Ferramentas Utilizadas

### Linguagem
- **Python**: Escolhida por sua simplicidade e eficiência na implementação de bots.

### Bibliotecas
- **[python-telegram-bot](https://python-telegram-bot.org/)**: Biblioteca oficial do Telegram para bots em Python.
  
- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web de alto desempenho, utilizado em conjunto com:
  - **Uvicorn**: Servidor ASGI.
    
- **telegram.SecureValue**: Para manejar dados sensíveis (atualização futura).

### Arquitetura
- **Webhooks**: Utilizado para melhor desempenho e eficiência no uso de recursos.
  
- **Servidor**: Implantação no serviço de hosting **render**.

### Testes de Stress
- **StresserTelegram**: Ferramenta utilizada para testar a resiliência do bot sob alta carga.

---

## 🛠️ Configuração do Projeto

### 1. Obtenção da Chave API do Bot no Telegram
Para configurar o bot, é necessário obter uma chave API do Telegram. Siga os passos abaixo:

1. Abra o aplicativo do Telegram e procure pelo usuário `@BotFather`.
   
2. Inicie uma conversa com o `@BotFather` e envie o comando `/start`.
 
3. Para criar um novo bot, envie o comando `/newbot`.

4. Siga as instruções e forneça um nome e um username para o bot.

5. O `@BotFather` fornecerá uma **chave API** após a criação do bot. Esta chave será necessária para configurar o projeto.

**Atenção**: Mantenha a chave API privada e não a compartilhe publicamente.

---

### 2. Clonando o Repositório

1. Certifique-se de ter o **Git** instalado. Caso não tenha, siga as instruções de instalação no site oficial: [Git Downloads](https://git-scm.com/downloads).
   
2. Abra um terminal ou prompt de comando e execute o seguinte comando para clonar o repositório:

```bash
git clone https://github.com/JonathasAmaral/Bot_Telegram.git
```

3. Acesse o diretório do projeto:

```bash
cd Bot_Telegram
```

---

## 📋 Passos Futuros

- Implementar o uso de `telegram.SecureValue` para gerenciar dados sensíveis.
  
- Realizar testes de stress utilizando **StresserTelegram** para validar a resiliência e desempenho do bot.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

---

## 📄 Licença

Este projeto está sob a licença [GPL-3.0](LICENSE).

