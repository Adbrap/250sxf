from pystyle import Add, Center, Anime, Colors, Colorate, Write, System

def remplacement (nom, remplace, fichier_lecture, fichier_modif): #pour remplacer les varible de la feuille imprimable 
    try:
        file = open(f"{fichier_lecture}","r+")
        a = str(file.read())
        file.close()
        file = open(f"{fichier_modif}","w")

        a = a.replace(f'{nom}', f'{remplace}')
        file.write(a)
        file.close()
        Write.Print("  Remplacement reussi  !", Colors.green, interval=0.000)
        print('')
    except:
        Write.Print("!! Remplacement echoué  !!", Colors.red, interval=0.000)
        print('')

#----- recuperer les variables des differents fichiers textes -----#
file = open('compteur_gagnant.txt', 'r')
compteur_gagnant = int(file.read())
file.close()

file = open('compteur_images.txt', 'r')
compteur_images = int(file.read())
file.close()

file = open('compteur_perdant.txt', 'r')
compteur_perdant = int(file.read())
file.close()

file = open('compteur_nombre_temps.txt', 'r')
compteur_nombre_temps = int(file.read())
file.close()

file = open('timeset.txt', 'r')
timeset = file.read()
file.close()

file = open('gain_cumulé.txt', 'r')
gain_cumulé = float(file.read())
file.close()

file = open('df.txt', 'r')
df = str(file.read())
file.close()

file = open('Tobjectif_25.txt', 'r') #Recuperer gains moyens
Tobjectif_25 = int(file.read())
file.close()

file = open('Tobjectif_50.txt', 'r')
Tobjectif_50 = int(file.read())
file.close()

file = open('Tobjectif_75.txt', 'r')
Tobjectif_75 = int(file.read())
file.close()

file = open('Tobjectif_100.txt', 'r')
Tobjectif_100 = int(file.read())
file.close()

file = open('Tobjectif_NULL.txt', 'r')
Tobjectif_NULL = int(file.read())
file.close()

#----- suppression de la derniere ligne (%{}%) car ne se converti pas en float-----#
sup_derniere_valeur = []
try:

    with open('df.txt', 'r') as fr:
        sup_derniere_valeur = fr.readlines()
    with open('df.txt', 'w') as fw:
        for line in sup_derniere_valeur:
            if line.strip("\n") != "%df_gain%":
                fw.write(line)
except:
    print('pas reussi a suprimer')
#----- suppression de la derniere ligne (%{}%) car ne se converti pas en float-----#

file_obj = open("df.txt", "r")
file_data = file_obj.read()
lines = file_data.splitlines()
file_obj.close()
dftxt=[]
#----- recuperer les variables des differents fichiers textes -----#

#----- creations des variables que l'on ne peut pas avoir depuis les fichiers textes -----#
somme_recup_trade = 0
for argument in lines:
    dftxt.append(float(argument))
    somme_recup_trade = somme_recup_trade + ((float(argument) *10000)/100) + 10000

dftxt.sort()
pourcentage_gagnant = int((compteur_gagnant * 100)/compteur_images)
moyenne_temps = int(compteur_nombre_temps / compteur_images)
moyenne_gain = round((gain_cumulé / compteur_images),2)
gros_gain = dftxt[len(dftxt)-1]
grosse_perte = dftxt[0]
argent_depart = 10000
argent_final = round((((gain_cumulé * argent_depart)/100) + argent_depart),2)

#nombre_de_jour = 6
#moysortie_jour = round((8000 / (moyenne_temps *nombre_de_jour)),2)
#moysortie_mois = round(((8000 / (moyenne_temps *nombre_de_jour))*30),2)

TOTAL_MISE = (10000 * compteur_images)
prix_moysortie_mois_TTC = round((((0.10) * (TOTAL_MISE))/100) + (somme_recup_trade * (0.10)/100),2)


nombre_de_minute = 75
moysortie_jour = round((8000 / (((moyenne_temps *nombre_de_minute)/60)/24)),2)
moysortie_mois = round((round((8000 / (((moyenne_temps *nombre_de_minute)/60)/24)),2)) * 30,2)

moygains_mois = round((moysortie_mois * moyenne_gain),2)
Tobjectif_moyen = round((((Tobjectif_25*25) + (Tobjectif_50*50) + (Tobjectif_75*75) + (Tobjectif_100*100))/(Tobjectif_25+Tobjectif_50+Tobjectif_75+Tobjectif_100)),2)
moysortie_mois_TTC = round(moygains_mois - (((prix_moysortie_mois_TTC *100)/(10000 * compteur_images)) * (moysortie_mois)),2)
gasfee = round((prix_moysortie_mois_TTC * 100)/(TOTAL_MISE + somme_recup_trade),4)
moysortie_mois_TTC_pourcent = round(moygains_mois - ((moysortie_mois*2)*gasfee),2)
#----- creations des variables que l'on ne peut pas avoir depuis les fichiers textes -----#

#----- lancement des fonctions remplacements -----#
remplacement('%{1}%', f'{compteur_images}', 'feuille_sortie_imprimable2.txt', 'feuille_sortie_imprimable.txt')
remplacement('%{2}%',f'{compteur_gagnant}','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{3}%',f'{compteur_perdant}','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{4}%',f'{compteur_nombre_temps}','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{5}%',f'{pourcentage_gagnant}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{6}%',f'{moyenne_temps}','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{7}%',f'{timeset} sans indicateurs','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{9}%',f'{gain_cumulé}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{10}%',f'{moyenne_gain}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{11}%',f'{gros_gain}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{12}%',f'{grosse_perte}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{13}%',f'{argent_depart}€','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{14}%',f'{argent_final}€','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{15}%',f'{moysortie_jour}','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{16}%',f'{moysortie_mois}','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{17}%',f'{moygains_mois}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{18}%',f'{Tobjectif_moyen}','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{19}%',f'{int((Tobjectif_25 * 100)/compteur_images)}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{20}%',f'{int((Tobjectif_50 * 100)/compteur_images)}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{21}%',f'{int((Tobjectif_75 * 100)/compteur_images)}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{22}%',f'{int((Tobjectif_100 * 100)/compteur_images)}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{23}%',f'{int((Tobjectif_NULL * 100)/compteur_images)}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{24}%',f'{moysortie_mois_TTC_pourcent}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
remplacement('%{25}%',f'{gasfee}%','feuille_sortie_imprimable.txt','feuille_sortie_imprimable.txt')
#----- lancement des fonctions remplacements -----#
