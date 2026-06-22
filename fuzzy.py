import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64

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
road['urban'] = fuzz.trapmf(road.universe,[0, 0, 30, 50])           # urban: gęsta zabudowa miejska, skrzyżowania, piesi, sygnalizacja świetlna
road['local'] = fuzz.trimf(road.universe,[40, 60, 80])              # local: drogi lokalne poza ścisłym centrum miasta, mniejszy ruch, mniej skrzyżowań
road['expressway'] = fuzz.trimf(road.universe,[70, 100, 120])       # expressway: droga szybkiego ruchu, ograniczony dostęp, bezkolizyjne skrzyżowania
road['motorway'] = fuzz.trapmf(road.universe,[110, 130, 140, 140])  # motorway: autostrada

# Wyjście: Bezpieczna prędkość
v_safe['very_low'] = fuzz.trapmf(v_safe.universe, [20, 25, 35, 45])
v_safe['low'] = fuzz.trimf(v_safe.universe, [40, 55, 70])
v_safe['mid'] = fuzz.trimf(v_safe.universe, [65, 80, 95])
v_safe['high'] = fuzz.trimf(v_safe.universe, [90, 105, 120])
v_safe['very_high'] = fuzz.trapmf(v_safe.universe, [115, 125, 140, 140])

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
# v_safe['very_low'] v_safe['low'] v_safe['mid'] v_safe['high'] v_safe['very_high']

# 3. BAZA REGUŁ ROZMYTYCH (LOGIKA IF-THEN)
rules = [
    ctrl.Rule(visibility['very_low'] & traffic['low'] & road['urban'],v_safe['very_low']),
    ctrl.Rule(visibility['very_low'] & traffic['low'] & road['local'],v_safe['very_low']),
    ctrl.Rule(visibility['very_low'] & traffic['low'] & road['expressway'],v_safe['low']),
    ctrl.Rule(visibility['very_low'] & traffic['low'] & road['motorway'],v_safe['low']),
    ctrl.Rule(visibility['very_low'] & traffic['mid'],v_safe['very_low']),
    ctrl.Rule(visibility['very_low'] & traffic['high'],v_safe['very_low']),
    ctrl.Rule(visibility['low'] & traffic['low'] & road['urban'],v_safe['low']),
    ctrl.Rule(visibility['low'] & traffic['low'] & road['local'],v_safe['low']),
    ctrl.Rule(visibility['low'] & traffic['low'] & road['expressway'],v_safe['mid']),
    ctrl.Rule(visibility['low'] & traffic['low'] & road['motorway'],v_safe['mid']),
    ctrl.Rule(visibility['low'] & traffic['mid'],v_safe['low']),
    ctrl.Rule(visibility['low'] & traffic['high'],v_safe['very_low']),
    ctrl.Rule(visibility['mid'] & traffic['low'] & road['urban'],v_safe['low']),
    ctrl.Rule(visibility['mid'] & traffic['low'] & road['local'],v_safe['mid']),
    ctrl.Rule(visibility['mid'] & traffic['low'] & road['expressway'],v_safe['high']),
    ctrl.Rule(visibility['mid'] & traffic['low'] & road['motorway'],v_safe['high']),
    ctrl.Rule(visibility['mid'] & traffic['mid'] & road['urban'],v_safe['low']),
    ctrl.Rule(visibility['mid'] & traffic['mid'] & road['local'],v_safe['mid']),
    ctrl.Rule(visibility['mid'] & traffic['mid'] & road['expressway'],v_safe['mid']),
    ctrl.Rule(visibility['mid'] & traffic['mid'] & road['motorway'],v_safe['high']),
    ctrl.Rule(visibility['mid'] & traffic['high'],v_safe['low']),
    ctrl.Rule(visibility['good'] & traffic['low'] & road['urban'],v_safe['mid']),
    ctrl.Rule(visibility['good'] & traffic['low'] & road['local'],v_safe['high']),
    ctrl.Rule(visibility['good'] & traffic['low'] & road['expressway'],v_safe['very_high']),
    ctrl.Rule(visibility['good'] & traffic['low'] & road['motorway'],v_safe['very_high']),
    ctrl.Rule(visibility['good'] & traffic['mid'] & road['urban'],v_safe['low']),
    ctrl.Rule(visibility['good'] & traffic['mid'] & road['local'],v_safe['mid']),
    ctrl.Rule(visibility['good'] & traffic['mid'] & road['expressway'],v_safe['high']),
    ctrl.Rule(visibility['good'] & traffic['mid'] & road['motorway'],v_safe['high']),
    ctrl.Rule(visibility['good'] & traffic['high'] & road['urban'],v_safe['low']),
    ctrl.Rule(visibility['good'] & traffic['high'] & road['local'],v_safe['low']),
    ctrl.Rule(visibility['good'] & traffic['high'] & road['expressway'],v_safe['mid']),
    ctrl.Rule(visibility['good'] & traffic['high'] & road['motorway'],v_safe['mid']),
    ctrl.Rule(vehicle_load['very_high'],v_safe['very_low']),
    ctrl.Rule(vehicle_load['high'] & visibility['very_low'],v_safe['very_low']),
    ctrl.Rule(vehicle_load['high'] & visibility['low'],v_safe['low'])
]


system = ctrl.ControlSystem(rules)

def calculate_safe_speed(vis, traf, load, road_value, only_value=False):
    sim = ctrl.ControlSystemSimulation(system)

    sim.input['visibility'] = vis
    sim.input['traffic'] = traf
    sim.input['vehicle_load'] = load
    sim.input['road'] = road_value
    sim.compute()
    result = float(sim.output['v_safe'])
    if only_value:
        return result

    v_safe.view(sim=sim)
    plt.title("Fuzzy output: v_safe")
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode("utf-8")

    plt.close()

    return result, img_base64

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

    print("\n=== DEBUG WEJŚCIA ===")
    print("visibility:", v_vis)
    print("traffic:", v_traf)
    print("vehicle_load:", v_load)
    print("road:", v_road)

    # === AUTOMATYCZNY DRUK AKTYWACJI REGUŁ ===
    print("\n=== AKTYWACJA REGUŁ (STAN SYSTEMU) ===")
    sim.print_state()

    # Wizualizacja wykresu
    v_safe.view(sim=sim)
    plt.show()

    return sim.output['v_safe']


# MAIN CODE
# debug = debug_system(0,0,0,140)
# print(f"prędkość wyjściowa: {debug}")
# test = calculate_safe_speed(30, 0, 0, 140)
# print(test)

