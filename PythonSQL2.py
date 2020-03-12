
from urllib.request import urlopen
from bs4 import BeautifulSoup
import mysql.connector as mysql
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as mBox

def conexion_bd():
    operacion.execute(f"INSERT IGNORE INTO links values('{pa_ini.get()}', 0)")
    conexion.commit()
    url=urlopen(str(pa_ini.get()))
    ite=1
    paux=pa_ini.get()
    ventana2=tk.Tk()
    exi=ttk.Label(ventana2, text="Extraer los enlaces de la página Web: "+pa_ini.get()+"\n")
    exi.grid(column=0, row=0)
    bs=BeautifulSoup(url.read(), 'html.parser')
    statuto=False
    while(statuto==False):
        ite=ite+1
        for enlaces in bs.find_all("a"):
            try:
                impri="href: {}".format(enlaces.get("href"))
                paginax=str(enlaces.get("href"))
                if str(paginax)[:3]=="htt":
                    operacion.execute(f"INSERT IGNORE INTO links values('{paginax}', 0)")
                    conexion.commit()
                    pipo=ttk.Label(ventana2, text=impri)
                    pipo.grid(column=0, row=ite)
                ite=ite+1
            except:
                print("")    
        fis=ttk.Label(ventana2, text="\nFin de los enlaces encontrados")
        fis.grid(column=0, row=ite)  
        operacion.execute(f"update links set estatus=1 where pagina='{paux}'")
        paux=""
        operacion.execute( "SELECT * FROM links" )
        for pagina, estatus in operacion.fetchall():
            if(estatus==0):
                statuto=False
                break
            else:
                statuto=True    
        if statuto==False:   
            try:
                paux=pagina
                url = urlopen(paux)
                bs = BeautifulSoup(url.read(), 'html.parser')
            except:
                print("")    
ventana=tk.Tk()
ventana.title("Topicos Avanzados de programacion")
ventana.geometry("400x200")

conexion = mysql.connect( host='localhost', user= 'root', passwd='root', db='topicos' )
operacion = conexion.cursor()

urr=ttk.Label(ventana, text="Ingresa el link: ")
urr.grid(column=0, row=0)
pa_ini=tk.StringVar()
urlCapturado=ttk.Entry(ventana, width=32, textvariable=pa_ini)
urlCapturado.grid(column=1, row=0)

impriper=ttk.Button(ventana, text="Iniciar", command=conexion_bd)
impriper.grid(column=2, row=1)

ventana.mainloop()