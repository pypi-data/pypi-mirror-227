from .content_compendium import Compendium
from .content_sequence import Sequence
#from .sequence import ClassSequence

from ._compendium_index import compendium_index
from ._compendium_content import compendium_content_one_elt





def compendium_content(
        collection:str=None,
        name:str=None,
        dis:str=None,
        lang:str=None,
        return_all_datas:bool=True
):

    if name == "index":

        name = None
        return compendium_index(collection=collection,name=name,dis=dis,lang=lang)

    else:

        if dis == "all":
            dis = None
        #endIf
        if lang == "all":
            lang = None
        #endIf

        idx = compendium_index(collection=collection,name=name,dis=dis,lang=lang)

        if len(idx["index"]) == 1 :

            return compendium_content_one_elt(collection=collection,name=name,dis=dis,lang=lang)

        elif not return_all_datas:

            return idx

        else:

            result = {}

            for k_name, v_datas in idx.items():

                if not v_datas:
                    continue
                #

                for k_idx, v_prayer in v_datas.items():
                    print(k_name, k_idx, "!!", v_prayer)
                    tmp = compendium_content_one_elt(
                        collection=v_prayer["collection"],
                        name=v_prayer["title"],
                        dis=v_prayer["disambiguation"],
                        lang=v_prayer["language"]
                    )
                    result = {**result, **tmp}
                #
            #
            return result
        #endIf

        return {"status": "Unexpected error! mod_compendium"}
#endDef

#

__all__ = ["Compendium", "Sequence"]
