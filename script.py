#!/usr/bin/python
import requests
import json
import time
import datetime
import sys
from elasticsearch import Elasticsearch

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

#création de l'index, ignore si existe déja
def create_es_index(es,index_name):
    try:
        es.indices.create(index=index_name)
        print("index "+index_name+" créé")
    except:
        pass
#endef

def search_data(es,index_name,rootme_name,rootme_idtrad):
    query_body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"rootme_nom": rootme_name}},
                    {"match": {"rootme_idtrad": rootme_idtrad}}
                ]
            }
        }
    }
    result = es.search(index=index_name, body=query_body )
    return len(result["hits"]["hits"])
#endef

def index_data(es,index,data):
    resp = es.index(index=index_name, document=resultat)
    print(resp['result'])
#endef


def set_rootme_date(date):
    date_annee=date[0:4]
    date_mois=date[5:7]
    date_jour=date[8:10]
    date_heure=date[11:13]
    date_min=date[14:16]
    date_sec=date[17:19]
    date=date_annee+"/"+date_mois+"/"+date_jour+" "+date_heure+":"+date_min+":"+date_sec

    return date
#endef

if __name__ == '__main__':

    pres= """        
                | |                               (_)               | (_)             
 _ __ ___   ___ | |_ ______ _ __ ___   ___  __   ___ ___ _   _  __ _| |_ _______ _ __ 
| '__/ _ \ / _ \| __|______| '_ ` _ \ / _ \ \ \ / / / __| | | |/ _` | | |_  / _ \ '__|
| | | (_) | (_) | |_       | | | | | |  __/  \ V /| \__ \ |_| | (_| | | |/ /  __/ |   
|_|  \___/ \___/ \__|      |_| |_| |_|\___|   \_/ |_|___/\__,_|\__,_|_|_/___\___|_|   
                                                                                                                                                                                                                                                                        
    """
    print(pres)

    elastic_ip="IP_A_CHANGER"
    cookies = {"api_key": "API_KEY_A_CHANGER"}
    uids=[412,38837,258150,139379,359178,487915,436761,122852,149440,225265,609569,449312,408261,491166,419693,5384,411124,112697,222479,525710,41353,348505,145667,406883,226807,354649,382779]
    index_name="rootme-0000002"
    elastic_password="PASS_A_CHANGER"
    es = Elasticsearch(
        "https://"+elastic_ip+":9200",
        basic_auth=("elastic", elastic_password),
        verify_certs=False
    )

    create_es_index(es,index_name)
    i=0
    while True:
        resp = requests.get("https://api.www.root-me.org/auteurs/"+str(uids[i])+'"', cookies=cookies)
        if resp.status_code != 200:
            raise Exception(resp.status_code)
        data = resp.json()
        validations=data["validations"]

        # recuperer challenges associes à l utilisateur
        for j in range(0,len(validations)):
            # print(validations[i])
            id_challenge=(validations[j]["id_challenge"])
            # récupérer nom du challenge
            url="https://api.www.root-me.org/challenges/"+id_challenge
            resp2 = requests.get(url, cookies=cookies)
            if resp2.status_code != 200:
                raise Exception(resp2.status_code)
            #endif
            data2 = resp2.json()

            # format valide pour Elasticsearch
            date=set_rootme_date(validations[j]["date"])

            resultat={"rootme_nom":data["nom"],"rootme_score":data["score"],"rootme_position":data["position"],"rootme_rang":data["rang"],"rootme_titre":data2[0]["titre"],"rootme_difficulte":data2[0]["difficulte"],"rootme_rubrique":data2[0]["rubrique"],"rootme_idtrad":data2[0]["id_trad"],"rootme_date_valid":date}
            trouve=search_data(es,index_name,data["nom"],data2[0]["id_trad"])

            if j == 0 and trouve >= 1: # Si le challenge le plus récent de l'utilisateur existe déja dans elasticsearch
                print(str(datetime.datetime.now())+' '+"pas de nouveau challenge pour "+data["nom"])
                break # on change d'utilisateur
            elif trouve == 0: # ingestion du challenge
                print(str(datetime.datetime.now())+' '+str(resultat))
                index_data(es,index_name,resultat)
            #endif
        #endfor
        if i == (len(uids)-1): # boucle infinie avec parcours du tableau depuis le début
            i=0
            time.sleep(600) # pause de 10 min pour éviter de surcharger l'API
        else:
            i=i+1
        #endif
    #endwhile
#endif
