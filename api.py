from datetime import datetime

import psycopg2
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

db_name = "savasan"
db_user = "postgres"
db_password = "fd49db33b2"
db_host = "localhost"
db_port = "5432"

conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
cur = conn.cursor()


class GirisData(BaseModel):
    kadi: str
    sifre: str


class UserSession:
    def __init__(self):
        self.authenticated_user = None

    def authenticate_user(self, kadi: str, sifre: str):
        query = "SELECT kadi, sifre FROM takimbilgileri WHERE kadi = %s AND sifre = %s"
        cur.execute(query, (kadi, sifre))
        result = cur.fetchone()

        if result:
            self.authenticated_user = result[0]
            return True
        else:
            return False

    def is_authenticated(self):
        return self.authenticated_user is not None

    def get_authenticated_user(self):
        return self.authenticated_user


user_session = UserSession()
app = FastAPI()


def get_current_user():
    if not user_session.is_authenticated():
        raise HTTPException(status_code=401, detail="Yetkisiz giriş denemesi!")
    return user_session.get_authenticated_user()


@app.post("/giris")
async def login(giris_data: GirisData):
    if user_session.authenticate_user(giris_data.kadi, giris_data.sifre):
        return {"message": "Giriş başarılı!", "kadi": giris_data.kadi}
    else:
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı.")


@app.get("/sunucusaati")
async def root(current_user: str = Depends(get_current_user)):
    return {"sunucusaati": datetime.now().isoformat()}


# Apply the same dependency to other endpoints
@app.post("/telemetri_gonder")
async def say_hello(current_user: str = Depends(get_current_user)):
    return {}


@app.post("/kilitlenme_bilgisi")
async def say_hello(current_user: str = Depends(get_current_user)):
    return {}


@app.post("/kamikaze_bilgisi")
async def say_hello(current_user: str = Depends(get_current_user)):
    return {}


def db_qr_al(qr_enlem=str, qr_boylam=str):
    query2 = "SELECT qr_enlem, qr_boylam FROM qrkoordinatlari"
    cur.execute(query2, (qr_enlem, qr_boylam))
    result = cur.fetchone()
    return result
@app.get("/qr_koordinati")
async def qr_koordinati(current_user: str = Depends(get_current_user)):
    return {db_qr_al()}
