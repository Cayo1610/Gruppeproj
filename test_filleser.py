# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 14:46:32 2021

@author: Erlend Tøssebro
"""
import matplotlib.pyplot as plt
import numpy as np
import math


# Konstant til del f
ANTALL_MAALINGER_MIDLE_OVER = 60


# Til del f
def standardavvik(gjennomsnitt, liste_av_verdier):
    sum_av_kvadrater = 0.0
    for element in liste_av_verdier:
        sum_av_kvadrater += (element-gjennomsnitt)**2
    avvik = math.sqrt(sum_av_kvadrater/len(liste_av_verdier))
    return avvik
    

# Til del f
def lopende_middel(tidspunkter, temperaturer, antall_aa_midle):
    lopende_sum = 0
    resultat_tidspunkter = list()
    resultat_temperaturer = list()
    resultat_avvik = list()
    for i in range(antall_aa_midle):
        lopende_sum += temperaturer[i]
    resultat_tidspunkter.append(tidspunkter[i-(antall_aa_midle//2)])
    resultat_temperaturer.append(lopende_sum/antall_aa_midle)
    resultat_avvik.append(standardavvik(lopende_sum/antall_aa_midle, temperaturer[0:antall_aa_midle]))
    i += 1
    while i < len(tidspunkter):
        lopende_sum += temperaturer[i]
        lopende_sum -= temperaturer[i-antall_aa_midle]
        resultat_tidspunkter.append(tidspunkter[i-(antall_aa_midle//2)])
        resultat_temperaturer.append(lopende_sum/antall_aa_midle)
        i += 1
        resultat_avvik.append(standardavvik(lopende_sum/antall_aa_midle, temperaturer[i-antall_aa_midle:i]))
    return resultat_tidspunkter, resultat_temperaturer, resultat_avvik


# Definerer listene over verdier, til del a
tider = list()
tidspunkter = list()
temperaturer = list()
absolutt_trykk = list()

# Definerer lister til del e
tidspunkter_barometrisk_trykk = list()
barometrisk_trykk = list()


# Leser fila, del a
with open("trykk_og_temperaturlogg.csv") as fila:
    fila.readline()         # Leser kolonnetitlene, som jeg ikke bruker
    for linje in fila:
        linje = linje.replace(",", ".")
        kolonner = linje.split(";")
        tider.append(kolonner[0])
        tidspunkter.append(float(kolonner[1]))
        try:        # Denne try...except blokken er til del e
            bar_trykk = float(kolonner[2])
            barometrisk_trykk.append(bar_trykk)
            tidspunkter_barometrisk_trykk.append(float(kolonner[1]))
        except ValueError:
            pass
        absolutt_trykk.append(float(kolonner[3]))
        temperaturer.append(float(kolonner[4]))
        
# Del b
plt.subplot(2, 2, 1)
plt.title("Temperaturmålinger")
print(f"Antall elementer i listene: tidspunkter: {len(tidspunkter)}, Temperaturer: {len(temperaturer)}")
plt.plot(tidspunkter, temperaturer)
plt.xlabel("Tidspunkt, sekunder etter start")
plt.ylabel("Temperatur")

# Del b og e
plt.subplot(2, 2, 2)
plt.title("Trykkmålinger")
plt.plot(tidspunkter_barometrisk_trykk, barometrisk_trykk, label="Barometrisk Trykk")
plt.plot(tidspunkter, absolutt_trykk, label="Absolutt trykk")
plt.xlabel("Tidspunkt, sekunder etter start")
plt.ylabel("Trykk i bar")
plt.legend()

# Del b og f
plt.subplot(2, 2, 3)
middel_tidspunkter, middel_temperaturer, middel_avvik = lopende_middel(tidspunkter, temperaturer, ANTALL_MAALINGER_MIDLE_OVER)
plt.title("Temperaturmålinger med midling")
plt.plot(tidspunkter, temperaturer, label="Temperaturer")
plt.plot(middel_tidspunkter, middel_temperaturer, label="Midlete temperaturer")
plt.plot(middel_tidspunkter, middel_avvik, label="Avvik mellom middel og målt temperatur")
plt.xlabel("Tidspunkt, sekunder etter start")
plt.ylabel("Temperatur")
plt.legend()

# Del c
plt.subplot(2, 2, 4)
plt.title("Histogram over temperaturer")
plt.hist(temperaturer, bins=np.arange(8, 24, 0.25))
plt.show()

# Del d
print("Tidspunkter hvor målingene stopper opp")
for i in range(len(tidspunkter)-1):
    if tidspunkter[i+1]-tidspunkter[i] > 10:
        print(f"Målingene stopper mellom {tidspunkter[i]} og {tidspunkter[i+1]}. Tider: {tider[i]} til {tider[i+1]}")
