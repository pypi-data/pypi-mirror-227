def dict2obj(d=None, obj=None):
    """Convert nested Python dictionnary to object

:author: geeksforgeeks.org

:param dict d: input dictionnary
:param obj: a class (could be empty)
    """

    if isinstance(d, list):  # si d est une liste
        d = [dict2obj(x) for x in d]
    # endIf

    if not isinstance(d, dict):  # si d est un dico
        return d
    # endIf

    if obj is None:
        class C:
            pass
        # endClass

        obj = C()
    # endIf

    for k in d:
        obj.__dict__[k] = dict2obj(d[k])
    # endFor

    return obj

# endDef


def invert_dict(dictionary):
    """
    Inverse les clés et les valeurs d'un dictionnaire.

    Args:
        dictionary (dict): Le dictionnaire à inverser.

    Returns:
        dict: Un nouveau dictionnaire avec les clés et les valeurs inversées.
    """

    # Vérifier que le paramètre est bien un dictionnaire
    if not isinstance(dictionary, dict):
        raise TypeError("Le paramètre 'dictionary' doit être un dictionnaire.")
    # endIF

    # Vérifier que les valeurs du dictionnaire sont uniques
    if len(set(dictionary.values())) != len(dictionary):
        raise ValueError("Les valeurs du dictionnaire ne sont pas uniques.")
    #endIf

    return {value: key for key, value in dictionary.items()}
#

def unprefix_keys(dico, prefix="prefix_", keep_only_prefixed=True):
    """Remove prefix of dico (for exemple : d = {"d_aa":1, "d_bb":2, "cc":4} > {'aa': 1, 'bb': 2}
:param dict dico: Input dictionnary
:param str prefix: Prefix (with an underscore if needed !)
:param bool keep_only_prefixed: Keep only prefixed var
"""
    if keep_only_prefixed:
        return {k[len(prefix):]:v for k,v in dico.items() if k[:len(prefix)]==prefix}
    else:
        return {k[len(prefix):] if k[:len(prefix)]==prefix else k:v  for k,v in dico.items() }
