import pandas as pd
def p_p(df):
    passes = df[df['type'] == 'Pass']
    passes['length'] = passes['end_x'] - passes['x']

    progressive_passes = passes[
        ((passes['end_x'] < 50) & (passes['length'] >= 30)) |
        ((passes['x'] < 50) & (passes['end_x'] >= 50) & (passes['length'] >= 15)) |
        ((passes['x'] >= 50) & (passes['end_x'] >= 50) & (passes['length'] >= 10))
    ]

    pp_player = progressive_passes.groupby('player_id').type.count().reset_index()
    pp_player.rename(columns={'type': 'progressive_passes'}, inplace=True)

    pp_player.head()
    return pp_player
