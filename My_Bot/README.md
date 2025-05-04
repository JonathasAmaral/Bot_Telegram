# Bot da FURIA para Telegram

Bot oficial da FURIA para Telegram, com informações sobre campeonatos, resultados, jogos futuros e muito mais.

## Funcionalidades

- 🚀 **/start** - Menu principal com todas as opções
- 🛒 **/loja** - Link para a loja oficial
- 🎮 **/furia** - Informações sobre campeonatos atuais e futuros
  - Próximos campeonatos
  - Resultados de jogos
  - Jogos futuros
  - Resumo da equipe
- 🖼️ **/imagem** - Imagens do time, logo e wallpapers
- 💰 **/fan_wallet** - Informações sobre a carteira de fãs

## Tecnologias Utilizadas

- [python-telegram-bot](https://python-telegram-bot.org/) - Framework Python para bots do Telegram
- [FastAPI](https://fastapi.tiangolo.com/) - API web rápida
- [Requests](https://requests.readthedocs.io/) - Biblioteca para requisições HTTP
- [aiohttp](https://docs.aiohttp.org/) - Cliente HTTP assíncrono
- [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI para FastAPI
- [Vercel](https://vercel.com/) - Deploy e hospedagem
- [JSON](https://www.json.org/) - Armazenamento de dados local
- [Pydantic](https://docs.pydantic.dev/) - Validação de dados e configurações

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
   python main.py
   ```

   Este método é recomendado para desenvolvimento e testes, pois não requer configuração de webhook.

5. Alternativamente, você pode executar o servidor FastAPI localmente:
   ```
   uvicorn webhook.routes:app --reload
   ```

   Este método simula o ambiente de produção com webhook, mas requer o uso de uma ferramenta como ngrok para expor seu servidor local à internet.

### Executando os Testes

O projeto inclui testes automatizados para verificar a funcionalidade do leitor JSON:

1. Teste simples de leitura de arquivos JSON:
   ```
   python tests/teste_simple_json.py
   ```

2. Teste completo da funcionalidade do leitor JSON:
   ```
   python tests/teste_local_json.py
   ```

Esses testes verificam se os dados dos jogos estão sendo carregados corretamente e se estão no formato esperado.

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
│   │   │   ├── fan_wallet/
│   │   │   ├── furia/
│   │   │   ├── imagem/
│   │   │   └── start/
│   │   └── utils/         # Utilitários
│   │       ├── keyboard.py
│   │       ├── leitor_json.py  # Leitor de dados em JSON
│   │       └── message.py
│   ├── config/            # Configurações
│   │   └── settings.py
├── local_data/            # Dados locais em JSON
│   ├── data/              # Pasta com dados organizados por jogo
│   │   ├── apexlegends/   # Apex Legends
│   │   ├── csgo/          # Counter-Strike 2
│   │   ├── freefile/      # Free Fire
│   │   ├── leagueoflegends/ # League of Legends
│   │   ├── pubg/          # PUBG
│   │   ├── rainbowsix/    # Rainbow Six Siege
│   │   ├── rocketleague/  # Rocket League
│   │   ├── smashbros/     # Super Smash Bros. Ultimate
│   │   └── valorant/      # VALORANT
│   ├── utils/             # Utilitários para gerenciamento de dados
│   └── atualizar_dados.py # Script para atualizar dados
├── secret/                # Armazenamento seguro de credenciais (local)
│   └── config.json
├── tests/                 # Testes automatizados
│   ├── teste_local_json.py  # Teste do leitor JSON
│   └── teste_simple_json.py # Teste simples de arquivos JSON
├── webhook/               # Configuração de webhook
│   ├── app_state.py
│   ├── config.py
│   ├── routes.py
│   └── token.py
├── main.py                # Ponto de entrada principal
├── requirements.txt       # Dependências do projeto
└── README.md
```

## Dados Locais

O projeto utiliza dados armazenados localmente em arquivos JSON para cada jogo suportado:

- **Team Info**: Informações sobre o time (nome, ranking, região, etc)
- **Players**: Lista de jogadores com detalhes (nome, nickname, nacionalidade, etc)
- **Upcoming Matches**: Partidas futuras (oponente, evento, data, formato)
- **Past Matches**: Resultados de partidas passadas (oponente, evento, data, placar)
- **Tournaments**: Informações sobre torneios (nome, data, premiação, colocação)

Os dados são carregados pelo módulo `leitor_json.py` e podem ser atualizados através do script `atualizar_dados.py`.

## Jogos Suportados

O bot atualmente suporta informações para os seguintes jogos:

1. Counter-Strike 2 (CS2)
2. VALORANT
3. League of Legends
4. Rocket League
5. Rainbow Six Siege
6. PUBG
7. Apex Legends
8. Free Fire
9. Super Smash Bros. Ultimate

## Resolução de Problemas

### Erros Comuns

- **Erro 500 no Vercel**: Verifique se as variáveis de ambiente estão configuradas corretamente
- **Erro de módulo não encontrado**: Execute `pip install -r requirements.txt` para instalar todas as dependências
- **Bot não responde localmente**: Verifique se você criou corretamente o arquivo `config.json` com um token válido
- **Dados não carregando**: Verifique se os arquivos JSON existem na estrutura de pastas correta em `local_data/data/`

## Segurança

- As credenciais são armazenadas apenas localmente no arquivo `config.json` ou como variáveis de ambiente no Vercel
- O arquivo `config.json` nunca é commitado no repositório (incluído no `.gitignore`)
- Em produção, as variáveis de ambiente são usadas para maior segurança

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir um Pull Request.

### Diretrizes de Contribuição

1. Mantenha o código limpo e bem documentado
2. Atualize os testes quando adicionar ou modificar funcionalidades
3. Certifique-se de que todos os testes estão passando antes de enviar um Pull Request
4. Nunca inclua credenciais ou tokens nos commits
5. Atualize o README.md quando adicionar novas funcionalidades