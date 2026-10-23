#!/usr/bin/env python3
"""Generate a large GeoJSON dataset with synthetic rivers and fords with nztopo50 metadata."""

import json
import math
import os
import random
import time

def generate_large_dataset(
    output_path: str = "rivers_large.geojson",
    river_count: int = 30000,
    ford_count: int = 10000,
    override_ratio: float = 0.5,
    seed: int = 42,
):
    random.seed(seed)

    # Major New Zealand regional clusters (longitude, latitude)
    regions = [
        (174.76, -36.85),  # Auckland
        (175.28, -37.78),  # Waikato
        (176.16, -37.68),  # Bay of Plenty
        (175.61, -40.35),  # Manawatu
        (174.77, -41.28),  # Wellington
        (173.28, -41.27),  # Nelson / Tasman
        (172.63, -43.53),  # Canterbury
        (170.50, -45.87),  # Otago
        (168.35, -46.41),  # Southland
        (171.21, -42.45),  # West Coast
    ]

    t0 = time.time()
    total_features = river_count + ford_count
    ford_indices = set(random.sample(range(river_count), min(ford_count, river_count)))

    river_crossing_points = []

    with open(output_path, "w", encoding="utf-8") as f:
        f.write('{\n  "type": "FeatureCollection",\n  "features": [\n')

        written_count = 0

        # 1. Generate Rivers
        for i in range(river_count):
            center_lon, center_lat = random.choice(regions)
            base_lon = center_lon + random.gauss(0, 0.4)
            base_lat = center_lat + random.gauss(0, 0.4)

            angle = random.uniform(0, 2 * math.pi)
            step = random.uniform(0.003, 0.008)

            p1 = [round(base_lon, 8), round(base_lat, 8)]
            p2 = [
                round(base_lon + math.cos(angle) * step + random.gauss(0, 0.0005), 8),
                round(base_lat + math.sin(angle) * step + random.gauss(0, 0.0005), 8),
            ]
            p3 = [
                round(p2[0] + math.cos(angle + random.uniform(-0.5, 0.5)) * step, 8),
                round(p2[1] + math.sin(angle + random.uniform(-0.5, 0.5)) * step, 8),
            ]

            coords = [p1, p2, p3]
            if i in ford_indices:
                river_crossing_points.append(p2)

            has_override = (i / river_count) < override_ratio

            if has_override:
                d_lon, d_lat = 0.00112, 0.00027
                wkt_pts = [f"{round(pt[0] + d_lon, 8)} {round(pt[1] + d_lat, 8)}" for pt in coords]
                wkt = f"LINESTRING ({wkt_pts[0]}, {wkt_pts[1]}, {wkt_pts[2]})"
                metadata_json = f'{{"nztopo50:geometry": "{wkt}"}}'
            else:
                metadata_json = "{}"

            feat_str = (
                f'    {{\n'
                f'      "type": "Feature",\n'
                f'      "properties": {{\n'
                f'        "type": "river",\n'
                f'        "metadata": {metadata_json}\n'
                f'      }},\n'
                f'      "geometry": {{\n'
                f'        "type": "LineString",\n'
                f'        "coordinates": {json.dumps(coords)}\n'
                f'      }}\n'
                f'    }}'
            )

            written_count += 1
            is_last = written_count == total_features
            f.write(feat_str + (",\n" if not is_last else "\n"))

        # 2. Generate Fords at river crossing points
        for i, pt in enumerate(river_crossing_points):
            # Random min (start_m) and max (end_m) values in meters
            # Realistic ranges: 0 to 50m for start_m, 10 to 100m for end_m
            start_m = round(random.choice([0, 5, 10, 15, 20, 25, 30, 40, 50, 75]), 1)
            end_m = round(random.uniform(start_m, start_m + random.uniform(10, 80)), 1)

            has_override = (i / len(river_crossing_points)) < override_ratio

            meta_dict = {
                "nztopo50:ford:start_m": start_m,
                "nztopo50:ford:end_m": end_m,
            }

            if has_override:
                # 100m East displacement matching the river override
                d_lon, d_lat = 0.00112, 0.00027
                override_pt = [round(pt[0] + d_lon, 8), round(pt[1] + d_lat, 8)]
                meta_dict["nztopo50:geometry"] = f"POINT ({override_pt[0]} {override_pt[1]})"

            feat_str = (
                f'    {{\n'
                f'      "type": "Feature",\n'
                f'      "properties": {{\n'
                f'        "type": "ford",\n'
                f'        "metadata": {json.dumps(meta_dict)}\n'
                f'      }},\n'
                f'      "geometry": {{\n'
                f'        "type": "Point",\n'
                f'        "coordinates": {json.dumps(pt)}\n'
                f'      }}\n'
                f'    }}'
            )

            written_count += 1
            is_last = written_count == total_features
            f.write(feat_str + (",\n" if not is_last else "\n"))

        f.write("  ]\n}\n")

    t1 = time.time()
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(
        f"Generated {river_count} rivers + {len(river_crossing_points)} fords "
        f"({total_features} total features) in {t1 - t0:.2f}s ({size_mb:.2f} MB)"
    )


if __name__ == "__main__":
    generate_large_dataset()
