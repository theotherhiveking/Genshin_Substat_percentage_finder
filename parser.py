#!/usr/bin/env python3
import json
from itertools import groupby
from operator import itemgetter
import csv
import sys

with open("ReliquaryAffixExcelConfigData.json") as f:
    data = json.load(f)
    data = list(filter(lambda x: x["DepotId"] == 501, data))

    substats = set([r["PropType"] for r in data])
    mainstat = substats.copy()
    mainstat.remove("FIGHT_PROP_DEFENSE")
    mainstat.add("PHYS_DMG")
    mainstat.add("ELEMENTAL_DMG")

    weights = {}
    for mainstat in mainstat:
        substat_dict = {}
        for substat in substats:
            if substat == mainstat:
                pass

            total_weight_excluding_mainstat = sum(r["Weight"] for r in data if r["PropType"] != substat)
            total_substat_weight = sum(r["Weight"] for r in data if r["PropType"] == substat)
            substat_dict[substat.replace("FIGHT_PROP_", "")] = (total_substat_weight/total_weight_excluding_mainstat)*100

        weights[mainstat.replace("FIGHT_PROP_", "")] = substat_dict

    with open("output.csv", "w") as f:
        w = csv.DictWriter(f, ["mainstat", "substat", "%"] )
        w.writeheader()
        for key, val in sorted(weights.items()):
            for substat in val.keys():
                row = { 'mainstat': key, 'substat': substat, '%': val[substat]}
                w.writerow(row)

    with open("output.json", "w") as f:
        json.dump(weights, f, sort_keys=True, indent=4) #pretty print

    print(json.dumps(weights, sort_keys=True, indent=4))
