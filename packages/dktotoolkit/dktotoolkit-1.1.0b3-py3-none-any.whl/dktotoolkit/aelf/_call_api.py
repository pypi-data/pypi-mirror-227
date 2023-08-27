# -*- coding: utf-8 -*-
"""
@author: Pierre
"""

import sys
import re
import requests, json

if __name__=="__main__":
    from ..datestr import is_valid_date
    from ..html import request_html_page
else:
    from dktotoolkit.datestr import is_valid_date
    from dktotoolkit.html import request_html_page
#

def call_api_aelf(
        office_name,
        date,
        zone=None,
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

    if "<title>AELF — 404</title>" in text:
        message="A parameter is wrong : page not found.\n"
        message+="office_name: {office_name}"+"\n"
        message+="date: {date}"+"\n"
        message+="zone: {zone}"+"\n"
        message+="\n\n"
        raise ValueError(message)
    #

    datas_from_aelf = json.loads(text)

    if return_alldatas:
        return datas_from_aelf
    else:
        return datas_from_aelf[office_name]
    #endIf

    return 1

#endDef



if __name__=="__main__":
    print(api_aelf("informations", date="2023-05-21"))
    print()
    #print(api_aelf("informations",the_day="3 juin"))
    print()
    #print(api_aelf("informations",the_day="hier"))
    print()
    #print(api_aelf("informations",the_day="avant-hier"))
    print()
