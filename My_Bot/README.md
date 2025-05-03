# Bot da FURIA para Telegram

Bot oficial da FURIA para Telegram, com informações sobre campeonatos, resultados, jogos futuros e muito mais.

## Funcionalidades

- 🚀 **/start** - Menu principal com todas as opções
- 🛒 **/loja** - Link para a loja oficial
- 🎮 **/campeonato** - Informações sobre campeonatos atuais e futuros
  - Próximos campeonatos
  - Resultados de jogos
  - Jogos futuros
  - Resumo da equipe
- 🖼️ **/imagem** - Imagens do time, logo e wallpapers

## Tecnologias Utilizadas

- [Aiogram 3.x](https://docs.aiogram.dev/en/latest/) - Framework moderno para bots do Telegram
- [FastAPI](https://fastapi.tiangolo.com/) - API web rápida
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - Scraping de informações
- [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI para FastAPI
- [Vercel](https://vercel.com/) - Deploy e hospedagem

## Configuração

### Pré-requisitos

- Python 3.10+
- Conta no Vercel
- Bot registrado no Telegram (via [@BotFather](https://t.me/botfather))

### Configuração de Credenciais

Existem duas formas de configurar as credenciais:

#### 1. Para Desenvolvimento Local

Crie manualmente um arquivo `config.json` na pasta `secret/` com o seguinte formato:

```json
{
  "BOT_TOKEN": "seu_token_aqui",
  "WEBHOOK_URL": "https://sua-url-do-webhook.vercel.app/api/webhook"
}
```

**IMPORTANTE**: 
- O arquivo `config.json` DEVE ser criado manualmente e não é gerado automaticamente
- Está incluído no `.gitignore` e nunca deve ser commitado no repositório

#### 2. Para Produção (Vercel)

Configure as seguintes variáveis de ambiente no painel do Vercel:

- `BOT_TOKEN` - Token do bot fornecido pelo BotFather
- `WEBHOOK_URL` - URL completa do webhook (opcional, será detectada automaticamente)

### Instalação e Execução Local

1. Clone o repositório
2. Instale as dependências
   ```
   pip install -r requirements.txt
   ```
3. Crie manualmente o arquivo `secret/config.json` com suas credenciais
4. Execute o bot localmente usando o script de polling:
   ```
   python run_local.py
   ```

   Este método é recomendado para desenvolvimento e testes, pois não requer configuração de webhook.

5. Alternativamente, você pode executar o servidor FastAPI localmente:
   ```
   uvicorn webhook.routes:app --reload
   ```

   Este método simula o ambiente de produção com webhook, mas requer o uso de uma ferramenta como ngrok para expor seu servidor local à internet.

### Deploy no Vercel

1. Configure as variáveis de ambiente no dashboard do Vercel
2. Conecte o repositório ao Vercel
3. Defina a pasta `My_Bot` como diretório raiz do projeto
4. Deploy!
5. Acesse a rota `/set-webhook` para configurar o webhook automaticamente

## Estrutura do Projeto

```
My_Bot/
├── api/
│   ├── assets/
│   │   └── images/        # Imagens usadas pelo bot
│   ├── bot/
│   │   ├── handlers/      # Handlers para comandos e callbacks
│   │   │   ├── commands.py
│   │   │   ├── campeonato/
│   │   │   │   └── campeonato_handler.py
│   │   │   ├── imagem/
│   │   │   │   └── imagem_handler.py
│   │   │   └── start/
│   │   │       └── start_handler.py
│   │   └── utils/         # Utilitários (scraper, etc)
│   │       └── scraper.py
│   ├── config/            # Configurações
│   │   └── settings.py
│   ├── secret/            # Armazenamento seguro de credenciais (local)
│   │   ├── config.json
│   │   └── config.txt
│   ├── webhook/ 
│   │   ├── config.py          # Rotas para webhook
│   │   ├── routes.py
│   │   ├── set_webhook.py
│   │   └── token.py
├── main.py                # Ponto de entrada principal
├── requirements.txt       # Dependências do projeto           # 
└── README.md
```

## Resolução de Problemas

### Erros Comuns

- **Erro 500 no Vercel**: Verifique se as variáveis de ambiente estão configuradas corretamente
- **Erro de módulo não encontrado**: Execute `pip install -r requirements.txt` para instalar todas as dependências
- **Bot não responde localmente**: Verifique se você criou corretamente o arquivo `config.json` com um token válido

## Segurança

- As credenciais são armazenadas apenas localmente no arquivo `config.json` ou como variáveis de ambiente no Vercel
- O arquivo `config.json` nunca é commitado no repositório (incluído no `.gitignore`)
- Em produção, as variáveis de ambiente são usadas para maior segurança

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir um Pull Request.