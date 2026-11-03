"""Misión 5 · Automatízalo."""

import os
import shlex
import subprocess


def ejecutar(comando, env=None):
    """Ejecuta un comando y devuelve su salida y código de retorno."""
    print(f"ejecuto: {comando}")
    resultado = subprocess.run(
        ["bash", "-c", comando],
        capture_output=True,
        text=True,
        env=env if env is not None else os.environ.copy(),
    )
    salida = (resultado.stdout + resultado.stderr).strip()
    if salida:
        print("   " + salida.replace("\n", "\n   ")[:400])
    return salida, resultado.returncode


def encontrar(nombre, tipo):
    """Busca un archivo o carpeta por su nombre."""
    comando = f"find . -type {tipo} -name {shlex.quote(nombre)} -print -quit"
    salida, codigo = ejecutar(comando)
    if codigo == 0 and salida:
        return salida.splitlines()[0]
    return None


def resolver():
    fragmentos = []

    # Fragmento 1: encontrar el archivo y leer su contenido.
    ruta = encontrar("fragmento1.txt", "f")
    if ruta:
        contenido, codigo = ejecutar(f"cat {shlex.quote(ruta)}")
        if codigo == 0 and "FRAGMENTO 1:" in contenido:
            fragmentos.append(
                contenido.split("FRAGMENTO 1:")[-1].strip().split()[0]
            )

    # Fragmento 2: encontrar el log y extraer el valor con grep.
    ruta = encontrar("app.log", "f")
    if ruta:
        salida, codigo = ejecutar(
            f"grep -o 'fragmento2=[A-Z0-9]*' {shlex.quote(ruta)}"
        )
        if codigo == 0 and "=" in salida:
            fragmentos.append(salida.split("=")[-1])

    # Fragmento 3: encontrar descargas, crear carpetas y mover archivos.
    descargas = encontrar("descargas", "d")
    if descargas:
        d = shlex.quote(descargas)
        comando = f"""
        mkdir -p {d}/imagenes {d}/documentos {d}/datos
        find {d} -maxdepth 1 -type f -print0 |
        while IFS= read -r -d '' archivo; do
            case "$archivo" in
                *.jpg|*.png) mv "$archivo" {d}/imagenes/ ;;
                *.pdf|*.txt) mv "$archivo" {d}/documentos/ ;;
                *.csv|*.json) mv "$archivo" {d}/datos/ ;;
            esac
        done
        """
        _, codigo = ejecutar(comando)

        if codigo == 0:
            salida, codigo = ejecutar("bash ../comprobar.sh orden")
            if codigo == 0 and "FRAGMENTO 3:" in salida:
                fragmentos.append(
                    salida.split("FRAGMENTO 3:")[-1].strip().split()[0]
                )

    # Fragmento 4: encontrar el script, darle permiso y ejecutarlo
    # con la variable de entorno AGENTE.
    ruta = encontrar("revelar.sh", "f")
    if ruta:
        ruta_segura = shlex.quote(ruta)
        _, codigo = ejecutar(f"chmod +x {ruta_segura}")

        if codigo != 0:
            print("No se pudo cambiar el permiso del script.")
        else:
            salida, codigo = ejecutar(
                ruta_segura,
                env={**os.environ, "AGENTE": "robot"}
            )
            if codigo == 0 and "FRAGMENTO 4:" in salida:
                fragmentos.append(
                    salida.split("FRAGMENTO 4:")[-1].strip().split()[0]
                )

    clave = "-".join(fragmentos)
    print(f"\nCLAVE: {clave}")
    return clave


if __name__ == "__main__":
    if not os.path.isdir("proyecto"):
        print("Ejecuta el script desde la carpeta mision/.")
        raise SystemExit(1)

    resolver()
