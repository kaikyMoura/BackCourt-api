from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats

def get_active_players():
    return players.get_active_players()

def get_all_players():
    return players.get_players()

def get_player_carrer_stats(player_id):
    return playercareerstats.PlayerCareerStats(player_id)

def get_all_teams():
    return teams.get_teams()

def get_team_by_name(abbreviation):
    teams.find_team_by_abbreviation(abbreviation)
