# Telegram Bot

Este projeto é um bot do Telegram desenvolvido para fornecer informações atualizadas sobre a FURIA Esports. O bot utiliza a API oficial da PandaScore para garantir dados precisos e em tempo real sobre jogos, resultados e estatísticas.

## 🚀 Tecnologias e Ferramentas Utilizadas

### Linguagem
- **Python**: Escolhida por sua simplicidade e eficiência na implementação de bots.

### Bibliotecas
- **[python-telegram-bot](https://python-telegram-bot.org/)**: Biblioteca oficial do Telegram para bots em Python.
  
- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web de alto desempenho.
  
- **telegram.SecureValue**: Para manejar dados sensíveis (atualização futura).

### Arquitetura
- **Webhooks**: Utilizado para melhor desempenho e eficiência no uso de recursos.
  
- **Servidor**: Implantação no serviço de hosting **render**.

### Testes de Stress
- **StresserTelegram**: Ferramenta utilizada para testar a resiliência do bot sob alta carga.

---

## 🛠️ Configuração do Projeto

### 1. Obtenção dos Tokens de API

#### Token do Bot Telegram
1. Abra o aplicativo do Telegram e procure pelo usuário `@BotFather`.
2. Inicie uma conversa com o `@BotFather` e envie o comando `/start`.
3. Para criar um novo bot, envie o comando `/newbot`.
4. Siga as instruções e forneça um nome e um username para o bot.
5. O `@BotFather` fornecerá uma **chave API**.

#### Token da PandaScore
1. Crie uma conta em [PandaScore](https://developers.pandascore.co/).
2. No dashboard, acesse a seção de API tokens.
3. Gere um novo token para seu projeto.

**Atenção**: Mantenha as chaves API privadas e não as compartilhe publicamente.

---

### 2. Clonando o Repositório

1. Certifique-se de ter o **Git** instalado.
   
2. Execute o comando para clonar o repositório:
```bash
git clone https://github.com/JonathasAmaral/Bot_Telegram.git
```

3. Acesse o diretório do projeto:
```bash
cd Bot_Telegram
```

### 3. Configuração do Ambiente

1. Crie o arquivo de configuração:
   - Copie o arquivo `secret/config.txt` para `secret/config.json`
   - Preencha os tokens necessários:
     ```json
     {
         "BOT_TOKEN": "SEU_TOKEN_DO_TELEGRAM",
         "WEBHOOK_URL": "https://{server_url}/api/webhook",
         "PANDASCORE_TOKEN": "SEU_TOKEN_DA_PANDASCORE",
         "DEBUG": false
     }
     ```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

---

## 📋 Funcionalidades

- 🎮 Informações em tempo real dos times de CS:GO e Valorant
- 📊 Estatísticas atualizadas via PandaScore API
- 🗂️ Cache inteligente para otimizar requisições
- 🔄 Atualizações automáticas de dados

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

---

## 📄 Licença

Este projeto está sob a licença [GPL-3.0](LICENSE).

