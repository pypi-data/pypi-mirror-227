def aelf_officecontent_to_elements(office_content, hunfolding=[]):
    """
:param dict office_content: datas from AELF API, v1
:param list hunfolding: Hunfolding (usefull to repeat the "antienne" for exemple)
:return: hunfolding with datas from AELF
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
            else:
                raise ValueError("Unexpected case here (0) !")
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
        if d is None:
            print(f"Error in the database ! {element} not found in {office_content}!")
            continue
        #
        print(d)
        if isinstance(d, str):
            element["texte"] = d
        elif isinstance(d, dict):
            element.update(d)
        else:
            raise ValueError("Unexpected case here (1) !")
    #
    return hunfolding
#
