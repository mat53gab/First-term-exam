from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3, hashlib, time, string, itertools

app = FastAPI()
DB = "users.db"

mayusculas="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
minusculas="abcdefghijklmnopqrstuvwxyz"
numeros="0123456789"
simbolos="!@#$%&*"
alphabeths = mayusculas+minusculas+numeros+simbolos

def fuerza_bruta(contrasena_objetivo):
    caracteres = alphabeths 
    intentos = 0
    inicio = time.time()

    for longitud in range(1, 4):
        for tupla in itertools.product(caracteres, repeat=longitud):
            intento = "".join(tupla)
            intentos += 1
            if intento == contrasena_objetivo:
                segundos = time.time() - inicio
                return intentos, segundos
    segundos = time.time() - inicio
    return intentos, segundos

with sqlite3.connect(DB) as conn:
    conn.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        is_active INTEGER NOT NULL DEFAULT 1
    )""")

class UserIn(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    is_active: Optional[bool] = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class LoginIn(BaseModel):
    username: str
    password: str

def to_user_dict(r):
    return {"id": r[0], "username": r[1], "email": r[3], "is_active": bool(r[4])}

@app.post("/users")
def create_user(u: UserIn):
    with sqlite3.connect(DB) as conn:
        try:
            cur = conn.execute(
                "INSERT INTO users(username,password,email,is_active) VALUES(?,?,?,?)",
                (u.username, hashlib.sha256(u.password.encode()).hexdigest(), u.email, 1 if u.is_active else 0)
            )
            r = conn.execute("SELECT * FROM users WHERE id=?", (cur.lastrowid,)).fetchone()
            return to_user_dict(r)
        except Exception:
            raise HTTPException(400, "username ya existe o datos inválidos")

@app.get("/users")
def list_users(skip: int=0, limit: int=100):
    with sqlite3.connect(DB) as conn:
        rows = conn.execute("SELECT * FROM users ORDER BY id LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    return [to_user_dict(r) for r in rows]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    with sqlite3.connect(DB) as conn:
        r = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if not r: raise HTTPException(404, "no encontrado")
    return to_user_dict(r)

@app.put("/users/{user_id}")
def update_user(user_id: int, d: UserUpdate):
    with sqlite3.connect(DB) as conn:
        r = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        if not r: raise HTTPException(404, "no encontrado")
        username = d.username if d.username is not None else r[1]
        email = d.email if d.email is not None else r[3]
        is_active = 1 if (d.is_active if d.is_active is not None else r[4]) else 0
        if username != r[1] and conn.execute("SELECT 1 FROM users WHERE username=? AND id<>?", (username, user_id)).fetchone():
            raise HTTPException(400, "username en uso")
        conn.execute("UPDATE users SET username=?, email=?, is_active=? WHERE id=?", (username, email, is_active, user_id))
        nr = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    return to_user_dict(nr)

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with sqlite3.connect(DB) as conn:
        if not conn.execute("SELECT 1 FROM users WHERE id=?", (user_id,)).fetchone():
            raise HTTPException(404, "no encontrado")
        conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    return {"detail":"eliminado"}

@app.post("/login")
def login(d: LoginIn):
    with sqlite3.connect(DB) as conn:
        r = conn.execute("SELECT password,is_active FROM users WHERE username=?", (d.username,)).fetchone()
    if not r or hashlib.sha256(d.password.encode()).hexdigest() != r[0]:
        return {"message":"Login fallido"}
    if not bool(r[1]): return {"message":"Usuario inactivo"}
    return {"message":"Login exitoso"}

@app.get("/simulate_bruteforce/{clave}")
def simulate_bruteforce(clave: str):
    intentos, segundos = fuerza_bruta(clave)
    return {"clave":clave,"intentos":intentos,"tiempo_s":round(segundos,6)}


