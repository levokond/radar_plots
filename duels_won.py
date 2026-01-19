import pandas as pd

def duels_won(df):
    """
    Parameters
    ----------
    df : dataframe
        dataframe with Wyscout event data.

    Returns
    -------
    duels_won: dataframe
        dataframe with number of won air and ground duels for a player

    """
    aerials = df[df['type'] == 'Aerial']
    won_aerial = aerials[aerials['outcome_type'] == 'Successful']

    wad_player =  won_aerial.groupby(["player_id"]).type.count().reset_index()
    wad_player.rename(columns = {'type':'air_duels_won'}, inplace=True)

    ground_duels = df[df['type'] == 'TakeOn']
    won_ground_duels = ground_duels[ground_duels['outcome_type'] == 'Successful']

    wgd_player = won_ground_duels.groupby(["player_id"]).type.count().reset_index()
    wgd_player.rename(columns = {'type':'ground_duels_won'}, inplace=True)

    duels_won = wgd_player.merge(wad_player, how = "outer", on = ["player_id"])
    duels_won = duels_won.fillna(0)
    return duels_won
