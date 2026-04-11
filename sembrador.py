#Este codigo detectara las memorias usb conectadas al sistema y creara una llave "key.dlt"
#El fin de este codigo es crear un cold storage de la llave que creara las maquinas enimga

# Librerias necesarias
import os
import hashlib
import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def listar_unidades_windows():
    unidades = []
    # psutil detecta las particiones y buscamos las 'removable' para encontrar nuestra usb objetivo
    for particion in psutil.disk_partitions():
        if 'removable' in particion.opts:
            try:
                uso = psutil.disk_usage(particion.mountpoint)
                unidades.append({
                    "letra": particion.mountpoint,
                    "total": f"{uso.total / (1024**3):.2f} GB"
                })
            except:
                continue
    return unidades

def ejecutar_sembrador():
    console.print(Panel("[bold cyan]DELTA PROJECT: ENIGMA 256[/bold cyan]\n[white]Fase 1: Sembrador[/white]", expand=False))
    
    usbs = listar_unidades_windows()
    
    if not usbs:
        console.print("[bold red]❌ ERROR: No se detectó ninguna USB conectada.[/bold red]")
        return

    # Crear tabla de seleccion ayuda visual
    tabla = Table(title="Dispositivos Extraíbles")
    tabla.add_column("ID", style="cyan", justify="center")
    tabla.add_column("Unidad", style="magenta")
    tabla.add_column("Capacidad", style="green")

    for idx, usb in enumerate(usbs):
        tabla.add_row(str(idx), usb['letra'], usb['total'])

    console.print(tabla)

    # Selección de usuario
    seleccion = Prompt.ask("Selecciona el [bold cyan]ID[/bold cyan] de la USB para la llave", choices=[str(i) for i in range(len(usbs))])
    ruta_destino = usbs[int(seleccion)]['letra']
    
    with console.status("[bold yellow]Cosechando ruido térmico del sistema..."):
        # Generar 2048 bytes de entropia deacuerdo con el sistema
        ruido = os.urandom(2048)
        # Refinar a llave maestra SHA-256 para crear el archivo hash
        llave_maestra = hashlib.sha256(ruido).digest()
        # Ruta final del archivo
        archivo_llave = os.path.join(ruta_destino, "key.dlt")
        
        with open(archivo_llave, "wb") as f:
            f.write(llave_maestra)

    console.print(f"\n[bold green]✔ PROCESO EXITOSO:[/bold green] Llave plantada en [white]{archivo_llave}[/white]")
    console.print("[dim]Recuerde: Si pierde este archivo, los mundos cifrados serán inaccesibles.[/dim]")

if __name__ == "__main__":
    ejecutar_sembrador()
