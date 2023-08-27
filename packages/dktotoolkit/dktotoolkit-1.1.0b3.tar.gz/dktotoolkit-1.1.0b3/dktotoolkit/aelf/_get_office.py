import sys
import json
import re

if __name__=="__main__":
    import os
    sys.path.insert(0, os.path.abspath('../..'))
#end

from dktotoolkit import compat_mode

from ._insert_doxo import insert_doxologie
from ._call_api import call_api_aelf
from ._office_content_to_elements import aelf_officecontent_to_elements

def get_aelf_office(office, date, zone="", hunfolding=[], **kwargs):
    """
:param str office: name of the office
:param str date: date, format YYYY-MM-DD
:param str zone: Zone (france, romain, ...)
:param list hunfolding: Hunfolding (usefull to repeat the "antienne" for exemple)
:return: hunfolding with datas from AELF
:rtypes: list
    """
    if kwargs and not zone:
        zone_proper, kwargs_proper = compatMode("zone", ["calendrier", "calendar"], **kwargs)
        if zone_proper:
            zone, kwargs = zone_proper, kwargs_proper
        # endIf
     # endIf

    datas_api = call_api_aelf(office_name=office, date=date, zone=zone)

    # Split datas
    elements = aelf_officecontent_to_elements(datas_api[office], hunfolding=hunfolding)
    infos = datas_api["informations"]
    del datas_api # Ne pas conserver de doublon : inutile et alourdi

    if not infos:
        raise ValueError(f"Unexpected empy 'infos' : please check {zone}, {date}, {office}:  {infos}")
    elif not elements:
        raise ValueError(f"Unexpected empy 'elements' : please check {zone}, {date}, {office}:  {elements}")
    #

    if isinstance(infos, list) or isinstance(infos, tuple) and len(infos) == 1:
        infos = infos[0]
    elif isinstance(infos, list) or isinstance(infos, tuple):
        raise ValueError(f"Unexpected empy 'infos' (len = {len(infos)}) : please check {zone}, {date}, {office} :  {infos}")
    #endIf

    if hunfolding:
        elements = insert_doxologie(elements)
    #
    return elements, infos
#
