from __future__ import annotations

import os
import sys
import itertools

import arrow
import requests
import dotenv
import pandas as pd

dotenv.load_dotenv()


URL = "https://ww2.banchileinversiones.cl/api/jsonws/invoke"
COOKIES = {"JSESSIONID": os.getenv("JSESSIONID")}
PARAMS = {"p_auth": os.getenv("AUTH")}

HEADERS = {
    "Referer": "https://ww2.banchileinversiones.cl/web/personas/movimientos",
    "Origin": "https://ww2.banchileinversiones.cl",
    "User-Agent": "Mozilla/5.0",
    'Content-Type': 'application/json',
    'Accept-Encoding': 'deflate',
}


def movement_query(month: int, year: int):
    start = arrow.Arrow(year=year, month=month, day=1)
    # ultimo día del mes
    end = start.shift(months=1).shift(days=-1)
    return {
        "/cl.banchile.general.movimientos.java.liferay.srv.portlet.movimientos/consultar-movimiento": {
            "reqJSON": {
                "reqMovimiento": {
                    "fechaInicio": start.strftime("'%d/%m/%Y'"),
                    "fechaFin": end.strftime("'%d/%m/%Y'"),
                    "nombrePortlet": "'GeneralMovimientos'",
                    "tipo": "persona"
                }
            }
        }
    }


def save(data: list[dict]):
    df = pd.DataFrame.from_dict(sorted(data, key=lambda e: e["fechaOperacion"]))
    df.to_json(os.path.join("output", "data.json"))
    df.to_csv(os.path.join("output", "data.csv"))
    df.to_excel(os.path.join("output", "data.xlsx"))


def main(strart_month: int, start_year: int, end_month: int, end_year: int):
    data = []
    session = requests.session()
    session.headers.update(HEADERS)
    session.cookies.update(COOKIES)
    date_ranges = range(strart_month, end_month + 1), range(start_year, end_year + 1)
    for month, year in itertools.product(*date_ranges):
        response = session.post(URL, json=movement_query(month, year), params=PARAMS)
        # Aveces el servidor retorna 5XX cuando la solicitud funciona
        # Estos casos parecen ser cuando no hay datos en la fecha solicitada
        if response.ok:
            response_data = response.json()
            data.extend(response_data["datos"]["resultadoOperacion"]["movimientosProductoLst"])
    # Dump
    save(data)


if __name__ == "__main__":
    import sys
    parameters = sys.argv[1:]
    if not parameters:
        print(f"Uso:  python {sys.argv[0]} <mes_inicial> <año_inicial> <mes_final> <año_final>")
    else:
        assert len(parameters) == 4, "Incorrecta cantidad de datos entregados"
        assert all(map(lambda p: p.isnumeric(), parameters)), "Parametros no numéricos"
        main(*map(int, parameters))
