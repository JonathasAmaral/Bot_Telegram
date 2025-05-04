# Dados Locais para o Bot FURIA

Este diretório contém todos os arquivos JSON que armazenam dados locais utilizados pelo bot da FURIA para Telegram.

## Estrutura de Arquivos

Os dados estão organizados por jogo (CS:GO e Valorant) e tipo de informação:

- **csgo_team.json** - Informações gerais do time de CS:GO
- **valorant_team.json** - Informações gerais do time de Valorant
- **csgo_players.json** - Lista de jogadores do time de CS:GO
- **valorant_players.json** - Lista de jogadores do time de Valorant
- **csgo_upcoming_matches.json** - Próximos jogos do time de CS:GO
- **valorant_upcoming_matches.json** - Próximos jogos do time de Valorant
- **csgo_past_matches.json** - Resultados recentes do time de CS:GO
- **valorant_past_matches.json** - Resultados recentes do time de Valorant
- **csgo_tournaments.json** - Informações sobre torneios do time de CS:GO
- **valorant_tournaments.json** - Informações sobre torneios do time de Valorant

## Como Atualizar os Dados

Para atualizar as informações exibidas pelo bot, basta editar os arquivos JSON correspondentes. Não é necessário reiniciar o bot para que as alterações entrem em vigor, pois o sistema de cache atualiza automaticamente quando os usuários solicitam uma atualização através do botão "Atualizar dados" no menu do jogo.

### Formato dos Dados

#### Team Info (csgo_team.json, valorant_team.json)

```json
{
    "name": "Nome do time",
    "country": "País",
    "region": "Região",
    "world_ranking": "Ranking mundial",
    "ranking": "Ranking regional",
    "created_at": "Data de criação",
    "modified_at": "Data de modificação",
    "acronym": "Sigla do time",
    "logo_url": "URL do logo"
}
```

#### Players (csgo_players.json, valorant_players.json)

```json
[
    {
        "id": "ID do jogador",
        "name": "Nome completo",
        "first_name": "Primeiro nome",
        "last_name": "Sobrenome",
        "nickname": "Nickname",
        "nationality": "Nacionalidade (código de 2 letras)",
        "role": "Função no time",
        "age": "Idade",
        "hometown": "Cidade natal"
    },
    // ... outros jogadores
]
```

#### Upcoming Matches (csgo_upcoming_matches.json, valorant_upcoming_matches.json)

```json
[
    {
        "opponent": "Nome do adversário",
        "event": "Nome do evento",
        "date": "DD/MM/AAAA",
        "time": "HH:MM UTC",
        "format": "Formato (BO1, BO3, etc)"
    },
    // ... outros jogos
]
```

#### Past Matches (csgo_past_matches.json, valorant_past_matches.json)

```json
[
    {
        "opponent": "Nome do adversário",
        "event": "Nome do evento",
        "date": "DD/MM/AAAA",
        "score": "X - Y",
        "map": "Mapas jogados"
    },
    // ... outros jogos
]
```

#### Tournaments (csgo_tournaments.json, valorant_tournaments.json)

```json
[
    {
        "name": "Nome do torneio",
        "date": "DD/MM/AAAA",
        "prize_pool": "Premiação",
        "location": "Local",
        "placement": "Colocação",
        "tier": "Tier do torneio"
    },
    // ... outros torneios
]
```

## Adicionando um Novo Jogo

Para adicionar um novo jogo (por exemplo, League of Legends), siga estes passos:

1. Crie os arquivos JSON necessários seguindo o padrão de nomenclatura:
   - `lol_team.json`
   - `lol_players.json`
   - `lol_upcoming_matches.json`
   - `lol_past_matches.json`
   - `lol_tournaments.json`

2. O sistema reconhecerá automaticamente o novo jogo na próxima vez que o bot for executado, sem necessidade de modificar o código.

## Considerações Técnicas

- Os arquivos são lidos e armazenados em cache para melhorar a performance.
- Quando um usuário solicita atualização dos dados, o cache para aquele jogo específico é limpo.
- O cache também é resetado automaticamente quando o bot é reiniciado.