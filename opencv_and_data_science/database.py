import socket
import sqlite3 as sql
import threading

bag1 = sql.connect("database.db")
cursor = bag1.cursor()

HOST = '127.0.0.1'
PORT = 80

def fon1():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS OGRENCILER(
        YUZVERISI text,
        AD text,
        SOYAD text,
        YAS text,
        BOY text,
        KILO text,
        ANNEADI text,
        BABAADI text,
        ANNETELNO text,
        BABATELNO text,
        BASARILARI text,
        OKUDUGUOKULLAR text,
        KENDITELNO text,
        TCKIMLIK text,
        DOGUMTARIHI text
    )""")
    bag1.commit()

def fon2(veri1):
    cursor.execute("""
    INSERT INTO OGRENCILER (
        YUZVERISI, AD, SOYAD, YAS, BOY, KILO, ANNEADI, BABAADI, ANNETELNO, 
        BABATELNO, BASARILARI, OKUDUGUOKULLAR, KENDITELNO, TCKIMLIK, DOGUMTARIHI
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, veri1)
    tabloyu_yazdir()
    bag1.commit()

def veri_al():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            veri = s.recv(1024)  
            if veri:
                print("Veri alındı:", veri.decode())
                return tuple(veri.decode().split(',')) 
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
    return None

def tabloyu_yazdir():
    cursor.execute("SELECT * FROM OGRENCILER")
    rows = cursor.fetchall()
    for row in rows:
        print(" | ".join(str(item) for item in row))

def close():
    bag1.close()

def main():
    veri1 = veri_al()
    if veri1:
        fon2(veri1)

tabloyu_yazdir()
fon1()

main()

close()
