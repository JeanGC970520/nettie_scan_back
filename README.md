# NettieScann
Es un proyecto hecho para extraer texto manuscrito de imagenes. Este repo en concreto cuenta son el servicio backend

## How to use

### Use UV 
Para poder ejecutar este proyecto es necesario [instalar](https://docs.astral.sh/uv/) el gestor de dependencias `uv`. Una 
vez instalado hay seguir los siguientes pasos:

1. Sincronizar las dependencias: `uv sync`
2. Ejecutar la app, esto crea el entorno virtual de manera automática: `uv run fastapi dev src/main.py`

Una vez ejecutado estos pasos, deberíamos ver la salida típica de FastAPI (logs)
