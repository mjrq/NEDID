from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import process, fuzz  # pip install fuzzywuzzy
import time
import pandas as pd
from unicodedata import normalize
from app.models import Vias

import spacy
nlp = spacy.load("es_core_news_md")  # python -m spacy download es_core_news_md


# =============================================================================
# SEARCH AND NORMALIZATION FUNCTIONS
# =============================================================================
def my_search(address, list_, measure_time=False, scorer=fuzz.WRatio, results=3):
    start_time = time.time()
    simil = process.extract(address.upper(), list_, scorer=scorer)[:results]
    if measure_time:
        return simil, round(time.time() - start_time, 2)
    return simil


def my_text_normalization(text):
    trans_tab = dict.fromkeys(map(ord, u'\u0300\u0301\u0308'), None)
    return normalize('NFKC', normalize('NFKD', text).translate(trans_tab))


# =============================================================================
# TABLES
# =============================================================================
def get_vias_lists(cpro, cmun):
    start_time = time.time()
    query = Vias.query.filter(Vias.CPRO == cpro).filter(
        Vias.CMUN == cmun)

    query_ntvia = query.with_entities(Vias.NTVIA).distinct()
    ntvia = pd.DataFrame(data=query_ntvia, columns=['NTVIA'])

    query_nviac = query.with_entities(Vias.NTVIA, Vias.NVIAC).distinct()
    nviac = pd.DataFrame(data=query_nviac, columns=['NTVIA', 'NVIAC'])

    query_ntvia_nviac = query.with_entities(Vias.NTVIA_NVIAC).distinct()
    ntvia_nviac = pd.DataFrame(data=query_ntvia_nviac, columns=['NTVIA_NVIAC'])

    elapsed_time = round(time.time() - start_time, 2)
    return ntvia, nviac, ntvia_nviac, elapsed_time


# =============================================================================
# GET service FOR TEST
# =============================================================================
def get_address(cpro, cmun, address):
    ''' Get the address from database'''
    address = my_text_normalization(address.upper())
    words = [w.text for w in nlp(address) if not w.is_punct]

    ntvia, nviac, ntvia_nviac, process_data_time = get_vias_lists(
        cpro, cmun)

    simil_ntvia, elapsed_time_ntvia = my_search(address,
                                                ntvia['NTVIA'].to_list(),
                                                measure_time=True,
                                                scorer=fuzz.token_set_ratio)
    ntvia_encountered = simil_ntvia[0][0]
    ntvia_encountered_score = simil_ntvia[0][1]
    elapsed_time_ = 0
    if ntvia_encountered_score > 75:
        start_time = time.time()
        ntvia_in_address = my_search(ntvia_encountered, words)[0][0]
        address_ = address.replace(ntvia_in_address, "").strip()

        nviac = nviac[nviac['NTVIA'] == ntvia_encountered].\
            drop_duplicates()

        elapsed_time_ = round(time.time() - start_time, 2)
    else:
        address_ = address

    simil_nviac, elapsed_time_nviac = my_search(address_,
                                                nviac['NVIAC'].to_list(),
                                                measure_time=True)
    nviac_encountered_score = simil_nviac[0][1]
    elapsed_time_nviac = round(elapsed_time_nviac + elapsed_time_, 2)

    if nviac_encountered_score > 95:
        # result = "¡Búsqueda exitosa!"
        status = 1
        result = simil_nviac[0]
    else:
        # result = "Dirección no encontrada..."
        status = -1
        result = simil_nviac

    return {'status': status, 'tvia': simil_ntvia[0], 'nvia': result}

    # simil_ntvia_nviac, elapsed_time_ntvia_nviac = my_search(address,
    #                                                         ntvia_nviac.values.tolist(),
    #                                                         measure_time=True)

    # return [{"Input": address, "Process Data Time": process_data_time},
    #         {"Seconds: ": elapsed_time_ntvia, "Tipo: ": simil_ntvia},
    #         {"Seconds: ": elapsed_time_nviac, "nombre: ": simil_nviac},
    #         {"Seconds: ": elapsed_time_ntvia_nviac,
    #          "total: ": simil_ntvia_nviac},
    #         {"Result": result}
    #         ]
