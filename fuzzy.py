import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. DEFINICJA UNIWERSUM (ZAKRESÓW LICZBOWYCH)

x_visibility = np.arange(0, 501, 1)           # visibility: od 0 - 500 meters
x_traffic = np.arange(0, 101, 1)              # Traffic intensity: 0 - 100 %
x_vehicle_load = np.arange(0, 101, 1)         # Vehicle load: 0 - 100 %
x_road = np.arange(0, 141, 1)                 # Road limiting: 0 - 140 km/h
x_v_safe = np.arange(0, 141, 1)               # Safe speed: 0 - 140 km/h
# dodatkowo ogranicznik (v_max) jako maksymalna wartosc


# Tworzenie obiektów zmiennych wejściowych (Antecedents) i wyjściowych (Consequents)
visibility = ctrl.Antecedent(x_visibility, 'visibility')
traffic = ctrl.Antecedent(x_traffic, 'traffic')
vehicle_load = ctrl.Antecedent(x_vehicle_load, 'vehicle_load')
road = ctrl.Antecedent(x_road, 'road')
v_safe = ctrl.Consequent(x_v_safe, 'v_safe')

# print(len(visibility))
# print(visibility.universe)


# 2. DEFINICJA FUNKCJI PRZYNALEŻNOŚCI (ZBIORÓW ROZMYTYCH)

# Wejście 1: Widoczność
visibility['very_low'] = fuzz.trapmf(visibility.universe, [0, 0, 20, 50])
visibility['low'] = fuzz.trimf(visibility.universe, [30, 80, 150])
visibility['mid'] = fuzz.trimf(visibility.universe, [100, 200, 300])
visibility['good'] = fuzz.trapmf(visibility.universe, [250, 300, 500, 500])
visibility.view()
plt.title("Funkcje przynależności dla zmiennej 'visibility'")
plt.grid(True)
plt.show()

# Wejście 2: Natężenie ruchu
traffic['low'] = fuzz.trapmf(traffic.universe, [0, 0, 20, 40])
traffic['medium'] = fuzz.trimf(traffic.universe, [30, 50, 80])
traffic['high'] = fuzz.trapmf(traffic.universe, [60, 80, 100, 100])
traffic.view()
plt.title("Funkcje przynależności dla zmiennej 'traffic'")
plt.grid(True)
plt.show()

# Wejście 3: Obciążenie pojazdu
vehicle_load['normal'] = fuzz.trapmf(vehicle_load.universe, [0, 0, 30, 75])
vehicle_load['high'] = fuzz.trimf(vehicle_load.universe, [65, 80, 95])
vehicle_load['very_high'] = fuzz.trapmf(vehicle_load.universe, [90, 95, 100, 100])
vehicle_load.view()
plt.title("Funkcje przynależności dla zmiennej 'vehicle_load'")
plt.grid(True)
plt.show()

# Wejście 4: Charakterystyka drogi
road['urban'] = fuzz.trapmf(road.universe,[0, 0, 30, 50])           # urban: gęsta zabudowa miejska, skrzyżowania, piesi, sygnalizacja świetlna
road['local'] = fuzz.trimf(road.universe,[40, 60, 80])              # local: drogi lokalne poza ścisłym centrum miasta, mniejszy ruch, mniej skrzyżowań
road['expressway'] = fuzz.trimf(road.universe,[70, 100, 120])       # expressway: droga szybkiego ruchu, ograniczony dostęp, bezkolizyjne skrzyżowania
road['motorway'] = fuzz.trapmf(road.universe,[110, 130, 140, 140])  # motorway: autostrada
road.view()
plt.title("Funkcje przynależności dla zmiennej 'road'")
plt.grid(True)
plt.show()

# Wyjście: Bezpieczna prędkość
v_safe['very_low'] = fuzz.trapmf(v_safe.universe, [0, 0, 20, 30])
v_safe['low'] = fuzz.trimf(v_safe.universe, [20, 40, 60])
v_safe['medium'] = fuzz.trapmf(v_safe.universe, [50, 60, 80, 90])
v_safe['high'] = fuzz.trimf(v_safe.universe, [80, 100, 120])
v_safe['very_high'] = fuzz.trapmf(v_safe.universe, [110, 120, 140, 140])
v_safe.view()
plt.title("Funkcje przynależności dla zmiennej 'v_safe'")
plt.grid(True)
plt.show()
