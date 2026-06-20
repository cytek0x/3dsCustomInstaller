import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys
import threading
import struct
from motor_backend import MotorInstalacion
import tkinter as tk
from PIL import Image, ImageDraw
from pyctr.type.cia import CIAReader
from pyctr.crypto import CryptoEngine 
import urllib.request
import json

try:
    import ctypes
    mi_app_id = 'cytek0x.3dscustominstaller.modern.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(mi_app_id)
except Exception:
    pass

def configurar_entorno_dependencias():
    try:
        ruta_binarios = os.path.join(sys._MEIPASS, "custominstall", "bin", "win32")
    except Exception:
        ruta_binarios = os.path.abspath(os.path.join("custominstall", "bin", "win32"))
        
    os.environ["PATH"] = ruta_binarios + os.pathsep + os.environ.get("PATH", "")

def resolver_ruta_recurso(ruta_relativa):
    if getattr(sys, 'frozen', False):
        ruta_base = os.path.dirname(sys.executable)
    else:
        ruta_base = os.path.abspath(".")
    return os.path.join(ruta_base, ruta_relativa)

def aplicar_icono(ventana):
    ruta = resolver_ruta_recurso("icon.ico")
    if os.path.exists(ruta):
        try:
            ventana.iconbitmap(ruta)
        except Exception:
            pass

configurar_entorno_dependencias()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

TEXTOS = {
    "es": {
        "titulo_app": "INSTALADOR DE CIAS (CUSTOM INSTALL)",
        "sd_ruta": "RUTA DE LA SD:",
        "sd_placeholder": "CARPETA RAÍZ DE LA SD (EJ: E:/)",
        "btn_examinar": "EXAMINAR",
        "archivos_sistema": "ARCHIVOS DEL SISTEMA",
        "seleccionar": "SELECCIONAR",
        "opcional_seeddb": "OPCIONAL (PARA JUEGOS +2015)",
        "juegos_instalar": "JUEGOS A INSTALAR (.CIA)",
        "btn_avanzadas": "FUNCIONES AVANZADAS",
        "titulo_partidas": "INYECCIÓN DE PARTIDAS (.SAV)",
        "titulo_region": "PARCHEO DE REGIÓN (LUMA)",
        "lbl_seleccionar_sav": "ARCHIVO DE PARTIDA (.SAV):",
        "btn_cargar_sav": "EXAMINAR .SAV",
        "chk_parche_region": "HABILITAR EMULACIÓN DE REGIÓN",
        "lbl_forzar_idioma": "FORZAR IDIOMA:",
        "btn_juegos_instalados": "JUEGOS INSTALADOS",
        "titulo_instalados": "DETECTADOS EN LA SD",
        "btn_escanear": "ESCANEAR SD",
        "popup_fin_titulo": "INSTALACIÓN COMPLETADA",
        "popup_fin_paso": "PASO FINAL:",
        "popup_fin_inst1": "EJECUTA CUSTOM-INSTALL-FINALIZE A TRAVÉS \nDEL HOMEBREW LAUNCHER.",
        "popup_fin_inst2": "ESTO INSTALARÁ LOS TICKETS Y LAS LLAVES (SEEDS) SI ES REQUERIDO.",
        "popup_fin_inst3": "CUSTOM-INSTALL-FINALIZE HA SIDO COPIADO A TU TARJETA SD.",
        "btn_entendido": "ENTENDIDO",
        "col_nombre": "NOMBRE",
        "col_tamano": "TAMAÑO",
        "col_ubicacion": "UBICACIÓN",
        "col_estado": "ESTADO",
        "btn_add_archivos": "AÑADIR ARCHIVOS",
        "btn_add_carpeta": "AÑADIR CARPETA",
        "btn_limpiar_lista": "LIMPIAR LISTA",
        "col_tipo": "TIPO",
        "tipo_juego": "JUEGO BASE",
        "tipo_update": "UPDATE",
        "tipo_dlc": "DLC",
        "tipo_dsiware": "DSIWARE",
        "tipo_otro": "DESCONOCIDO",
        "tamano_total": "TAMAÑO TOTAL A INSTALAR:",
        "btn_instalar": "INSTALAR",
        "btn_mostrar_log": "MOSTRAR LOG",
        "log_titulo": "LOG DE INSTALACIÓN - EN TIEMPO REAL",
        "estado_espera": "EN ESPERA...",
        "estado_instalando": "INSTALANDO...",
        "estado_finalizando": "FINALIZANDO...",
        "estado_instalado": "INSTALADO",
        "estado_error": "ERROR",
        "dialogo_sd_titulo": "SELECCIONA LA CARPETA RAÍZ DE TU TARJETA SD",
        "dialogo_add_juegos": "SELECCIONA LOS JUEGOS",
        "dialogo_add_carpeta": "SELECCIONA LA CARPETA CON JUEGOS .CIA",
        "modal_importando": "IMPORTANDO...",
        "modal_procesando": "PROCESANDO",
        "modal_archivos_espera": "ARCHIVOS...\n\nPOR FAVOR, ESPERA.",
        "msg_archivos_faltan_titulo": "ARCHIVOS NO ENCONTRADOS",
        "msg_archivos_faltan_texto": "NO SE ENCONTRARON LOS ARCHIVOS NECESARIOS EN LA SD, DEBES DE BUSCARLOS MANUALMENTE.",
        "msg_error_critico_titulo": "ERROR CRÍTICO",
        "msg_error_critico_texto": "FALTAN ARCHIVOS ESENCIALES (BOOT9.BIN O MOVABLE.SED).",
        "msg_lista_vacia_titulo": "LISTA VACÍA",
        "msg_lista_vacia_texto": "NO HAS AÑADIDO NINGÚN JUEGO (.CIA) PARA INSTALAR.",
        "msg_falta_seeddb_titulo": "ADVERTENCIA: FALTA SEEDDB.BIN",
        "msg_falta_seeddb_texto": "NO HAS SELECCIONADO EL ARCHIVO SEEDDB.BIN.\n\nLOS JUEGOS BASE CLÁSICOS SE INSTALARÁN SIN PROBLEMA, PERO LOS TÍTULOS RECIENTES (2015+) O ACTUALIZACIONES PODRÍAN NO FUNCIONAR.\n\n¿DESEAS CONTINUAR CON LA INSTALACIÓN DE TODOS MODOS?",
        "titulo_ventana": "3DS CUSTOM INSTALL - MODERN GUI",
        "msg_sd_invalida": "SELECCIONA UNA SD VÁLIDA.",
        "msg_no_nintendo3ds": "CARPETA 'NINTENDO 3DS' NO ENCONTRADA.",
        "msg_cargando_db": "CARGANDO BASE DE DATOS \nY ANALIZANDO SD...",
        "msg_error_lectura": "ERROR DE LECTURA:\n{}",
        "msg_no_juegos": "NO SE ENCONTRARON JUEGOS.",
        "msg_titulo_desconocido": "TÍTULO DESCONOCIDO",
        "log_err_db_local": "ERROR LEYENDO LA DB LOCAL: {}. SE VOLVERÁ A DESCARGAR.",
        "log_db_no_encontrada": "BASE DE DATOS NO ENCONTRADA. DESCARGANDO PARA USO OFFLINE...",
        "log_aviso_descarga": "AVISO: NO SE PUDO DESCARGAR LA REGIÓN {}: {}",
        "log_db_guardada": "BASE DE DATOS GUARDADA EN {}. ¡AHORA ES 100% OFFLINE!",
        "log_err_guardar_db": "ERROR AL GUARDAR EL ARCHIVO OFFLINE: {}",
        "log_err_seeddb": "ERROR AL LEER SEEDDB.BIN: {}",
        "log_llave_no_seeddb": "[{}] LA LLAVE DE {} NO ESTÁ EN TU SEEDDB.BIN. SE USARÁ EL ÍCONO GRIS.",
        "log_err_extraer_icono": "[{}] NO SE PUDO EXTRAER EL ICONO DE {}: {}",
        "log_err_grave": "ERROR GRAVE EN {}: {}",
        "msg_archivos_corruptos_titulo": "ARCHIVOS DESCARTADOS",
        "msg_archivos_corruptos_texto": "LOS SIGUIENTES ARCHIVOS ESTÁN CORRUPTOS O NO SON CIAS VÁLIDOS Y FUERON DESCARTADOS:\n\n{}",
        "estado_omitido": "OMITIDO (SIN SEED)",
    },
    
    "en": {
        "titulo_app": "CIA INSTALLER (CUSTOM INSTALL)",
        "sd_ruta": "SD PATH:",
        "sd_placeholder": "SD ROOT FOLDER (EX: E:/)",
        "btn_examinar": "BROWSE",
        "archivos_sistema": "SYSTEM FILES",
        "seleccionar": "SELECT",
        "opcional_seeddb": "OPTIONAL (FOR 2015+ GAMES)",
        "juegos_instalar": "GAMES TO INSTALL (.CIA)",
        "btn_avanzadas": "ADVANCED FEATURES",
        "titulo_partidas": "SAVE INJECTION (.SAV)",
        "titulo_region": "REGION PATCHING (LUMA)",
        "lbl_seleccionar_sav": "SAVE FILE (.SAV):",
        "btn_cargar_sav": "BROWSE .SAV",
        "chk_parche_region": "ENABLE REGION EMULATION",
        "lbl_forzar_idioma": "FORCE LANGUAGE:",
        "btn_juegos_instalados": "INSTALLED GAMES",
        "titulo_instalados": "DETECTED ON SD",
        "btn_escanear": "SCAN SD",
        "popup_fin_titulo": "INSTALLATION COMPLETE",
        "popup_fin_paso": "FINAL STEP:",
        "popup_fin_inst1": "RUN CUSTOM-INSTALL-FINALIZE THROUGH \nTHE HOMEBREW LAUNCHER.",
        "popup_fin_inst2": "THIS WILL INSTALL A TICKET AND SEED IF REQUIRED.",
        "popup_fin_inst3": "CUSTOM-INSTALL-FINALIZE HAS BEEN COPIED TO THE SD CARD.",
        "btn_entendido": "GOT IT",
        "col_nombre": "NAME",
        "col_tamano": "SIZE",
        "col_ubicacion": "LOCATION",
        "col_estado": "STATUS",
        "btn_add_archivos": "ADD FILES",
        "btn_add_carpeta": "ADD FOLDER",
        "btn_limpiar_lista": "CLEAR LIST",
        "col_tipo": "TYPE",
        "tipo_juego": "BASE GAME",
        "tipo_update": "UPDATE",
        "tipo_dlc": "DLC",
        "tipo_dsiware": "DSIWARE",
        "tipo_otro": "UNKNOWN",
        "tamano_total": "TOTAL SIZE TO INSTALL:",
        "btn_instalar": "INSTALL",
        "btn_mostrar_log": "SHOW LOG",
        "log_titulo": "INSTALLATION LOG - REAL TIME",
        "estado_espera": "WAITING...",
        "estado_instalando": "INSTALLING...",
        "estado_finalizando": "FINISHING...",
        "estado_instalado": "INSTALLED",
        "estado_error": "ERROR",
        "dialogo_sd_titulo": "SELECT THE ROOT FOLDER OF YOUR SD CARD",
        "dialogo_add_juegos": "SELECT THE GAMES",
        "dialogo_add_carpeta": "SELECT THE FOLDER CONTAINING .CIA GAMES",
        "modal_importando": "IMPORTING...",
        "modal_procesando": "PROCESSING",
        "modal_archivos_espera": "FILES...\n\nPLEASE WAIT.",
        "msg_archivos_faltan_titulo": "FILES NOT FOUND",
        "msg_archivos_faltan_texto": "THE NECESSARY FILES WERE NOT FOUND ON THE SD CARD, YOU MUST SEARCH FOR THEM MANUALLY.",
        "msg_error_critico_titulo": "CRITICAL ERROR",
        "msg_error_critico_texto": "ESSENTIAL FILES ARE MISSING (BOOT9.BIN OR MOVABLE.SED).",
        "msg_lista_vacia_titulo": "EMPTY LIST",
        "msg_lista_vacia_texto": "YOU HAVE NOT ADDED ANY GAME (.CIA) TO INSTALL.",
        "msg_falta_seeddb_titulo": "WARNING: MISSING SEEDDB.BIN",
        "msg_falta_seeddb_texto": "YOU HAVE NOT SELECTED THE SEEDDB.BIN FILE.\n\nCLASSIC BASE GAMES WILL INSTALL WITHOUT ISSUE, BUT RECENT TITLES (2015+) OR UPDATES MIGHT NOT WORK.\n\nDO YOU WANT TO PROCEED WITH THE INSTALLATION ANYWAY?",
        "titulo_ventana": "3DS CUSTOM INSTALL - MODERN GUI",
        "msg_sd_invalida": "SELECT A VALID SD CARD.",
        "msg_no_nintendo3ds": "'NINTENDO 3DS' FOLDER NOT FOUND.",
        "msg_cargando_db": "LOADING DATABASE \nAND ANALYZING SD...",
        "msg_error_lectura": "READ ERROR:\n{}",
        "msg_no_juegos": "NO GAMES FOUND.",
        "msg_titulo_desconocido": "UNKNOWN TITLE",
        "log_err_db_local": "ERROR READING LOCAL DB: {}. WILL REDOWNLOAD.",
        "log_db_no_encontrada": "DATABASE NOT FOUND. DOWNLOADING FOR OFFLINE USE...",
        "log_aviso_descarga": "WARNING: COULD NOT DOWNLOAD REGION {}: {}",
        "log_db_guardada": "DATABASE SAVED IN {}. NOW 100% OFFLINE!",
        "log_err_guardar_db": "ERROR SAVING OFFLINE FILE: {}",
        "log_err_seeddb": "ERROR READING SEEDDB.BIN: {}",
        "log_llave_no_seeddb": "[{}] THE KEY FOR {} IS NOT IN YOUR SEEDDB.BIN. GREY ICON WILL BE USED.",
        "log_err_extraer_icono": "[{}] COULD NOT EXTRACT ICON FROM {}: {}",
        "log_err_grave": "CRITICAL ERROR IN {}: {}",
        "msg_archivos_corruptos_titulo": "FILES DISCARDED",
        "msg_archivos_corruptos_texto": "THE FOLLOWING FILES ARE CORRUPTED OR INVALID CIAS AND WERE DISCARDED:\n\n{}",
        "estado_omitido": "SKIPPED (NO SEED)",
    }
}

class RedireccionConsola:
    def __init__(self, app_referencia, consola_original):
        self.app = app_referencia
        self.consola_original = consola_original

    def write(self, mensaje):
        if self.consola_original:
            self.consola_original.write(mensaje)
        self.app.escribir_en_log(mensaje)

    def flush(self):
        if self.consola_original:
            self.consola_original.flush()

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.mostrar)
        self.widget.bind("<Leave>", self.ocultar)

    def mostrar(self, event=None):
        if self.tooltip_window or not self.text: 
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 25
        
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=self.text, background="#2B2B2B", foreground="white", 
                         relief="solid", borderwidth=1, font=("Arial", 10), padx=5, pady=2)
        label.pack()

    def ocultar(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class CustomInstallModern(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.historial_logs = []
        self.ventana_log = None
        sys.stdout = RedireccionConsola(self, sys.stdout)
        sys.stderr = RedireccionConsola(self, sys.stderr)

        self.idioma_actual = "es"
        t = TEXTOS[self.idioma_actual]

        self.title(t["titulo_ventana"])
        self.ancho_base = 850  
        self.ancho_expandido = 1150 
        self.alto_base = 750   
        self.geometry(f"{self.ancho_base}x{self.alto_base}")
        self.panel_abierto = False
        self.resizable(False, False)

        ruta_icono = resolver_ruta_recurso("icon.ico")
        if os.path.exists(ruta_icono):
            self.iconbitmap(ruta_icono)

        self.frame_principal = ctk.CTkFrame(self, fg_color="transparent", width=self.ancho_base)
        self.frame_principal.pack(side="left", fill="both", expand=True)
        self.frame_principal.pack_propagate(False) 

        self.frame_cabecera = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_cabecera.pack(fill="x", pady=(15, 5), padx=20)

        self.menu_idioma = ctk.CTkOptionMenu(self.frame_cabecera, values=["Español", "English"], width=100, command=self.cambiar_idioma)
        self.menu_idioma.pack(side="left")

        self.label_titulo = ctk.CTkLabel(self.frame_cabecera, text=t["titulo_app"], font=ctk.CTkFont(size=22, weight="bold"))
        self.label_titulo.pack(side="left", expand=True)

        self.btn_avanzadas = ctk.CTkButton(self.frame_cabecera, text=t.get("btn_juegos_instalados", "JUEGOS INSTALADOS"), command=self.toggle_panel, fg_color="#2E86C1")
        self.btn_avanzadas.pack(side="right")

        self.frame_sd = ctk.CTkFrame(self.frame_principal)
        self.frame_sd.pack(pady=5, padx=20, fill="x")
        
        self.lbl_sd_ruta = ctk.CTkLabel(self.frame_sd, text=t["sd_ruta"], width=100, anchor="e")
        self.lbl_sd_ruta.pack(side="left", padx=10, pady=10)
        
        self.entry_sd = ctk.CTkEntry(self.frame_sd, width=500, placeholder_text=t["sd_placeholder"])
        self.entry_sd.pack(side="left", padx=5)
        
        self.btn_sd_examinar = ctk.CTkButton(self.frame_sd, text=t["btn_examinar"], width=100, command=self.seleccionar_sd)
        self.btn_sd_examinar.pack(side="right", padx=10)

        self.frame_crypto = ctk.CTkFrame(self.frame_principal)
        self.frame_crypto.pack(pady=10, padx=20, fill="x")
        
        self.lbl_archivos_sis = ctk.CTkLabel(self.frame_crypto, text=t["archivos_sistema"], font=ctk.CTkFont(weight="bold"))
        self.lbl_archivos_sis.pack(pady=(10, 5))

        self.crear_fila_archivo(self.frame_crypto, "boot9.bin:", f"{t['seleccionar']} boot9.bin", "boot9")
        self.crear_fila_archivo(self.frame_crypto, "movable.sed:", f"{t['seleccionar']} movable.sed", "movable")
        self.crear_fila_archivo(self.frame_crypto, "seeddb.bin:", t["opcional_seeddb"], "seeddb")

        self.frame_cias = ctk.CTkFrame(self.frame_principal)
        self.frame_cias.pack(pady=5, padx=20, fill="both", expand=True)

        self.lbl_juegos_instalar = ctk.CTkLabel(self.frame_cias, text=t["juegos_instalar"], font=ctk.CTkFont(weight="bold"))
        self.lbl_juegos_instalar.pack(pady=(10, 5))

        self.frame_headers = ctk.CTkFrame(self.frame_cias, fg_color="transparent")
        self.frame_headers.pack(fill="x", padx=15, pady=(0, 2))
        
        self.anchos_cols = [270, 90, 80, 140, 170] 

        self.lbl_col_nombre = ctk.CTkLabel(self.frame_headers, text=t["col_nombre"], width=self.anchos_cols[0], anchor="w", font=ctk.CTkFont(weight="bold"))
        self.lbl_col_nombre.grid(row=0, column=0, padx=5)
        
        self.lbl_col_tipo = ctk.CTkLabel(self.frame_headers, text=t["col_tipo"], width=self.anchos_cols[1], anchor="w", font=ctk.CTkFont(weight="bold"))
        self.lbl_col_tipo.grid(row=0, column=1, padx=5)
        
        self.lbl_col_tamano = ctk.CTkLabel(self.frame_headers, text=t["col_tamano"], width=self.anchos_cols[2], anchor="w", font=ctk.CTkFont(weight="bold"))
        self.lbl_col_tamano.grid(row=0, column=2, padx=5)
        
        self.lbl_col_ubicacion = ctk.CTkLabel(self.frame_headers, text=t["col_ubicacion"], width=self.anchos_cols[3], anchor="w", font=ctk.CTkFont(weight="bold"))
        self.lbl_col_ubicacion.grid(row=0, column=3, padx=5)
        
        self.lbl_col_estado = ctk.CTkLabel(self.frame_headers, text=t["col_estado"], width=self.anchos_cols[4], anchor="w", font=ctk.CTkFont(weight="bold"))
        self.lbl_col_estado.grid(row=0, column=4, padx=(5, 25))

        self.scroll_cias = ctk.CTkScrollableFrame(self.frame_cias, height=150)
        self.scroll_cias.pack(pady=2, padx=15, fill="both", expand=True)

        self.juegos_data = {}
        self.juego_seleccionado_actual = None

        self.frame_botones_cia = ctk.CTkFrame(self.frame_cias, fg_color="transparent")
        self.frame_botones_cia.pack(pady=10)
        
        self.btn_anadir_cia = ctk.CTkButton(self.frame_botones_cia, text=t["btn_add_archivos"], width=120, command=self.anadir_cia)
        self.btn_anadir_cia.pack(side="left", padx=10)
        
        self.btn_anadir_carpeta = ctk.CTkButton(self.frame_botones_cia, text=t["btn_add_carpeta"], width=120, command=self.anadir_carpeta_cia)
        self.btn_anadir_carpeta.pack(side="left", padx=10)
        
        self.btn_limpiar_cias = ctk.CTkButton(self.frame_botones_cia, text=t["btn_limpiar_lista"], width=120, fg_color="#8B0000", hover_color="#5C0000", command=self.limpiar_cias)
        self.btn_limpiar_cias.pack(side="left", padx=10)

        self.frame_ejecucion = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_ejecucion.pack(pady=10, fill="x", padx=20)

        self.lbl_total_tamano = ctk.CTkLabel(self.frame_ejecucion, text=f"{t['tamano_total']} 0.00 MB", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_total_tamano.pack(side="top", pady=(0, 5))

        self.barra_general = ctk.CTkProgressBar(self.frame_ejecucion, mode="determinate", height=15)
        self.barra_general.pack(side="top", fill="x", pady=(0, 10))
        self.barra_general.set(0.0)

        self.frame_botones_inferiores = ctk.CTkFrame(self.frame_ejecucion, fg_color="transparent")
        self.frame_botones_inferiores.pack(side="top")

        self.btn_instalar = ctk.CTkButton(self.frame_botones_inferiores, text=t["btn_instalar"], font=ctk.CTkFont(size=16, weight="bold"), height=40, command=self.ejecutar_instalacion)
        self.btn_instalar.pack(side="left", padx=10)

        self.btn_log = ctk.CTkButton(self.frame_botones_inferiores, text=t["btn_mostrar_log"], font=ctk.CTkFont(weight="bold"), fg_color="#4A4A4A", hover_color="#333333", height=40, command=self.abrir_ventana_log)
        self.btn_log.pack(side="left", padx=10)

        self.btn_creditos = ctk.CTkButton(self.frame_principal, text="Créditos", width=60, height=25, fg_color="transparent", text_color="#808B96", hover_color="#2C3E50", command=self.mostrar_creditos)
        self.btn_creditos.place(relx=0.98, rely=0.98, anchor="se")

        self.cambiar_estado_interfaz("disabled")

        self.frame_lateral = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.frame_lateral.pack_propagate(False) 

        self.lbl_titulo_instalados = ctk.CTkLabel(self.frame_lateral, text=t.get("titulo_instalados", "DETECTADOS EN LA SD"), font=ctk.CTkFont(weight="bold", size=16))
        self.lbl_titulo_instalados.pack(pady=(20, 10))

        self.btn_escanear_sd = ctk.CTkButton(self.frame_lateral, text=t.get("btn_escanear", "ESCANEAR SD"), command=self.escanear_juegos_sd, fg_color="#17A589")
        self.btn_escanear_sd.pack(pady=10, padx=20, fill="x")

        self.scroll_instalados = ctk.CTkScrollableFrame(self.frame_lateral)
        self.scroll_instalados.pack(fill="both", expand=True, padx=15, pady=(10, 20))

    def cambiar_idioma(self, seleccion):
        self.idioma_actual = "en" if seleccion == "English" else "es"
        t = TEXTOS[self.idioma_actual]

        self.title(t["titulo_ventana"])
        self.label_titulo.configure(text=t["titulo_app"])
        
        self.lbl_sd_ruta.configure(text=t["sd_ruta"])
        self.btn_sd_examinar.configure(text=t["btn_examinar"])
        
        self.lbl_archivos_sis.configure(text=t["archivos_sistema"])
        self.btn_boot9.configure(text=t["btn_examinar"])
        self.btn_movable.configure(text=t["btn_examinar"])
        self.btn_seeddb.configure(text=t["btn_examinar"])
        
        estado_sd = self.entry_sd.cget("state")
        self.entry_sd.configure(state="normal")
        self.entry_sd.configure(placeholder_text=t["sd_placeholder"])
        self.entry_sd.configure(state=estado_sd)

        estado_b9 = self.entry_boot9.cget("state")
        self.entry_boot9.configure(state="normal")
        self.entry_boot9.configure(placeholder_text=f"{t['seleccionar']} boot9.bin")
        self.entry_boot9.configure(state=estado_b9)

        estado_mv = self.entry_movable.cget("state")
        self.entry_movable.configure(state="normal")
        self.entry_movable.configure(placeholder_text=f"{t['seleccionar']} movable.sed")
        self.entry_movable.configure(state=estado_mv)

        estado_sdb = self.entry_seeddb.cget("state")
        self.entry_seeddb.configure(state="normal")
        self.entry_seeddb.configure(placeholder_text=t["opcional_seeddb"])
        self.entry_seeddb.configure(state=estado_sdb)

        self.btn_avanzadas.configure(text=t["btn_juegos_instalados"])
        
        self.lbl_titulo_instalados.configure(text=t["titulo_instalados"])
        self.btn_escanear_sd.configure(text=t["btn_escanear"])

        self.lbl_col_tipo.configure(text=t["col_tipo"])
        
        self.lbl_juegos_instalar.configure(text=t["juegos_instalar"])
        self.lbl_col_nombre.configure(text=t["col_nombre"])
        self.lbl_col_tamano.configure(text=t["col_tamano"])
        self.lbl_col_ubicacion.configure(text=t["col_ubicacion"])
        self.lbl_col_estado.configure(text=t["col_estado"])

        self.btn_anadir_cia.configure(text=t["btn_add_archivos"])
        self.btn_anadir_carpeta.configure(text=t["btn_add_carpeta"])
        self.btn_limpiar_cias.configure(text=t["btn_limpiar_lista"])
        
        self.btn_instalar.configure(text=t["btn_instalar"])
        self.btn_log.configure(text=t["btn_mostrar_log"])
        
        if self.ventana_log and self.ventana_log.winfo_exists():
            self.ventana_log.title(t["log_titulo"])

        self._actualizar_tamano_total()
        self._traducir_filas_existentes()

    def _traducir_filas_existentes(self):
        t = TEXTOS[self.idioma_actual]
        for ruta, datos in self.juegos_data.items():
            lbl = datos["lbl_estado"]
            if lbl.cget("text") in ["EN ESPERA...", "WAITING..."]:
                lbl.configure(text=t["estado_espera"])

    def toggle_panel(self):
        if self.panel_abierto:
            self.frame_lateral.pack_forget() 
            self.geometry(f"{self.ancho_base}x{self.alto_base}")
            self.panel_abierto = False
            
            if getattr(self, 'juego_seleccionado_actual', None):
                if self.juego_seleccionado_actual in self.juegos_data:
                    frame_anterior = self.juegos_data[self.juego_seleccionado_actual]["frame"]
                    frame_anterior.configure(fg_color="transparent") 
                self.juego_seleccionado_actual = None 
                
        else:
            self.geometry(f"{self.ancho_expandido}x{self.alto_base}")
            self.frame_lateral.pack(side="right", fill="y") 
            self.panel_abierto = True

    def abrir_ventana_log(self):
        if self.ventana_log is None or not self.ventana_log.winfo_exists():
            self.ventana_log = ctk.CTkToplevel(self)
            aplicar_icono(self.ventana_log)
            self.ventana_log.title(TEXTOS[self.idioma_actual]["log_titulo"])
            self.ventana_log.geometry("650x450")
            
            self.textbox_log = ctk.CTkTextbox(self.ventana_log, font=ctk.CTkFont(family="Consolas", size=12))
            self.textbox_log.pack(fill="both", expand=True, padx=10, pady=10)
            
            self.textbox_log.insert("end", "".join(self.historial_logs))
            self.textbox_log.configure(state="disabled")
            self.textbox_log.see("end")
        else:
            self.ventana_log.focus()

    def escribir_en_log(self, mensaje):
        self.historial_logs.append(mensaje)
        self.after(0, self._actualizar_textbox_log, mensaje)

    def _actualizar_textbox_log(self, mensaje):
        if self.ventana_log and self.ventana_log.winfo_exists():
            self.textbox_log.configure(state="normal")
            self.textbox_log.insert("end", mensaje)
            self.textbox_log.configure(state="disabled")
            self.textbox_log.see("end")

    def crear_fila_archivo(self, parent, label_text, placeholder, attr_name):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=2)
        
        lbl = ctk.CTkLabel(frame, text=label_text, width=100, anchor="e")
        lbl.pack(side="left", padx=10)
        setattr(self, f"lbl_{attr_name}", lbl)
        
        entry = ctk.CTkEntry(frame, width=500, placeholder_text=placeholder)
        entry.pack(side="left", padx=5)
        setattr(self, f"entry_{attr_name}", entry)
        
        btn = ctk.CTkButton(frame, text=TEXTOS[self.idioma_actual]["btn_examinar"], width=100, command=lambda: self.seleccionar_archivo(entry, label_text))
        btn.pack(side="right", padx=10)
        setattr(self, f"btn_{attr_name}", btn)

    def cambiar_estado_interfaz(self, estado):
        self.entry_boot9.configure(state=estado)
        self.btn_boot9.configure(state=estado)
        self.entry_movable.configure(state=estado)
        self.btn_movable.configure(state=estado)
        self.entry_seeddb.configure(state=estado)
        self.btn_seeddb.configure(state=estado)
        
        self.btn_anadir_cia.configure(state=estado)
        self.btn_anadir_carpeta.configure(state=estado)
        self.btn_limpiar_cias.configure(state=estado)
        self.btn_instalar.configure(state=estado)

    def seleccionar_sd(self):
        t = TEXTOS[self.idioma_actual]
        ruta = filedialog.askdirectory(title=t["dialogo_sd_titulo"])
        if ruta:
            ruta_normalizada = os.path.normpath(ruta)
            self.entry_sd.delete(0, 'end')
            self.entry_sd.insert(0, ruta_normalizada)
            self.buscar_archivos_clave(ruta_normalizada)

    def buscar_archivos_clave(self, ruta_sd):
        self.cambiar_estado_interfaz("normal")
        archivos_buscados = {"boot9": "boot9.bin", "movable": "movable.sed", "seeddb": "seeddb.bin"}
        subrutas = ["", "gm9/out"] 
        encontrados = {"boot9": False, "movable": False, "seeddb": False}

        for clave, nombre_archivo in archivos_buscados.items():
            entry_widget = getattr(self, f"entry_{clave}")
            entry_widget.delete(0, 'end')
            
            for subruta in subrutas:
                ruta_prueba = os.path.normpath(os.path.join(ruta_sd, subruta, nombre_archivo))
                if os.path.exists(ruta_prueba):
                    entry_widget.insert(0, ruta_prueba)
                    encontrados[clave] = True
                    break
                    
        if not encontrados["boot9"] or not encontrados["movable"]:
            t = TEXTOS[self.idioma_actual]
            messagebox.showwarning(t["msg_archivos_faltan_titulo"], t["msg_archivos_faltan_texto"])

    def seleccionar_archivo(self, entry_widget, tipo_archivo):
        t = TEXTOS[self.idioma_actual]
        ruta = filedialog.askopenfilename(title=f"{t['seleccionar']} {tipo_archivo}", filetypes=[("Archivos Binarios/SED", "*.*")])
        if ruta:
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, os.path.normpath(ruta))

    def obtener_tamano_formateado(self, ruta_archivo):
        tamano_bytes = os.path.getsize(ruta_archivo)
        tamano_mb = tamano_bytes / (1024 * 1024)
        if tamano_mb >= 1000:
            return f"{tamano_mb / 1024:.2f} GB"
        else:
            return f"{tamano_mb:.2f} MB"

    def _generar_icono_fallback(self):
        img = Image.new('RGB', (48, 48), color=(50, 50, 50)) 
        draw = ImageDraw.Draw(img)
        grosor = 3
        draw.line((16, 16, 32, 32), fill=(180, 70, 70), width=grosor)
        draw.line((16, 32, 32, 16), fill=(180, 70, 70), width=grosor)
        return ctk.CTkImage(light_image=img, dark_image=img, size=(32, 32))

    def _extraer_metadatos(self, ruta_cia):
        import re 
        t = TEXTOS[self.idioma_actual]
        icono = self._generar_icono_fallback()
        tipo_clave = "tipo_otro" 
        title_id = "0000000000000000" 
        
        try:
            boot9_path = self.entry_boot9.get()
            seeddb_path = self.entry_seeddb.get() 
            
            if not boot9_path or not os.path.exists(boot9_path):
                return icono, tipo_clave, title_id 

            crypto = CryptoEngine(boot9=boot9_path)
            necesita_seed = False
            
            try:
                with CIAReader(ruta_cia, crypto=crypto) as cia:
                    title_id = cia.tmd.title_id.lower()
            except Exception as e:
                error_str = repr(e)
                if "MissingSeedError" in error_str:
                    necesita_seed = True
                    match = re.search(r"([0-9a-fA-F]{16})", error_str)
                    if match:
                        title_id = match.group(1).lower()
                else:
                    raise e

            if title_id:
                prefijo = title_id[:8]
                if prefijo == "00040000": tipo_clave = "tipo_juego"
                elif prefijo == "0004000e": tipo_clave = "tipo_update"
                elif prefijo == "0004008c": tipo_clave = "tipo_dlc"
                elif prefijo in ["00048000", "0004800f", "00048004"]: tipo_clave = "tipo_dsiware"

            seed_bytes = None
            if necesita_seed and seeddb_path and os.path.exists(seeddb_path) and title_id:
                try:
                    target_tid = bytes.fromhex(title_id)[::-1] 
                    with open(seeddb_path, 'rb') as f:
                        data = f.read()
                        if len(data) >= 16:
                            count = int.from_bytes(data[0:4], byteorder='little')
                            for i in range(count):
                                offset = 16 + (i * 32)
                                if offset + 32 <= len(data):
                                    if data[offset : offset+8] == target_tid:
                                        seed_bytes = data[offset+8 : offset+24]
                                        break
                except Exception as e:
                    print(t["log_err_seeddb"].format(e))

            if necesita_seed and not seed_bytes:
                print(t["log_llave_no_seeddb"].format(title_id, os.path.basename(ruta_cia)))
            else:
                kwargs = {'crypto': crypto}
                if seed_bytes:
                    kwargs['seed'] = seed_bytes

                try:
                    with CIAReader(ruta_cia, **kwargs) as cia:
                        if cia.contents and 0 in cia.contents and cia.contents[0].exefs and cia.contents[0].exefs.icon:
                            icon_matrix = cia.contents[0].exefs.icon.icon_large_array
                            flat_pixels = [pixel for row in icon_matrix for pixel in row]
                            img_pil = Image.new('RGB', (48, 48))
                            img_pil.putdata(flat_pixels)
                            icono = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(32, 32))
                except Exception as error_icono:
                    print(t["log_err_extraer_icono"].format(title_id, os.path.basename(ruta_cia), repr(error_icono)))
                    
        except Exception as e:
            print(t["log_err_grave"].format(os.path.basename(ruta_cia), repr(e)))
            
        return icono, tipo_clave, title_id 

    def agregar_fila_tabla(self, ruta_normalizada, base_games_presentes=None):
        if ruta_normalizada in self.juegos_data: return 

        t = TEXTOS[self.idioma_actual]
        nombre_archivo = os.path.basename(ruta_normalizada)
        tamano_legible = self.obtener_tamano_formateado(ruta_normalizada)
        directorio = os.path.dirname(ruta_normalizada)
        
        icono_ctk, tipo_clave, title_id = self._extraer_metadatos(ruta_normalizada)
        texto_tipo = t.get(tipo_clave, t["tipo_otro"]) 
        
        prefijo = ""
        if tipo_clave in ["tipo_update", "tipo_dlc"]:
            id_base_correspondiente = "00040000" + title_id[8:]
            
            if base_games_presentes and id_base_correspondiente in base_games_presentes:
                prefijo = "   └─ "
            else:
                prefijo = " ─ " 
            
        max_chars_nombre = 35 
        limite_real = max_chars_nombre - len(prefijo)
        
        if len(nombre_archivo) > limite_real:
            nombre_mostrar = prefijo + nombre_archivo[:limite_real-3] + "..."
        else:
            nombre_mostrar = prefijo + nombre_archivo

        max_chars_ubicacion = 18 
        if len(directorio) > max_chars_ubicacion:
            ubicacion_mostrar = f"...{directorio[-max_chars_ubicacion+3:]}"
        else:
            ubicacion_mostrar = directorio if directorio else "\\"

        fila_frame = ctk.CTkFrame(self.scroll_cias, fg_color="transparent")
        fila_frame.pack(fill="x", pady=2)

        lbl_nombre = ctk.CTkLabel(fila_frame, text=f" {nombre_mostrar}", image=icono_ctk, compound="left", width=self.anchos_cols[0], anchor="w")
        lbl_nombre.grid(row=0, column=0, padx=5)
        if len(nombre_archivo) > limite_real: Tooltip(lbl_nombre, nombre_archivo)

        lbl_tipo = ctk.CTkLabel(fila_frame, text=texto_tipo, width=self.anchos_cols[1], anchor="w", text_color="#A9CCE3") 
        lbl_tipo.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(fila_frame, text=tamano_legible, width=self.anchos_cols[2], anchor="w").grid(row=0, column=2, padx=5)
        
        lbl_ubicacion = ctk.CTkLabel(fila_frame, text=ubicacion_mostrar, width=self.anchos_cols[3], anchor="w")
        lbl_ubicacion.grid(row=0, column=3, padx=5)
        if len(directorio) > max_chars_ubicacion: Tooltip(lbl_ubicacion, directorio)

        frame_estado = ctk.CTkFrame(fila_frame, fg_color="transparent", width=self.anchos_cols[4], height=25)
        frame_estado.grid(row=0, column=4, padx=(5, 25), sticky="w")
        frame_estado.pack_propagate(False)

        lbl_estado = ctk.CTkLabel(frame_estado, text=t["estado_espera"], text_color="#F1C40F", anchor="w")
        lbl_estado.pack(side="left", fill="both", expand=True)

        barra_progreso = ctk.CTkProgressBar(frame_estado, mode="determinate", height=10, width=140)
        barra_progreso.set(0.0)

        self.juegos_data[ruta_normalizada] = {
            "nombre": nombre_archivo,
            "tamano": tamano_legible,
            "frame": fila_frame,
            "lbl_estado": lbl_estado,
            "barra_progreso": barra_progreso,
            "icono": icono_ctk,
            "title_id": title_id
        }

    def _actualizar_tamano_total(self):
        total_bytes = 0
        for ruta in self.juegos_data.keys():
            try:
                total_bytes += os.path.getsize(ruta)
            except OSError:
                pass 
        
        t_base = TEXTOS[self.idioma_actual]["tamano_total"]
        if total_bytes == 0:
            texto = f"{t_base} 0.00 MB"
        elif total_bytes < 1024 * 1024 * 1024:
            texto = f"{t_base} {total_bytes / (1024*1024):.2f} MB"
        else:
            texto = f"{t_base} {total_bytes / (1024*1024*1024):.2f} GB"
            
        self.lbl_total_tamano.configure(text=texto)

    def anadir_cia(self):
        t = TEXTOS[self.idioma_actual]
        archivos = filedialog.askopenfilenames(title=t["dialogo_add_juegos"], filetypes=[("Archivos CIA", "*.cia")])
        if not archivos: 
            return
        self._mostrar_modal_y_procesar(archivos)

    def anadir_carpeta_cia(self):
        t = TEXTOS[self.idioma_actual]
        carpeta = filedialog.askdirectory(title=t["dialogo_add_carpeta"])
        if not carpeta:
            return
            
        archivos_cia = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.lower().endswith('.cia')]
        if not archivos_cia:
            return
        self._mostrar_modal_y_procesar(archivos_cia)

    def _obtener_title_id_rapido(self, ruta_cia):
        import re
        try:
            boot9_path = self.entry_boot9.get()
            crypto = None
            if boot9_path and os.path.exists(boot9_path):
                crypto = CryptoEngine(boot9=boot9_path)
                
            with CIAReader(ruta_cia, crypto=crypto) as cia:
                return cia.tmd.title_id.lower()
        except Exception as e:
            match = re.search(r"([0-9a-fA-F]{16})", repr(e))
            if match:
                return match.group(1).lower()
                
        return "zzzzzzzzzzzzzzzz" 

    def _mostrar_modal_y_procesar(self, lista_rutas):
        t = TEXTOS[self.idioma_actual]
        
        ventana_carga = ctk.CTkToplevel(self)
        aplicar_icono(ventana_carga)
        ventana_carga.title(t["modal_importando"])
        ventana_carga.geometry("300x120")
        ventana_carga.transient(self) 
        ventana_carga.grab_set() 
        
        x = self.winfo_x() + (self.winfo_width() // 2) - 150
        y = self.winfo_y() + (self.winfo_height() // 2) - 60
        ventana_carga.geometry(f"+{x}+{y}")

        lbl_carga = ctk.CTkLabel(ventana_carga, text=f"{t['modal_procesando']} {len(lista_rutas)} {t['modal_archivos_espera']}", font=ctk.CTkFont(size=14))
        lbl_carga.pack(expand=True, fill="both", pady=20)
        
        ventana_carga.update()

        def procesar_juegos():
            base_games_presentes = set()
            
            for datos in self.juegos_data.values():
                if "title_id" in datos and datos["title_id"].startswith("00040000"):
                    base_games_presentes.add(datos["title_id"])
            
            rutas_con_tid = []
            archivos_corruptos = []
            
            for ruta in lista_rutas:
                tid = self._obtener_title_id_rapido(ruta)
                if tid == "zzzzzzzzzzzzzzzz":
                    archivos_corruptos.append(os.path.basename(ruta))
                    continue
                    
                rutas_con_tid.append((ruta, tid))
                if tid.startswith("00040000"):
                    base_games_presentes.add(tid)
            
            rutas_con_tid.sort(key=lambda x: (x[1][8:], x[1][:8], os.path.basename(x[0])))

            for ruta, tid in rutas_con_tid:
                self.agregar_fila_tabla(os.path.normpath(ruta), base_games_presentes)
                
            self._actualizar_tamano_total()
            ventana_carga.grab_release()
            ventana_carga.destroy()

            if archivos_corruptos:
                lista_nombres = "\n".join(archivos_corruptos[:10])
                if len(archivos_corruptos) > 10:
                    lista_nombres += f"\n...Y {len(archivos_corruptos) - 10} MÁS"
                messagebox.showwarning(t["msg_archivos_corruptos_titulo"], t["msg_archivos_corruptos_texto"].format(lista_nombres))

        self.after(50, procesar_juegos)

    def limpiar_cias(self):
        for data in self.juegos_data.values():
            data["frame"].destroy()
        self.juegos_data.clear()
        self._actualizar_tamano_total()

    def ejecutar_instalacion(self):
        t = TEXTOS[self.idioma_actual]
        boot9 = self.entry_boot9.get()
        movable = self.entry_movable.get()
        seeddb = self.entry_seeddb.get()

        if not boot9 or not movable:
            messagebox.showerror(t["msg_error_critico_titulo"], t["msg_error_critico_texto"])
            return

        if not self.juegos_data:
            messagebox.showwarning(t["msg_lista_vacia_titulo"], t["msg_lista_vacia_texto"])
            return

        if not seeddb:
            respuesta = messagebox.askyesno(t["msg_falta_seeddb_titulo"], t["msg_falta_seeddb_texto"])
            if not respuesta:
                return

        self.btn_instalar.configure(state="disabled")
        self.abrir_ventana_log()
        
        hilo = threading.Thread(target=self._hilo_instalacion, args=(boot9, movable, seeddb), daemon=True)
        hilo.start()

    def _hilo_instalacion(self, boot9, movable, seeddb):
        sd = self.entry_sd.get()
        rutas_cias = list(self.juegos_data.keys())
        config_avanzada = None
        self.after(0, lambda: self.barra_general.set(0.0))
        motor = MotorInstalacion(
            ruta_sd=sd, 
            ruta_boot9=boot9, 
            ruta_movable=movable, 
            ruta_seeddb=seeddb, 
            lista_cias=rutas_cias, 
            config_avanzada=config_avanzada,  
            log_callback=print, 
            status_callback=self._actualizar_status_desde_backend,
            progress_callback=self._actualizar_progreso_cia,
            general_progress_callback=self._actualizar_progreso_general,
            idioma=self.idioma_actual
        )
        exito = motor.ejecutar()
        
        if exito:
            self.after(0, lambda: self.barra_general.set(1.0))
            self.mostrar_popup_finalizacion() 
        else:
            self.after(0, self._marcar_errores_residuales)
            
        self.after(0, lambda: self.btn_instalar.configure(state="normal"))

    def _marcar_errores_residuales(self):
        t = TEXTOS[self.idioma_actual]
        for ruta, datos in self.juegos_data.items():
            lbl = datos["lbl_estado"]
            texto_actual = lbl.cget("text")
            if texto_actual in [t["estado_espera"], t["estado_instalando"]]:
                self._actualizar_estado_fila(ruta, t["estado_error"], "#E74C3C", False)

    def _actualizar_status_desde_backend(self, ruta, status):
        from custominstall.core_installer import InstallStatus
        t = TEXTOS[self.idioma_actual]
        ruta_normalizada = os.path.normpath(ruta)
        
        if ruta_normalizada in self.juegos_data:
            if status == InstallStatus.Starting or status == InstallStatus.Writing:
                self.after(0, self._actualizar_estado_fila, ruta_normalizada, t["estado_instalando"], "#F39C12", True)
            elif status == InstallStatus.Finishing:
                self.after(0, self._actualizar_estado_fila, ruta_normalizada, t["estado_finalizando"], "#3498DB", False)
            elif status == InstallStatus.Done:
                self.after(0, self._actualizar_estado_fila, ruta_normalizada, t["estado_instalado"], "#2ECC71", False)
            elif status == InstallStatus.Failed:
                self.after(0, self._actualizar_estado_fila, ruta_normalizada, t["estado_error"], "#E74C3C", False)
            elif status == "OMITIDO":
                self.after(0, self._actualizar_estado_fila, ruta_normalizada, t.get("estado_omitido", "OMITIDO"), "#95A5A6", False)

    def _actualizar_estado_fila(self, ruta, texto, color, mostrar_barra):
        if ruta in self.juegos_data:
            datos = self.juegos_data[ruta]
            lbl = datos["lbl_estado"]
            barra = datos["barra_progreso"]
            
            if mostrar_barra:
                lbl.pack_forget()
                barra.configure(width=130)
                barra.place(x=0, rely=0.5, anchor="w")
            else:
                barra.place_forget()
                barra.pack_forget()
                
                lbl.configure(text=texto, text_color=color)
                lbl.pack(side="left", fill="both", expand=True)

    def _actualizar_progreso_cia(self, ruta, porcentaje):
        ruta_normalizada = os.path.normpath(ruta)
        if ruta_normalizada in self.juegos_data:
            barra = self.juegos_data[ruta_normalizada]["barra_progreso"]
            self.after(0, lambda: barra.set(porcentaje / 100.0))

    def _actualizar_progreso_general(self, porcentaje):
        self.after(0, lambda: self.barra_general.set(porcentaje / 100.0))
    
    def mostrar_popup_finalizacion(self):
        t = TEXTOS[self.idioma_actual]
        popup = ctk.CTkToplevel(self)
        aplicar_icono(popup)
        popup.title(t.get("popup_fin_titulo", "INSTALACIÓN COMPLETADA"))
        popup.geometry("500x260")
        popup.transient(self) 
        popup.grab_set()      
        popup.resizable(False, False)
        
        x = self.winfo_x() + (self.winfo_width() // 2) - 250
        y = self.winfo_y() + (self.winfo_height() // 2) - 130
        popup.geometry(f"+{x}+{y}")
        
        lbl_paso = ctk.CTkLabel(popup, text=t.get("popup_fin_paso", "PASO FINAL:"), font=ctk.CTkFont(weight="bold", size=18), text_color="#F39C12")
        lbl_paso.pack(pady=(25, 10))
        
        lbl_inst1 = ctk.CTkLabel(popup, text=t.get("popup_fin_inst1", "EJECUTA CUSTOM-INSTALL-FINALIZE A TRAVÉS DEL HOMEBREW LAUNCHER."), font=ctk.CTkFont(size=14, weight="bold"))
        lbl_inst1.pack(pady=2)
        
        lbl_inst2 = ctk.CTkLabel(popup, text=t.get("popup_fin_inst2", "ESTO INSTALARÁ LOS TICKETS Y LAS LLAVES (SEEDS) SI ES REQUERIDO."), font=ctk.CTkFont(size=14))
        lbl_inst2.pack(pady=2)
        
        lbl_inst3 = ctk.CTkLabel(popup, text=t.get("popup_fin_inst3", "CUSTOM-INSTALL-FINALIZE HA SIDO COPIADO A TU TARJETA SD."), font=ctk.CTkFont(size=12), text_color="#808B96")
        lbl_inst3.pack(pady=(15, 20))
        
        btn_ok = ctk.CTkButton(popup, text=t.get("btn_entendido", "ENTENDIDO"), width=150, height=35, command=popup.destroy)
        btn_ok.pack(pady=10)

    def mostrar_creditos(self):
        popup = ctk.CTkToplevel(self)
        aplicar_icono(popup)
        popup.title("Créditos")
        popup.geometry("480x200")
        popup.transient(self)
        popup.grab_set()
        popup.resizable(False, False)
        
        x = self.winfo_x() + (self.winfo_width() // 2) - 240
        y = self.winfo_y() + (self.winfo_height() // 2) - 100
        popup.geometry(f"+{x}+{y}")
        
        lbl_dev = ctk.CTkLabel(popup, text="Desarrollado por Cytek0x", font=ctk.CTkFont(weight="bold", size=18), text_color="#3498DB")
        lbl_dev.pack(pady=(25, 10))
        
        texto_creditos = "Utilizando herramientas y desarrollos previos de:\nihaveamac, wwylele, nek0bit, LyfeOnEdge, CrafterPika, archbox, BpyH64.\n\nIcono de Icons8."
        
        lbl_info = ctk.CTkLabel(popup, text=texto_creditos, font=ctk.CTkFont(size=12), justify="center")
        lbl_info.pack(pady=5, padx=20)

    def _cargar_base_datos_nombres(self):
        t = TEXTOS[self.idioma_actual]
        if hasattr(self, "base_datos_titulos") and self.base_datos_titulos:
            return 
            
        self.base_datos_titulos = {}
        ruta_db_local = "titledb_offline.json"
        
        import json
        import os
        import urllib.request
        import ssl

        if os.path.exists(ruta_db_local):
            try:
                with open(ruta_db_local, "r", encoding="utf-8") as f:
                    self.base_datos_titulos = json.load(f)
                return 
            except Exception as e:
                print(t["log_err_db_local"].format(e))

        print(t["log_db_no_encontrada"])
        urls_regiones = [
            "https://raw.githubusercontent.com/hax0kartik/3dsdb/master/jsons/list_US.json",
            "https://raw.githubusercontent.com/hax0kartik/3dsdb/master/jsons/list_GB.json", 
            "https://raw.githubusercontent.com/hax0kartik/3dsdb/master/jsons/list_JP.json"
        ]

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        for url in urls_regiones:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
                    datos = json.loads(response.read().decode('utf-8'))
                    for juego in datos:
                        tid = juego.get("TitleID", "").lower()
                        nombre = juego.get("Name", t.get("tipo_otro", "DESCONOCIDO"))
                        if tid:
                            self.base_datos_titulos[tid] = nombre
            except Exception as e:
                nombre_archivo = url.split('/')[-1]
                print(t["log_aviso_descarga"].format(nombre_archivo, e))

        if self.base_datos_titulos:
            try:
                with open(ruta_db_local, "w", encoding="utf-8") as f:
                    json.dump(self.base_datos_titulos, f, indent=4, ensure_ascii=False)
                print(t["log_db_guardada"].format(ruta_db_local))
            except Exception as e:
                print(t["log_err_guardar_db"].format(e))

    def _obtener_info_juego_instalado(self, tid_completo):
        t = TEXTOS[self.idioma_actual]
        tid_lower = tid_completo.lower()
        prefijo = tid_lower[:8]
        
        if prefijo == "00040000": 
            tipo_clave = "tipo_juego"
            color_hex = "#2980B9" 
        elif prefijo == "0004000e": 
            tipo_clave = "tipo_update"
            color_hex = "#27AE60" 
        elif prefijo == "0004008c": 
            tipo_clave = "tipo_dlc"
            color_hex = "#8E44AD" 
        elif prefijo in ["00048000", "0004800f", "00048004"]: 
            tipo_clave = "tipo_dsiware"
            color_hex = "#F39C12" 
        else: 
            tipo_clave = "tipo_otro"
            color_hex = "#7F8C8D" 
            
        texto_tipo = t.get(tipo_clave, t["tipo_otro"])
        
        nombre = self.base_datos_titulos.get(tid_lower)
        es_desconocido = False
        
        if not nombre:
            nombre = f"{t['msg_titulo_desconocido']} ({tid_completo.upper()})"
            es_desconocido = True
            
        return nombre, texto_tipo, color_hex, tipo_clave, es_desconocido

    def escanear_juegos_sd(self):
        t = TEXTOS[self.idioma_actual]
        for widget in self.scroll_instalados.winfo_children():
            widget.destroy()

        ruta_sd = self.entry_sd.get()
        if not ruta_sd or not os.path.exists(ruta_sd):
            ctk.CTkLabel(self.scroll_instalados, text=t["msg_sd_invalida"], text_color="#E74C3C").pack(pady=20)
            return

        ruta_nintendo = os.path.join(ruta_sd, "Nintendo 3DS")
        if not os.path.exists(ruta_nintendo):
            ctk.CTkLabel(self.scroll_instalados, text=t["msg_no_nintendo3ds"], text_color="#F1C40F").pack(pady=20)
            return

        lbl_cargando = ctk.CTkLabel(self.scroll_instalados, text=t["msg_cargando_db"], text_color="#3498DB")
        lbl_cargando.pack(pady=20)
        self.update()

        self._cargar_base_datos_nombres()
        
        juegos_brutos = []
        tipos_buscar = ["00040000", "0004000e", "0004008c"] 
        
        try:
            for id0 in os.listdir(ruta_nintendo):
                ruta_id0 = os.path.join(ruta_nintendo, id0)
                if len(id0) == 32 and os.path.isdir(ruta_id0):
                    for id1 in os.listdir(ruta_id0):
                        ruta_id1 = os.path.join(ruta_id0, id1)
                        if len(id1) == 32 and os.path.isdir(ruta_id1):
                            for tipo in tipos_buscar:
                                ruta_juegos = os.path.join(ruta_id1, "title", tipo)
                                if os.path.exists(ruta_juegos):
                                    for tid in os.listdir(ruta_juegos):
                                        if len(tid) == 8:
                                            juegos_brutos.append(f"{tipo}{tid.lower()}")
        except Exception as e:
            lbl_cargando.destroy()
            ctk.CTkLabel(self.scroll_instalados, text=t["msg_error_lectura"].format(e), text_color="#E74C3C").pack(pady=20)
            return

        lbl_cargando.destroy()

        if not juegos_brutos:
            ctk.CTkLabel(self.scroll_instalados, text=t["msg_no_juegos"], text_color="gray").pack(pady=20)
            return

        juegos_procesados = []
        for tid in juegos_brutos:
            nombre, tipo_txt, color_hex, tipo_clave, es_desconocido = self._obtener_info_juego_instalado(tid)
            if es_desconocido:
                continue
                
            juegos_procesados.append({
                "tid": tid, "nombre": nombre, "tipo_txt": tipo_txt, 
                "color_hex": color_hex, "tipo_clave": tipo_clave
            })
            
        juegos_procesados.sort(key=lambda x: (x["tid"][8:], x["tid"][:8]))

        familias_agrupadas = {}
        for juego in juegos_procesados:
            familia = juego["tid"][8:]
            if familia not in familias_agrupadas:
                familias_agrupadas[familia] = []
            familias_agrupadas[familia].append(juego)

        for familia, items in familias_agrupadas.items():
            frame_item = ctk.CTkFrame(self.scroll_instalados, fg_color="#2C3E50")
            frame_item.pack(fill="x", pady=2)
            
            tiene_base = any(j["tipo_clave"] == "tipo_juego" for j in items)
            
            for juego in items:
                tid = juego["tid"]
                
                prefijo_visual = ""
                espacio_secundario = "   "
                
                if juego["tipo_clave"] in ["tipo_update", "tipo_dlc"]:
                    if tiene_base:
                        prefijo_visual = "   └─ "
                        espacio_secundario = "      "
                    else:
                        prefijo_visual = " ─ "
                        espacio_secundario = "   "
                
                nombre_real = juego["nombre"]
                max_chars = 30 - len(prefijo_visual) 
                
                if len(nombre_real) > max_chars:
                    nombre_truncado = nombre_real[:max_chars-3] + "..."
                else:
                    nombre_truncado = nombre_real
                    
                nombre_mostrar = prefijo_visual + nombre_truncado
                
                lbl_info = ctk.CTkLabel(
                    frame_item, 
                    text=f"{nombre_mostrar}\n{espacio_secundario}{juego['tipo_txt']} | ID: {tid.upper()}", 
                    anchor="w",
                    justify="left",
                    font=ctk.CTkFont(size=12)
                )
                lbl_info.pack(anchor="w", padx=15, pady=(8, 2), fill="x")
                
                if len(nombre_real) > max_chars:
                    Tooltip(lbl_info, nombre_real)
                
                linea_color = ctk.CTkFrame(frame_item, height=3, fg_color=juego["color_hex"], corner_radius=0)
                linea_color.pack(fill="x", padx=10, pady=(0, 6))

if __name__ == "__main__":
    app = CustomInstallModern()
    app.mainloop()