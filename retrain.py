import pickle
import tensorflow as tf
import pandas as pd
import numpy as np

# TODO: move save_obj/load_obj to a shared utility module

def retrain_model(modelNum, path, username, home_score, visitor_score, strength_decimal):
    data = pd.read_csv(path)

    try:
        modelSettings = load_obj(str(username)+'ModelSettings'+modelNum)
    except FileNotFoundError:
        return 'error'

    optimizer_class = getattr(tf.keras.optimizers, modelSettings['optimizer'].capitalize())
    default_lr = optimizer_class().learning_rate.numpy()
    lr = default_lr * strength_decimal * .1

    custom_optimizer = getattr(tf.keras.optimizers, modelSettings['optimizer'].capitalize())(learning_rate=lr)

    print('------------ default learning rate: ', default_lr, '==== new lr: ', lr)

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(modelSettings['layer1Count'], activation=modelSettings['layer1Activation']),
        tf.keras.layers.Dense(modelSettings['layer2Count'], activation=modelSettings['layer2Activation']),
        tf.keras.layers.Dense(2, activation='linear'),
    ])
    model.load_weights('./userModels/'+username+'/'+modelNum+'/checkpoints/my_checkpoint')

    d = ['gameid','home_id','visitor_id','home_history_gameid','visitor_history_gameid','home_history2_gameid','visitor_history2_gameid']
    try:
        if modelSettings['streaks'] != 'true':
            d=d+['home_streak','visitor_streak']
        if modelSettings['wl'] != 'true':
            d=d+['hw','hl','vw','vl']
        if modelSettings['gp'] != 'true':
            d=d+['hgp','vgp']
        if modelSettings['ps'] != 'true':
            d.append('spread')
        labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
        for currentPlayer in range(int(modelSettings['players']),7):
            team_prefixes = ['home_', 'visitor_']
            for foo in team_prefixes:
                    for label in labels:
                        stat = foo+str(currentPlayer)+'_'+label
                        d.append(stat)

        features = ['min']
        if modelSettings['ast'] == 'true':
            features.append('ast')
        if modelSettings['blk'] == 'true':
            features.append('blk')
        if modelSettings['reb'] == 'true':
            features.append('dreb')
            features.append('oreb')
        if modelSettings['fg3'] == 'true':
            features.append('fg3m')
            features.append('fg3a')
        if modelSettings['fg'] == 'true':
            features.append('fga')
            features.append('fgm')
        if modelSettings['ft'] == 'true':
            features.append('fta')
            features.append('ftm')
        if modelSettings['pf'] == 'true':
            features.append('pf')
        if modelSettings['pts'] == 'true':
            features.append('pts')
        if modelSettings['stl'] == 'true':
            features.append('stl')
        if modelSettings['turnover'] == 'true':
            features.append('turnover')

        for currentPlayer in range(0,int(modelSettings['players'])):
            team_prefixes = ['home_', 'visitor_']
            for foo in team_prefixes:
                    for label in labels:
                        if label not in features:
                            stat = foo+str(currentPlayer)+'_'+label
                            d.append(stat)
    except KeyError:
        d = ['gameid','home_id','visitor_id','home_streak','visitor_streak','hgp','hw','hl','vgp','vw','vl']
    data.drop(d, axis=1, inplace=True)

    data = data.values
    data = data.astype(float)

    model.compile(optimizer=custom_optimizer, loss='mean_squared_error', metrics=['accuracy'])
    x_train = data
    home_score = float(home_score)
    visitor_score = float(visitor_score)
    y_train = np.array([[home_score, visitor_score]])
    model.fit(x_train, y_train, epochs=1, batch_size=1, shuffle=False)
    model.save_weights('./userModels/'+username+'/'+str(modelNum)+'/checkpoints/my_checkpoint')

    return 'Model retrained on the new game data, the update model weights have also been saved.'
