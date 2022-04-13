#!/bin/bash
# Script para probar de seguido la funcionalidad del cliente

# Greeting
python3 heraClient.py 'Hola'
python3 heraClient.py 'Hola Alice!'
# How r u
python3 heraClient.py 'Que tal estas'
python3 heraClient.py 'Ey, ¿que tal estas?'

# Date (today)
python3 heraClient.py 'Que dia es'
python3 heraClient.py 'Que dia es hoy'
# Date (yesterday)
python3 heraClient.py 'Que dia fue ayer'

# Time
python3 heraClient.py 'Que hora es'
python3 heraClient.py 'DAME la hora'

# Weather
python3 heraClient.py 'El tiempo en Madrid.'
python3 heraClient.py '¿Que tiempo hace en Moralzarzal?'
python3 heraClient.py 'Dime la temperatura en Toronto!!!'
python3 heraClient.py 'Dime el tiempo que hace en Valencia'

