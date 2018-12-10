#!/usr/bin/env python

import requests
import json
import argparse

api_url = 'http://api.gios.gov.pl/pjp-api/rest'

'''
Takes station ID as argument and returns station details
'''
def getStationDetails(baseurl, id):
    url = baseurl + "/station/stationDetails/" + str(id)
    result = json.loads(requests.get(url).text)
    return result

'''
Takes station ID as argument and returns a list of available sensors
'''
def getStationSensors(baseurl, id):
    url = baseurl + "/station/sensors/" + str(id)
    result = json.loads(requests.get(url).text)
    return result

'''
Takes a dictionary of available sensors as argument
Prints formulas and descriptions of available measurments (parameters)
'''
def printParameterNames(sensors):
    print("Dostępne parametry:")
    for id in sensors:
        print("\t", id['param']['paramCode'], "\t", id['param']['paramName'])

'''
Takes parameter ID as returned by getStationSensors() and returns it's newest value
'''
def getLatestParameterValue(baseurl, id):
    url = baseurl + "/data/getData/" + str(id)
    result = json.loads(requests.get(url).text)
    index = 0
    lastValue = {}
    lastValue['value'] = result['values'][index]['value']
    lastValue['date'] = result['values'][index]['date']
    while not lastValue['value']:
        index += 1
        lastValue['value'] = result['values'][index]['value']
        lastValue['date'] = result['values'][index]['date']
    return lastValue

'''
Takes station ID as argument and returns latest values of all available measurements
'''
def getLatestMeasurements(baseurl, station_id):
    sensors = getStationSensors(baseurl, station_id)
    results = {}
    for sensor in sensors:
        value = getLatestParameterValue(baseurl, sensor['id'])
        value['name'] = sensor['param']['paramName']
        results[sensor['param']['paramCode']] = value
    return results

'''
Get general air quality index for a station
'''
def getCurrentIndex(baseurl, station_id):
    url = baseurl + "/aqindex/getIndex/" + str(station_id)
    result = json.loads(requests.get(url).text)
    return result['stIndexLevel']['indexLevelName']

'''
Takes dictionary of measurement data and prints it nicely
'''
def printMeasurements(measurements):
    for param in measurements:
        print(param, end='\t')
        for value in measurements[param]:
            print(measurements[param][value], end='\t')
        print()

'''
Takes dictionary of station information and prints it nicely
'''
def printStationInfo(station):
    print(station['city']['commune']['communeName'], end=", ")
    print(station['addressStreet'], end="\n")

'''
Nicely print general air quality index
'''
def printStationIndex(index):
    print("Ogólny stan:", str(index), sep="\t", end="\n")

parser = argparse.ArgumentParser(description="Get air quality information from GIOS")
parser.add_argument("-s", "--station", action="store", dest="station", required=True)
args = parser.parse_args()

if not args.station:
    parser.print_help()
    exit(1)

index = getCurrentIndex(api_url, args.station)
details = getStationDetails(api_url, args.station)
measure = getLatestMeasurements(api_url, args.station)

printStationInfo(details)
printStationIndex(index)
printMeasurements(measure)
