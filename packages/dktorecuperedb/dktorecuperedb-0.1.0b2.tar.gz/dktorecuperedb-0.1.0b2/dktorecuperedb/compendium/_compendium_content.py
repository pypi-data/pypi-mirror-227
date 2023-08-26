from .content_compendium import Compendium

def compendium_content_one_elt(
        collection:str=None,
        name:str=None,
        dis:str=None,
        lang:str=None,
):
    """
Return a prayer (ONLY ONE)

dis = disambiguation
lang = language
"""

    try:
        comp = Compendium(collection=collection, title=name, disambiguation=dis, language=lang)
        exec_code = comp.name2data()

        content = {}
        if exec_code == 0:
            content[comp.key]={
                "name": comp.title,
                "collection": comp.collection,
                "disambiguation":comp.disambiguation,
                "language":comp.language,
                "content": comp.text,
                "author": comp.author,
                "editor": comp.editor,
            }

        elif exec_code == 1:
            content["index"] = {}
        else:
            content["index"] = {}
        #endIf
        #TODO : gerer si erreur (par exemple, pas de donnee trouvee)

        #content = f"Coucou compendium : collection={collection} ; name={name} ; disambiguation={dis} ; language={lang}"
    except:
        content = {}
        raise Exception("COMPENDIUM CONTENT")
    #endTry

    return content
#endDef
