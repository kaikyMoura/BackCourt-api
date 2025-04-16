import json
from fastapi import HTTPException
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import (
    playercareerstats,
    commonplayerinfo,
    playerawards,
    playerdashboardbyyearoveryear,
)
import pandas as pd


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


def get_player_dashboard_by_year_over_year(params: dict):
    """
    Retrieve the fantasy profile for a specific player using provided parameters.

    Args:
        params (dict): A dictionary of parameters to fetch the player's fantasy profile.

    Returns:
        list: A list of data frames containing the player's fantasy profile information.

    Raises:
        HTTPException: If there is an error decoding JSON response or an unexpected error occurs.
    """

    try:
        return playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(**params)

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=502, detail=f"Error decoding JSON: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


def get_player_seasons_dashboard(params: dict, dataset_index: int = 0):
    dfs = []
    player_id = params.get("player_id")
    season_type = params.get("season_type_playoffs", "Regular Season")
    per_mode = params.get("per_mode_detailed", "PerGame")

    career_stats = get_player_carrer_totals(player_id)
    if season_type == "Regular Season":
        season_df = career_stats.season_totals_regular_season.get_data_frame()
    else:
        season_df = career_stats.season_totals_post_season.get_data_frame()

    all_seasons = season_df["SEASON_ID"].unique()

    for season_id in all_seasons:
        try:
            profile = get_player_dashboard_by_year_over_year(
                {
                    "player_id": player_id,
                    "season": season_id,
                    "per_mode_detailed": per_mode,
                    "season_type_playoffs": season_type,
                }
            ).get_data_frames()

            df = profile[dataset_index]
            df.columns = df.columns.str.lower()
            df["SEASON"] = season_id
            dfs.append(df)

        except Exception as e:
            print(
                f"[WARN] Error getting fantasy profile for player {player_id} in season {season_id}: {e}"
            )

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)


def get_player_awards(player_id):
    """
    Get awards for a specific player by their player ID.

    Args:
        player_id (int): The unique identifier for the player.

    Returns:
        dict: A dictionary containing the awards information.

    Raises:
        HTTPException: If no awards are found for the player.
    """
    awards_list = playerawards.PlayerAwards(player_id=player_id).get_data_frames()

    if not awards_list or awards_list[0].empty:
        raise HTTPException(status_code=404, detail=f"No awards found for this player")

    awards_df = awards_list[0]
    awards_df.columns = awards_df.columns.str.lower()

    return awards_df.to_dict(orient="records")


def get_all_teams():
    return teams.get_teams()


def get_team_by_name(full_name):
    teams.find_teams_by_full_name(full_name)


def get_team_by_nickname(nickname):
    teams.find_teams_by_nickname(nickname)
