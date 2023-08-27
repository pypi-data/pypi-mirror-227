import sys
import json
import re

if __name__=="__main__":
    import os
    sys.path.insert(0, os.path.abspath('../..'))
#end

from dktotoolkit import ParserHTML, clean_json
from dktotoolkit.dict import unprefix_keys
from dktotoolkit import get_aelf_office
from dktotoolkit import discordify_dict
from .db import OfficeDB
from ..compendium import Compendium


SKIP_PARSER_INFOS=["date", "date_requete", "id_office"]
SKIP_PARSER_ELTS=["cle_element", "element_defaut", "reference", "id_office", "nom_office"]

KEY_NAME="key_name" # ex :cle_element

def get_office(self, **kwargs)->None:
    """Recuperer tout l'office a partir de la base de donnee, retourne les donnees au format self.format_output

    :param str kwargs[format_X]: output format (format_discordwrap, format_discordwrap_width)
    :param str kwargs[office_Y]: office kwargs (office_doxologie, ...)
    :returns: office
    :rtypes: dict
    """

    format_kwargs = unprefix_keys(dico=kwargs, prefix="format_")
    office_kwargs = unprefix_keys(dico=kwargs, prefix="office_")
    kwargs = {k:kwargs[k] for k in set(kwargs.keys())-set(["format_"+i for i in format_kwargs.keys()]) - set(["office_"+i for i in format_kwargs.keys()])}

    # 3. (dict) info, (dict) hunfolding, (dict) office (=nom_office) = call_db_complet(date_office, calendrier, source="aelf"))

    hunfolding = []
    if self.options.get("use_hunfolding", False):
        db = OfficeDB()
        hunfolding = db.get_hunfolding(self.calendar, self.date, self.office, self.source, details=self.options["details"])
        db.close()
    #

    if self.source == "aelf":
        elements, infos = get_aelf_office(office=self.office, date=self.date, zone=self.calendar, hunfolding=hunfolding)
    else:
        raise ValueError("source must be AELF")
    #

    # 4. Si formatting = html : conversion recursive
    # 4. Si formatting = markdown : conversion recursive

    # Ajout des donnees par default:
    for element in elements:
        if element.get("default_element_key", False):
            office_kwargs[element.get(KEY_NAME, None)] = element.get("default_element_key", None)
        #
    #

    # Modification des donnees (office_kwargs):
    if office_kwargs and not "doxologie" in office_kwargs.keys():
        office_kwargs["doxologie"] = "doxologie_court"
    else:
        office_kwargs = {"doxologie":"doxologie_court"}
    #endIf

    for k, v in office_kwargs.items():

        cles = [e[KEY_NAME] if KEY_NAME in e.keys() else None for e in elements]
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

            for i in range(len(elements)):
                if mask_cle[i] and isinstance(content, dict):
                    for k, v in content.items():
                        elements[i][k] = v
                    #endFor
                #endIf
            #endFor

        #endIf

    #endFor


    if self.format_output is None or self.format_output.lower() in ["html", "native"]:

        return {
            "informations": infos,
            self.office:elements
        }

    elif not isinstance(self.format_output, str):

        raise ValueError(f"format_output must be a string {self.format_output}")

    elif self.format_output.lower() in ["clean_html", "simple_html"]:

        info = ParserHTML(
            infos,
            convertEmptyNone=True,
            convert_keys=False,
        ).clean_html()

        elements=ParserHTML(
            elements,
            convertEmptyNone=True,
            convert_keys=False,
        ).clean_html()

        return {
            "informations": infos,
            self.office:elements
        }

    elif self.format_output.lower()=="markdown":

        return {
            "informations": discordify_dict(infos, key="texte"),
            self.office:discordify_dict(elements, key="texte")
        }

    else:

        raise ValueError(f"format_output not expected {self.format_output}")
    #

#endDef
