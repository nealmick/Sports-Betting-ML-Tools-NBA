import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split
import datetime

if __name__ == '__main__':
    path = "csv/train.csv"
    test_path = "csv/test.csv"
    current_time = str(time.time())

    data = pd.read_csv(path)

    homeScore = data['home_score'].values
    visitorScore = data['visitor_score'].values
    data.drop(['home_score', 'visitor_score', 'gameid'], axis=1, inplace=True)

    data = data.values
    data = data.astype(float)

    x_train, x_test, y_train, y_test = train_test_split(data, np.column_stack((homeScore, visitorScore)), test_size=0.0001)

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(2, activation='linear'),
    ])

    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=25, validation_split=0.1, batch_size=64, callbacks=[tensorboard_callback], shuffle=True)
    model.save_weights('./checkpoints/my_checkpoint')

    data = pd.read_csv(test_path)
    homeTestScore = data['home_score'].values
    visitorTestScore = data['visitor_score'].values
    spread = data['spread'].values

    data.drop(['gameid', 'home_score', 'visitor_score'], axis=1, inplace=True)

    data = data.values
    data = data.astype(float)

    def print_prediction(model, data):
        p = model.predict(data)
        c = 0
        n = 0
        s = 0
        ev = 0

        evMargin4Count = 0
        evMargin4 = 0

        evMargin3Count = 0
        evMargin3 = 0
        evMargin2Count = 0
        evMargin2 = 0
        evMargin1Count = 0
        evMargin1 = 0

        for i in range(len(p)):
            correct = False
            spreadCorrect = False
            pmscore = round(homeTestScore[i]-visitorTestScore[i])
            pmp = p[i][0]-p[i][1]
            n+=1
            spread[i]=spread[i]*-1

            if spread[i]>0 and homeTestScore[i]>visitorTestScore[i]:
                spreadCorrect = True
                s +=1
            if spread[i]<0 and homeTestScore[i]<visitorTestScore[i]:
                s +=1
                spreadCorrect = True

            if p[i][0] > p[i][1] and homeTestScore[i] > visitorTestScore[i]:
                correct = True
            elif p[i][0] < p[i][1] and homeTestScore[i] < visitorTestScore[i]:
                correct = True
            spreadError = abs(spread[i]-pmscore)
            predictionError = abs(pmp-pmscore)

            pred = ''
            if spread[i]>pmp and pmp <0:
                pred = 0
            elif spread[i]>pmp and pmp >0:
                pred = 0
            elif spread[i]<pmp and pmp <0:
                pred = 1
            elif spread[i]<pmp and pmp >0:
                pred = 1
            swin = ''
            if spread[i]>pmscore and pmscore <0:
                swin = 0
            elif spread[i]>pmscore and pmscore >0:
                swin = 0
            elif spread[i]<pmscore and pmscore <0:
                swin = 1
            elif spread[i]<pmscore and pmscore >0:
                swin = 1
            mcorrect = True
            if pred == 0 and swin == 0:
                ev +=1
                print('correct agaist spread',pred,swin)
            elif pred == 1 and swin == 1:
                ev +=1
                print('correct agaist spread',pred,swin)
            else:
                mcorrect = False
                print('wrong agaist spread',pred,swin)

            if abs(pmp-spread[i]) > 4:
                evMargin4Count+=1
                if mcorrect:
                    evMargin4+=1

            if abs(pmp-spread[i]) > 3:
                evMargin3Count+=1
                if mcorrect:
                    evMargin3+=1

            if abs(pmp-spread[i]) > 2:
                evMargin2Count+=1
                if mcorrect:
                    evMargin2+=1

            if abs(pmp-spread[i]) > 1:
                evMargin1Count+=1
                if mcorrect:
                    evMargin1+=1

            print('spread:',spreadCorrect,spread[i], 'prediction: ',correct,round(p[i][0]),round(p[i][1]),'=',round(p[i][0]-p[i][1]),' actual:' ,homeTestScore[i],visitorTestScore[i],'=',pmscore)

            print('#-------------------------------------------#')
            if correct:
                c+=1
        print('percent correct winners: ', c/n*100,'%')
        print('spread percent correct winners: ', s/n*100,'%')
        print('expected value all games: ', ev/n*100,'%')
        print('expected value over 1 point margins: ',evMargin1,'/',evMargin1Count,'=', evMargin1/evMargin1Count*100,'%')
        print('spent:', round(evMargin1Count*100),'profits ',round((evMargin1 * 190.91)-(evMargin1Count*100)),' total :',round((evMargin1 * 190.91)))
        print('expected value over 2 point margins: ',evMargin2,'/',evMargin2Count,'=', evMargin2/evMargin2Count*100,'%')
        print('spent:', round(evMargin2Count*100),'profits ',round((evMargin2 * 190.91)-(evMargin2Count*100)),' total :',round((evMargin2 * 190.91)))
        print('expected value over 3 point margins: ',evMargin3,'/',evMargin3Count,'=', evMargin3/evMargin3Count*100,'%')
        print('spent:', round(evMargin3Count*100),'profits ',round((evMargin3 * 190.91)-(evMargin3Count*100)),' total :',round((evMargin3 * 190.91)))
        print('expected value over 4 point margins: ',evMargin4,'/',evMargin4Count,'=', evMargin4/evMargin4Count*100,'%')
        print('spent:', round(evMargin4Count*100),' profits :',round((evMargin4 * 190.91)-(evMargin4Count*100)),' total :',round((evMargin4 * 190.91)))

    print_prediction(model, data)
