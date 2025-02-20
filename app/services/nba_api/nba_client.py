from nba_api.stats.static import players, teams

def get_active_players():
    return players.get_active_players()

def get_player_by_last_name(name):
    return players.find_players_by_last_name(name)

def get_all_teams():
    return teams.get_teams()

def get_team_by_name(abbreviation):
    teams.find_team_by_abbreviation(abbreviation)
