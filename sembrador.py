#Este codigo detectara las memorias usb conectadas al sistema y creara una llave "key.dlt"
#El fin de este codigo es crear un cold storage de la llave que creara las maquinas enimga

import os
import hashlib
import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def get_usbs():
    usbs = []
    # Filtramos solo los discos extraíbles
    for p in psutil.disk_partitions():
        if 'removable' in p.opts:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                gb_size = usage.total / (1024**3)
                usbs.append({
                    "ruta": p.mountpoint, 
                    "size": f"{gb_size:.2f} GB"
                })
            except Exception:
                pass # Ignoramos si la unidad está vacía o no se deja leer
    return usbs

def main():
    console.print(Panel("[bold cyan]DELTA PROJECT: ENIGMA 256[/bold cyan]\n[white]Fase 1: Sembrador[/white]", expand=False))
    
    usbs = get_usbs()
    
    if not usbs:
        console.print("[bold red]❌ Error: Conecta una USB primero.[/bold red]")
        return

    # Render de la tabla
    tabla = Table(title="Dispositivos detectados")
    tabla.add_column("ID", style="cyan", justify="center")
    tabla.add_column("Ruta", style="magenta")
    tabla.add_column("Tamaño", style="green")

    for i, usb in enumerate(usbs):
        tabla.add_row(str(i), usb['ruta'], usb['size'])

    console.print(tabla)

    # Input del usuario
    try:
        opcion = int(Prompt.ask("Selecciona el [bold cyan]ID[/bold cyan] destino", choices=[str(i) for i in range(len(usbs))]))
    except ValueError:
        return

    destino = usbs[opcion]['ruta']
    
    with console.status("[bold yellow]Generando entropía térmica..."):
        # 2KB de ruido al azar
        ruido = os.urandom(2048)
        key = hashlib.sha256(ruido).digest()
        
        key_path = os.path.join(destino, "key.dlt")
        
        try:
            with open(key_path, "wb") as f:
                f.write(key)
            console.print(f"\n[bold green]✔ LISTO:[/bold green] Llave guardada en [white]{key_path}[/white]")
            console.print("[dim]Ojo: Sin este archivo no hay vuelta atrás para los entornos cifrados.[/dim]")
        except Exception as e:
            console.print(f"\n[bold red]❌ Error al intentar escribir en la USB:[/bold red] {e}")

if __name__ == "__main__":
    main()
