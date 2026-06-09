import os
import csv
import sys

os.environ.setdefault('MPLBACKEND', 'Agg')
try:
    import fuzzy
except Exception as e:
    print("Błąd podczas importu modułu fuzzy:", e, file=sys.stderr)
    raise



# próbki
vis_samples = [0, 20, 40, 50, 100, 200, 250, 300, 400, 500]
traf_samples = [0, 20, 40, 50, 60, 80, 100]
load_samples = [0, 50, 70, 75, 85, 90, 100]
road_samples = [0, 20, 40, 50, 60, 70, 90, 100, 120, 140]

print("Uruchamiam testy przez pętlę for, wywołując funkcję przyjmującą 4 wartości (test_system)...")
results = []
total = len(vis_samples) * len(traf_samples) * len(load_samples) * len(road_samples)
cnt = 0
for vis in vis_samples:
    for traf in traf_samples:
        for load in load_samples:
            for rd in road_samples:
                cnt += 1
                try:
                    v = fuzzy.calculate_safe_speed(vis, traf, load, rd, only_value=True)
                    v_safe = float(v)
                except Exception as e:
                    # Jeśli symulacja nie zwróci wartości (np. brak aktywacji), zapisujemy NaN
                    print(f"  Ostrzeżenie: nie udało się obliczyć dla ({vis},{traf},{load},{rd}): {e}")
                    v_safe = float('nan')
                results.append((vis, traf, load, rd, v_safe))
                if cnt % 20 == 0 or cnt == total:
                    print(f"  Przetworzono {cnt}/{total}...")

out_path = os.path.join(os.path.dirname(__file__), 'debug_results.csv')
with open(out_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['visibility', 'traffic', 'vehicle_load', 'road', 'v_safe'])
    for row in results:
        writer.writerow(row)

print(f"Zapisano {len(results)} wyników do: {out_path}")

