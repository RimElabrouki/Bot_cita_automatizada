import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from PIL import Image, ImageTk

# Lista de provincias en España
provincias = [
    "Zaragoza", "Valladolid", "Toledo", "Segovia", "Palencia", "Ourense",
    "Navarra", "Murcia", "Málaga", "Lugo", "Lleida", "León", "La Rioja",
    "Islas Baleares", "Huelva", "Granada", "Guipúzkoa", "Cuenca", "Córdoba",
    "Ceuta", "Cantabria", "Cádiz", "Cáceres", "Burgos", "Vizcaya", "Badajoz",
    "Asturias", "Almería", "Albacete", "A Coruña"
]

# Lista de países
paises = [
    "España", "Francia", "Alemania", "Italia", "Reino Unido", "Estados Unidos", "México",
    "Argentina", "Colombia", "Chile", "Perú", "Uruguay", "Venezuela"
]

def obtener_tramites(driver):
    """Obtiene los trámites disponibles desde la página web."""
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'tramiteGrupo[0]'))
        )
        tramites = []
        try:
            tramite_element_1 = driver.find_element(By.ID, 'tramiteGrupo[0]')
            tramites.extend([option.text for option in Select(tramite_element_1).options])
        except:
            pass

        try:
            tramite_element_2 = driver.find_element(By.ID, 'tramiteGrupo[1]')
            tramites.extend([option.text for option in Select(tramite_element_2).options])
        except:
            pass

        return tramites
    except Exception as e:
        print(f"Error al obtener la lista de trámites: {e}")
        return []

def actualizar_tramites(event=None):
    """Actualiza el combo box de trámites basado en la provincia seleccionada."""
    selected_province = province_var.get()
    if selected_province != "Selecciona una provincia":
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get("https://icp.administracionelectronica.gob.es/icpplus/index.html")

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'form'))
            )
            select_provincia = Select(driver.find_element(By.ID, 'form'))
            select_provincia.select_by_visible_text(selected_province)

            accept_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Aceptar']"))
            )
            accept_button.click()

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'tramiteGrupo[0]'))
            )

            tramites = obtener_tramites(driver)
            tramites = ["Selecciona un trámite"] + tramites
            tramite_combo['values'] = tramites
            tramite_combo.set('Selecciona un trámite')
            tramite_combo.config(state='normal')
            habilitar_boton_solicitar(True)
        finally:
            driver.quit()
    else:
        tramite_combo.config(state='disabled')
        tramite_combo.set('Selecciona un trámite')
        habilitar_boton_solicitar(False)

def habilitar_boton_solicitar(habilitar):
    """Habilita o deshabilita el botón de solicitar cita."""
    solicitar_button.config(state='normal' if habilitar else 'disabled')

def solicitar_cita():
    """Gestiona la solicitud de cita basándose en las selecciones realizadas."""
    selected_province = province_var.get()
    selected_tramite = tramite_var.get()
    documento_tipo = documento_var.get()
    numero_documento = numero_var.get()
    nombre = nombre_var.get()
    apellidos = apellidos_var.get()
    nacimiento = nacimiento_var.get()
    pais = pais_var.get()

    if selected_province != "Selecciona una provincia" and selected_tramite != "Selecciona un trámite":
        gg(selected_province, selected_tramite, documento_tipo, numero_documento, nombre, apellidos, nacimiento, pais)
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona tanto la provincia como el trámite.")

def gg(selected_province, selected_tramite, documento_tipo, numero_documento, nombre, apellidos, nacimiento, pais):
    """Automatiza la selección de la provincia y el trámite y realiza la solicitud."""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    driver.get("https://icp.administracionelectronica.gob.es/icpplus/index.html")

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'form'))
        )
        select_provincia = Select(driver.find_element(By.ID, 'form'))
        select_provincia.select_by_visible_text(selected_province)

        accept_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Aceptar']"))
        )
        accept_button.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'tramiteGrupo[0]'))
        )

        tramites = obtener_tramites(driver)
        if selected_tramite in tramites:
            if selected_tramite in Select(driver.find_element(By.ID, 'tramiteGrupo[0]')).options:
                tramite_section_id = 'tramiteGrupo[0]'
            else:
                tramite_section_id = 'tramiteGrupo[1]'
            
            tramite_section = Select(driver.find_element(By.ID, tramite_section_id))
            tramite_section.select_by_visible_text(selected_tramite)

            accept_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Aceptar']"))
            )
            accept_button.click()

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@value='Entrar']"))
            )

            entrar_button = driver.find_element(By.XPATH, "//input[@value='Entrar']")
            entrar_button.submit()

            completar_formulario(driver, documento_tipo, numero_documento, nombre, apellidos, nacimiento, pais)

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, 'btnSiguiente'))
            )

            siguiente_button = driver.find_element(By.NAME, 'btnSiguiente')
            siguiente_button.click()

            print("Automatización completa. El navegador permanecerá abierto.")
            input("Presiona Enter para cerrar el navegador...")
        else:
            print(f"El trámite seleccionado no está disponible para la provincia seleccionada.")
    except Exception as e:
        print(f"Error durante la automatización: {e}")
    finally:
        driver.quit()

def completar_formulario(driver, documento_tipo, numero_documento, nombre, apellidos, nacimiento, pais):
    """Completa el formulario de la segunda página."""
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'txtIdCitado'))
        )

        id_citado_field = driver.find_element(By.NAME, 'txtIdCitado')
        id_citado_field.clear()
        id_citado_field.send_keys(numero_documento)

        driver.find_element(By.NAME, 'txtDesCitado').clear()
        driver.find_element(By.NAME, 'txtDesCitado').send_keys(nombre + " " + apellidos)
        driver.find_element(By.NAME, 'txtAnnoCitado').clear()
        driver.find_element(By.NAME, 'txtAnnoCitado').send_keys(nacimiento)
        driver.find_element(By.NAME, 'txtPaisNac').clear()
        driver.find_element(By.NAME, 'txtPaisNac').send_keys(pais)
        driver.find_element(By.NAME, 'txtTipoDoc').clear()
        driver.find_element(By.NAME, 'txtTipoDoc').send_keys(documento_tipo)

        # Ahora se añade el tipo de documento automáticamente en el formulario
        # Si hay un campo de selección para tipo de documento, selecciona el valor aquí
        tipo_doc_select = Select(driver.find_element(By.NAME, 'tipoDocumento'))  # Asegúrate de que este sea el nombre correcto
        tipo_doc_select.select_by_visible_text(documento_tipo)

        # Hacer clic en el botón "Aceptar"
        accept_button = driver.find_element(By.XPATH, "//input[@value='Aceptar']")
        accept_button.click()

    except Exception as e:
        print(f"Error al completar el formulario: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Solicitud de Cita Automatizada")

# Cargar la imagen y redimensionarla
imagen_fondo_pil = Image.open('bot.png')  # Cambia la ruta al archivo de tu imagen
imagen_fondo_pil = imagen_fondo_pil.resize((600, 325), Image.LANCZOS)  # Cambia el tamaño según sea necesario
imagen_fondo = ImageTk.PhotoImage(imagen_fondo_pil)

# Crear un Canvas
canvas = tk.Canvas(root, width=imagen_fondo_pil.width, height=imagen_fondo_pil.height)
canvas.grid(row=0, column=0, columnspan=3, sticky="nsew")

# Colocar la imagen en el Canvas
canvas.create_image(0, 0, anchor='nw', image=imagen_fondo)

# Título de la aplicación
title_label = tk.Label(root, text="Solicitud de Cita Automatizada", font=('Arial', 16, 'bold'), bg='#d3d3d3')
title_label.grid(row=0, column=0, columnspan=3, pady=20)

# Combo box para seleccionar la provincia
province_var = tk.StringVar(value='Selecciona una provincia')
province_combo = ttk.Combobox(root, textvariable=province_var)
province_combo['values'] = ['Selecciona una provincia'] + provincias
province_combo.grid(column=0, row=1, padx=10, pady=10, sticky='ew')
province_combo.bind("<<ComboboxSelected>>", actualizar_tramites)

# Combo box para seleccionar el trámite
tramite_var = tk.StringVar(value='Selecciona un trámite')
tramite_combo = ttk.Combobox(root, textvariable=tramite_var, state='disabled')
tramite_combo.grid(column=1, row=1, padx=10, pady=10, sticky='ew')

# Combo box para seleccionar el documento (NIE o Pasaporte)
documento_var = tk.StringVar(value='Pasaporte')
documento_combo = ttk.Combobox(root, textvariable=documento_var, values=['NIE', 'Pasaporte'], state='readonly')
documento_combo.grid(column=0, row=2, padx=10, pady=10, sticky='ew')

# Entry para el número de documento
numero_var = tk.StringVar()
numero_entry = tk.Entry(root, textvariable=numero_var, font=('Arial', 12))
numero_entry.grid(column=1, row=2, padx=10, pady=10, sticky='ew')

# Combo box para seleccionar el país
pais_var = tk.StringVar(value='Selecciona un país')
pais_combo = ttk.Combobox(root, textvariable=pais_var, values=['Selecciona un país'] + paises, state='readonly')
pais_combo.grid(column=0, row=3, padx=10, pady=10, sticky='ew')

# Campos del formulario
nombre_var = tk.StringVar()
apellidos_var = tk.StringVar()
nacimiento_var = tk.StringVar()

nombre_label = tk.Label(root, text="Nombre:", bg='#d3d3d3')
nombre_label.grid(column=0, row=4, padx=10, pady=5, sticky='e')
nombre_entry = tk.Entry(root, textvariable=nombre_var, font=('Arial', 12))
nombre_entry.grid(column=1, row=4, padx=10, pady=5, sticky='ew')

apellidos_label = tk.Label(root, text="Apellidos:", bg='#d3d3d3')
apellidos_label.grid(column=0, row=5, padx=10, pady=5, sticky='e')
apellidos_entry = tk.Entry(root, textvariable=apellidos_var, font=('Arial', 12))
apellidos_entry.grid(column=1, row=5, padx=10, pady=5, sticky='ew')

nacimiento_label = tk.Label(root, text="Año de Nacimiento:", bg='#d3d3d3')
nacimiento_label.grid(column=0, row=6, padx=10, pady=5, sticky='e')
nacimiento_entry = tk.Entry(root, textvariable=nacimiento_var, font=('Arial', 12))
nacimiento_entry.grid(column=1, row=6, padx=10, pady=5, sticky='ew')

# Botón para solicitar la cita
solicitar_button = ttk.Button(root, text="Solicitar Cita", command=solicitar_cita, state='disabled')
solicitar_button.grid(column=2, row=1, rowspan=6, padx=10, pady=10, sticky='ns')

# Ajustar el peso de las columnas y filas para que se expandan adecuadamente
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)

root.mainloop()
