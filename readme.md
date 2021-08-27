# Extractor de Movimientos Banchile Inversiones

> Ultima vez actualizado: 07/08/2022

La interfaz de Banchile inversiones es desagradable y lenta.
Para obtener que movimientos se realizaron hay que ir buscando
de mes en mes, que resulta tedioso. Y tampoco se hay una opción para
descargar todos los movimientos.

Este scrip obtiene los movimientos utilizando su API interna,
realizando un dump de los movimientos en archivos JSON, CSV y Excel.
Require que se cree un archivo `.env` a partir de las cookies y
parámetros que se realizan al servidor, que se pueden obtener en la
pestaña de Network en las herramientas de desarrolladores.


1. Instalar python y instalar sus dependencias
   ```ps
   python3 -m venv .venv
   # En windows:
   . .venv\Scripts\activate
   # En unix (Mac, Linux)
   . .venv/bin/activate
   # Instalar dependencias
   pip install -r requirements.txt
   ```
2. Ir a [página de movimientos][p-movimientos]
3. Abrir DevTools (inspeccionar elemento o Ctrl + Shift + i)
4. Ir a la pestaña de Red
5. Seleccionar un mes en la página
6. Inspeccionar la request, ver Cabeceras para obtener `p_auth`
   y Cookies para obtener `JSESSIONID`
7. Crear el archivo `.venv` de la forma
   ```env
   JSESSIONID={JSESSIONID}
   AUTH={p_auth}
   ```
8. Correr el script con `python movements.py`


[p-movimientos]: https://ww2.banchileinversiones.cl/web/personas/movimientos
