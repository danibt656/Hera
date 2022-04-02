#!/bin/bash
# Script para probar de seguido la funcionalidad del cliente

# Greeting
python3 heraClient.py 'Hola'
python3 heraClient.py 'Hola Alice!'
# How r u
python3 heraClient.py 'Que tal estas'

# Date (today)
python3 heraClient.py 'Que dia es'
# Date (today)
python3 heraClient.py 'Que dia es hoy'
# Date (yesterday)
python3 heraClient.py 'Que dia fue ayer'

# Time
python3 heraClient.py 'Que hora es'

# Weather
python3 heraClient.py 'El tiempo en Madrid'
python3 heraClient.py 'El tiempo en Moralzarzal'
python3 heraClient.py 'El tiempo en Toronto'

