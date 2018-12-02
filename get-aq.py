#!/usr/bin/env python

import requests
import json
import pprint

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
Takes dictionary of measurement data and prints it nicely
'''
def printMeasurements(measurements):
    for param in measurements:
        print(param, end='\t')
        for value in measurements[param]:
            print(measurements[param][value], end='\t')
        print()

measure = getLatestMeasurements(api_url, 987)

printMeasurements(measure)

