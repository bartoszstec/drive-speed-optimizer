import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. DEFINICJA UNIWERSUM (ZAKRESÓW LICZBOWYCH)

x_visibility = np.arange(0, 501, 1)           # visibility: od 0 - 500 meters
x_traffic = np.arange(0, 101, 1)              # Traffic intensity: 0 - 100 %
x_vehicle_load = np.arange(0, 101, 1)         # Vehicle load: 0 - 100 %
x_v_max = np.arange(0, 141, 1)                # Max speed: 0 - 140 km/h
x_v_safe = np.arange(0, 141, 1)               # Safe speed: 0 - 140 km/h


# Tworzenie obiektów zmiennych wejściowych (Antecedents) i wyjściowych (Consequents)
visibility = ctrl.Antecedent(x_visibility, 'visibility')
traffic = ctrl.Antecedent(x_traffic, 'traffic')
vehicle_load = ctrl.Antecedent(x_vehicle_load, 'vehicle_load')
v_max = ctrl.Antecedent(x_v_max, 'v_max')
v_safe = ctrl.Consequent(x_v_safe, 'v_safe')

print(len(visibility))
print(visibility[0])


# 2. DEFINICJA FUNKCJI PRZYNALEŻNOŚCI (ZBIORÓW ROZMYTYCH)

# Wejście 1: Widoczność (funkcje trójkątne i trapezowe)
visibility['low'] = fuzz.trapmf(visibility.universe, [0, 0, 50, 100])
visibility['mid'] = fuzz.trimf(visibility.universe, [50, 150, 250])
visibility['good'] = fuzz.trapmf(visibility.universe, [200, 250, 300, 300])

# # Wejście 2: Dopuszczalna prędkość
# dopuszczalna['miejska'] = fuzz.trapmf(dopuszczalna.universe, [0, 0, 50, 70])
# dopuszczalna['podmiejska'] = fuzz.trimf(dopuszczalna.universe, [50, 90, 110])
# dopuszczalna['szybka'] = fuzz.trapmf(dopuszczalna.universe, [90, 120, 140, 140])


