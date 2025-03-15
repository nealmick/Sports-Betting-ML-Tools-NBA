import time
import datetime
import logging
import os
import sys
import contextlib

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split


class ImmediateFileHandler(logging.FileHandler):
    def __init__(self, log_filename, mode='a', encoding=None, delay=False):
        super().__init__(log_filename, mode, encoding, delay)
        self.terminator = ''

    def emit(self, record):
        super().emit(record)
        self.flush()


def setup_logging(username, modelNum):
    log_directory = f'./userModels/{username}/{modelNum}'
    log_filename = os.path.join(log_directory, 'training_log.txt')
    os.makedirs(log_directory, exist_ok=True)

    logger = logging.getLogger(f'tensorflow_logger_{username}_{modelNum}')
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = ImmediateFileHandler(log_filename, mode='w')
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


class DirectWriteLoggerCallback(tf.keras.callbacks.Callback):
    def __init__(self, logger):
        super(DirectWriteLoggerCallback, self).__init__()
        self.logger = logger


@contextlib.contextmanager
def log_stdout(logger):
    class LoggerWriter:
        def __init__(self, level):
            self.level = level

        def write(self, message):
            if message != '\n':
                self.level(message)

        def flush(self):
            pass

    old_stdout = sys.stdout
    sys.stdout = LoggerWriter(logger.info)
    try:
        yield
    finally:
        sys.stdout = old_stdout


class MarginTracker:
    def __init__(self, threshold):
        self.threshold = threshold
        self.count = 0
        self.correct = 0
        self.current = 0
        self.min_val = -1
        self.max_val = 0

    def update(self, margin, mcorrect):
        if abs(margin) > self.threshold:
            self.count += 1
            if mcorrect:
                self.correct += 1
                self.current += 1
            else:
                self.current -= 1
            if self.current < self.min_val:
                self.min_val = self.current
            if self.current > self.max_val:
                self.max_val = self.current
            return True
        return False


def print_prediction(model, data, homeTestScore, visitorTestScore, spread):
    p = model.predict(data)
    c = 0
    n = 0
    s = 0
    ev = 0

    margin1 = MarginTracker(1)
    margin2 = MarginTracker(2)
    margin3 = MarginTracker(3)
    margin4 = MarginTracker(4)
    margin6 = MarginTracker(6)

    gameSeries1 = []
    gameSeries2 = []
    gameSeries3 = []
    SeriesStepCounter = 0

    for i in range(len(p)):
        SeriesStepCounter += 1
        correct = False
        spreadCorrect = False
        pmscore = round(homeTestScore[i] - visitorTestScore[i])
        pmp = p[i][0] - p[i][1]
        n += 1
        spread[i] = spread[i] * -1

        if spread[i] > 0 and homeTestScore[i] > visitorTestScore[i]:
            spreadCorrect = True
            s += 1
        if spread[i] < 0 and homeTestScore[i] < visitorTestScore[i]:
            s += 1
            spreadCorrect = True

        if p[i][0] > p[i][1] and homeTestScore[i] > visitorTestScore[i]:
            correct = True
        elif p[i][0] < p[i][1] and homeTestScore[i] < visitorTestScore[i]:
            correct = True

        pred = ''
        if spread[i] > pmp and pmp < 0:
            pred = 0
        elif spread[i] > pmp and pmp > 0:
            pred = 0
        elif spread[i] < pmp and pmp < 0:
            pred = 1
        elif spread[i] < pmp and pmp > 0:
            pred = 1

        swin = ''
        if spread[i] > pmscore and pmscore < 0:
            swin = 0
        elif spread[i] > pmscore and pmscore > 0:
            swin = 0
        elif spread[i] < pmscore and pmscore < 0:
            swin = 1
        elif spread[i] < pmscore and pmscore > 0:
            swin = 1

        mcorrect = True
        if pred == 0 and swin == 0:
            ev += 1
        elif pred == 1 and swin == 1:
            ev += 1
        else:
            mcorrect = False

        margin = abs(pmp) - abs(spread[i])

        if float(pmp) < 0 and spread[i] < 0:
            pass

        margin6.update(margin, mcorrect)
        margin4.update(margin, mcorrect)
        margin3.update(margin, mcorrect)
        margin2.update(margin, mcorrect)
        margin1.update(margin, mcorrect)

        if SeriesStepCounter >= len(p) / 100:
            gameSeries1.append(margin1.current)
            gameSeries2.append(margin2.current)
            gameSeries3.append(margin3.current)
            SeriesStepCounter = 0

        if correct:
            c += 1

    print('percent correct winners: ', c / n * 100, '%')
    print('spread percent correct winners: ', s / n * 100, '%')
    print('expected value all games: ', ev / n * 100, '%')
    print('expected value over 1 point margins: ', margin1.correct, '/', margin1.count, '=', margin1.correct / margin1.count * 100, '%')
    print('spent:', round(margin1.count * 100), 'profits ', round((margin1.correct * 190.91) - (margin1.count * 100)), ' total :', round((margin1.correct * 190.91)))
    print('expected value over 2 point margins: ', margin2.correct, '/', margin2.count, '=', margin2.correct / margin2.count * 100, '%')
    print('spent:', round(margin2.count * 100), 'profits ', round((margin2.correct * 190.91) - (margin2.count * 100)), ' total :', round((margin2.correct * 190.91)))
    print('expected value over 3 point margins: ', margin3.correct, '/', margin3.count, '=', margin3.correct / margin3.count * 100, '%')
    print('spent:', round(margin3.count * 100), 'profits ', round((margin3.correct * 190.91) - (margin3.count * 100)), ' total :', round((margin3.correct * 190.91)))
    print('expected value over 4 point margins: ', margin4.correct, '/', margin4.count, '=', margin4.correct / margin4.count * 100, '%')
    print('spent:', round(margin4.count * 100), ' profits :', round((margin4.correct * 190.91) - (margin4.count * 100)), ' total :', round((margin4.correct * 190.91)))

    res = {}
    res['wl'] = round(c / n * 100)
    res['swl'] = round(s / n * 100)
    res['count'] = round(n)
    res['evMargin1'] = str(margin1.correct)
    res['evMargin1Count'] = str(margin1.count)
    res['evMargin1Pct'] = str(round(margin1.correct / margin1.count * 100))
    res['evMargin1Min'] = margin1.min_val
    res['evMargin1Max'] = margin1.max_val
    res['evMargin1Total'] = round((margin1.count * 100))
    res['evMargin1Profit'] = round((margin1.correct * 190.91) - (margin1.count * 100))

    res['evMargin2'] = str(margin2.correct)
    res['evMargin2Count'] = str(margin2.count)
    res['evMargin2Pct'] = str(round(margin2.correct / margin2.count * 100))
    res['evMargin2Min'] = margin2.min_val
    res['evMargin2Max'] = margin2.max_val
    res['evMargin2Total'] = round((margin2.count * 100))
    res['evMargin2Profit'] = round((margin2.correct * 190.91) - (margin2.count * 100))

    res['evMargin3'] = str(margin3.correct)
    res['evMargin3Count'] = str(margin3.count)
    res['evMargin3Pct'] = str(round(margin3.correct / margin3.count * 100))
    res['evMargin3Min'] = margin3.min_val
    res['evMargin3Max'] = margin3.max_val
    res['evMargin3Total'] = round((margin3.count * 100))
    res['evMargin3Profit'] = round((margin3.correct * 190.91) - (margin3.count * 100))

    res['evMargin4'] = str(margin4.correct)
    res['evMargin4Count'] = str(margin4.count)
    res['evMargin4Pct'] = str(round(margin4.correct / margin4.count * 100))
    res['evMargin4Min'] = margin4.min_val
    res['evMargin4Max'] = margin4.max_val
    res['evMargin4Total'] = round((margin4.count * 100))
    res['evMargin4Profit'] = round((margin4.correct * 190.91) - (margin4.count * 100))

    res['gameSeries1'] = gameSeries1
    res['gameSeries2'] = gameSeries2
    res['gameSeries3'] = gameSeries3

    eval_ = {}
    eval_['correct'] = c
    eval_['wrong'] = n - c
    eval_['spreadCorrect'] = s
    eval_['spreadWrong'] = n - s
    eval_['evMargin1'] = margin1.correct
    eval_['evMargin1wrong'] = margin1.count - margin1.correct
    eval_['evMargin2'] = margin2.correct
    eval_['evMargin2wrong'] = margin2.count - margin2.correct
    eval_['evMargin3'] = margin3.correct
    eval_['evMargin3wrong'] = margin3.count - margin3.correct

    return [eval_, res]


def webappTrain(modelNum, epochs, size, layer1Count, layer1Activation, layer2Count, layer2Activation, optimizer, username, es, rmw, kr, streaks, wl, gp, ps, players, ast, blk, reb, fg3, fg, ft, pf, pts, stl, turnover):
    logger = setup_logging(username, modelNum)
    with log_stdout(logger):
        labels = ['ast', 'blk', 'dreb', 'fg3_pct', 'fg3a', 'fg3m', 'fga', 'fgm', 'fta', 'ftm', 'oreb', 'pf', 'pts', 'reb', 'stl', 'turnover', 'min']
        print('players-------------', players)

        path = "csv/train.csv"
        test_path = "csv/test.csv"

        current_time = str(time.time())
        data = pd.read_csv(path)
        homeScore = data['home_score'].values
        visitorScore = data['visitor_score'].values
        home_id = data['home_id'].values
        visitor_id = data['visitor_id'].values

        columns_to_drop = ['home_score', 'visitor_score', 'gameid', 'home_id', 'visitor_id', 'home_history_gameid', 'visitor_history_gameid', 'home_history2_gameid', 'visitor_history2_gameid']

        if streaks != 'true':
            columns_to_drop = columns_to_drop + ['home_streak', 'visitor_streak']
        if wl != 'true':
            columns_to_drop = columns_to_drop + ['hw', 'hl', 'vw', 'vl']
        if gp != 'true':
            columns_to_drop = columns_to_drop + ['hgp', 'vgp']
        if ps != 'true':
            columns_to_drop.append('spread')

        for currentPlayer in range(int(players), 7):
            team_prefixes = ['home_', 'visitor_']
            for foo in team_prefixes:
                for label in labels:
                    stat = foo + str(currentPlayer) + '_' + label
                    columns_to_drop.append(stat)

        features = ['min']
        if ast == 'true':
            features.append('ast')
        if blk == 'true':
            features.append('blk')
        if reb == 'true':
            features.append('dreb')
            features.append('oreb')
        if fg3 == 'true':
            features.append('fg3m')
            features.append('fg3a')
        if fg == 'true':
            features.append('fga')
            features.append('fgm')
        if ft == 'true':
            features.append('fta')
            features.append('ftm')
        if pf == 'true':
            features.append('pf')
        if pts == 'true':
            features.append('pts')
        if stl == 'true':
            features.append('stl')
        if turnover == 'true':
            features.append('turnover')

        for currentPlayer in range(0, int(players)):
            team_prefixes = ['home_', 'visitor_']
            for foo in team_prefixes:
                for label in labels:
                    if label not in features:
                        stat = foo + str(currentPlayer) + '_' + label
                        columns_to_drop.append(stat)

        print(columns_to_drop)
        data.drop(columns_to_drop, axis=1, inplace=True)
        data.fillna(0, inplace=True)
        data = data.values
        data = data.astype(float)

        x_train, x_test, y_train, y_test = train_test_split(data, np.column_stack((homeScore, visitorScore)), test_size=0.0001)

        if kr == 'true':
            model = tf.keras.Sequential([
                tf.keras.layers.Dense(layer1Count, activation=layer1Activation, kernel_regularizer=tf.keras.regularizers.l2(0.001)),
                tf.keras.layers.Dense(layer2Count, activation=layer2Activation, kernel_regularizer=tf.keras.regularizers.l2(0.001)),
                tf.keras.layers.Dense(2, activation='linear'),
            ])
        else:
            model = tf.keras.Sequential([
                tf.keras.layers.Dense(layer1Count, activation=layer1Activation),
                tf.keras.layers.Dense(layer2Count, activation=layer2Activation),
                tf.keras.layers.Dense(2, activation='linear'),
            ])

        if rmw == 'true':
            early_stopping = tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                restore_best_weights=True,
                patience=4, verbose=0, mode='auto')
        else:
            early_stopping = tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                restore_best_weights=False,
                patience=4, verbose=0, mode='auto')

        log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

        model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])
        logger = setup_logging(username, modelNum)
        direct_write_logger_callback = DirectWriteLoggerCallback(logger)

        if es == 'true':
            model.fit(x_train, y_train, epochs=epochs, validation_split=0.1, batch_size=size, callbacks=[tensorboard, early_stopping, direct_write_logger_callback], shuffle=False)
        else:
            model.fit(x_train, y_train, epochs=epochs, validation_split=0.1, batch_size=size, callbacks=[tensorboard, direct_write_logger_callback], shuffle=False)

        model.save_weights('./userModels/' + username.username + '/' + str(modelNum) + '/checkpoints/my_checkpoint')

        data = pd.read_csv(test_path)
        data.fillna(0, inplace=True)

        homeTestScore = data['home_score'].values
        visitorTestScore = data['visitor_score'].values
        spread = data['spread'].values
        data.drop(columns_to_drop, axis=1, inplace=True)
        data = data.values
        data = data.astype(float)

        return print_prediction(model, data, homeTestScore, visitorTestScore, spread)
