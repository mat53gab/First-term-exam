Crear un entorno virtual

1.	Creamos una carpeta dentro del esquipo llamada "FastAPI".

2.	Abrimos el VSCODE y la ejecutamos ahí.

3.	Abrimos el terminal de VSCODE e ingresamos los siguientes comandos para crear el entorno virtual.

⦁	python -m venv fastapi-env

⦁	.\fastapi-env\Scripts\Activate, 

4. Una vez ingresado este comando te va llevar al directorio del entorno virtual, dentro de ese directorio colocamos los siguiente comando para instalar el fastapi y uvicorn:

⦁	pip install fastapi

⦁	ip install uvicorn

5. Una vez hecho esto creamos nuestro "main.py" para trabajar ahí.

6. Dentro del main, colocamos el siguiente código para activar la app de fastapi en Python:

from fastapi import FastAPI

app = FastAPI()

@app.get("/")

7. Una vez creado el código, se ingresa el siguiente comando: "uvicorn main:app --reload", para que nos salga la dirección del fastapi para ver nuestra app creada

Ejemplos de salida

[
  {
    "id": 1,
    "username": "Matt",
    "email": "mat@gmail.com",
    "is_active": true
  }
]

{
  "clave": "123",
  "intentos": 260945,
  "tiempo_s": 0.053133
}

