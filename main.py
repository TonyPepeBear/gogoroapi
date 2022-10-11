import csv
import os
from pykml import parser as kp

goStations = []

try:
    os.mkdir("output")
except FileExistsError:
    pass

with open("data.kml", "r", encoding="utf-8") as file:
    doc = kp.parse(file).getroot().Document
    folders = list(doc.Folder)
    for f in folders:
        if f.name != "GoStation 換電站":
            continue
        for p in f.Placemark:
            addr = ""
            isAct = False
            lng = ""
            lat = ""
            for d in p.ExtendedData[0].Data:
                if d.attrib["name"] == "地址":
                    addr = d.value
                if d.attrib["name"] == "目前狀態":
                    isAct = (d.value == "已啟用")
                if d.attrib["name"] == "Longitude":
                    lng = d.value
                if d.attrib["name"] == "Latitude":
                    lat = d.value
            goStations.append({"name": p.name,
                              "address": addr,
                               "lng": lng,
                               "lat": lat,
                               })

print("Total GoStation: " + str(len(goStations)))

with open("output/go-station.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "address", "lng", "lat"])
    for e in goStations:
        writer.writerow([e["name"], e["address"], e["lng"], e["lat"]])
