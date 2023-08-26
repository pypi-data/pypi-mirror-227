import sys
import json
import re

if __name__=="__main__":
    import os
    sys.path.insert(0, os.path.abspath('../..'))
#end

from dktotoolkit import ParserHTML, clean_json
from dktotoolkit.dict import unprefix_keys

from .db import OfficeDB
from ..compendium import Compendium

SKIP_PARSER_INFOS=["date", "date_requete", "id_office"]
SKIP_PARSER_ELTS=["cle_element", "element_defaut", "reference", "id_office", "nom_office"]
def insert_doxologie(lst):
    """
    Insère un élément spécifique après chaque élément ayant "b" à True dans une liste de dictionnaires.

    Args:
        lst (list): La liste de dictionnaires.

    Returns:
        list: La liste modifiée avec l'insertion de l'élément supplémentaire.
    """
    result = []
    next_id = 0
    i = 0
    for item in lst:

        item["id_deroule"] = next_id
        result.append(item)
        next_id += 1

        if "ajouter_doxologie" in item.keys() and item["ajouter_doxologie"]:

            new_item = {"id_deroule": next_id, "cle_element":f"doxologie", "texte": "INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER   INSERER"}
            result.append(new_item)
            next_id += 1
            i += 1

        #endIf

    #endFor

    return result
#endDef

if __name__=="__main__":
    # Exemple d'utilisation
    data = [
        {"id_deroule": 1, "ajouter_doxologie": True, "t": "coucou"},
        {"id_deroule": 2, "ajouter_doxologie": None, "t": "Bonjour"},
        {"id_deroule": 3, "ajouter_doxologie": False, "t": "Hello"},
        {"id_deroule": 4, "ajouter_doxologie": True, "t": "Bye"},
        {"id_deroule": 5, "ajouter_doxologie": False, "t": "Haa", "p": "papa"},
    ]

    modified_data = insert_doxologie(data)
    print(modified_data)
#endIf

def get_office(self, format_output:str=None, **kwargs)->None:
    """Recuperer tout l'office a partir de la base de donnee, retourne les donnees au format self.format_output

    :returns: office
    :rtypes: dict
    """
    format_kwargs = unprefix_keys(dico=kwargs, prefix="format_")
    office_kwargs = {k:kwargs[k] for k in set(kwargs.keys())-set(["format_"+i for i in format_kwargs.keys()])}

    print("get office >> FORMAT KWARGS", format_kwargs)
    print("get office >> OFFICE KWARGS", office_kwargs)

    self.update_db()
    db = OfficeDB()

    # 3. (dict) info, (dict) hunfolding, (dict) office (=nom_office) = call_db_complet(date_office, calendrier, source="aelf"))
    elements = db.get_elements(self.calendar, self.date, self.office, self.source)
    infos = db.get_infos(self.calendar, self.date, self.office, self.source)

    if not infos:
        path = db.db_path
        db.close()
        raise ValueError(f"Unexpected empy 'infos' : please check {self.calendar}, {self.date}, {self.office}, {self.source} in database {path}:  {infos}")
    elif not elements:
        path = db.db_path
        db.close()
        raise ValueError(f"Unexpected empy 'elements' : please check {self.calendar}, {self.date}, {self.office}, {self.source} in database {path}:  {elements}")
    #
    db.close()

    if isinstance(infos, list) or isinstance(infos, tuple) and len(infos) == 1:
        infos = infos[0]
    elif isinstance(infos, list) or isinstance(infos, tuple):
        raise ValueError(f"Unexpected empy 'infos' (len = {len(infos)}) : please check {self.calendar}, {self.date}, {self.office}, {self.source} in database :  {infos}")
    #endIf

    # print(elements[13])
    # elements_parser = ParserHTML(
    #     [elements[13],],
    #     convertEmptyNone=True,
    #     convert_keys=False,
    #     skip_values=["cle_element", "element_defaut", "reference", "id_office", "nom_office"]
    # )
    #
    # e = elements_parser.utf8_to_html(inplace=True, cleanHTML=True)
    # print()
    # try:
    #     print("p1>", elements_parser.data[13])
    # except:
    #     print("P1>", elements_parser.data)
    # #
    # try:
    #     print("e1>", e[13])
    # except:
    #     print("E1>", e)
    # #end
    # print()
    # e = elements_parser.html_to_markdown(inplace=True)
    # print()
    # try:
    #     print("p2>", elements_parser.data[13])
    # except:
    #     print("P2>", elements_parser.data)
    # #
    # try:
    #     print("e2>", e[13])
    # except:
    #     print("E2>", e)
    # #end
    # print()
    # import sys ; sys.exit(5)


    # 4. Si formatting = html : conversion recursive
    # 4. Si formatting = markdown : conversion recursive

    # Modification des donnees :
    elements = insert_doxologie(elements)

    if office_kwargs and not "doxologie" in office_kwargs.keys():
        office_kwargs["doxologie"] = "doxologie_court"
    else:
        office_kwargs = {"doxologie":"doxologie_court"}
    #endIf

    for k, v in office_kwargs.items():

        cles = [e['cle_element'] if 'cle_element' in e.keys() else None for e in elements]
        mask_cle = [k == e for e in cles]

        if v is None or not v or v.lower() == "aelf": # utiliser la valeur par defaut
            continue
        #endIf

        if not k in cles: # Ne pas ajouter d'element qui ne serait pas présent dans le déroulé
            sys.stderr.write(f"Key {k} is not in the hunfolding: {cles}\n")
            continue
        #endIf

        comp = Compendium(key=v)
        exec_code = comp.name2data()

        if exec_code == 0:

            content={
                "titre": comp.title,
                "texte": comp.text,
                "editeur": comp.editor,
                "auteur": comp.author,
                "reference": comp.collection,
                "disambiguation":comp.disambiguation,
                "langue":comp.language,
            }

            # Il n'y a que la que j ai besoin de nettoyer, car le contenu d'AELF l'a ete
            content = ParserHTML(
                content,
                convertEmptyNone=False,
                convert_keys=False,
                skip_values=SKIP_PARSER_ELTS
            ).utf8_to_html(
                cleanHTML=True #(
                    #True or self.format_output in ["simple_html", "markdown"]
                    #)
            )

            for i in range(len(elements)):
                print("CONTENT GETO", content, "..")
                if mask_cle[i] and isinstance(content, dict):
                    print("CONTENT GET1", content, "..")
                    for k, v in content.items():
                        elements[i][k] = v
                    #endFor
                #endIf
            #endFor

        #endIf

    #endFor

    #endIf

    if format_output is None:
        format_output = self.format_output
    #

    # if format_output=="native" :
    #     return  {
    #         "informations":infos,
    #         self.office:elements
    #     }
    # #endIf

    # if isinstance(infos, list) and len(infos) == 1:
    #     infos = infos[0]
    # elif isinstance(infos, list):
    #     raise Exception(f"infos_parser is not expected to be a list: {infos}, {len(infos)}")
    # else:
    #     raise Exception(f"{type(infos)} -- {infos}")
    # #
    infos_parser = ParserHTML(
        infos,
        convertEmptyNone=True,
        convert_keys=False,
        skip_values=SKIP_PARSER_INFOS,
    )
    infos_parser.utf8_to_html(inplace=True, cleanHTML=True)

    elements_parser = ParserHTML(
        elements,
        convertEmptyNone=True,
        convert_keys=False,
        skip_values=SKIP_PARSER_ELTS
    )

    elements_parser.utf8_to_html(inplace=True, cleanHTML=True)


    # 5. Retourner les infos

    # == Pretraitement des kwargs
    # === Kwargs par defaut
    format_kwargs.update({"inplace":False, "data":None})

    # === Modification des kwargs donnes
    dwrap = str(format_kwargs.get("discordwrap")).lower() in ["true", "yes", "1"]

    if (
            isinstance(format_kwargs.get("discordwrap_width"), str) and
            format_kwargs.get("discordwrap_width").isdigit() ):
        dwrapwidth = int(format_kwargs.get("discordwrap_width"))
    else:
        dwrapwidth = "0"
    #
    format_kwargs.update(
        {
            "discordwrap":dwrap,
            "discordwrap_width":dwrapwidth
        }
    )

    # == On continue maintenant

    print("get_office datas : ",elements_parser.__dict__)
    print("get_office PASSING KWARGS", format_kwargs)
    print()
    if format_output.lower() == "simple_html" :
        almost_out = {
            "informations":infos_parser.html_to_utf8(**format_kwargs),
            self.office:elements_parser.html_to_utf8(**format_kwargs)
        }
    elif format_output.lower() == "html" :
        almost_out = {
            "informations":infos_parser.get_data(), # On ne passe pas de kwargs si on recupere simplement les donnees
            self.office:elements_parser.get_data()
        }
    elif format_output.lower() == "markdown" :
        almost_out = {
            "informations":infos_parser.html_to_markdown(**format_kwargs),
            self.office:elements_parser.html_to_markdown(**format_kwargs)
        }
    else:
        sys.stderr.write("dktorecuperedb.office.get_office : format_output = {format_output} not defined ! (I'll out HTML datas)\n")
        almost_out = {
            "informations":infos_parser.get_data(), # On ne passe pas de kwargs si on recupere simplement les donnees
            self.office:elements_parser.get_data()
        }
    #endIf

    return clean_json(almost_out)

#endDef
