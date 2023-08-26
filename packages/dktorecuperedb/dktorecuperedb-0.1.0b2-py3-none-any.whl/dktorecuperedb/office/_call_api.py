# -*- coding: utf-8 -*-
"""
@author: Pierre
"""

import sys
import re
import requests, json

from dktotoolkit.datestr import is_valid_date
from dktotoolkit.html import request_html_page

def api_aelf(
        office_name,
        date,
        zone="france",
        return_alldatas=True # retourner toutes les donnees ou juste la priere
):
    """
    Recuperer le dictionnaire de donnees d'aelf (vient de ProphetiS)

:param str office_name: nom de l'office
:param str date: jour
:param str zone: calendrier utilise
:param bool return alldatas: Retourner toutes les donnees (informations + priere) ou juste la priere
    """

    if not is_valid_date(date):
        err = "Error : needs "
        err += f"date (= {date}) in format YYYY-MM-DD"
        raise ValueError(err)
    # endIf

    if not office_name or not date or not zone:
        err = "Error : needs "
        err += f"office_name (= {office_name}), "
        err += f"date (= {date}) and zone (={zone})"
        raise ValueError(err)
    #endIf

    requested_url="https://api.aelf.org/v1/{0}/{1}/{2}".format(
        office_name,
        date,
        zone
    )

    text = request_html_page(requested_url)

    datas_from_aelf = json.loads(text)

    if return_alldatas:
        return datas_from_aelf
    else:
        return datas_from_aelf[office_name]
    #endIf

    return 1

#endDef



def _call_api(source, calendar, date, office):
    """Selectionner l'API à utiliser - uniquement AELF pour le moment

:param str source: Nom de la source : UNIQUEMENT AELF
:param str calendar: Nom du calendrier (pour aelf)
:param str date: Date YYYY-MM-DD
:param str office: Nom de l'office
"""

    if source == "aelf":
        return api_aelf(zone=calendar, date=date,  office_name=office)
    #endIf

    return None

#endDef



if __name__=="__main__":
    print(api_aelf("informations", date="2023-05-21"))
    print()
    print(call_api("aelf", calendar="france", office="complies", date="2023-05-21"))
    #print(api_aelf("informations",the_day="3 juin"))
    print()
    #print(api_aelf("informations",the_day="hier"))
    print()
    #print(api_aelf("informations",the_day="avant-hier"))
    print()
    #print(api_aelf("informations",the_day="demain"))
    # str2date(date_string="01 juin")
    # str2date(date_string="01 juin 21")
    # str2date(date_string="01 juin 2021")

    # str2date(date_string="02/07")
    # str2date(date_string="2/7")
    # str2date(date_string="02/07/21")
    # str2date(date_string="02/07/2022")

    # str2date(date_string="2022/08/01")
    # str2date(date_string="21/08/01", format_us=True)


