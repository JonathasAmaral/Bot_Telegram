"""
Utilitário para atualizar os arquivos JSON locais
Este script fornece uma interface interativa para atualizar 
os dados da FURIA em arquivos JSON locais.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Importar classes da pasta utils
from utils.json_manager import JsonManager
from utils.data_editor import (
    TeamEditor, 
    PlayersEditor, 
    UpcomingMatchesEditor as UpcomingEditor, 
    PastMatchesEditor as PastEditor,
    TournamentsEditor
)

# Inicializar gerenciador
json_manager = JsonManager()
GAMES = ["csgo", "valorant"]

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def edit_team(game):
    """Edit team information using TeamEditor"""
    editor = TeamEditor(json_manager, game)
    editor.load()
    
    print(f"\nEditando informações do time de {game.upper()}")
    print("-" * 40)
    
    for key in editor.data.keys():
        if key in ["created_at", "modified_at"]:
            continue
        
        current = editor.data[key]
        new_value = input(f"{key} [{current}]: ")
        if new_value:
            editor.edit_field(key, new_value)
    
    return editor.save()

def edit_players(game):
    """Edit players list using PlayersEditor"""
    editor = PlayersEditor(json_manager, game)
    editor.load()
    
    print(f"\nEditando jogadores do time de {game.upper()}")
    print("-" * 40)
    
    while True:
        print("\nJogadores atuais:")
        players = editor.get_players()
        for idx, player in enumerate(players):
            print(f"{idx+1}. {player['nickname']} ({player['name']})")
        
        print("\nOpções:")
        print("1. Adicionar jogador")
        print("2. Editar jogador")
        print("3. Remover jogador")
        print("4. Salvar e voltar")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == "1":
            # Add new player
            player = {
                "name": "",
                "first_name": "",
                "last_name": "",
                "nickname": "",
                "nationality": "BR",
                "role": "",
                "age": "",
                "hometown": ""
            }
            
            print("\nDigite as informações do novo jogador:")
            player["nickname"] = input("Nickname: ")
            player["first_name"] = input("Nome: ")
            player["last_name"] = input("Sobrenome: ")
            player["name"] = f"{player['first_name']} {player['last_name']}"
            player["nationality"] = input("Nacionalidade (BR): ") or "BR"
            player["role"] = input("Função: ")
            player["age"] = input("Idade: ")
            player["hometown"] = input("Cidade natal: ")
            
            editor.add_player(player)
            print(f"✓ Jogador {player['nickname']} adicionado com sucesso!")
            
        elif choice == "2":
            # Edit existing player
            idx = int(input("Digite o número do jogador para editar: ")) - 1
            players = editor.get_players()
            if 0 <= idx < len(players):
                player = players[idx].copy()  # Criar cópia para edição
                print(f"\nEditando jogador {player['nickname']}")
                
                player["nickname"] = input(f"Nickname [{player['nickname']}]: ") or player["nickname"]
                player["first_name"] = input(f"Nome [{player['first_name']}]: ") or player["first_name"]
                player["last_name"] = input(f"Sobrenome [{player['last_name']}]: ") or player["last_name"]
                player["name"] = f"{player['first_name']} {player['last_name']}"
                player["nationality"] = input(f"Nacionalidade [{player['nationality']}]: ") or player["nationality"]
                player["role"] = input(f"Função [{player['role']}]: ") or player["role"]
                player["age"] = input(f"Idade [{player['age']}]: ") or player["age"]
                player["hometown"] = input(f"Cidade natal [{player['hometown']}]: ") or player["hometown"]
                
                editor.update_player(idx, player)
                print(f"✓ Jogador {player['nickname']} atualizado com sucesso!")
            else:
                print("❌ Índice inválido!")
                
        elif choice == "3":
            # Remove player
            idx = int(input("Digite o número do jogador para remover: ")) - 1
            players = editor.get_players()
            if 0 <= idx < len(players):
                player = players[idx]
                confirm = input(f"Tem certeza que deseja remover {player['nickname']}? (s/n): ")
                if confirm.lower() == "s":
                    removed = editor.remove_player(idx)
                    print(f"✓ Jogador {removed['nickname']} removido com sucesso!")
            else:
                print("❌ Índice inválido!")
                
        elif choice == "4":
            # Save and exit
            return editor.save()
        
        else:
            print("❌ Opção inválida!")

def edit_upcoming_matches(game):
    """Edit upcoming matches using UpcomingEditor"""
    editor = UpcomingEditor(json_manager, game)
    editor.load()
    
    print(f"\nEditando próximos jogos do time de {game.upper()}")
    print("-" * 40)
    
    while True:
        print("\nPróximos jogos:")
        matches = editor.get_matches()
        for idx, match in enumerate(matches):
            print(f"{idx+1}. vs {match['opponent']} - {match['date']} ({match['event']})")
        
        print("\nOpções:")
        print("1. Adicionar jogo")
        print("2. Editar jogo")
        print("3. Remover jogo")
        print("4. Salvar e voltar")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == "1":
            # Add new match
            match = {
                "opponent": "",
                "event": "",
                "date": "",
                "time": "",
                "format": "BO3"
            }
            
            print("\nDigite as informações do novo jogo:")
            match["opponent"] = input("Adversário: ")
            match["event"] = input("Evento: ")
            match["date"] = input("Data (DD/MM/AAAA): ")
            match["time"] = input("Horário (HH:MM UTC): ")
            match["format"] = input("Formato (BO3): ") or "BO3"
            
            editor.add_match(match)
            print(f"✓ Jogo contra {match['opponent']} adicionado com sucesso!")
            
        elif choice == "2":
            # Edit existing match
            idx = int(input("Digite o número do jogo para editar: ")) - 1
            matches = editor.get_matches()
            if 0 <= idx < len(matches):
                match = matches[idx].copy()  # Criar cópia para edição
                print(f"\nEditando jogo contra {match['opponent']}")
                
                match["opponent"] = input(f"Adversário [{match['opponent']}]: ") or match["opponent"]
                match["event"] = input(f"Evento [{match['event']}]: ") or match["event"]
                match["date"] = input(f"Data [{match['date']}]: ") or match["date"]
                match["time"] = input(f"Horário [{match['time']}]: ") or match["time"]
                match["format"] = input(f"Formato [{match['format']}]: ") or match["format"]
                
                editor.update_match(idx, match)
                print(f"✓ Jogo contra {match['opponent']} atualizado com sucesso!")
            else:
                print("❌ Índice inválido!")
                
        elif choice == "3":
            # Remove match
            idx = int(input("Digite o número do jogo para remover: ")) - 1
            matches = editor.get_matches()
            if 0 <= idx < len(matches):
                match = matches[idx]
                confirm = input(f"Tem certeza que deseja remover o jogo contra {match['opponent']}? (s/n): ")
                if confirm.lower() == "s":
                    removed = editor.remove_match(idx)
                    print(f"✓ Jogo contra {removed['opponent']} removido com sucesso!")
            else:
                print("❌ Índice inválido!")
                
        elif choice == "4":
            # Save and exit
            return editor.save()
        
        else:
            print("❌ Opção inválida!")

def edit_past_matches(game):
    """Edit past matches using PastEditor"""
    editor = PastEditor(json_manager, game)
    editor.load()
    
    print(f"\nEditando resultados recentes do time de {game.upper()}")
    print("-" * 40)
    
    while True:
        print("\nResultados recentes:")
        matches = editor.get_matches()
        for idx, match in enumerate(matches):
            print(f"{idx+1}. vs {match['opponent']} - {match['score']} ({match['event']})")
        
        print("\nOpções:")
        print("1. Adicionar resultado")
        print("2. Editar resultado")
        print("3. Remover resultado")
        print("4. Salvar e voltar")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == "1":
            # Add new result
            match = {
                "opponent": "",
                "event": "",
                "date": "",
                "score": "",
                "map": ""
            }
            
            print("\nDigite as informações do novo resultado:")
            match["opponent"] = input("Adversário: ")
            match["event"] = input("Evento: ")
            match["date"] = input("Data (DD/MM/AAAA): ")
            match["score"] = input("Placar (X - Y): ")
            match["map"] = input("Mapas: ")
            
            editor.add_match(match)
            print(f"✓ Resultado contra {match['opponent']} adicionado com sucesso!")
            
        elif choice == "2":
            # Edit existing result
            idx = int(input("Digite o número do resultado para editar: ")) - 1
            matches = editor.get_matches()
            if 0 <= idx < len(matches):
                match = matches[idx].copy()  # Criar cópia para edição
                print(f"\nEditando resultado contra {match['opponent']}")
                
                match["opponent"] = input(f"Adversário [{match['opponent']}]: ") or match["opponent"]
                match["event"] = input(f"Evento [{match['event']}]: ") or match["event"]
                match["date"] = input(f"Data [{match['date']}]: ") or match["date"]
                match["score"] = input(f"Placar [{match['score']}]: ") or match["score"]
                match["map"] = input(f"Mapas [{match['map']}]: ") or match["map"]
                
                editor.update_match(idx, match)
                print(f"✓ Resultado contra {match['opponent']} atualizado com sucesso!")
            else:
                print("❌ Índice inválido!")
                
        elif choice == "3":
            # Remove result
            idx = int(input("Digite o número do resultado para remover: ")) - 1
            matches = editor.get_matches()
            if 0 <= idx < len(matches):
                match = matches[idx]
                confirm = input(f"Tem certeza que deseja remover o resultado contra {match['opponent']}? (s/n): ")
                if confirm.lower() == "s":
                    removed = editor.remove_match(idx)
                    print(f"✓ Resultado contra {removed['opponent']} removido com sucesso!")
            else:
                print("❌ Índice inválido!")
                
        elif choice == "4":
            # Save and exit
            return editor.save()
        
        else:
            print("❌ Opção inválida!")

def edit_tournaments(game):
    """Edit tournaments using TournamentsEditor"""
    editor = TournamentsEditor(json_manager, game)
    editor.load()
    
    print(f"\nEditando torneios do time de {game.upper()}")
    print("-" * 40)
    
    while True:
        print("\nTorneios:")
        tournaments = editor.get_tournaments()
        for idx, tournament in enumerate(tournaments):
            print(f"{idx+1}. {tournament['name']} - {tournament['placement']} ({tournament['date']})")
        
        print("\nOpções:")
        print("1. Adicionar torneio")
        print("2. Editar torneio")
        print("3. Remover torneio")
        print("4. Salvar e voltar")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == "1":
            # Add new tournament
            tournament = {
                "name": "",
                "date": "",
                "prize_pool": "",
                "location": "",
                "placement": "",
                "tier": ""
            }
            
            print("\nDigite as informações do novo torneio:")
            tournament["name"] = input("Nome: ")
            tournament["date"] = input("Data (DD/MM/AAAA): ")
            tournament["prize_pool"] = input("Premiação: ")
            tournament["location"] = input("Local: ")
            tournament["placement"] = input("Colocação: ")
            tournament["tier"] = input("Tier (S-Tier, A-Tier, etc): ")
            
            editor.add_tournament(tournament)
            print(f"✓ Torneio {tournament['name']} adicionado com sucesso!")
            
        elif choice == "2":
            # Edit existing tournament
            idx = int(input("Digite o número do torneio para editar: ")) - 1
            tournaments = editor.get_tournaments()
            if 0 <= idx < len(tournaments):
                tournament = tournaments[idx].copy()  # Criar cópia para edição
                print(f"\nEditando torneio {tournament['name']}")
                
                tournament["name"] = input(f"Nome [{tournament['name']}]: ") or tournament["name"]
                tournament["date"] = input(f"Data [{tournament['date']}]: ") or tournament["date"]
                tournament["prize_pool"] = input(f"Premiação [{tournament['prize_pool']}]: ") or tournament["prize_pool"]
                tournament["location"] = input(f"Local [{tournament['location']}]: ") or tournament["location"]
                tournament["placement"] = input(f"Colocação [{tournament['placement']}]: ") or tournament["placement"]
                tournament["tier"] = input(f"Tier [{tournament['tier']}]: ") or tournament["tier"]
                
                editor.update_tournament(idx, tournament)
                print(f"✓ Torneio {tournament['name']} atualizado com sucesso!")
            else:
                print("❌ Índice inválido!")
                
        elif choice == "3":
            # Remove tournament
            idx = int(input("Digite o número do torneio para remover: ")) - 1
            tournaments = editor.get_tournaments()
            if 0 <= idx < len(tournaments):
                tournament = tournaments[idx]
                confirm = input(f"Tem certeza que deseja remover o torneio {tournament['name']}? (s/n): ")
                if confirm.lower() == "s":
                    removed = editor.remove_tournament(idx)
                    print(f"✓ Torneio {removed['name']} removido com sucesso!")
            else:
                print("❌ Índice inválido!")
                
        elif choice == "4":
            # Save and exit
            return editor.save()
        
        else:
            print("❌ Opção inválida!")

def main():
    """Main menu function"""
    while True:
        clear_screen()
        print("=" * 40)
        print("    ATUALIZAÇÃO DE DADOS LOCAIS DA FURIA")
        print("=" * 40)
        print("\nEscolha um jogo para editar:")
        print("1. CS:GO")
        print("2. Valorant")
        print("\n3. Sair")
        
        choice = input("\nOpção: ")
        
        if choice == "1":
            game_menu("csgo")
        elif choice == "2":
            game_menu("valorant")
        elif choice == "3":
            clear_screen()
            print("Obrigado por atualizar os dados!")
            sys.exit(0)
        else:
            input("❌ Opção inválida! Pressione ENTER para continuar...")

def game_menu(game):
    """Game submenu"""
    while True:
        clear_screen()
        print("=" * 40)
        print(f"    EDIÇÃO DOS DADOS DE {game.upper()}")
        print("=" * 40)
        print("\nO que você deseja editar?")
        print("1. Informações do time")
        print("2. Jogadores")
        print("3. Próximos jogos")
        print("4. Resultados recentes")
        print("5. Torneios")
        print("\n6. Voltar")
        
        choice = input("\nOpção: ")
        
        if choice == "1":
            edit_team(game)
        elif choice == "2":
            edit_players(game)
        elif choice == "3":
            edit_upcoming_matches(game)
        elif choice == "4":
            edit_past_matches(game)
        elif choice == "5":
            edit_tournaments(game)
        elif choice == "6":
            return
        else:
            input("❌ Opção inválida! Pressione ENTER para continuar...")
        
        if choice in ["1", "2", "3", "4", "5"]:
            input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()
