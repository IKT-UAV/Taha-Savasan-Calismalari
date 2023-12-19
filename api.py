from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import psycopg2

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
        valid_kadi = "iktuavarac1"
        valid_sifre = "123456"

        if kadi == valid_kadi and sifre == valid_sifre:
            self.authenticated_user = kadi
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
        raise HTTPException(status_code=401, detail="Yetkisiz giris denemesi")
    return user_session.get_authenticated_user()


@app.post("/giris")
async def login(giris_data: GirisData):
    if user_session.authenticate_user(giris_data.kadi, giris_data.sifre):
        query = """
            INSERT INTO takimbilgileri (kadi, sifre)
            VALUES (%s, %s)
            """
        cur.execute(query, (giris_data.kadi, giris_data.sifre))
        conn.commit()
        return {"message": "Giris basarili!", "kadi": giris_data.kadi}
    else:
        raise HTTPException(status_code=401, detail="Yetkisiz giris denemesi")


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


@app.get("/qr_koordinati")
async def say_hello(current_user: str = Depends(get_current_user)):
    return {"enlem": "51", "boylam": "53,123456,11"}
