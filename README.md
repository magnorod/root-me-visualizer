# root-me-visualizer

Le but de ce projet est de visualiser via Kibana les logs Root-me de l'URCA

Il se compose de plusieurs parties:
* un script Python pour interagir avec l'API de Root-me et envoyer les logs dans un index Elasticsearch
* un noeud Elasticsearch qui stocke les données
* un noeud Kibana qui permet de visualiser les données


![root-me-visualizer](https://user-images.githubusercontent.com/12548183/159528881-47d992b1-9648-4c03-beb3-06df77fa34bc.png)
