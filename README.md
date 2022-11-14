# Hallacas pipeline simulation

## Problem statement (in Spanish)
En el momento de hacer hallacas se reúnen varias personas para trabajar de forma síncrona y garantiza el mayor número de hallacas en el menor tiempo posible:

**Preparación de las hojas de cambur:** el encargado de preparar las hojas de cambur, debe lavar, asar y cortar las hojas. El tiempo para hacer esta tarea se modela por medio de una distribución normal con media `M1` y desviación estándar `D1`. El proceso se detiene cuando al encargado de poner el guiso dá la orden de detener el proceso. Cada hoja lista se colocará en la mesa de subproductos.

**Colocación de la masa en la hoja:** si hay hojas disponible, el encargado de poner la masa en la hoja procede a engrasar la hoja y colocar la masa. El tiempo requerido para ponerla masa en la hoja se puede modelar por medio de una distribución normal con media `M2` y desviación estándar `D2`. Una vez colocada la masa en la hoja se coloca en la mesa de subproductos.

**Colocar el guiso:** el encargado de colocar el guiso recibe `X`Kg de guiso para hallacas, y debe estar pendiente que cuando queden `Y`grs o menos ordenar al encargado de preparar las hojas que se detenga. A cada hallaca se le colocaran al menos **80**grs de guiso. El tiempo requerido para colocar el guiso se puede modelar por medio de una distribución normal con media `M3` y desviación estándar `D3`. Una vez colocado el guiso y cerrada la hoja de la hallaca se coloca en la mesa de subproductos.

**Amarre de hallacas:** El encargado de amarrar las hallacas debe contabilizar las hallacas amarradas y ser capaz de responder consultas sobre hallacas amarradas y hallacas listas por amarrar, así como sacar las estadísticas de cuanto fue el tiempo para hacer las hallacas. El tiempo requerido para amarrar cada hallaca se puede modelar por medio de una distribución normal con media `M4` y desviación estándar `D4`.

Se pide:
- Modelar cada una de las 4 tareas como un procesos independientes, cada proceso debe escribir por consola lo que está haciendo.
- Además de los 4 procesos debe existir un proceso que obtenga y muestre los estados (libre/ocupado) de cada una de las personas.

Observación: en este problema hay una única área común para compartir los subproductos, por lo que se debe garantizar que se eviten los problemas de Race Condition

# Implementation

Each person working on making hallacas is named a worker, and all the workers inherit from the `HallacaWorker` class, which has some common functionalities for them.
The problem of sharing memory is solved by using a server process that hosts and serves the memory to the processes that require sharing data.

Aside from the 4 workers, and the server there are other 2 processes:
1. [query_client.py] A process with a console interface that allows the user to make queries to the HallacaTier.
2. [run.py] The main process which runs the server, the 4 hallaca workers, and the query client, and also shows what every hallaca worker is doing and kills all the remaining processes when the simulation has finished and the user wants to close the program.

The HallacaTier worker has 2 threads, the main thread keeps listening for queries, so it can execute the requests, while the second thread does the main job of the HallacaTier which is to simulate the process of tying up hallacas to make hallacas with their co-workers.

## Brief runtime explanation

When run.py is executed, it runs the server process.
The server process prepares to serve, the OS gives it an available port, and the process sends the network address of the server to the main process (run.py) by using a pipe and starts serving in a secondary thread (this is necessary for allowing easy communication between the main process and the server)
The main process then runs the 4 workers, and the query client with the network address as two arguments and then waits for all the workers to be ready to start the simulation.
Every worker also waits for the other workers to start the simulation.
When every worker is ready, the simulation starts, and the main process shows the state (free/busy) of the workers until the simulation finishes.
While the simulation is started and even after that, the user can use the query client to request data at any moment (some messages will be shown in the HallacaTier console and could be opened new windows that show the statistics)
When the simulation ends, the user can press Enter in the main process's console to kill the remaining processes.

## Shared memory

I used 2 different objects to save the shared data:
* The `Var` object is a wrapper for any object with `get` and `set` methods.
* The `Stack` object can `put` and `pop` any object type, and you can use `len` on it. 

There's several shared objects, but the most important ones are the stacks: after each step of any hallaca's creation, the hallaca is put into the correspondent stack.

Note: every process is protected against race conditions.

## Statistics

When the query client asks the HallacaTier for showing statistics, it will show 2:
1. A graph with hallaca's starting time and finishing time represented with blue, and red dots. The x axis represents the id of each hallaca, and the y axis represents time.
2. A histogram of the time it takes to create each hallaca

## Configuration

The problem statement demands some constant variables which are in the `settings.py` file.
Whenever you want to use distinct variables, you must change them on that file.
(I think this is the more comfortable way for the user of setting those variables since there are many, and that's why I chose this approach).

### Speed
There is also a `speed` variable which is used to increase the speed of the simulation since a realistic simulation takes too much time.
By default it's set to `10` which means a speed of 10x, `1` for example means no change, `2` means double the fast as in real-time, and so on.

### Client-Server auth
The workers need authentication to access the data on the server, and they use a key to do so, and you have to set it up.
To do this, create a new file named `local_settings.py` with a variable named `AUTH_KEY` on it and a string as a value.
The file `local_settings.py.example` is an example of what the `local_settings.py` file should contain.

# How to run it

## Requirements
* Python 3
* Windows, macOS, or a Linux distribution (with a desktop environment able to open windows)

## Instructions
1. Create a python virtual environment:
```sh
python -m venv venv
```
(your python command could be `python3` instead of `python`)

2. Activate the virtual environment:
macOS and Linux:
```sh
. venv/bin/activate
```
Windows:
```powershell
.\venv\Scripts\activate
```

3. With the `requirements.txt` file of this repo, execute:
```sh
pip install -r requirements.txt
```

4. In the root folder of the project, create a `local_settings.py` file with the `AUTH_KEY` variable as in `local_settings.py.example`

5. Then run the simulation
```sh
python run.py
```
