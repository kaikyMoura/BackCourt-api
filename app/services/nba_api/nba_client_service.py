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
def get_player_carrer_totals(params: dict):
    return playercareerstats.PlayerCareerStats(**params, timeout=70)


def get_player_info(player_id):
    player_info_df = commonplayerinfo.CommonPlayerInfo(
        player_id, timeout=70
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
        return playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(**params, timeout=70)

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=502, detail=f"Error decoding JSON: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


def get_player_seasons_dashboard(params: dict):
    dfs = []
    season_df = pd.DataFrame()
    player_id = params.get("player_id")
    season_type = params.get("season_type_playoffs", "Regular Season")
    per_mode = params.get("per_mode_detailed", "PerGame")
    season = params.get("season", "All")

    career_stats = get_player_carrer_totals({"player_id": player_id})
    print(season)
    if season != "All":
        if season_type == "Playoffs":
            season_df = career_stats.career_totals_post_season.get_data_frame()
        else:
            season_df = career_stats.career_totals_regular_season.get_data_frame()
    else:
        if season_type == "Playoffs":
            season_df = career_stats.season_totals_post_season.get_data_frame()
        else:
            season_df = career_stats.season_totals_regular_season.get_data_frame()

    all_seasons = season_df["SEASON_ID"].unique()

    for season_id in all_seasons:
        try:
            dashboard = get_player_dashboard_by_year_over_year(
                {
                    "player_id": player_id,
                    "season": season_id,
                    "per_mode_detailed": per_mode,
                    "season_type_playoffs": season_type,
                }
            )

            df = dashboard.by_year_player_dashboard.get_data_frame()
            df.columns = df.columns.str.lower()
            df["SEASON"] = season_id

            dfs.append(df)

        except Exception as e:
            print(
                f"[WARN] Error getting fantasy profile for player {player_id} in season {season_id}: {e}"
            )

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def get_player_career_dashboard(params: dict):
    """
    Retrieve the fantasy profile for a specific player using provided parameters.
    Returns a DataFrame containing the player's fantasy profile and career totals stats.

    Args:
        params (dict): A dictionary of parameters to fetch the player's fantasy profile.

    Returns:
        pd.DataFrame: A DataFrame containing the player's fantasy profile information.

    Raises:
        HTTPException: If no fantasy profile is found for the player.
    """
    player_id = params.get("player_id")
    season_type = params.get("season_type_playoffs", "Regular Season")
    
    career_stats = get_player_carrer_totals({"player_id": player_id})
    
    if season_type == "Playoffs":
        base_df = career_stats.career_totals_post_season.get_data_frame()
    else:
        base_df = career_stats.career_totals_regular_season.get_data_frame()
    
    base_df.columns = base_df.columns.str.lower()
    
    params_all = params.copy()
    params_all["season"] = "All"
    all_seasons_df = get_player_seasons_dashboard(params_all)
    
    if not all_seasons_df.empty:
        fantasy_cols = [col for col in all_seasons_df.columns 
                       if "fantasy" in col or "advanced" in col
                       or col in ["plus_minus", "pf", "pfd", "dd2", "td3"]]
        
        all_seasons_df = all_seasons_df.loc[:, ~all_seasons_df.columns.duplicated()]

        totals_df = all_seasons_df.drop_duplicates(subset=["group_value"], keep="first")

        fantasy_totals = totals_df[fantasy_cols].sum().to_frame().T
        final_df = pd.concat([base_df.reset_index(drop=True), fantasy_totals.reset_index(drop=True)], axis=1)
        return final_df

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
    awards_list = playerawards.PlayerAwards(player_id=player_id, timeout=70).get_data_frames()

    if not awards_list or awards_list[0].empty:
        raise HTTPException(status_code=404, detail=f"No awards found for this player")

    awards_df = awards_list[0]
    awards_df.columns = awards_df.columns.str.lower()

    return awards_df.to_dict(orient="records")


def get_all_teams():
    return teams.get_teams()


def get_team_by_name(full_name):
    return teams.find_teams_by_full_name(full_name)


def get_team_by_nickname(nickname):
    return teams.find_teams_by_nickname(nickname)
