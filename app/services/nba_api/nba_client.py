from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo

def get_active_players():
    return players.get_active_players()

def get_inactive_players():
    return players.get_inactive_players()

def get_all_players():
    return players.get_players()

def get_player_carrer_stats(player_id):
    return playercareerstats.PlayerCareerStats(player_id)

def get_player_info(player_id):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id).common_player_info.get_dict()
    
    if isinstance(player_info, dict):
        return player_info
    else:
        return {"data": player_info}
    
def get_all_teams():
    return teams.get_teams()

def get_team_by_name(full_name):
    teams.find_teams_by_full_name(full_name)

def get_team_by_nickname(nickname):
    teams.find_teams_by_nickname(nickname)