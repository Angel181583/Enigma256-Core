import os
import psutil

class Enigma256:

    
    def __init__(self, ruta_llave=None):
        self.rotores = []
        self.posiciones = [0] * 8
        
        # Intentamos obtener la llave ya sea manual o buscando en dispositivos
        if ruta_llave:
            self.llave = self._cargar_llave_desde_ruta(ruta_llave)
        else:
            self.llave = self._buscar_llave_en_dispositivos()
        
        self._configurar_rotores()

    def _buscar_llave_en_dispositivos(self):
        
        #Escanea las unidades de almacenamiento conectadas buscando el archivo 'key.dlt'.
        
        rutas_comunes = ['/media', '/run/media']
        
        for particion in psutil.disk_partitions(all=False):
            # Determinamos si es una unidad extraíble
            es_usb_windows = 'removable' in particion.opts
            es_usb_linux = any(ruta in particion.mountpoint for ruta in rutas_comunes)
            
            if es_usb_windows or es_usb_linux:
                # Omitimos sistemas de archivos virtuales o de sistema
                if 'snap' in particion.mountpoint or 'loop' in particion.device:
                    continue
                
                archivo_objetivo = os.path.join(particion.mountpoint, "key.dlt")
                
                if os.path.exists(archivo_objetivo):
                    print(f"[*] ¡Llave encontrada en: {particion.mountpoint}!")
                    with open(archivo_objetivo, "rb") as f:
                        return list(f.read())
        
        raise FileNotFoundError("No logré encontrar ningún archivo 'key.dlt' en los dispositivos conectados.")

    def _cargar_llave_desde_ruta(self, ruta):
        """Carga la llave desde una ubicación específica proporcionada por el usuario."""
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"Parece que la ruta '{ruta}' no existe. Por favor, verifica el archivo.")
        
        with open(ruta, "rb") as f:
            return list(f.read())

    def _configurar_rotores(self):
    
        # Inicializa y baraja los 8 rotores usando un algoritmo Fisher-Yates 
        # basado en los fragmentos de la llave cargada.
    
        for n in range(8):
            rotor = list(range(256))
            # Tomamos un segmento de la llave para generar la semilla
            segmento_llave = self.llave[n * 4 : (n + 1) * 4]
            suma_semilla = sum(segmento_llave)
            
            # Aplicamos barajado determinista
            for i in range(255, 0, -1):
                j = (suma_semilla + i) % (i + 1)
                rotor[i], rotor[j] = rotor[j], rotor[i]
            
            self.rotores.append(rotor)

# --- Bloque principal de ejecución ---
if __name__ == "__main__":
    print("--- Sistema de Cifrado ---")
    print("Iniciando escaneo...")
    
    try:
        maquina = Enigma256()
        print("Llave detectada y rotores configurados.\n")
        
        print("Estado inicial de los rotores (primeros 10 bytes):")
        print("-" * 50)
        for indice, rotor in enumerate(maquina.rotores):
            print(f"Rotor {indice + 1}: {rotor[:10]}")
        print("-" * 50)
            
    except FileNotFoundError as error:
        print(f"\n[Atención]: {error}")
    except Exception as e:
        print(f"\n[Error inesperado]: {e}")
