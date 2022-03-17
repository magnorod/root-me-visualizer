# root-me-visualizer

Le but de ce projet est de visualiser via Kibana les logs Root-me de l'URCA

Il se compose de plusieurs parties:
* un script Python pour interagir avec l'API de Root-me et envoyer les logs dans un index Elasticsearch
* un noeud Elasticsearch qui stocke les données
* un noeud Kibana qui permet de visualiser les données

![root-me-visualizer](https://user-images.githubusercontent.com/12548183/158899873-4a0c7f5a-894a-42a2-bfb3-ba99226d6651.png)
