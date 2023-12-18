import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
from pydantic import BaseModel

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

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.199", port=8080)
