import requests
from bs4 import BeautifulSoup
from helpers.db import db_session
from models.model import Team, Player
from sqlalchemy import select, insert, update, delete
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO

def crawling_all_team(domain, head, url):
    response = requests.get(url, headers=head)
    collect_updates = []
    collect_inserts = []

    if response.status_code == 200:
        LOGO_IDX = 0
        TEAM_NAME_IDX = 1
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find('div', class_='pk-col--content')
        
        # Extract the teams of the content
        teams = content.find_all('div', class_='team team-is-club')
        
        for team in teams:
            info = team.find_all('span')
            link_team_detail = team.find('a', href=True)
            
            link_logo = info[LOGO_IDX].find('pk-badge')['src']
            team_name = info[TEAM_NAME_IDX].text.strip()
            link_team_detail = domain + link_team_detail['href'] + "/squad/"
            
            # Get file name
            file_name = link_logo.split('/')[-1]
            file_path = f"uploads/{file_name}"
            
            # Get response object for link
            response_logo = requests.get(link_logo, headers=head)
            
            # Write content in image file
            download_file(response_logo, file_path)
            
            # Validate and collect Insert or update data
            team_obj = db_session.execute(select(Team).filter_by(name=team_name)).scalar()
            if team_obj:
                collect_updates.append({"id": team_obj.id, "logo": file_path, "link_detail": link_team_detail})
            else:
                collect_inserts.append({"name": team_name, "logo": file_path, "link_detail": link_team_detail})
            
            # # Print console output
            # print(team_name)
            # print(link_logo)
            # print(file_path)
            # print(link_team_detail)
            # print('\n')
            
            # break
    
    # Commit insert or update here
    bulk_update_db(Team, collect_updates)
    bulk_insert_db(Team, collect_inserts)
        
def crawling_team_detail(head, url=None):
    teams = db_session.execute(select(Team)).scalars().all()
    
    for team in teams:
        collect_inserts = []
        url = team.link_detail
        response = requests.get(url, headers=head)

        if response.status_code == 200:
            CONTENT_HEADER_IDX = 0
            CONTENT_PLAYERS_IDX = 2
            CELL_PLAYER_NAME_IDX = 0            
            CELL_PLAYER_NUMBER_IDX = 0
            CELL_NATIONALITY_IDX = 1
            CELL_AGE_IDX = 2            
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.find_all('div', class_='pk-col--content')
            content_players = content[CONTENT_PLAYERS_IDX]
            content_header = content[CONTENT_HEADER_IDX]
            
            # Extract the teams of the content
            players = content_players.find_all('pk-table-row', class_='row--squadlist')
            for player in players:
                player_cells = player.find_all('pk-table-cell')
                
                player_name = player_cells[CELL_PLAYER_NAME_IDX].find('span', class_='pk-d--none').text.replace('*', '').strip()
                try:
                    player_number = player_cells[CELL_PLAYER_NUMBER_IDX].find('span', class_='squad--player-num').text.strip()
                except AttributeError:
                    player_number = None
                link_logo = content_header.find('pk-badge', class_='team-logo')['src']
                nationality = player_cells[CELL_NATIONALITY_IDX].text.strip()
                age = player_cells[CELL_AGE_IDX].text.strip()
                
                # Validate and collect Insert data
                player_obj = db_session.execute(select(Player).filter_by(team_id=team.id, name=player_name)).scalar()
                if player_obj:
                    stmt = delete(Player).where(Player.id == player_obj.id)
                    db_session.execute(stmt)
                    db_session.commit()
                collect_inserts.append(
                    {
                        "team_id": team.id,
                        "name": player_name, 
                        "club_number": player_number, 
                        "logo": link_logo, 
                        "nationality": nationality, 
                        "age": age
                    }
                )
                
                # # Print console output
                # print(f"player_name: {player_name}\
                #     \nplayer_number: {player_number}\
                #     \nlink_logo: {link_logo}\
                #     \nnationality: {nationality}\
                #     \nage: {age} \n")
                
                # break
            
            # Commit insert or update here
            bulk_insert_db(Player, collect_inserts)
        # break
        
# ------------- COMMON FUNCTIONS -------------
def download_file(response, file_path):
    logo = open(file_path, 'wb')
    logo.write(response.content)
    logo.close()
    
def bulk_insert_db(model, data):
    if model and data:
        db_session.execute(insert(model), data)
        db_session.commit()

def bulk_update_db(model, data):
    if model and data:
        db_session.execute(update(model), data)
        db_session.commit()
    
# ------------- MAIN -------------
if __name__=="__main__": 
    domain = 'https://www.uefa.com'
    url = 'https://www.uefa.com/uefachampionsleague/clubs/'
    head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
    
    try:
        logging.info("Crawling all team and save them in to database...")
        crawling_all_team(domain, head, url)
        logging.info("And then crawling all of players from each team to save it to database...")
        crawling_team_detail(head)
        logging.info("Crawling successfully.")
    except Exception as e:
        logging.error("Error crawling data: %s", str(e))
    
   
    