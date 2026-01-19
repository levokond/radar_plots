import pandas as pd

def goals_assists_key_passes(df):
    """
    Parameters
    ----------
    df : dataframe
        dataframe with event data.

    Returns
    -------
    data: dataframe
        dataframe with number of goals, assists and key passes per player.
    """
    df_sorted = df.sort_values(['game_id', 'expanded_minute', 'second']).reset_index(drop=True)
    
    # Get goals
    goals = df_sorted[df_sorted['is_goal'] == True]
    
    # Get assisted shots
    assisted_shots = df_sorted[(df_sorted['is_shot'] == True) & 
                                (df_sorted['qualifiers'].str.contains('Assisted', na=False))]
    
    # Find key passes and track if they led to goals
    key_passes = []
    for idx, shot in assisted_shots.iterrows():
        prior = df_sorted[(df_sorted.index < idx) & 
                          (df_sorted['game_id'] == shot['game_id']) & 
                          (df_sorted['team'] == shot['team']) & 
                          (df_sorted['type'] == 'Pass')]
        if len(prior) > 0:
            pass_row = prior.iloc[-1].copy()
            pass_row['led_to_goal'] = shot['is_goal'] == True
            key_passes.append(pass_row)
    
    key_passes_df = pd.DataFrame(key_passes)
    assists_df = key_passes_df[key_passes_df['led_to_goal'] == True] if len(key_passes_df) > 0 else pd.DataFrame()
    
    # Goals by player
    g_player = goals.groupby(['player_id']).size().reset_index(name='goals')
    
    # Assists by player
    a_player = assists_df.groupby(['player_id']).size().reset_index(name='assists') if len(assists_df) > 0 else pd.DataFrame(columns=['player_id', 'assists'])
    
    # Key passes by player
    kp_player = key_passes_df.groupby(['player_id']).size().reset_index(name='key_passes') if len(key_passes_df) > 0 else pd.DataFrame(columns=['player_id', 'key_passes'])
    
    # Merge all
    data = g_player.merge(a_player, how='outer', on='player_id').merge(kp_player, how='outer', on='player_id')
    data = data.fillna(0).astype({'goals': int, 'assists': int, 'key_passes': int})
    
    return data
