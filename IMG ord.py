import os
import shutil
from datetime import datetime, time
from tkinter import Tk, Label, OptionMenu, Button, StringVar, Entry
from tkinter.filedialog import askdirectory

#Obtener nombre de usuario de la pc para trabajar en el directorio del usuario
usuario = os.environ.get("USERNAME")

#Ruta de las imagenes a clasificar
ruta_imagenes = rf"C:\Users\{usuario}\Pictures\Screenshots"

#Destino
ruta_destino = rf"C:\Users\{usuario}\Desktop"

def actualizar_dst():
    global label_ruta_dest
    ruta_anterior = label_ruta_dest["text"]
    ruta_actual = recortar_ruta_dst()
    if ruta_actual != "":
        label_ruta_dest.config(text=ruta_actual)
    else:
        label_ruta_dest.config(text=ruta_anterior)

def actualizar_img():
    global label_ruta_img
    ruta_anterior = label_ruta_img["text"]
    ruta_actual = recortar_ruta_img()

    if ruta_actual != "":
        label_ruta_img.config(text=ruta_actual)
    else:
        label_ruta_img.config(text=ruta_anterior)

def cambiar_dst():
    cambiar_ruta_dst()
    recortar_ruta_dst()
    actualizar_dst()

def cambiar_img():
    cambiar_ruta_img()
    recortar_ruta_img()
    actualizar_img()

def cambiar_ruta_dst():
    global ruta_destino
    ruta_nueva = askdirectory(title="Selecciona la carpeta de destino")
    if ruta_nueva:
        ruta_destino = ruta_nueva
    else:
        ruta_destino = ruta_destino

def cambiar_ruta_img():
    global ruta_imagenes
    ruta_nueva = askdirectory(title="Selecciona la carpeta de origen")
    if ruta_nueva:
        ruta_imagenes = ruta_nueva
    else:
        ruta_imagenes = ruta_imagenes

#Funcion para ejecutar la tarea
def procesar_seleccion():
    #Obtener el día de la semana seleccionado
    dia_semana = dias_semana.index(dia_var.get())

    #Obtener la hora de inicio y fin
    hora_inicio_str = hora_inicio_var.get()
    hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M")
    hora_inicio = datetime.combine(datetime.today(), hora_inicio.time())

    hora_fin_str = hora_fin_var.get()
    hora_fin = datetime.strptime(hora_fin_str, "%H:%M")
    hora_fin = datetime.combine(datetime.today(), hora_fin.time())

    #Crear la carpeta de destino si no existe
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)

    #Recorrer todas las imágenes en la carpeta de origen
    for archivo in os.listdir(ruta_imagenes):
        ruta_archivo = os.path.join(ruta_imagenes, archivo)

        #Verificar si el archivo es una imagen PNG(las capturas hechas estan en .png)
        if os.path.isfile(ruta_archivo) and archivo.lower().endswith(".png"):
            #Obtener datos de la fecha y hora de la imagen
            fecha_archivo = datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
            hora_archivo = fecha_archivo.time()

            #Comparar la hora de la imagen con la hora de inicio y fin previamente definido
            if fecha_archivo.weekday() == dia_semana and hora_inicio.time() <= hora_archivo <= hora_fin.time():
                #Copiar la imagen a la carpeta de destino
                shutil.move(ruta_archivo, ruta_destino)
                print(f"Imagen {archivo} copiada.")
    #Print para verificar que cada archivo se copie adecuadaente
    print("Finalizado :D")

#Configurar la interfaz gráfica con tkinter
ventana = Tk()
ventana.title("Filtrado de imagenes por día y hora")
#ventana.iconbitmap("channels4_profile.ico") icono de la app
#ventana.config(background="white")
ventana.geometry("400x200")
ventana.resizable(False, False)

# Label y lista desplegable para el día de la semana
Label(ventana, text="Día de la semana:").place(x=3, y=5)
dia_var = StringVar(ventana)
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
dia_var.set(dias_semana[0])
dia_menu = OptionMenu(ventana, dia_var, *dias_semana)
dia_menu.config(width=10)
dia_menu.place(x=100, y=3)

# Label y menú desplegable para la hora de inicio
Label(ventana, text="Hora de inicio:").place(x=3, y=40)
hora_inicio_var = StringVar(ventana)
hora_inicio_var.set("07:00") #Correspondiente a mi horario de clases para seleccionar rangos de horas INICIO
hora_inicio_menu = OptionMenu(ventana, hora_inicio_var, *["07:00", "08:00", "09:00", "10:00", "11:00",
                                                          "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
                                                          "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"])
hora_inicio_menu.place(x=100, y=35)

#Label y menú desplegable para la hora de fin definidos
Label(ventana, text="Hora de fin:").place(x=3, y=70)
hora_fin_var = StringVar(ventana)
hora_fin_var.set("23:00") #Correspondiente a mi horario de clases para seleccionar rangos de horas FIN
hora_fin_menu = OptionMenu(ventana, hora_fin_var, *["07:00", "08:00", "09:00", "10:00", "11:00",
                                                    "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
                                                    "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"])
hora_fin_menu.place(x=100, y=66)

#Label y entrada para cambiar la ruta de la carpeta
def recortar_ruta_dst():
    if len(ruta_destino) > 30:
        ruta_cortada_dst = f"{ruta_destino[:14]}...{ruta_destino[-15:]}"
    else:
        ruta_cortada_dst = ruta_destino
    return ruta_cortada_dst

label_text_dst = Label(ventana, text=f"Ruta destino:")
label_text_dst.place(x=3, y=128)
label_ruta_dest = Label(ventana, text=f"{recortar_ruta_dst()}")
label_ruta_dest.place(x=100, y=128)

Button(ventana, text="Cambiar", command=cambiar_img).place(x=300, y=96)

#Label para mostrar la ruta de la carpeta actual de manera estetética
def recortar_ruta_img():
    if len(ruta_imagenes) > 30:
        ruta_cortada_img = f"{ruta_imagenes[:14]}...{ruta_imagenes[-15:]}"
    else:
        ruta_cortada_img = ruta_imagenes
    return ruta_cortada_img

label_text_img = Label(ventana, text=f"Ruta origen:")
label_text_img.place(x=3, y=98)
label_ruta_img = Label(ventana, text=f"{recortar_ruta_img()}")
label_ruta_img.place(x=100, y=98)

Button(ventana, text="Cambiar", command=cambiar_dst).place(x=300, y=127)

#Botón para ejecutar la tarea
Button(ventana, text="Procesar", command=procesar_seleccion).place(x=155, y=160)

while ventana.winfo_exists():
    try:
        ventana.update()
    except KeyboardInterrupt:
        break