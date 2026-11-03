"""Misión 5 · Automatízalo. Pruébalo con:  bash comprobar.sh python"""
import os
import subprocess


def ejecutar(comando, env=None):
    """Ejecuta un comando de terminal y devuelve (salida, codigo_de_salida)."""
    print(f"ejecuto: {comando}")
    resultado = subprocess.run(
        ["bash", "-c", comando], capture_output=True, text=True,   # siempre bash, también en Windows
        env=env if env is not None else os.environ.copy(),
    )
    salida = (resultado.stdout + resultado.stderr).strip()
    if salida:
        print("   " + salida.replace("\n", "\n   ")[:400])
    return salida, resultado.returncode


def resolver():
    fragmentos = []

    # Fragmento 1: find + cat (carpeta oculta en proyecto/datos)
    salida, codigo = ejecutar("find proyecto/datos -name fragmento1.txt")
    if codigo == 0 and salida:
        ruta = salida.splitlines()[0]
        contenido, codigo = ejecutar(f"cat '{ruta}'")
        if codigo == 0:
            fragmentos.append(contenido.split("FRAGMENTO 1:")[-1].strip().split()[0])

    # Fragmento 2: grep en proyecto/logs/app.log
    salida, codigo = ejecutar("grep -o 'fragmento2=[A-Z0-9]*' proyecto/logs/app.log")
    if codigo == 0 and salida:
        fragmentos.append(salida.split("=")[1])

    # Fragmento 3: mkdir + mv en proyecto/descargas, luego ejecutar('bash ../comprobar.sh orden')
    salida, codigo = ejecutar("bash ../comprobar.sh orden")
    if codigo == 0 and "FRAGMENTO 3:" in salida:
        fragmentos.append(salida.split("FRAGMENTO 3:")[-1].strip().split()[0])

    # Fragmento 4: chmod +x y ejecutar('cd proyecto && ./herramientas/revelar.sh', env={**os.environ, "AGENTE": "robot"})
    salida, codigo = ejecutar("chmod +x proyecto/herramientas/revelar.sh")
    if codigo == 0:
        salida, codigo = ejecutar(
            "cd proyecto && ./herramientas/revelar.sh",
            env={**os.environ, "AGENTE": "robot"}
        )
        if codigo == 0 and "FRAGMENTO 4:" in salida:
            fragmentos.append(salida.split("FRAGMENTO 4:")[-1].strip().split()[0])

    clave = "-".join(fragmentos)
    print(f"\nCLAVE: {clave}")
    return clave


if __name__ == "__main__":
    if not os.path.isdir("proyecto"):
        print("Ejecútame desde la carpeta mision/ :  cd mision && python3 ../entrega/resolver.py   (o python)")
        raise SystemExit(1)
    resolver()
