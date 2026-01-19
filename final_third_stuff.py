import pandas as pd


def final_third_things(df):
    """
    Parameters
    ----------
    df : dataframe
        dataframe with Opta via Whoscored event data.

    Returns
    -------
    final_third: dataframe
        dataframe with number of passes ending in final third and receptions in that area for a player.

    """

    df["next_player_id"] = df["player_id"].shift(-1)
    passes = df[df['type'] == 'Pass']

    suc_passes = passes[passes['outcome_type'] == 'Successful']

    final_third_passes = suc_passes.loc[suc_passes['end_x'] > 2*100/3]

    ftp_player = final_third_passes.groupby(["player_id"]).end_x.count().reset_index()
    ftp_player.rename(columns = {'end_x':'final_third_passes'}, inplace=True)
    
    rtp_player = final_third_passes.groupby(["next_player_id"]).end_x.count().reset_index()
    rtp_player.rename(columns = {'end_x':'final_third_receptions', "next_player_id": "player_id"}, inplace=True)
    
    final_third = ftp_player.merge(rtp_player, how = "outer", on = ["player_id"])
    
    return final_third
