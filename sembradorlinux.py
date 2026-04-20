# Librerias necesarias
import os
import hashlib
import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def listar_unidades_linux():
    unidades = []
    # En Linux, las particiones extraíbles de usuario suelen montarse aquí
    rutas_comunes = ['/media', '/run/media']
    
    for particion in psutil.disk_partitions(all=False):
        # Filtramos solo los puntos de montaje de las USB
        if any(ruta in particion.mountpoint for ruta in rutas_comunes):
            # Evitamos particiones del sistema como snaps o flatpaks
            if 'snap' in particion.mountpoint or 'loop' in particion.device:
                continue
            try:
                uso = psutil.disk_usage(particion.mountpoint)
                unidades.append({
                    "ruta": particion.mountpoint,
                    "total": f"{uso.total / (1024**3):.2f} GB"
                })
            except Exception as e:
                continue
    return unidades

def ejecutar_sembrador():
    console.print(Panel("[bold cyan]DELTA PROJECT: ENIGMA 256[/bold cyan]\n[white]Fase 1: Sembrador de Entropía (Linux Edition)[/white]", expand=False))
    
    usbs = listar_unidades_linux()
    
    if not usbs:
        console.print("[bold red]❌ ERROR: No se detectó ninguna USB conectada en /media o /run/media.[/bold red]")
        console.print("[dim]Asegúrate de que la USB esté montada (abierta en el explorador de archivos).[/dim]")
        return

    # Crear tabla de seleccion ayuda visual
    tabla = Table(title="Dispositivos Extraíbles")
    tabla.add_column("ID", style="cyan", justify="center")
    tabla.add_column("Punto de Montaje", style="magenta")
    tabla.add_column("Capacidad", style="green")

    for idx, usb in enumerate(usbs):
        tabla.add_row(str(idx), usb['ruta'], usb['total'])

    console.print(tabla)

    # Selección de usuario
    seleccion = Prompt.ask("Selecciona el [bold cyan]ID[/bold cyan] de la USB para la llave", choices=[str(i) for i in range(len(usbs))])
    ruta_destino = usbs[int(seleccion)]['ruta']
    
    with console.status("[bold yellow]Cosechando ruido térmico del kernel..."):
        # Generar 2048 bytes de entropia y refinar a llave maestra SHA-256
        ruido = os.urandom(2048)
        llave_maestra = hashlib.sha256(ruido).digest()
        
        # Ruta final del archivo
        archivo_llave = os.path.join(ruta_destino, "key.dlt")
        
        with open(archivo_llave, "wb") as f:
            f.write(llave_maestra)

    console.print(f"\n[bold green]✔ PROCESO EXITOSO:[/bold green] Llave plantada en [white]{archivo_llave}[/white]")
    console.print("[dim]Recuerde: Si pierde este archivo, los mundos cifrados serán inaccesibles.[/dim]")

if __name__ == "__main__":
    ejecutar_sembrador()