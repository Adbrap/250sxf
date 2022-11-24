#----- initialistion des modules -----#
import pandas as pd
import numpy
from tkinter import Tk
from tkinter import messagebox
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import requests
import datetime
from numpy import *
from matplotlib.pyplot import *
import colorama
from colorama import Fore
import os
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
#----- initialistion des modules -----#

#----- initialistion des couleurs du modules pystyle -----#
class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
    PURPLE = '\033[35m'  # PURPLE
w = Fore.WHITE
b = Fore.BLACK
g = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX
m = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLUE_EX
#----- initialistion des couleurs du modules pystyle -----#


#----- initialistion des temps de recherches -----#
date = datetime.datetime.now()
my_lock = threading.RLock()
end = str(pd.Timestamp.today() + pd.DateOffset(5))[0:10]
start_15m = str(pd.Timestamp.today() + pd.DateOffset(-10000))[0:10]
start_30m = str(pd.Timestamp.today() + pd.DateOffset(-3))[0:10]
start_1h = str(pd.Timestamp.today() + pd.DateOffset(-100))[0:10]
start_6h = str(pd.Timestamp.today() + pd.DateOffset(-20))[0:10]
start_1d = str(pd.Timestamp.today() + pd.DateOffset(-30))[0:10]
start_1week = str(pd.Timestamp.today() + pd.DateOffset(-120))[0:10]
start_1month = str(pd.Timestamp.today() + pd.DateOffset(-240))[0:10]
#----- initialistion des temps de recherches -----#

#----- initialistion de l'API key -----#
api_key = '1KsqKOh1pTAJyWZx6Qm9pvnaNcpKVh_8'
#----- initialistion de l'API key -----#

#----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('les courbes ne se coupent pas')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
#----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#



def Finder_iete(time1, time_name1, start1):
    #----- initialisation des pointers -----#
    i = 0
    fa = 0
    fb = 1
    fc = 1
    fd = 2
    fe = 2
    ff = 3
    fg = 3
    compteur = 0
    #----- initialisation des pointers -----#

    objectif_name = 'Objectif à 50%'

    while i != 1:

        with my_lock:


            #----- recuperations des donnees polygons.io -----#
            api_url_OHLC = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time1}/{time_name1}/{start1}/{end}?adjusted=true&limit=50000&apiKey={api_key}'

            #----- recuperations des donnees polygons.io -----#

            #----- creation des df -----#
            data = requests.get(api_url_OHLC).json()
            df = pd.DataFrame(data['results'])
            #----- creation des df -----#

            #----- pour augmenter le temps dans le fichier txt -----#
            file = open('compteur_nombre_temps.txt', 'r')
            compteur_nombre_temps = int(file.read())
            file.close()

            file = open('compteur_nombre_temps.txt', 'w')
            compteur_nombre_temps = compteur_nombre_temps + len(df)
            file.write(f'{compteur_nombre_temps}')
            file.close()
            file.close()

            file = open('timeset.txt', 'w')
            file.write(f'{time1} {time_name1} - {objectif_name}')
            file.close()
            file.close()
            #----- pour augmenter le temps dans le fichier txt -----#





        #----- creation des local(min/max) -----#
        local_max = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]
        local_max1 = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min1 = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]

        local_max2 = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min2 = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]

        local_max3 = argrelextrema(df['v'].values, np.greater, order=1, mode='clip')[0]
        local_min3 = argrelextrema(df['v'].values, np.less, order=1, mode='clip')[0]
        #----- creation des local(min/max) -----#

        #----- suppresion des points morts de la courbe -----#
        test_min = []
        test_max = []

        if local_min[0] > local_max[0]:
            local_max = local_max[1:]
            print('oui')

        q = 0
        p = 0

        len1 = len(local_min)
        len2 = len(local_max)
        while p < len1-5 or p < len2-5:
            if local_min[p+1] < local_max[p]:
                test_min.append(local_min[p])
                local_min = np.delete(local_min, p)


                p = p - 1
            if local_max[p + 1] < local_min[p+1]:
                test_max.append(local_max[p])
                local_max = np.delete(local_max, p)

                p = p - 1
            p = p + 1

            len1 = len(local_min)
            len2 = len(local_max)



        highs = df.iloc[local_max, :]
        lows = df.iloc[local_min, :]
        highs1 = df.iloc[test_max, :]
        lows1 = df.iloc[test_min, :]

        decalage = 0

        #----- suppresion des points morts de la courbe -----#
        while i != 1:

            if ((len(df.iloc[local_max, :])) - (ff + 1)) > 3 and ((len(df.iloc[local_min, :])) - (ff + 1)) > 4:

                A = float(highs['c'].iloc[fa])
                B = float(lows['c'].iloc[fb])
                C = float(highs['c'].iloc[fc])
                D = float(lows['c'].iloc[fd])
                E = float(highs['c'].iloc[fe])
                F = float(lows['c'].iloc[ff])
                G = float(highs['c'].iloc[fg])

#
                if C > E:
                    differ = (C-E)
                    pas = (local_max[fe] - local_max[fc])
                    suite = differ / pas
                if C < E:
                    differ = (E - C)
                    pas = (local_max[fe] - local_max[fc])
                    suite = differ / pas

                print('--- Mode recherche', nom, time1, time_name1, ' ---', flush=True)



                data_A = []
                data_B = []
                data_C = []
                data_D = []
                data_E = []
                data_F = []
                data_G = []

                rouge = []
                vert = []
                bleu = []

                rouge.append(local_max[fa])
                rouge.append(local_min[fb])
                rouge.append(local_max[fc])
                rouge.append(local_min[fd])
                rouge.append(local_max[fe])
                rouge.append(local_min[ff])
                rouge.append(local_max[fg])

                vert.append(local_max[fa])
                vert.append(local_max[fc])
                vert.append(local_max[fe])
                vert.append(local_max[fg])
                i = 0
                for i in range(local_min[fa] - 1, local_max[ff] + 5):
                    bleu.append(i)

                mirande2 = df.iloc[vert, :]
                mirande = df.iloc[rouge, :]
                mirande3 = df.iloc[bleu, :]


                if E > C:
                    mirande2['c'].values[0] = mirande2['c'].values[1] - ((suite * (local_max[fc] - local_max[fa])))
                    mirande2['c'].values[3] = mirande2['c'].values[2] + ((suite * (local_max[fg] - local_max[fe])))
                if E < C:
                    mirande2['c'].values[0] = mirande2['c'].values[1] + ((suite * (local_max[fc] - local_max[fa])))
                    mirande2['c'].values[3] = mirande2['c'].values[2] - ((suite * (local_max[fg] - local_max[fe])))
                if E == C:
                    mirande2['c'].values[0] = df['c'].values[local_max[fc]]
                    mirande2['c'].values[3] = df['c'].values[local_max[fe]]

                vert1 = {'c': vert}
                vert2 = pd.DataFrame(data=vert1)
                rouge1 = {'c': rouge}
                rouge2 = pd.DataFrame(data=rouge1)
                bleu1 = {'c': bleu}
                bleu2 = pd.DataFrame(data=bleu1)
                # --- premier droite ---#
                AI = [local_max[fa], mirande2['c'].iloc[0]]
                BI = [local_max[fc], mirande2['c'].iloc[1]]

                # --- deuxieme droite ---#
                CI = [local_max[fa], A]
                DI = [local_min[fb], B]
                #I = line_intersection((AI, BI), (CI, DI))

                #----------------------------------------------------------------------------#
                #----------------------------------------------------------------------------#

                AJ = [local_max[fe], mirande2['c'].iloc[2]]
                BJ = [local_max[fg], mirande2['c'].iloc[3]]

                # --- deuxieme droite ---#
                CJ = [local_max[fg], G]
                DJ = [local_min[ff], F]
                #J = line_intersection((AJ, BJ), (CJ, DJ))
                pop = 0
                verif = 0

                for pop in range(0, len(test_min)):
                    if test_min[pop] > local_max[fa] and test_min[pop] < local_max[fg]:
                        verif = verif + 1
                pop = 0
                for pop in range(0, len(test_max)):
                    if test_max[pop] > local_max[fa] and test_max[pop] < local_max[fg]:
                        verif = verif + 1

                #moyenne_epaule1 = ((I[1] - B) +(C - B))/2
                #moyenne_epaule2 =((E - F) + (J[1] - F))/2
                #moyenne_tete = ((C - D) + (E - D))/2

                def rsi(df, periods=14, ema=True):

                    close_delta = df['c'].diff()

                    # Make two series: one for lower closes and one for higher closes
                    up = close_delta.clip(lower=0)
                    down = -1 * close_delta.clip(upper=0)

                    if ema == True:
                        # Use exponential moving average
                        ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
                        ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
                    else:
                        # Use simple moving average
                        ma_up = up.rolling(window=periods, adjust=False).mean()
                        ma_down = down.rolling(window=periods, adjust=False).mean()

                    rsi = ma_up / ma_down
                    rsi = 100 - (100 / (1 + rsi))
                    return rsi

                if (C - B) < (C - D) and (C - B) < (E - D) and (E- F) < (E - D) and (E - F) < (C - D) and B > D and F > D  and B < C and F < E and A >= mirande2['c'].iloc[0] and verif == 0 :
                    try:
                        j = [0, 0]
                        J = line_intersection((AJ, BJ), (CJ, DJ))
                        I = line_intersection((AI, BI), (CI, DI))
                        accept = True
                    except:
                        accept = False
                    if accept == True:
                        moyenne_epaule1 = ((I[1] - B) + (C - B)) / 2
                        moyenne_epaule2 = ((E - F) + (J[1] - F)) / 2
                        moyenne_tete = ((C - D) + (E - D)) / 2

                        #------------------ determinage de la place de la premiere cloture apres ligne de coup ----------------#
                        tuche = 0
                        noo = 0
                        place_pc = 0

                        point_max = J[0] + ((J[0] - I[0]))
                        point_max = int(round(point_max, 0))

                        while tuche != 1:
                            if df['c'].values[local_min[ff]+noo] >= J[1] and local_min[ff]+noo <= point_max and local_min[ff]+noo > local_min[ff]:
                                place_pc = local_min[ff]+noo
                                tuche = 1
                            if noo >= 10:
                                tuche = 1
                            noo = noo +1
                        df['rsi'] = rsi(df)
                        if df['v'].values[local_max[fa]] > df['v'].values[local_max[fa]+1] :
                            Z = local_max[fa] +2
                            essoufflement = False
                            stop = 0
                            while stop != 1 :
                                if Z == place_pc-1 or Z > place_pc-1:
                                    stop = 1
                                if df['v'].values[Z] > (df['v'].values[Z - 1] + df['v'].values[Z - 2]) / 2:
                                    essoufflement = False
                                    stop = 1
                                if df['v'].values[Z] <= (df['v'].values[Z-1]+df['v'].values[Z-2]) /2 :
                                    essoufflement = True
                                Z = Z +1
                        macd_croisee = False
                        try:
                            if df['e9'].iloc[place_pc] < df['MACD'].iloc[place_pc]:
                                macd_croisee = True
                        except:
                            print('probleme inconnu!')
                        #------------------ determinage de la place de la premiere cloture apres ligne de coup ----------------#
                        if I[1] > B and J[1] > F and moyenne_epaule1 <= moyenne_tete/2 and moyenne_epaule2 <= moyenne_tete/2 and moyenne_epaule1 >= moyenne_tete/4 and moyenne_epaule2 >= moyenne_tete/4 and df['c'].values[place_pc] <= J[1] + (moyenne_tete) / 4 and df['c'].values[place_pc] >= J[1]  and G >= j[1] and place_pc <= J[0] and place_pc < local_max[fg] and accept == True :#and df['rsi'].values[place_pc] > df['rsi'].values[place_pc-1]  :#and C < E and moyenne_epaule1 < moyenne_epaule2 and df['v'].values[place_pc-1] <= (df['v'].values[place_pc]) - ((df['v'].values[place_pc]*25)/100):#  and macd_croisee == True: #and essoufflement==True :# and (F-D) > (D-B) - (((D-B)*25)/100) and (F-D) < (D-B) + (((D-B)*25)/100) :# :

                            compteur = compteur + 1


                            def sma(data, window):
                                sma = data.rolling(window=window).mean()
                                return sma

                            df['sma_20'] = sma(df['c'], 20)
                            df.tail()

                            def bb(data, sma, window):
                                std = data.rolling(window=window).std()
                                upper_bb = sma + std * 2
                                lower_bb = sma - std * 2
                                return upper_bb, lower_bb

                            df['upper_bb'], df['lower_bb'] = bb(df['c'], df['sma_20'], 20)
                            df.tail()

                            def createMACD(df):
                                df['e26'] = pd.Series.ewm(df['c'], span=26).mean()
                                df['e12'] = pd.Series.ewm(df['c'], span=12).mean()
                                df['MACD'] = df['e12'] - df['e26']
                                df['e9'] = pd.Series.ewm(df['MACD'], span=9).mean()
                                df['HIST'] = df['MACD'] - df['e9']

                            createMACD(df)



                           # macd = ""
                           # volume = ""
                           # boolinger = "PAS DE BULLE BANDES DE BOLLINGER"
                           # tendance = ""
#
                           # #if df['c'].values[ff] > df['upper_bb'].values[ff] and df['c'].values[local_max2[ff]] > \
                            #        df['upper_bb'].values[local_max2[ff]]:
                            #    print('-- ATTENTION BULLE BANDES DE BOLLINGER --')
                            #    boolinger = "BULLE BANDES DE BOLLINGER BAISSIERE"
#
                            #if df['c'].values[ff] < df['lower_bb'].values[ff] or df['c'].values[local_min2[ff]] < \
                            #        df['lower_bb'].values[local_min2[ff]]:
                            #    print('-- EN BULLE DE BOLLINGER HAUSSIERE --')
                            #    boolinger = "BULLE BANDES DE BOLLINGER HAUSSIERE"
#
                            #if local_max3[ff] > local_min3[ff] and df['v'].values[ff] < df['v'].values[local_max3[ff]]:
                            #    print('-- LE VOLUME DESCEND --')
                            #    volume = "DESCEND"
                            #else:
                            #    print('-- LE VOLUME MONTE --')
                            #    volume = "MONTE"
#
                           # if local_max2[-1] > local_min21[-1] and df2['c'].values[-1] > df2['c'].values[local_max21[-1]]:
                           #     print('-- EN TENDANCE BAISSIERE --')
                           #     tendance = "BAISSIERE"
                           # else:
                           #     print('-- EN TENDANCE HAUSSIERE --')
                           #     tendance = "HAUSSIERE"

                            #if df['HIST'].values[ff] > df['HIST'].values[ff - 1]:
                            #    print('-- MACD QUI MONTE --')
                            #    macd = "MONTE"
                            #else:
                            #    print('-- MACD QUI DESCEND --')
                            #    macd = "DESCEND"

                            fig = plt.figure(figsize=(10, 7))

                            #fig.patch.set_facecolor('#17abde')


                            plt.plot([], [], ' ')

                            file = open('compteur_images.txt', 'r')
                            compteur_nombre_image = int(file.read())
                            file.close()
                            heure_debut = ((df['t'].iloc[local_max[fa]])/1000)  # ATTENTION ENLEVER L'AJOUT DES 6H SUR LES AUTRES ORDINATEURS
                            heure_fin = ((df['t'].iloc[local_max[fg]])/1000)  # ATTENTION ENLEVER L'AJOUT DES 6H SUR LES AUTRES ORDINATEURS
                            temps_debut = datetime.datetime.fromtimestamp(heure_debut)
                            temps_demarrage = temps_debut.strftime('%Y-%m-%d')

                            plt.title(f'IETE : {compteur} | {nom} | {time1} {time_name1} | {compteur_nombre_image+1} | {temps_demarrage}', fontweight="bold", color='black')
                            mirande3['c'].plot(color=['blue'], label ='Clotures', alpha=0.3)
                            mirande3['h'].plot(color=['orange'], label='highs')
                            #mirande['c'].plot(color=['#FF0000'])
                            mirande2['c'].plot(color=['green'], linestyle='--', label ='Ligne de coup')


                            plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label ='100% objectif')
                            plt.axhline(y=J[1] + (((moyenne_tete)/2)+ ((moyenne_tete) / 4)), linestyle='--', alpha=0.3, color='black',label='75% objectif')
                            plt.axhline(y=J[1] + (moyenne_tete)/2, linestyle='--', alpha=0.3, color='orange', label ='50% objectif')
                            plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black',label='25% objectif')
                            plt.grid(visible=True, which='major', color='#666666', linestyle='-', alpha=0.1)
                            taille_diviser = (local_max[fe] - local_max[fc]) / (local_min[fd] - local_max[fc])
                            #point_max = J[0]+((J[0] - I[0])/taille_diviser)

                            plt.scatter(point_max, df['c'].values[int(round(point_max, 0))], color='red', label ='Max temps realisation')
                            plt.scatter(place_pc, df['c'].values[place_pc], color='orange',label='PC')
                            plt.legend()

                            plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
                            plt.text(J[0], J[1] + (moyenne_tete)/2, f"{round((J[1] + (moyenne_tete)/2),2)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
                            plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
                            plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
                            plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='red', wrap=True)
                            plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
                            plt.text(local_min[ff], F, f"F   {round(F,2)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
                            plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='red', wrap=True)
                            plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
                            plt.text(J[0], J[1], f"J {round(J[1],2)}", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
                            test_valeur =df['c'].iloc[round(J[0])+1]
                            plt.text(round(J[0]), df['c'].iloc[round(J[0])], f"J+1 {test_valeur}", ha='left', style='normal', size=10.5,color='#00FF36', wrap=True)

                            plt.scatter(I[0], I[1], color='green')
                            plt.scatter(J[0], J[1], color='green')


                            # -----------------------lire et connaitre nom de image et enregistrer image--------------------------#

                            file = open('compteur_images.txt', 'w')
                            compteur_nombre_image = compteur_nombre_image + 1
                            file.write(f'{compteur_nombre_image}')
                            file.close()
                            plt.savefig(f'images/figure_{compteur_nombre_image}_r1.png')

                            # -----------------------lire et connaitre nom de image et enregistrer image--------------------------#

                            #fig = plt.figure(figsize=(10, 7))
##
                            ##fig.patch.set_facecolor('#17abde')
##
##
                            #plt.plot([], [], ' ')
##
                            ##plt.subplot(3, 1, 1)
                            #plt.title(f'IETE : {compteur} | {nom} | {time1} {time_name1} | {compteur_nombre_image}', fontweight="bold", color='black')
                            #mirande3['c'].plot(color=['blue'], alpha=0.3, label ='Clotures')
                            #mirande2['c'].plot(color=['green'], alpha=0.3, linestyle='--', label ='Ligne de coup')
##
##
##
                            #width = .4
                            #width2 = .05
##
                            ## define up and down prices
                            #up = mirande3[mirande3.c >= mirande3.o]
                            #down = mirande3[mirande3.c < mirande3.o]
##
                            ## define colors to use
                            #col1 = 'green'
                            #col2 = 'red'
##
                            ## plot up prices9
                            #plt.bar(up.index, up.c - up.o, width, bottom=up.o, color=col1, label ='Bougies Japonnaises')
                            #plt.bar(up.index, up.h - up.c, width2, bottom=up.c, color=col1)
                            #plt.bar(up.index, up.l - up.o, width2, bottom=up.o, color=col1)
##
                            ## plot down prices
                            #plt.bar(down.index, down.c - down.o, width, bottom=down.o, color=col2)
                            #plt.bar(down.index, down.h - down.o, width2, bottom=down.o, color=col2)
                            #plt.bar(down.index, down.l - down.c, width2, bottom=down.c, color=col2)
                            #plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                            #plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='blue', wrap=True)
##
##
                            #plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
                            #plt.legend()
                            ## -----------------------lire et connaitre nom de image et enregistrer image--------------------------#
##
                            #plt.savefig(f'/home/yumin/Desktop/admatv2/btest/iete/images/figure_{compteur_nombre_image}_v1.png')
##
                            ### -----------------------lire et connaitre nom de image et enregistrer image--------------------------#
#
#
#
#
                            fig = plt.figure(figsize=(10, 7))
#
                            #fig.patch.set_facecolor('#17abde')
#
#
                            plt.plot([], [], ' ', label="e")
#
#
#
                            plt.title(f'IETE : {compteur} | {nom} | {time1} {time_name1} | {compteur_nombre_image}', fontweight="bold", color='black')
                            plt.bar(df['v'][(local_max[fa]):(local_max[fg])+1].index, df['v'].values[(local_max[fa]):(local_max[fg])+1])
                            plt.legend(['Volumes'])
#
                            plt.text(local_max[fa], df['v'][(local_max[fa])], "A", ha='left', style='normal', size=10.5, color='red',
                                     wrap=True)
                            plt.text(local_min[fb], df['v'][(local_min[fb])], "B", ha='left', style='normal', size=10.5, color='red',
                                     wrap=True)
                            plt.text(local_max[fc], df['v'][(local_max[fc])], "C", ha='left', style='normal', size=10.5, color='red',
                                     wrap=True)
                            plt.text(local_min[fd], df['v'][(local_min[fd])], "D", ha='left', style='normal', size=10.5, color='red',
                                     wrap=True)
                            plt.text(local_max[fe], df['v'][(local_max[fe])], "E", ha='left', style='normal', size=10.5, color='red',
                                     wrap=True)
                            plt.text(local_min[ff], df['v'][(local_min[ff])], "F", ha='left', style='normal', size=10.5, color='red',
                                     wrap=True)
                            plt.text(local_max[fg], df['v'][(local_max[fg])], "G", ha='left', style='normal', size=10.5, color='red',
                                     wrap=True)
#
                            #plt.subplot(2, 1, 2)
#
                            #df['rsi'].iloc[(local_min[fa] - 1):(local_max[ff] + 5)].plot(color=['purple'], alpha=0.6)
                            #plt.axhline(y=30, alpha=0.3, color='black')
                            #plt.axhline(y=70, alpha=0.3, color='black')
                            #plt.axhline(y=50,  linestyle='--', alpha=0.3, color='grey')
                            #plt.legend(['Rsi'])
#
                            #plt.text(local_max[fa], df['rsi'].iloc[local_max[fa]], "A", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_min[fb], df['rsi'].iloc[local_min[fb]], "B", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_max[fc], df['rsi'].iloc[local_max[fc]], "C", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_min[fd], df['rsi'].iloc[local_min[fd]], "D", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_max[fe], df['rsi'].iloc[local_max[fe]], "E", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_min[ff], df['rsi'].iloc[local_min[ff]], "F", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            #plt.text(local_max[fg], df['rsi'].iloc[local_max[fg]], "G", ha='left', style='normal', size=10.5, color='blue',
                            #         wrap=True)
                            ##plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                            ##plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='blue', wrap=True)
##
                            ## -----------------------lire et connaitre nom de image et enregistrer image--------------------------#
#
                # plt.savefig(f'images/figure_{compteur_nombre_image}_r2.png')
#
                            ## -----------------------lire et connaitre nom de image et enregistrer image--------------------------#
#
                            #fig = plt.figure(figsize=(10, 7))
#
                            ## fig.patch.set_facecolor('#17abde')
#
                            #plt.plot([], [], ' ')
#
                            #plt.subplot(2, 1, 1)
                            #plt.title(f'IETE : {compteur} | {nom} | {time1} {time_name1} | {compteur_nombre_image}', fontweight="bold", color='black')
                            #plt.bar(df['HIST'][(local_max[fa]-1):(local_max[fg]) + 5].index,df['HIST'].values[(local_max[fa]-1):(local_max[fg]) + 5], color='purple', alpha=0.6)
                            #df['MACD'].iloc[(local_max[fa] - 1):(local_max[fg] + 5)].plot(color=['blue'], alpha=0.6)
                            #df['e9'].iloc[(local_max[fa] - 1):(local_max[fg] + 5)].plot(color=['red'], alpha=0.6)
#
                            #plt.text(local_max[fa], df['HIST'].iloc[(local_max[fa])], "A", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                            #plt.text(local_min[fb], df['HIST'].iloc[(local_min[fb])], "B", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                            #plt.text(local_max[fc], df['HIST'].iloc[(local_max[fc])], "C", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                            #plt.text(local_min[fd], df['HIST'].iloc[(local_min[fd])], "D", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                            #plt.text(local_max[fe], df['HIST'].iloc[(local_max[fe])], "E", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                            #plt.text(local_min[ff], df['HIST'].iloc[(local_min[ff])], "F", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                            #plt.text(local_max[fg], df['HIST'].iloc[(local_max[fg])], "G", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                            ##plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
                            ##plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
##
#
#
#
                            #plt.legend(['Macd','Signal','histogramme'])
                            #a2 = plt.subplot(2, 1, 2)
                            #a2.axis('off')
                            #plt.axis([0, 10, 0, 10])
                            temps_formation = int((J[0] - I[0]) * time1)
                            heure_debut = ((df['t'].iloc[local_max[fa]])/1000)  # ATTENTION ENLEVER L'AJOUT DES 6H SUR LES AUTRES ORDINATEURS
                            heure_fin = ((df['t'].iloc[local_max[fg]])/1000)  # ATTENTION ENLEVER L'AJOUT DES 6H SUR LES AUTRES ORDINATEURS
                            temps_debut = datetime.datetime.fromtimestamp(heure_debut)
                            temps_fin = datetime.datetime.fromtimestamp(heure_fin)
                            #click = datetime.datetime.fromtimestamp(df['t'].iloc[local_max[fa]]).strftime('%Y-%m-%d %H:%M:%S')
                            g = 0
                            compteur2 = 0
                            resultat = "NE SAIS PAS"
                            fait_25  = 0
                            fait_50 = 0
                            fait_75 = 0
                            fait_100 = 0



                            while g !=1:
                                if df['c'].iloc[place_pc + compteur2] < F and fait_50 ==0:
                                    resultat = "PERDANT "
                                    file = open('compteur_perdant.txt', 'r')
                                    compteur_nombre_perdant = int(file.read())
                                    file.close()
                                    file = open('compteur_perdant.txt', 'w')
                                    compteur_nombre_perdant = compteur_nombre_perdant + 1
                                    file.write(f'{compteur_nombre_perdant}')
                                    file.close()
                                    file.close()
                                    file = open('gain_cumulé.txt', 'r')
                                    gain_cumulé = float(file.read())
                                    file.close()
                                    file = open('gain_cumulé.txt', 'w')
                                    #gain_cumulé = gain_cumulé - (((J[-1] - F )*100)/J[1])
                                    gain_cumulé = gain_cumulé - round((((df['c'].iloc[place_pc] - (df['c'].iloc[place_pc + compteur2]) )*100)/df['c'].iloc[place_pc]),2)
                                    file.write(f'{round(gain_cumulé,2)}')
                                    file.close()
                                    file.close()
                                    file = open('df.txt', 'r')
                                    df_gain = str(file.read())
                                    file.close()
                                    file = open('df.txt', 'w')
                                    valeur = round((((df['c'].iloc[place_pc] - (df['c'].iloc[place_pc + compteur2]) )*100)/df['c'].iloc[place_pc]),2)
                                    df_gain = df_gain.replace('%df_gain%',f'-{valeur}\n%df_gain%')
                                    file.write(f'{df_gain}')
                                    file.close()
                                    file.close()

                                    g = 1
                                if (df['h'].iloc[place_pc + compteur2] >= J[1] + (moyenne_tete)/4) and fait_25  == 0: # !!! MODIFIER NOM OBJECTIF EN HAUT !!!!
                                    fait_25 = 1
                                    file = open('Tobjectif_25.txt', 'r')
                                    Tobjectif_25 = int(file.read())
                                    file.close()
                                    file = open('Tobjectif_25.txt', 'w')
                                    Tobjectif_25 = Tobjectif_25 + 1
                                    file.write(f'{Tobjectif_25}')
                                    file.close()
                                    file.close()



                                if (df['h'].iloc[place_pc + compteur2] >= J[1] + (moyenne_tete)/2) and fait_50 == 0: # !!! MODIFIER NOM OBJECTIF EN HAUT !!!!
                                    fait_50 = 1
                                    resultat = "GAGNANT À 50%"
                                    file = open('compteur_gagnant.txt', 'r')
                                    compteur_nombre_gagnant = int(file.read())
                                    file.close()
                                    file = open('compteur_gagnant.txt', 'w')
                                    compteur_nombre_gagnant = compteur_nombre_gagnant + 1
                                    file.write(f'{compteur_nombre_gagnant}')
                                    file.close()
                                    file.close()

                                    file = open('gain_cumulé.txt', 'r')
                                    gain_cumulé = float(file.read())
                                    file.close()
                                    file = open('gain_cumulé.txt', 'w')
                                    gain_cumulé = gain_cumulé + round(((((J[1] + (moyenne_tete)/2) - (df['c'].iloc[place_pc]))*100)/df['c'].iloc[place_pc]),2)
                                    file.write(f'{round(gain_cumulé,2)}')
                                    file.close()
                                    file.close()

                                    file = open('df.txt', 'r')
                                    df_gain = str(file.read())
                                    file.close()
                                    file = open('df.txt', 'w')
                                    valeur2 = round(((((J[1] + (moyenne_tete)/2) - (df['c'].iloc[place_pc]))*100)/df['c'].iloc[place_pc]),2)
                                    df_gain = df_gain.replace('%df_gain%', f'{valeur2}\n%df_gain%')
                                    file.write(f'{df_gain}')
                                    file.close()
                                    file.close()

                                    file = open('Tobjectif_50.txt', 'r')
                                    Tobjectif_50 = int(file.read())
                                    file.close()
                                    file = open('Tobjectif_50.txt', 'w')
                                    Tobjectif_50 = Tobjectif_50 + 1
                                    file.write(f'{Tobjectif_50}')
                                    file.close()
                                    file.close()

                                if (df['h'].iloc[place_pc + compteur2] >= J[1] + (((moyenne_tete)/4) + ((moyenne_tete)/2))) and fait_75 == 0: # !!! MODIFIER NOM OBJECTIF EN HAUT !!!!
                                    fait_75 = 1
                                    file = open('Tobjectif_75.txt', 'r')
                                    Tobjectif_75 = int(file.read())
                                    file.close()
                                    file = open('Tobjectif_75.txt', 'w')
                                    Tobjectif_75 = Tobjectif_75 + 1
                                    file.write(f'{Tobjectif_75}')
                                    file.close()
                                    file.close()
                                if (df['h'].iloc[place_pc + compteur2] >= J[1] + (moyenne_tete)) and fait_100 == 0: # !!! MODIFIER NOM OBJECTIF EN HAUT !!!!
                                    fait_100 = 1
                                    file = open('Tobjectif_100.txt', 'r')
                                    Tobjectif_100 = int(file.read())
                                    file.close()
                                    file = open('Tobjectif_100.txt', 'w')
                                    Tobjectif_100 = Tobjectif_100 + 1
                                    file.write(f'{Tobjectif_100}')
                                    file.close()
                                    file.close()
                                    g = 1
                                if int(round(J[0], 0)) + compteur2 == int(point_max):
                                    g = 1
                                    if resultat == "NE SAIS PAS":
                                        resultat = "PERDANT MAIS SANS STOPLOSS"
                                        file = open('compteur_perdant.txt', 'r')
                                        compteur_nombre_perdant = int(file.read())
                                        file.close()
                                        file = open('compteur_perdant.txt', 'w')
                                        compteur_nombre_perdant = compteur_nombre_perdant + 1
                                        file.write(f'{compteur_nombre_perdant}')
                                        file.close()
                                        file.close()

                                        file = open('Tobjectif_NULL.txt', 'r')
                                        Tobjectif_NULL = int(file.read())
                                        file.close()
                                        file = open('Tobjectif_NULL.txt', 'w')
                                        Tobjectif_NULL = Tobjectif_NULL + 1
                                        file.write(f'{Tobjectif_NULL}')
                                        file.close()
                                        file.close()

                                        file = open('df.txt', 'r')
                                        df_gain = str(file.read())
                                        file.close()
                                        file = open('df.txt', 'w')
                                        df_gain = df_gain.replace('%df_gain%','0.0\n%df_gain%')
                                        file.write(f'{df_gain}')
                                        file.close()
                                        file.close()



                                compteur2 = compteur2+ 1


                            #plt.text(0, 8, f" ▶ LA FIGURE DEMARRE : {temps_debut.strftime('%Y-%m-%d %H:%M:%S')}", ha='left', style='normal', size=9.5, color='black',
                            #         wrap=True, alpha=1)
                            #plt.text(0, 6.5, f" ▶ LA FIGURE TERMINE : {temps_fin.strftime('%Y-%m-%d %H:%M:%S')}", ha='left', style='normal', size=9.5, color='black',
                            #         wrap=True, alpha=1)
                            #plt.text(0, 5, f" ▶ LE  POURCENTAGE GAIN EST : -", ha='left', style='normal', size=9.5, color='black', wrap=True,
                            #         alpha=1)
                            #plt.text(0, 3.5, f" ▶ L'INCLINAISON DE LDC EST : -", ha='left', style='normal', size=9.5, color='black', wrap=True,
                            #         alpha=1)
                            #plt.text(5, 8, f" ▶ LA TENDANCE PRECEDENTE EST : {tendance}", ha='left', style='normal', size=9.5,
                            #         color='black', wrap=True, alpha=1)
#
                            #plt.text(5, 6.5,
                            #         f" ▶ LE RSI DE F: {int(df['rsi'].iloc[local_min[ff]])}  I  LE RSI DE G:  {int(df['rsi'].iloc[local_max[fg]])}  I  LE RSI DE J:  {int(df['rsi'].iloc[int(round(J[0], 0))])}",
                            #         ha='left', style='normal',
                            #         size=9.5, color='black', alpha=1)
                            #plt.text(5, 5, f" ▶ LA FIGURE S'EST FORMÉE EN : {temps_formation} {time_name1}", ha='left',
                            #         style='normal', size=9.5,
                            #         color='black', wrap=True, alpha=1)
                            #plt.text(5, 3.5, f" ▶ SUCCÉS OU ECHEC : {resultat}", ha='left',
                            #         style='normal', size=9.5,
                            #         color='black', wrap=True, alpha=1)
                            ## -----------------------lire et connaitre nom de image et enregistrer image--------------------------#

                            #plt.savefig(f'/home/yumin/Desktop/admatv2/btest/iete/images/figure_{compteur_nombre_image}_v2.png')

                            # -----------------------lire et connaitre nom de image et enregistrer image--------------------------#

                            #fig = plt.figure(figsize=(10, 7))
                            #plt.title(f'IETE : {compteur} | {nom} | {time1} {time_name1} | {compteur_nombre_image}',fontweight="bold", color='black')
#
                            ## BB indicateur
                            #mirande3['c'].plot(color=['blue'], label='Clotures')
                            #mirande['c'].plot(color=['orange'], label='Forme figure', alpha=0.7)
                            #mirande2['c'].plot(color=['green'], alpha=0.3, linestyle='--', label='Ligne de coup')
#
                            #def sma(data, window):
                            #    sma = data.rolling(window=window).mean()
                            #    return sma
#
                            #df['sma_20'] = sma(df['c'], 20)
                            #df['sma_9'] = sma(df['c'], 9)
                            #df.tail()
#
                            #def bb(data, sma, window):
                            #    std = data.rolling(window=window).std()
                            #    upper_bb = sma + std * 2
                            #    lower_bb = sma - std * 2
                            #    return upper_bb, lower_bb
#
                            #df['upper_bb'], df['lower_bb'] = bb(df['c'], df['sma_20'], 20)
                            #df.tail()
#
                            #df['upper_bb'].iloc[(local_max[fa]-1):(local_max[fg]) + 5].plot(label='Haut Band', linestyle='--', linewidth=1, color='red')
                            #df['sma_20'].iloc[(local_max[fa]-1):(local_max[fg]) + 5].plot(label='Ema 20', linestyle='-', linewidth=1.2, color='grey')
                            #df['lower_bb'].iloc[(local_max[fa]-1):(local_max[fg]) + 5].plot(label='Bas Band', linestyle='--', linewidth=1, color='green')
                            ## df2['v'].plot(color=['orange'], ls='--', label='volume')
                            #plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='green', wrap=True)
                            #plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='green', wrap=True)
#
#
                            #plt.scatter(x=highs.iloc[fa:fg+1].index, y=highs['c'].iloc[fa:fg+1])
                            #plt.scatter(x=lows.iloc[fb-1:ff+2].index, y=lows['c'].iloc[fb-1:ff+2])
                            #plt.scatter(I[0], I[1], color='red')
                            #plt.scatter(J[0], J[1], color='red')
                            #plt.scatter(point_max, df['c'].values[int(round(point_max, 0))], color='red',label='Max temps realisation')
##
                            #plt.legend(loc='upper left')
                            # -----------------------lire et connaitre nom de image et enregistrer image--------------------------#

                            #plt.savefig(f'/home/yumin/Desktop/admatv2/btest/iete/images/figure_{compteur_nombre_image}_r3.png')

                            # -----------------------lire et connaitre nom de image et enregistrer image--------------------------#

                            #fig = plt.figure(figsize=(10, 7))
                            #plt.title(f'IETE : {compteur} | {nom} | {time1} {time_name1} | {compteur_nombre_image}',fontweight="bold", color='black')
#
                            #df['c'].iloc[(local_max[fa]-30):(local_max[fg]) + 30].plot(color=['blue'], label='Clotures')
                            #mirande['c'].plot(color=['orange'], label='Forme figure', alpha=0.7)
                            #mirande2['c'].plot(color=['green'], alpha=0.3, linestyle='--', label='Ligne de coup')
                            #df['sma_20'].iloc[(local_max[fa] - 30):(local_max[fg]) + 30].plot(color=['red'], label='Sma 20')
                            #df['sma_9'].iloc[(local_max[fa] - 30):(local_max[fg]) + 30].plot(color=['green'], label='Sma 9')
                            #plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='green',
                            #         wrap=True)
                            #plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='green', wrap=True)
                            #plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='green', wrap=True)
                            #plt.scatter(point_max, df['c'].values[int(round(point_max, 0))], color='red', label='Max temps realisation')
                            #plt.legend()



                            # -----------------------lire et connaitre nom de image et enregistrer image--------------------------#

                            #plt.savefig(f'/home/yumin/Desktop/admatv2/btest/iete/images/figure_{compteur_nombre_image}_v3.png')

                            # -----------------------lire et connaitre nom de image et enregistrer image--------------------------#

                            taille = (local_min[fa]) - 20
                            l = 0
                            l2 = 0
                            l3 = 0
                            while l != 1:
                                if local_min[l2] > taille:
                                    l3 = l2 - 1
                                    l = 1
                                if local_min[l2] < taille:
                                    l2 = l2 + 1
                                if local_min[l2] == taille:
                                    l3 = l2
                                    l = 1
                            l = 0
                            while l != 1:
                                if local_min[l2] > local_max[ff + 2]:
                                    l2 = l2 - 1
                                    l = 1
                                if local_min[l2] < local_max[ff + 2]:
                                    l2 = l2 + 1
                                if local_min[l2] == local_max[ff + 2]:
                                    l = 1

                            m = 0
                            m2 = 0
                            m3 = 0
                            while m != 1:

                                if local_max[m2] > taille:
                                    m3 = m2 - 1
                                    m = 1
                                if local_max[m2] < taille:
                                    m2 = m2 + 1
                                if local_max[m2] == taille:
                                    m3 = m2
                                    m = 1
                            m = 0
                            while m != 1:
                                if local_max[m2] > local_max[ff + 2]:
                                    m2 = m2 - 1
                                    m = 1
                                if local_max[m2] < local_max[ff + 2]:
                                    m2 = m2 + 1
                                if local_max[m2] == local_max[ff + 2]:
                                    m = 1


                            data_A.append(A)
                            data_B.append(B)
                            data_C.append(C)
                            data_D.append(D)
                            data_E.append(E)
                            data_F.append(F)
                            data_F.append(G)


                            data_A_ = pd.DataFrame(data_A, columns=['A'])
                            data_B_ = pd.DataFrame(data_B, columns=['B'])
                            data_C_ = pd.DataFrame(data_C, columns=['C'])
                            data_D_ = pd.DataFrame(data_D, columns=['D'])
                            data_E_ = pd.DataFrame(data_E, columns=['E'])
                            data_F_ = pd.DataFrame(data_E, columns=['F'])
                            data_G_ = pd.DataFrame(data_E, columns=['G'])
                            df_IETE = pd.concat([data_A_, data_B_, data_C_, data_D_, data_E_, data_F_, data_G_], axis=1)

                fa = fa + 1
                fb = fb + 1
                fc = fc + 1
                fd = fd + 1
                fe = fe + 1
                ff = ff + 1
                fg = fg + 1
                print(f'{compteur} iete on etaient trouvés')
                print('----------------------------------------------------------------------', flush=True)
            else:
                print('pas assez de place pour continuer')
                i = 1


tout = False

remisea0 = 0
remiseazero_ok='oui'

if remiseazero_ok == 'oui':
    file = open('compteur_gagnant.txt', 'w')
    file.write(f'{remisea0}')
    file.close()
    file.close()

    file = open('compteur_images.txt', 'w')
    file.write(f'{remisea0}')
    file.close()
    file.close()

    file = open('compteur_perdant.txt', 'w')
    file.write(f'{remisea0}')
    file.close()
    file.close()

    file = open('compteur_nombre_temps.txt', 'w')
    file.write(f'{remisea0}')
    file.close()
    file.close()

    file = open('gain_cumulé.txt', 'w')
    file.write(f'0.00')
    file.close()
    file.close()

    file = open('df.txt', 'w')
    file.write(f'%df_gain%')
    file.close()
    file.close()

    file = open('Tobjectif_25.txt', 'w')
    file.write(f'{remisea0}')
    file.close()
    file.close()

    file = open('Tobjectif_50.txt', 'w')
    file.write(f'{remisea0}')
    file.close()
    file.close()

    file = open('Tobjectif_75.txt', 'w')
    file.write(f'{remisea0}')
    file.close()
    file.close()

    file = open('Tobjectif_100.txt', 'w')
    file.write(f'{remisea0}')
    file.close()
    file.close()

    file = open('Tobjectif_NULL.txt', 'w')
    file.write(f'{remisea0}')
    file.close()
    file.close()

os.system('clear')


print(' ')
print(' ')
Write.Print("                                          /$$$$$$  /$$$$$$$  /$$      /$$  /$$$$$$  /$$$$$$$$\n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                         /$$__  $$| $$__  $$| $$$    /$$$ /$$__  $$|__  $$__/\n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                        | $$  \ $$| $$  \ $$| $$$$  /$$$$| $$  \ $$   | $$   \n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                        | $$$$$$$$| $$  | $$| $$ $$/$$ $$| $$$$$$$$   | $$   \n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                        | $$__  $$| $$  | $$| $$  $$$| $$| $$__  $$   | $$   \n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                        | $$  | $$| $$  | $$| $$\  $ | $$| $$  | $$   | $$   \n", Colors.purple_to_blue, interval=0.000)
Write.Print("                                        | $$  | $$| $$$$$$$/| $$ \/  | $$| $$  | $$   | $$   \n", Colors.purple_to_blue, interval=0.000)
Write.Print(" > ADMAT Version 1.1                    |__/  |__/|_______/ |__/     |__/|__/  |__/   |__/   \n", Colors.purple_to_blue, interval=0.000)

Write.Print("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", Colors.purple_to_blue, interval=0.000)
time.sleep(0.5)
print(' ')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}1{Fore.RESET}{m}]{Fore.RESET} ADAUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}11{Fore.RESET}{m}]{Fore.RESET} LINKUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}21{Fore.RESET}{m}]{Fore.RESET}  XRPUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}2{Fore.RESET}{m}]{Fore.RESET} AVAXUSD         {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}12{Fore.RESET}{m}]{Fore.RESET} MANAUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}22{Fore.RESET}{m}]{Fore.RESET}  XTZUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}3{Fore.RESET}{m}]{Fore.RESET} BTCUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}13{Fore.RESET}{m}]{Fore.RESET} MATICUSD         {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}23{Fore.RESET}{m}]{Fore.RESET}  YFIUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}4{Fore.RESET}{m}]{Fore.RESET} CROUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}14{Fore.RESET}{m}]{Fore.RESET} SANDUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}24{Fore.RESET}{m}]{Fore.RESET}  DOTUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}5{Fore.RESET}{m}]{Fore.RESET} DOGEUSD         {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}15{Fore.RESET}{m}]{Fore.RESET} SHIBUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}6{Fore.RESET}{m}]{Fore.RESET} EGLDUSD         {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}16{Fore.RESET}{m}]{Fore.RESET} SOLUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}7{Fore.RESET}{m}]{Fore.RESET} EOSUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}17{Fore.RESET}{m}]{Fore.RESET} THETAUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}8{Fore.RESET}{m}]{Fore.RESET} ETHUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}18{Fore.RESET}{m}]{Fore.RESET} TRXUSD           {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}T{Fore.RESET}{m}]{Fore.RESET}{lr} TOUT ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}9{Fore.RESET}{m}]{Fore.RESET} FTMUSD          {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}19{Fore.RESET}{m}]{Fore.RESET} UNIUSD ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}10{Fore.RESET}{m}]{Fore.RESET} GALAUSD        {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}20{Fore.RESET}{m}]{Fore.RESET} UOSUSD           {m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}M{Fore.RESET}{m}]{Fore.RESET}{lb} RETOUR ''')
print(' ')
Write.Print("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", Colors.purple_to_blue, interval=0.000)

print('                      ')
Write.Print(" CHOISSISEZ VOTRE MONNAIE : ", Colors.purple, interval=0.000)
time.sleep(0.5)
print(' ')

nom = ""

a = 0
while a != 1:
    monnaie = input(' >>\x1B[1m ')
    if monnaie == "1":
        nom = "ADA"
        a = 1
    if monnaie == "2":
        nom = "AVAX"
        a = 1
    if monnaie == "3":
        nom = "BTC"
        a = 1
    if monnaie == "4":
        nom = "CRO"
        a = 1
    if monnaie == "5":
        nom = "DOGE"
        a = 1
    if monnaie == "6":
        nom = "EGLD"
        a = 1
    if monnaie == "7":
        nom = "EOS"
        a = 1
    if monnaie == "8":
        nom = "ETH"
        a = 1
    if monnaie == "9":
        nom = "FTM"
        a = 1
    if monnaie == "10":
        nom = "GALA"
        a = 1
    if monnaie == "11":
        nom = "LINK"
        a = 1
    if monnaie == "12":
        nom = "MANA"
        a = 1
    if monnaie == "13":
        nom = "MATIC"
        a = 1
    if monnaie == "14":
        nom = "SAND"
        a = 1
    if monnaie == "15":
        nom = "SHIB"
        a = 1
    if monnaie == "16":
        nom = "SOL"
        a = 1
    if monnaie == "17":
        nom = "THETA"
        a = 1
    if monnaie == "18":
        nom = "TRX"
        a = 1
    if monnaie == "19":
        nom = "UNI"
        a = 1
    if monnaie == "20":
        nom = "UOS"
        a = 1
    if monnaie == "21":
        nom = "XRP"
        a = 1
    if monnaie == "22":
        nom = "XTZ"
        a = 1
    if monnaie == "23":
        nom = "YFI"
        a = 1
    if monnaie == "24":
        nom = "DOT"
        a = 1
    if monnaie == "m" or monnaie == "M":
        a = 1
        stream = os.system('python3 Launcher.py')
    if monnaie == "t" or monnaie == "T":
        a = 1
        tout = True
    if monnaie != "1" and monnaie != "2" and monnaie != "3" and monnaie != "4" and monnaie != "5" and monnaie != "6" and monnaie != "7" and monnaie != "8" and monnaie != "9" and monnaie != "10" and monnaie != "11" and monnaie != "12" and monnaie != "13" and monnaie != "14" and monnaie != "15" and monnaie != "16" and monnaie != "17" and monnaie != "18" and monnaie != "19" and monnaie != "20" and monnaie != "21" and monnaie != "22" and monnaie != "23" and monnaie != "24" and monnaie != "m" and monnaie != "M" and monnaie != "t" and monnaie != "T":
        print(bcolors.FAIL + 'Choix non reconnu, veuillez recommencer' + bcolors.RESET)
ticker = f'X:{nom}USD'


print(' ')
Write.Print(" CHOISSISEZ VOTRE TIME-FRAME ? : ", Colors.purple, interval=0.000)
print(' ')
print(' ')
time.sleep(0.5)

print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}1{Fore.RESET}{m}]{Fore.RESET} NON ''')
print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}2{Fore.RESET}{m}]{Fore.RESET} OUI ''')
print(' ')
print(' ')

b = 0
while b != 1:
    frame = input(bcolors.PURPLE + '' + bcolors.RESET)

    if frame != "1" and frame != "2":
        print(bcolors.FAIL + 'Choix non reconnu, veuillez recommencer' + bcolors.RESET)

    if frame == "1":
        b = 1
        minute = "minute"
        hour = "hour"
        Finder_iete(5, minute, start_15m)

    if frame == "2":

        b = 1
        print(' ')
        Write.Print(" CHOISSISEZ VOTRE TIME-FRAME  : ", Colors.purple, interval=0.000)
        print(' ')
        print(' ')
        time.sleep(0.5)

        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}1{Fore.RESET}{m}]{Fore.RESET} 1 MINUTE          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}2{Fore.RESET}{m}]{Fore.RESET} 5 MINUTES          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}3{Fore.RESET}{m}]{Fore.RESET} 15 MINUTES          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}4{Fore.RESET}{m}]{Fore.RESET} 30 MINUTES          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}5{Fore.RESET}{m}]{Fore.RESET} 1 HEURE          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}6{Fore.RESET}{m}]{Fore.RESET} 6 HEURES          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}7{Fore.RESET}{m}]{Fore.RESET} 1 JOUR          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}8{Fore.RESET}{m}]{Fore.RESET} 1 MOI          ''')

        print(' ')
        print(' ')
        c = 0
        while c != 1:
            timea = input(' >>\x1B[1m ')

            if timea == "1":
                time1 = 1
                c = 1
                time_name1 = "minute"
            if timea == "2":
                time1 = 5
                c = 1
                time_name1 = "minute"
            if timea == "3":
                time1 = 20
                c = 1
                time_name1 = "minute"
            if timea == "4":
                time1 = 75
                c = 1
                time_name1 = "minute"
            if timea == "5":
                time1 = 1
                c = 1
                time_name1 = "hour"
            if timea == "6":
                time1 =  10
                c = 1
                time_name1 = "hour"
            if timea == "7":
                time1 = 1
                c = 1
                time_name1 = "day"
            if timea == "8":
                time1 = 1
                c = 1
                time_name1 = "month"
            if timea != "1" and timea != "2" and timea != "3" and timea != "4" and timea != "5" and timea != "6" and timea != "7" and timea != "8":
                print(bcolors.FAIL + 'Choix non reconnu, veuillez recommencer' + bcolors.RESET)
        print(' ')
        Write.Print(" CHOISSISEZ VOTRE DEPART 1: ", Colors.purple, interval=0.000)
        print(' ')
        print(' ')
        time.sleep(0.5)

        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}1{Fore.RESET}{m}]{Fore.RESET} START_15M          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}2{Fore.RESET}{m}]{Fore.RESET} START_30M          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}3{Fore.RESET}{m}]{Fore.RESET} START_1H          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}6{Fore.RESET}{m}]{Fore.RESET} START_6H         ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}4{Fore.RESET}{m}]{Fore.RESET} START_1D          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}5{Fore.RESET}{m}]{Fore.RESET} START_1WEEK          ''')
        print(f'''{m}'''.replace('$', f'{m}${w}') + f'''{m}[{w}7{Fore.RESET}{m}]{Fore.RESET} START_1MONTH          ''')

        print(' ')
        print(' ')
        e = 0
        while e != 1:
            timec = input(' >>\x1B[1m ')

            if timec == "1":
                start1 = start_15m
                e = 1
            if timec == "2":
                start1 = start_30m
                e = 1
            if timec == "3":
                start1 = start_1h
                e = 1
            if timec == "4":
                start1 = start_6h
                e = 1
            if timec == "5":
                start1 = start_1d
                e = 1
            if timec == "6":
                start1 = start_1week
                e = 1
            if timec == "7":
                start1 = start_1month
                e = 1
            if timec != "1" and timec != "2" and timec != "3" and timec != "4" and timec != "5" and timec != "6" and timec != "7" and timec != "8":
                print(bcolors.FAIL + 'Choix non reconnu, veuillez recommencer' + bcolors.RESET)

time.sleep(0.5)
Write.Print(" LANCEMENT DU GRAPH  :    ", Colors.purple, interval=0.000)
print(' ')
print(' ')





if tout == False:
    Finder_iete(time1, time_name1, start1)
if tout == True:

    file_obj = open("titre.txt", "r")
    file_data = file_obj.read()
    lines = file_data.splitlines()
    file_obj.close()
    for titre in lines:
        ticker = titre
        nom = titre
        try:
            Finder_iete(time1, time_name1, start1)
        except:
            print('Defaut de titre!')
