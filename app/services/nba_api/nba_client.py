from fastapi import HTTPException
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, cumestatsplayer


def get_active_players():
    return players.get_active_players()


def get_inactive_players():
    return players.get_inactive_players()


def get_all_players():
    return players.get_players()


# Get the player totals
def get_player_carrer_totals(player_id):
    return playercareerstats.PlayerCareerStats(player_id)


def get_player_info(player_id):
    player_info_df = commonplayerinfo.CommonPlayerInfo(
        player_id
    ).common_player_info.get_data_frame()

    if player_info_df.empty:
        raise HTTPException(status_code=404, detail="Player not found")

    return player_info_df.to_dict(orient="records")[0]


def get_cumulative_player_stats(game_ids, league_id, player_id, season, season_type):
    return cumestatsplayer.CumeStatsPlayer(
        game_ids, league_id, player_id, season, season_type
    )


def get_all_teams():
    return teams.get_teams()


def get_team_by_name(full_name):
    teams.find_teams_by_full_name(full_name)


def get_team_by_nickname(nickname):
    teams.find_teams_by_nickname(nickname)
