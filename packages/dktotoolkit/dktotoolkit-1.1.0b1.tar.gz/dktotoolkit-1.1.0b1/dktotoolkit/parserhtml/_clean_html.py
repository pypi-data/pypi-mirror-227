from bs4 import BeautifulSoup
import html
import re

if __name__=="__main__":
    import os, sys
    sys.path.insert(0, os.path.abspath('..'))
    from function_recursive import recurs_function
else:
    from ..function_recursive import recurs_function
#end


def _clean_html(data, **kwargs):
    """
    OK pour test unitaires !
    TODO : convertir caracteres speciaux hors balises...

    Nettoie le code HTML en uniformisant les balises et en convertissant les caractères spéciaux en entités HTML.
    Assure l'uniformité des valeurs pour les attributs spécifiques tels que `class`, `id`, `href`, `src` et `alt`.

    :param str content: Le code HTML à nettoyer.
    :return: Le code HTML nettoyé.
    :rtype: str
    """

    if data is None:
        return ""
    #
    if not isinstance(data,str):

        recurs_datas = recurs_function(
            _clean_html,
            data=data,
            recurs=True,
            **kwargs
        )

        return recurs_datas

    #endIf

    print("CONTENT >>>", data)
    soup = BeautifulSoup(data, 'html.parser')

    # Liste des balises à rechercher et remplacer avec leurs variantes
    tag_variants = {
        'br': ['br', 'br/', 'br /', 'br /'],
        #'hr': ['hr', 'hr/', 'hr /'], # Supprime ici a cause des attributs
        #'img': ['img', 'img/', 'img /'], # idem
        'input': ['input', 'input/', 'input /'],
        'link': ['link', 'link/', 'link /'],
        'meta': ['meta', 'meta/', 'meta /'],
        'source': ['source', 'source/', 'source /'],
        'track': ['track', 'track/', 'track /'],
        'wbr': ['wbr', 'wbr/', 'wbr /']
    }

    # Liste des attributs nécessitant une uniformité de valeurs
    uniform_attributes = ['class', 'id', 'href', 'src', 'alt']

    for tag in soup.find_all():

        # Nettoyage des balises avec les variantes
        if '\xa0' in tag.name :
            tag.replace_with(soup.new_tag(str(tag.name).replace("\xa0", "")))
        #
        for original_tag, variant_tags in tag_variants.items():
            if tag.name == original_tag or str(tag) in [f"<{variant}/>" for variant in variant_tags]:
                tag.replace_with(soup.new_tag(original_tag))
            #
        #

        # Vérification si la balise est présente dans l'arborescence avant de la remplacer
        if tag.find_parent():
            # Nettoyage des attributs nécessitant une uniformité de valeurs
            for attribute in uniform_attributes:
                if attribute in tag.attrs:
                    attribute_value = tag.attrs[attribute]
                    if isinstance(attribute_value, str):
                        attribute_value = attribute_value.strip()
                        tag.attrs[attribute] = attribute_value


        # Nettoyage des balises avec les variantes
        balises_variants = [str(tag)]
        for attr in tag.attrs:
            if attr in uniform_attributes:
                attr_value = tag.attrs[attr]
                balises_variants.append(f"<{tag.name} {attr}='{attr_value}'>")
                balises_variants.append(f"<{tag.name} {attr}=\"{attr_value}\">")
                # balises_variants.append(f"<{tag.name} {attr}=\\\"{attr_value}\\\">")

        # Vérification si la balise est présente dans l'arborescence avant de la remplacer
        if tag.find_parent():
            replace_tag = True  # Variable pour vérifier si la balise doit être remplacée
            for variant in balises_variants:
                if variant == str(tag):  # Si la balise est égale à l'une des variantes, elle ne doit pas être remplacée
                    replace_tag = False
                    break
                #
            #
            if replace_tag:
                tag.replace_with(soup.new_tag(tag.name))
            #
        #

    # Conversion des caractères spéciaux en entités HTML
    # cleaned_content = html.escape(str(soup))
    # Remplacer les caractères spéciaux en dehors des balises
    #cleaned_content = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', content)
    cleaned_content = str(soup)
    return cleaned_content


## Exemple d'utilisation
if __name__=="__main__":
    html_content = '<p>Hello, <br\xa0/><span class=\"verse_number\">R/</span>world!</p> <img src="image.jpg"  alt="Image" />'
    cleaned_html = _clean_html(html_content)
    print("-", html_content)
    print("+", cleaned_html)
#
