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

# Wejście 2: Natężenie ruchu
traffic['low'] = fuzz.trapmf(traffic.universe, [0, 0, 20, 40])
traffic['mid'] = fuzz.trimf(traffic.universe, [30, 50, 80])
traffic['high'] = fuzz.trapmf(traffic.universe, [60, 80, 100, 100])

# Wejście 3: Obciążenie pojazdu
vehicle_load['normal'] = fuzz.trapmf(vehicle_load.universe, [0, 0, 30, 75])
vehicle_load['high'] = fuzz.trimf(vehicle_load.universe, [65, 80, 95])
vehicle_load['very_high'] = fuzz.trapmf(vehicle_load.universe, [90, 95, 100, 100])

# Wejście 4: Charakterystyka drogi
road['urban'] = fuzz.trapmf(road.universe,[0, 10, 30, 50])           # urban: gęsta zabudowa miejska, skrzyżowania, piesi, sygnalizacja świetlna
road['local'] = fuzz.trimf(road.universe,[40, 60, 80])              # local: drogi lokalne poza ścisłym centrum miasta, mniejszy ruch, mniej skrzyżowań
road['expressway'] = fuzz.trimf(road.universe,[70, 100, 120])       # expressway: droga szybkiego ruchu, ograniczony dostęp, bezkolizyjne skrzyżowania
road['motorway'] = fuzz.trapmf(road.universe,[110, 130, 140, 140])  # motorway: autostrada

# Wyjście: Bezpieczna prędkość
v_safe['very_low'] = fuzz.trapmf(v_safe.universe, [0, 15, 30, 45])
v_safe['low'] = fuzz.trimf(v_safe.universe, [20, 40, 60])
v_safe['mid'] = fuzz.trapmf(v_safe.universe, [50, 60, 80, 90])
v_safe['high'] = fuzz.trimf(v_safe.universe, [80, 100, 120])
v_safe['very_high'] = fuzz.trapmf(v_safe.universe, [110, 120, 140, 140])

# wykresy
# visibility.view()
# traffic.view()
# vehicle_load.view()
# road.view()
# v_safe.view()
# plt.grid(True)
# plt.show()

# ALL STATES FOR FUZZY VARIABLES
# visibility['very_low'] visibility['low'] visibility['mid'] visibility['good']
# traffic['low'] traffic['mid'] traffic['high']
# vehicle_load['normal'] vehicle_load['high'] vehicle_load['very_high']
# road['urban'] road['local'] road['expressway'] road['motorway']

# 3. BAZA REGUŁ ROZMYTYCH (LOGIKA IF-THEN)
# REGUŁY PIORYTETOWE
rule1 = ctrl.Rule(visibility['very_low'], v_safe['very_low'])
rule2 = ctrl.Rule(visibility['low'] & traffic['high'], v_safe['very_low'])
rule3 = ctrl.Rule(visibility['low'] & road['urban'], v_safe['very_low'])
rule4 = ctrl.Rule(vehicle_load['very_high'], v_safe['low'])

# REGUŁY OGRANICZAJĄCE
rule5 = ctrl.Rule(traffic['high'] & road['urban'], v_safe['very_low'])
rule6 = ctrl.Rule(traffic['high'] & vehicle_load['high'], v_safe['low'])
rule7 = ctrl.Rule(visibility['mid'] & traffic['high'], v_safe['low'])
rule8 = ctrl.Rule(road['urban'] & vehicle_load['high'], v_safe['low'])
rule9 = ctrl.Rule(traffic['mid'] & road['urban'], v_safe['low'])

# REGUŁY ŚREDNIE
rule10 = ctrl.Rule(visibility['mid'] & traffic['mid'] & road['local'], v_safe['mid'])
rule11 = ctrl.Rule(visibility['good'] & traffic['mid'] & vehicle_load['normal'], v_safe['mid'])
rule12 = ctrl.Rule(road['local'] & traffic['low'] & vehicle_load['high'], v_safe['mid'])
rule13 = ctrl.Rule(visibility['mid'] & road['expressway'], v_safe['mid'])

# DOBRE WARUNKI
rule14 = ctrl.Rule(visibility['good'] & traffic['low'] & road['expressway'], v_safe['high'])
rule15 = ctrl.Rule(visibility['good'] & traffic['low'] & road['motorway'], v_safe['high'])
rule16 = ctrl.Rule(road['motorway'] & traffic['mid'] & visibility['good'], v_safe['mid'])
rule17 = ctrl.Rule(visibility['good'] & traffic['low'] & vehicle_load['normal'], v_safe['high'])

# OPTIMUM
rule18 = ctrl.Rule(visibility['good'] & traffic['low'] & road['motorway'] & vehicle_load['normal'],v_safe['very_high'])
rule19 = ctrl.Rule(visibility['good'] & traffic['low'] & road['motorway'] & vehicle_load['high'],v_safe['high'])

rule20 = ctrl.Rule(traffic['low'] & visibility['good'], v_safe['mid'])

system = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5,
    rule6, rule7, rule8, rule9, rule10,
    rule11, rule12, rule13, rule14, rule15,
    rule16, rule17, rule18, rule19, rule20
])

def test_system(vis, traf, load, r):
    sim = ctrl.ControlSystemSimulation(system)

    sim.input['visibility'] = vis
    sim.input['traffic'] = traf
    sim.input['vehicle_load'] = load
    sim.input['road'] = r

    sim.compute()
    return sim.output['v_safe']

def debug_system(vis, traf, load, r):
    sim = ctrl.ControlSystemSimulation(system)

    sim.input['visibility'] = vis
    sim.input['traffic'] = traf
    sim.input['vehicle_load'] = load
    sim.input['road'] = r
    sim.compute()

    print("\n=== DEBUG WEJŚCIA ===")
    print(f"visibility = {vis}")
    print(f"traffic = {traf}")
    print(f"vehicle_load = {load}")
    print(f"road = {r}")

    v_vis = {
        'very_low': fuzz.interp_membership(visibility.universe, visibility['very_low'].mf, vis),
        'low': fuzz.interp_membership(visibility.universe, visibility['low'].mf, vis),
        'mid': fuzz.interp_membership(visibility.universe, visibility['mid'].mf, vis),
        'good': fuzz.interp_membership(visibility.universe, visibility['good'].mf, vis),
    }

    v_traf = {
        'low': fuzz.interp_membership(traffic.universe, traffic['low'].mf, traf),
        'mid': fuzz.interp_membership(traffic.universe, traffic['mid'].mf, traf),
        'high': fuzz.interp_membership(traffic.universe, traffic['high'].mf, traf),
    }

    v_load = {
        'normal': fuzz.interp_membership(vehicle_load.universe, vehicle_load['normal'].mf, load),
        'high': fuzz.interp_membership(vehicle_load.universe, vehicle_load['high'].mf, load),
        'very_high': fuzz.interp_membership(vehicle_load.universe, vehicle_load['very_high'].mf, load),
    }

    v_road = {
        'urban': fuzz.interp_membership(road.universe, road['urban'].mf, r),
        'local': fuzz.interp_membership(road.universe, road['local'].mf, r),
        'expressway': fuzz.interp_membership(road.universe, road['expressway'].mf, r),
        'motorway': fuzz.interp_membership(road.universe, road['motorway'].mf, r),
    }

    print("\n=== AKTYWACJA ZBIORÓW ===")
    print("visibility:", v_vis)
    print("traffic:", v_traf)
    print("vehicle_load:", v_load)
    print("road:", v_road)

    rules_activation = {
        "rule1": v_vis['very_low'],
        "rule2": min(v_vis['low'], v_traf['high']),
        "rule3": min(v_vis['low'], v_road['urban']),
        "rule4": v_load['very_high'],
        "rule5": min(v_traf['high'], v_road['urban']),
        "rule6": min(v_traf['high'], v_load['high']),
        "rule7": min(v_vis['mid'], v_traf['high']),
        "rule8": min(v_road['urban'], v_load['high']),
        "rule9": min(v_traf['mid'], v_road['urban']),
        "rule10": min(v_vis['mid'], v_traf['mid'], v_road['local']),
        "rule11": min(v_vis['good'], v_traf['mid'], v_load['normal']),
        "rule12": min(v_road['local'], v_traf['low'], v_load['high']),
        "rule13": min(v_vis['mid'], v_road['expressway']),
        "rule14": min(v_vis['good'], v_traf['low'], v_road['expressway']),
        "rule15": min(v_vis['good'], v_traf['low'], v_road['motorway']),
        "rule16": min(v_road['motorway'], v_traf['mid'], v_vis['good']),
        "rule17": min(v_vis['good'], v_traf['low'], v_load['normal']),
        "rule18": min(v_vis['good'], v_traf['low'], v_road['motorway'], v_load['normal']),
        "rule19": min(v_vis['good'], v_traf['low'], v_road['motorway'], v_load['high']),
        "rule20": min(v_traf['low'], v_vis['good']),
    }

    print("\n=== AKTYWACJA REGUŁ (FIRING STRENGTH) ===")
    for k, v in rules_activation.items():
        print(k, "=", round(v, 3))
    v_safe.view(sim=sim)
    plt.show()
    return sim.output['v_safe']

debug = debug_system(50, 0, 0, 140)
print(f"prędkość wyjściowa: {debug}")
# test = test_system(30, 0, 0, 140)
# print(test)

