import os
import sys
import hashlib
from custominstall.core_installer import CustomInstall
import traceback
from pyctr.crypto.seeddb import MissingSeedError

TEXTOS_MOTOR = {
    "es": {
        "inicio_motor": "=== INICIANDO MOTOR DE INSTALACIÓN ===\n",
        "prep_ok": "FASE DE PREPARACIÓN COMPLETADA CON ÉXITO. CONFIGURANDO MOTOR DE CIFRADO...\n",
        "err_cifrado": "[ERROR] FALLO AL INICIAR EL MOTOR DE CIFRADO: {error}\n",
        "analizando": "ANALIZANDO Y LEYENDO ARCHIVOS CIA SELECCIONADOS...\n",
        "err_espacio": "[ERROR] NO HAY SUFICIENTE ESPACIO LIBRE EN LA TARJETA SD.\n",
        "iniciando_inyeccion": "INICIANDO DESCIFRADO, RE-CIFRADO POR HARDWARE E INYECCIÓN EN LA DB...\n",
        "err_fuse": "[ERROR] EL PROCESO DE INYECCIÓN FALLÓ DEBIDO A UN PROBLEMA CON SAVE3DS_FUSE.\n",
        "err_excepcion": "[ERROR] EXCEPCIÓN CRÍTICA DURANTE LA INYECCIÓN DE BLOQUES: {error}\n",
        "calc_id0": "CALCULANDO ID0 ÚNICO DE LA CONSOLA...\n",
        "ok_id0": "[ÉXITO] ID0 CALCULADO: {id0}\n",
        "err_movable": "[ERROR CRÍTICO] NO SE PUDO LEER EL MOVABLE.SED: {error}\n",
        "validando_dir": "VALIDANDO ESTRUCTURA DE DIRECTORIOS EN LA TARJETA SD...\n",
        "err_no_id0": "[ERROR] NO SE ENCONTRÓ LA CARPETA DEL ID0 EN LA SD: {ruta}\n",
        "err_no_id1": "[ERROR] NO SE ENCONTRÓ LA SUBCARPETA ID1 EN LA SD.\n",
        "ok_dir": "[ÉXITO] DIRECTORIOS VALIDADOS. RUTA DE INYECCIÓN: {ruta}\n",
        "err_io": "[ERROR CRÍTICO] PÉRDIDA DE CONEXIÓN CON LA SD. ¿SE EXTRAJO LA TARJETA? ({error})\n",
        "debug_buscando": "[DEBUG] Buscando binario en: {ruta}\n",
        "err_bin_no_encontrado": "[ERROR] Binario no encontrado. Asegúrate de que la carpeta 'custominstall' esté junto al .exe\n",
        "err_critico": "[ERROR CRÍTICO] Detalle técnico: {error}\n",
        "err_missing_seed": "[ADVERTENCIA] Omitiendo '{archivo}' - Faltan las llaves (Seed) para {title_id}\n",
        "err_cia_corrupto": "[ADVERTENCIA] Omitiendo '{archivo}' - Archivo dañado o ilegible ({error})\n",
        "err_sin_juegos": "[ERROR] Ninguno de los juegos seleccionados puede ser instalado. Asegúrate de tener un seeddb.bin actualizado.\n",
    },
    "en": {
        "inicio_motor": "=== STARTING INSTALLATION ENGINE ===\n",
        "prep_ok": "PREPARATION PHASE COMPLETED SUCCESSFULLY. CONFIGURING CRYPTO ENGINE...\n",
        "err_cifrado": "[ERROR] FAILED TO START CRYPTO ENGINE: {error}\n",
        "analizando": "ANALYZING AND READING SELECTED CIA FILES...\n",
        "err_espacio": "[ERROR] NOT ENOUGH FREE SPACE ON THE SD CARD.\n",
        "iniciando_inyeccion": "STARTING DECRYPTION, HARDWARE RE-ENCRYPTION, AND DB INJECTION...\n",
        "err_fuse": "[ERROR] THE INJECTION PROCESS FAILED DUE TO AN ISSUE WITH SAVE3DS_FUSE.\n",
        "err_excepcion": "[ERROR] CRITICAL EXCEPTION DURING BLOCK INJECTION: {error}\n",
        "calc_id0": "CALCULATING UNIQUE CONSOLE ID0...\n",
        "ok_id0": "[SUCCESS] ID0 CALCULATED: {id0}\n",
        "err_movable": "[CRITICAL ERROR] COULD NOT READ MOVABLE.SED: {error}\n",
        "validando_dir": "VALIDATING DIRECTORY STRUCTURE ON THE SD CARD...\n",
        "err_no_id0": "[ERROR] ID0 FOLDER NOT FOUND ON SD: {ruta}\n",
        "err_no_id1": "[ERROR] ID1 SUBFOLDER NOT FOUND ON SD.\n",
        "ok_dir": "[SUCCESS] DIRECTORIES VALIDATED. INJECTION PATH: {ruta}\n",
        "err_io": "[CRITICAL ERROR] CONNECTION LOST WITH SD. WAS THE CARD REMOVED? ({error})\n",
        "debug_buscando": "[DEBUG] Searching for binary at: {ruta}\n",
        "err_bin_no_encontrado": "[ERROR] Binary not found. Make sure the 'custominstall' folder is next to the .exe\n",
        "err_critico": "[CRITICAL ERROR] Technical detail: {error}\n",
        "err_missing_seed": "[WARNING] Skipping '{archivo}' - Missing keys (Seed) for {title_id}\n",
        "err_cia_corrupto": "[WARNING] Skipping '{archivo}' - Corrupted or unreadable file ({error})\n",
        "err_sin_juegos": "[ERROR] None of the selected games can be installed. Make sure you have an updated seeddb.bin.\n",
    }
}

class MotorInstalacion:
    def __init__(self, ruta_sd, ruta_boot9, ruta_movable, ruta_seeddb, lista_cias, 
                 log_callback=print, status_callback=None, progress_callback=None, general_progress_callback=None,
                 idioma="es",config_avanzada=None,):
        self.ruta_sd = ruta_sd
        self.ruta_boot9 = ruta_boot9
        self.ruta_movable = ruta_movable
        self.ruta_seeddb = ruta_seeddb
        self.lista_cias = lista_cias
        self.config_avanzada = config_avanzada or {}
        self.log = log_callback 
        self.status_callback = status_callback 
        self.progress_callback = progress_callback
        self.general_progress_callback = general_progress_callback
        self.id0 = None
        self.ruta_cia_actual = None
        self.total_cias = len(lista_cias)
        self.t = TEXTOS_MOTOR.get(idioma, TEXTOS_MOTOR["es"])

    def ejecutar(self):
        self.log(self.t["inicio_motor"])
        
        if not self._derivar_id0(): return False
        if not self._validar_directorios(): return False

        self.log(self.t["prep_ok"])
        
        try:
            installer = CustomInstall(
                boot9=self.ruta_boot9,
                seeddb=self.ruta_seeddb,
                movable=self.ruta_movable,
                sd=self.ruta_sd
            )
        except Exception as e:
            self.log(self.t["err_cifrado"].format(error=str(e)))
            return False

        installer.event.on_log_msg += lambda msg, end='\n': self.log(msg.strip() + "\n")
        if self.status_callback:
            installer.event.update_status += lambda path, status: self.status_callback(path, status)

        def al_iniciar_cia(idx):
            if idx < len(self.lista_cias):
                self.ruta_cia_actual = self.lista_cias[idx]
            if self.general_progress_callback:
                porcentaje_gen = (idx / self.total_cias) * 100
                self.general_progress_callback(porcentaje_gen)
                
        installer.event.on_cia_start += al_iniciar_cia

        def al_actualizar_porcentaje(porcentaje_total, leido_mb, total_mb):
            if self.progress_callback and self.ruta_cia_actual:
                self.progress_callback(self.ruta_cia_actual, porcentaje_total)
                
        installer.event.update_percentage += al_actualizar_porcentaje

        self.log(self.t["analizando"])
        
        cias_validos = []
        for ruta_cia in self.lista_cias:
            try:
                from pyctr.type.cia import CIAReader
                lector_prueba = CIAReader(ruta_cia)
                lector_prueba.close() 
                cias_validos.append(ruta_cia)
                
            except MissingSeedError as e:
                title_id_str = str(e)
                nombre_archivo = os.path.basename(ruta_cia)
                self.log(self.t["err_missing_seed"].format(archivo=nombre_archivo, title_id=title_id_str), 1)
                
                if self.status_callback:
                    self.status_callback(ruta_cia, "OMITIDO")
                
            except Exception as e:
                nombre_archivo = os.path.basename(ruta_cia)
                tipo_error = type(e).__name__
                self.log(self.t["err_cia_corrupto"].format(archivo=nombre_archivo, error=tipo_error), 1)
                
                if self.status_callback:
                    self.status_callback(ruta_cia, "OMITIDO")

        if not cias_validos:
            self.log(self.t["err_sin_juegos"])
            return False

        self.lista_cias = cias_validos
        self.total_cias = len(self.lista_cias)
        
        installer.prepare_titles(self.lista_cias)

        total_size, free_space = installer.check_size()
        if total_size > free_space:
            self.log(self.t["err_espacio"])
            return False

        self.log(self.t["iniciando_inyeccion"])
        
        try:
            if getattr(sys, 'frozen', False):
                ruta_base = os.path.dirname(sys.executable)
            else:
                ruta_base = os.path.dirname(os.path.abspath(__file__))

            ruta_bin = os.path.join(ruta_base, "custominstall", "bin", "win32", "save3ds_fuse.exe")
            
            entorno = os.environ.copy()
            entorno["PATH"] = os.path.dirname(ruta_bin) + os.pathsep + entorno.get("PATH", "")
            
            self.log(self.t.get("debug_buscando", "[DEBUG] Buscando binario en: {ruta}\n").format(ruta=ruta_bin))
            
            if not os.path.exists(ruta_bin):
                self.log(self.t.get("err_bin_no_encontrado", "[ERROR] Binario no encontrado.\n"))
                return False

            result, _, _ = installer.start()
            
            if result is None:
                self.log(self.t["err_fuse"])
                return False

        except Exception as e:
            mapa_error = traceback.format_exc()
            self.log(f"[ERROR CRÍTICO] Traza del fallo interno:\n{mapa_error}\n")
            self.log(self.t["err_critico"].format(error=repr(e)))
            return False
        return True
    
    def _derivar_id0(self):
        self.log(self.t["calc_id0"])
        try:
            with open(self.ruta_movable, "rb") as f:
                f.seek(0x110)
                key_y = f.read(0x10)
                
            hash_sha256 = hashlib.sha256(key_y).digest()
            primeros_16_bytes = hash_sha256[:16]
            id0_bytes = b"".join(primeros_16_bytes[i:i+4][::-1] for i in range(0, 16, 4))
            
            self.id0 = id0_bytes.hex()
            self.log(self.t["ok_id0"].format(id0=self.id0))
            return True
            
        except Exception as e:
            self.log(self.t["err_movable"].format(error=str(e)))
            return False

    def _validar_directorios(self):
        self.log(self.t["validando_dir"])
        ruta_base_3ds = os.path.join(self.ruta_sd, "Nintendo 3DS", self.id0)
        
        if not os.path.exists(ruta_base_3ds):
            self.log(self.t["err_no_id0"].format(ruta=ruta_base_3ds))
            return False

        carpetas_id1 = [d for d in os.listdir(ruta_base_3ds) if len(d) == 32 and os.path.isdir(os.path.join(ruta_base_3ds, d))]
        
        if not carpetas_id1:
            self.log(self.t["err_no_id1"])
            return False
            
        self.id1 = carpetas_id1[0]
        self.ruta_title = os.path.join(ruta_base_3ds, self.id1, "title")
        os.makedirs(self.ruta_title, exist_ok=True)
        
        self.log(self.t["ok_dir"].format(ruta=self.ruta_title))
        return True