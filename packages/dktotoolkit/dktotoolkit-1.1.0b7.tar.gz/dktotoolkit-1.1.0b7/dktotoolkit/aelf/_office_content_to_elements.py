import logging

def aelf_officecontent_to_elements(office_content, hunfolding:list=[], skip_empty_items:bool=True):
    """
:param dict office_content: datas from AELF API, v1
:param list hunfolding: Hunfolding (usefull to repeat the "antienne" for exemple, optionnal)
:param bool skip_empty_item: skip empty items, or keep it inside the hunfolding ?
:return: hunfolding (or "hunfolding-like") with datas from AELF
:rtypes: list
    """

    datas = []

    if not hunfolding:
        for k,v in office_content.items():
            dico = {}
            dico["element_key"] = k
            if isinstance(v, dict):
                dico.update(v)
            elif isinstance(v, str):
                dico["texte"] = v
            elif v is None:
                logging.warning(f"office_content_to_element (NOT hunfolding): {k} value is None here !")
                if skip_empty_items:
                    continue
                #
            else:
                raise ValueError(f"Unexpected case here (0) for {k} : {type(v)} -- {v} !")
            # endIf
            datas += [dico,]
        # endFor

        return datas

    # endIf

    for element in hunfolding:
        if not "key_name" in element.keys():
            raise ValueError(f"Error in the database (1) : 'key_name' not found in {element}!")
        #

        d = office_content.get(element["key_name"], None)

        if d is None and skip_empty_items:
            logging.warning(f"office_content_to_element (hunfolding : 1.1): {element['key_name']} value is None here and not 'default_element_key'!")
            continue
        #

        if isinstance(d, str):
            element["texte"] = d
        elif isinstance(d, dict) and d.get("text", None) is None and d.get('default_element_key', None) :
            logging.warning(f"office_content_to_element (hunfolding : 2): {element['key_name']} value is None here and not 'default_element_key'  !")
            if skip_empty_items:
                continue
            else:
                element["texte"] = None
            #
        elif isinstance(d, dict):
            element.update(d)
        elif d is None and not skip_empty_items:
            element["texte"] = None
        else:
            raise ValueError("Unexpected case here (1) !")
        #
        datas += [element,]
    #

    return datas
#
