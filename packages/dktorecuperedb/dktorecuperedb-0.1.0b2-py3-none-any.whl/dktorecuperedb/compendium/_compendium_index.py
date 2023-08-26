from .content_compendium import Compendium


def compendium_usage(
        usage:str=None,
):
    if usage and isinstance(usage, str):
        try:
            comp = Compendium()
        except:
            content = {}
            raise Exception("COMP IDX 1")
        #endTry

        content = {"index":{}}
        content["index"] = comp.collectionkey2data(usage)
        return content
    #

def compendium_index(
        collection:str=None,
        name:str=None,
        dis:str=None,
        lang:str=None,
):
    """Return a prayer
    # dis = disambiguation
    # lang = language
"""
    if collection is None or name == "index" :
        name, dis = None, None
    elif name is None :
        name = None
    elif dis == "all" or lang == "all":
        dis, lang = None, None
    #endIf

    try:
        comp = Compendium(collection=collection, title=name, disambiguation=dis, language=lang)
    except:
        content = {}
        raise Exception("COMP IDX 0")
    #endTry

    try:
        content = {"index":{}}
        i = 0
        for elt in comp.get_index():

            if "title" in elt.keys():

                if not elt["title"] in content.keys():
                    content[elt["title"]] = {}
                #endIf

                i = len(content[elt["title"]])
                content[elt["title"]][i] = elt

            elif "key" in elt.keys():

                content[elt["key"]] = elt
                content["index"] += [elt["key"],]

            else:

                content["index"] += [elt,]

            #endIf

        #EndFor

        #TODO : gerer si erreur (par exemple, pas de donnee trouvee)

        #content = f"Coucou compendium : collection={collection} ; name={name} ; disambiguation={dis} ; language={lang}"
    except:
        content = {}
        raise Exception("COMP IDX 1")
    #endTry

    return content
#endDef
