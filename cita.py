import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from PIL import Image, ImageTk
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta del archivo de recursos, compatible con PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# Lista de provincias
provincias = ["Zaragoza", "Valladolid", "Toledo", "Segovia", "Palencia", "Ourense", "Navarra", "Murcia", "Málaga", "Lugo", "Lleida", "León", "La Rioja", "Islas Baleares", "Huelva", "Granada", "Guipúzkoa", "Cuenca", "Córdoba", "Ceuta", "Cantabria", "Cádiz", "Cáceres", "Burgos", "Vizcaya", "Badajoz", "Asturias", "Almería", "Albacete", "A Coruña"]
tramites = ['Despliega para ver trámites disponibles en esta provincia', 'FAMILIARES DE RESIDENTES COMUNITARIOS', 'INFORMACIÓN', 'RENOVACIONES, PRÓRROGAS Y MODIFICACIONES', 'RESIDENCIA INICIAL', 'Despliega para ver trámites disponibles en esta provincia', 'POLICIA - RECOGIDA DE TARJETA DE IDENTIDAD DE EXTRANJERO (TIE)', 'POLICIA - TÍTULOS DE VIAJE', 'POLICIA- SOLICITUD ASILO', 'POLICIA-AUTORIZACIÓN DE REGRESO', 'POLICIA-CARTA DE INVITACIÓN', 'POLICIA-CERTIFICADO DE REGISTRO DE CIUDADANO DE LA U.E.', 'POLICIA-CERTIFICADOS (DE RESIDENCIA, DE NO RESIDENCIA Y DE CONCORDANCIA)', 'POLICIA-INFORMACION DE TRÁMITES DE LA COMISARÍA DE POLICIA', 'POLICIA-TOMA DE HUELLA (EXPEDICIÓN DE TARJETA), RENOVACIÓN DE TARJETA DE LARGA DURACIÓN Y DUPLICADO', 'POLICÍA - CÉDULA DE INSCRIPCIÓN', 'POLICÍA TARJETA CONFLICTO UCRANIA–ПОЛІЦІЯ -КАРТКА ДЛЯ ПЕРЕМІЩЕНИХ ОСІБ ВНАСЛІДОК КОНФЛІКТУ В УКРАЇНІ', 'POLICÍA-RECOGIDA DE TARJETA ROJA (PROTECCIÓN INTERNACIONAL)']
paises =["Seleccionar ...","AFGANISTAN","ALBANIA","ALEMANIA","ANDORRA","ANGOLA","ANGUILLA","ANTIGUA Y BARBUDA","ANTILLAS NL.","APATRIDA","ARABIA SAUDI","ARGELIA","ARGENTINA","ARMENIA","ARUBA","AUSTRALIA","AUSTRIA","AZERBAYAN","BAHAMAS","BAHREIN","BANGLADESH","BARBADOS","BELGICA","BELICE","BENIN","BHUTAN","BIELORRUSIA O BELARUS","BOLIVIA","BOSNIA-HERZEGOVINA","BOTSWANA","BRASIL","BRUNEI DARUSSALAM","BULGARIA","BURKINA FASO","BURUNDI","CABO VERDE","CAMBOYA","CAMERUN","CANADA","CENTROAFRICA REPUBLICA","CHAD","CHILE","CHINA","CHIPRE","COLOMBIA","COMORES","CONGO BRAZZAVILLE","COREA"," REP. POP. DEMOC.","COREA"," REPUBLICA","COSTA DE MARFIL","COSTA RICA","CROACIA","CUBA","DINAMARCA","DJIBOUTI","DOMINICA","DOMINICANA REPUBLICA","ECUADOR","EEUU","EGIPTO","EL SALVADOR","EL VATICANO","EMIRATOS ARABES UNIDOS","ERITREA","ESLOVAQUIA","ESLOVENIA","ESPAÑA","ESTONIA","ETIOPIA","FIDJI","FILIPINAS","FINLANDIA","FRANCIA","GABON","GAMBIA","GEORGIA","GHANA","GRANADA REPUBLICA","GRECIA","GUATEMALA","GUAYANA","GUINEA ECUATORIAL","GUINEA REPUBLICA","GUINEA-BISSAU","HAITI","HOLANDA","HONDURAS","HUNGRIA","INDIA","INDONESIA","IRAK","IRAN","IRLANDA","ISLANDIA","ISLAS MARSCHALL","ISRAEL","ITALIA","JAMAICA","JAPON","JORDANIA","KAZAJSTAN","KENIA","KIRGUISTAN","KIRIBATI","KUWAIT","LAOS","LAS MALDIVAS","LESOTHO","LETONIA","LIBANO","LIBERIA","LIBIA","LIECHTENSTEIN","LITUANIA","LUXEMBURGO","MACAO","MACEDONIA","MADAGASCAR","MALASIA","MALASIA - GRAN BRETAÑA","MALAWI","MALI","MALTA","MARRUECOS","MAURICIO","MAURITANIA","MEJICO","MICRONESIA","MOLDAVIA","MONACO","MONGOLIA","MONTENEGRO","MOZAMBIQUE","MYANMAR","NAMIBIA","NAURU","NEPAL","NICARAGUA","NIGER","NIGERIA","NORUEGA","NUEVA ZELANDA","OMAN","PAKISTAN","PALESTINA","PANAMA","PAPUA NUEVA GUINEA","PARAGUAY","PERU","POLONIA","PORTUGAL","PUERTO RICO","QATAR","REINO UNIDO","REP. DEMOCRATICA DEL CONGO (EX-ZAIRE)","REPUBLICA CHECA","REUNION-COMO","RUANDA","RUMANIA","RUSIA","SALOMON","SAMOA OCCIDENTAL","SAN CRISTOBAL Y NEVIS","SAN MARINO","SAN VICENTE","SANTA LUCIA","SANTO TOME Y PRINCIPE","SEICHELLES","SENEGAL","SENEGAMBIA","SERBIA","SIERRA LEONA","SINGAPUR","SIRIA","SOMALIA","SRI LANKA","SUDAFRICA","SUDAN","SUECIA","SUIZA","SURINAM","SWAZILANDIA","TADJIKISTAN","TAIWAN","TANZANIA","THAILANDIA","TIMOR ORIENTAL","TOGO","TONGA","TRINIDAD Y TOBAGO","TUNEZ","TURKMENIA","TURQUIA","TUVALU","UCRANIA","UGANDA","URUGUAY","UZBEKISTAN","VANUATU","VENEZUELA","VIETNAM","YEMEN","ZAMBIA","ZIMBABWE"]
def obtener_tramites(driver):
    """Obtiene los trámites disponibles desde la página web."""
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'tramiteGrupo[0]')))
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
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option("detach", True)
        # driver = webdriver.Chrome(options=options)
        # driver.get("https://icp.administracionelectronica.gob.es/icpplus/index.html")

            # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'form')))
            # select_provincia = Select(driver.find_element(By.ID, 'form'))
            # select_provincia.select_by_visible_text(selected_province)

            # accept_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Aceptar']")))
            # accept_button.click()

            # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'tramiteGrupo[0]')))

            #tramites = obtener_tramites(driver)
        tramite_combo['values'] = tramites
        tramite_combo.config(state='normal')
        habilitar_boton_solicitar(True)
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
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'form')))
        select_provincia = Select(driver.find_element(By.ID, 'form'))
        select_provincia.select_by_visible_text(selected_province)

        accept_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Aceptar']")))
        accept_button.click()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'tramiteGrupo[0]')))

        #tramites = obtener_tramites(driver)
        if selected_tramite in tramites:
            if selected_tramite in Select(driver.find_element(By.ID, 'tramiteGrupo[0]')).options:
                tramite_section_id = 'tramiteGrupo[0]'
            else:
                tramite_section_id = 'tramiteGrupo[1]'
            
            tramite_section = Select(driver.find_element(By.ID, tramite_section_id))
            tramite_section.select_by_visible_text(selected_tramite)

            accept_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Aceptar']")))
            accept_button.click()

            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Entrar']")))

            entrar_button = driver.find_element(By.XPATH, "//input[@value='Entrar']")
            entrar_button.submit()

            completar_formulario(driver, documento_tipo, numero_documento, nombre, apellidos, nacimiento, pais)

            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'btnSiguiente')))

            siguiente_button = driver.find_element(By.NAME, 'btnSiguiente')
            siguiente_button.click()

            print("Automatización completa. El navegador permanecerá abierto.")
            input("Presiona Enter para cerrar el navegador...")
        else:
            print(f"El trámite seleccionado no está disponible para la provincia seleccionada.")
    except Exception as e:
        print(f"Error durante la automatización: {e}")
    finally:
        print('fin')

def completar_formulario(driver, documento_tipo, numero_documento, nombre, apellidos, nacimiento, pais):
    """Completa el formulario de la segunda página."""
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'txtIdCitado')))
        if documento_tipo == 'PASAPORTE':
            radio_button_id = 'rdbTipoDocPas'
        else:
            radio_button_id = 'rdbTipoDocNie'

        radio_button = driver.find_element(By.ID, radio_button_id)
        if not radio_button.is_selected():
            radio_button.click()

        id_citado_field = driver.find_element(By.NAME, 'txtIdCitado')
        id_citado_field.clear()
        id_citado_field.send_keys(numero_documento)

        driver.find_element(By.NAME, 'txtDesCitado').clear()
        driver.find_element(By.NAME, 'txtDesCitado').send_keys(nombre + " " + apellidos)
        driver.find_element(By.NAME, 'txtAnnoCitado').clear()
        driver.find_element(By.NAME, 'txtAnnoCitado').send_keys(nacimiento)

        # Seleccionar el país introducido por el usuario
        select_pais = Select(driver.find_element(By.NAME, 'txtPaisNac'))
        select_pais.select_by_visible_text(pais.upper())

        driver.find_element(By.NAME, 'btnAceptar').click()
    except Exception as e:
        print(f"Error al completar el formulario: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Solicitud de Cita Automatizada")
root.configure(bg='#39777C')

# Cargar imagen
img_path = resource_path("bot.png")  # Reemplaza con el nombre de tu archivo de imagen
try:
    img = Image.open(img_path)
    img = img.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=img, bg='#39777C')
    img_label.grid(row=0, column=0, columnspan=4, sticky="nsew")
except Exception as e:
    print(f"Error al cargar la imagen: {e}")

# Título de la aplicación
title_label = tk.Label(root, text="Solicitud de Cita Automatizada", font=('Arial', 16, 'bold'), bg='#39777C', fg='black')
title_label.grid(row=1, column=0, columnspan=3, pady=20)

# Combo box para seleccionar la provincia
province_var = tk.StringVar(value='Selecciona una provincia')
province_label = tk.Label(root, text="Provincia:", bg='#39777C', fg='black')
province_label.grid(column=0, row=2, padx=10, pady=5, sticky='e')
province_combo = ttk.Combobox(root, textvariable=province_var, values=['Selecciona una provincia'] + provincias)
province_combo.grid(column=1, row=2, padx=10, pady=5, sticky='ew')
province_combo.bind("<<ComboboxSelected>>", actualizar_tramites)

# Combo box para seleccionar el trámite
tramite_var = tk.StringVar(value='Selecciona un trámite')
tramite_label = tk.Label(root, text="Trámite:", bg='#39777C', fg='black')
tramite_label.grid(column=0, row=3, padx=10, pady=5, sticky='e')
tramite_combo = ttk.Combobox(root, textvariable=tramite_var, state='disabled')
tramite_combo.grid(column=1, row=3, padx=10, pady=5, sticky='ew')

# Combo box para seleccionar el tipo de documento
documento_var = tk.StringVar(value='PASAPORTE')
documento_label = tk.Label(root, text="Tipo de Documento:", bg='#39777C', fg='black')
documento_label.grid(column=0, row=4, padx=10, pady=5, sticky='e')
documento_combo = ttk.Combobox(root, textvariable=documento_var, values=['N.I.E.', 'PASAPORTE'], state='readonly')
documento_combo.grid(column=1, row=4, padx=10, pady=5, sticky='ew')

# Entry para el número de documento
numero_var = tk.StringVar()
numero_label = tk.Label(root, text="Número de Documento:", bg='#39777C', fg='black')
numero_label.grid(column=0, row=5, padx=10, pady=5, sticky='e')
numero_entry = tk.Entry(root, textvariable=numero_var, font=('Arial', 12))
numero_entry.grid(column=1, row=5, padx=10, pady=5, sticky='ew')

# Entry para el país
pais_var = tk.StringVar(value='Seleccionar ...')
pais_label = tk.Label(root,text="País:", bg='#39777C', fg='black')
pais_label.grid(column=0, row=6, padx=10, pady=5, sticky='e')
pais_combo = ttk.Combobox(root, textvariable=pais_var, values=paises, state='readonly')
pais_combo.grid(column=1, row=6, padx=10, pady=5, sticky='ew')

# Campos del formulario
nombre_var = tk.StringVar()
apellidos_var = tk.StringVar()
nacimiento_var = tk.StringVar()

nombre_label = tk.Label(root, text="Nombre:", bg='#39777C', fg='black')
nombre_label.grid(column=0, row=7, padx=10, pady=5, sticky='e')
nombre_entry = tk.Entry(root, textvariable=nombre_var, font=('Arial', 12))
nombre_entry.grid(column=1, row=7, padx=10, pady=5, sticky='ew')

apellidos_label = tk.Label(root, text="Apellidos:", bg='#39777C', fg='black')
apellidos_label.grid(column=0, row=8, padx=10, pady=5, sticky='e')
apellidos_entry = tk.Entry(root, textvariable=apellidos_var, font=('Arial', 12))
apellidos_entry.grid(column=1, row=8, padx=10, pady=5, sticky='ew')

nacimiento_label = tk.Label(root, text="Año de Nacimiento:", bg='#39777C', fg='black')
nacimiento_label.grid(column=0, row=9, padx=10, pady=5, sticky='e')
nacimiento_entry = tk.Entry(root, textvariable=nacimiento_var, font=('Arial', 12))
nacimiento_entry.grid(column=1, row=9, padx=10, pady=5, sticky='ew')

# Botón para solicitar cita
solicitar_button = tk.Button(root, text="Solicitar Cita", font=('Arial', 12, 'bold'), bg='#E85821', fg='black', state='disabled', command=solicitar_cita)
solicitar_button.grid(row=10, column=0, columnspan=3, pady=20)

# Ajustar el peso de las columnas y filas para que se expandan adecuadamente
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_rowconfigure(9, weight=1)
root.grid_rowconfigure(10, weight=1)

root.mainloop()
