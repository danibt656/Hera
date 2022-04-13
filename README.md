<div style='text-align: center;' align='center'>
    <img style='max-width: 300px;' src='hera_logo.png'/>
</div>

<center><h3><i>El asistente de voz definitivo</i></h3></center>

## Qué es esto?

> Este proyecto es mi segundo intento de crear un asistente de voz interactivo

Hace varios años, intenté crear mi propio asistente de voz con un código JavaScript muy básico, que puedes ver <a href="https://github.com/danibt656/SpeechAssistant" target="_blank">aquí</a>.

Conforme han aumentado mis conocimientos, con ellos han crecido las ganas de llevar aquel asistente de voz al siguiente nivel. Así, *Hera* nace con la idea de ser una emulación de un asistente virtual completo: dispone de un sistema de conexiones TCP que permitirán tenerlo conectado en casa todo el día, para que cualquier dispositivo pueda hacerle preguntas. Además, hace uso del aprendizaje difuso de <a href="https://github.com/ArtificialIntelligenceToolkit/aiml" target="_blank">AIML</a> para procesar las peticiones del usuario.

## Qué puedo preguntarle?

> De momento la funcionalidad, aunque limitada, permite lo siguiente:

+ Saludar
+ Preguntar qué tal estás
+ Dar la hora
+ Dar la fecha
+ Dar el tiempo (climático)

## Cómo lo hago funcionar?

> Dado que Hera funciona bajo un protocolo cliente-servidor, debes seguir los siguientes pasos:

1. Elige si el Cliente y el Servidor correrán en la misma máquina, o en máquinas distintas (ojo, siempre dentro de la misma <a href="https://en.wikipedia.org/wiki/Local_area_network" target="_blank">LAN</a>).
2. Una vez te hayas decidido, ajusta los parámetros de IP y Puerto del servidor en el fichero `server_conf.json`, para configurar el Servidor.
Por ejemplo, si quieres que el Servidor funcione en un ordenador con IP 10.0.0.2, en el puerto 3333, deberás escribir esto en el fichero de configuración del servidor:
```
{
    "host": "10.0.0.2",
    "port": 3333,
    "max_clients": 5
}
```
3. Inicia un entorno virtual en la máquina Servidor e instala los paquetes apropiados con los siguientes comandos:
```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
4. Inicia el programa servidor con:
```
$ python3 heraServer.py
```
5. A continuación, repite el paso **3** para la máquina Cliente
6. Inicia el programa cliente en su máquina apropiada con:
````
$ python3 heraClient.py <TU_PREGUNTA>
````
Donde la pregunta que le quieras hacer a Hera deberá ser provista como una cadena de caracteres en el lugar de <TU_PREGUNTA>.
**IMPORTANTE: La cadena con la pregunta deberá contener la palabra 'Hera' en algún punto, de no hacerlo no será reconocida!**
Por ejemplo:
```
$ python3 heraClient.py "Hola, Hera"
```
