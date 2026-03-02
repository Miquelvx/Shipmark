# Shipmark

Shipmark est un projet de groupe en collaboration avec Airbus Defense and Space dans le cadre des Engineering Project de Master 2. L'appel d'offres consistait à proposer une solution de détection de bateaux et de placement de point de repère pour la surveillance des espaces maritimes français.

## Fonctionnalités
    * Affiche du projet pour les Engineering Project Awards
    * Démo de la détection de bateaux du modèle 
    * Lien vers un dashboard Comet ML de l'entrainement

## Hébergement Cloud
Déploiment via Streamlit Cloud : https://shipmark-demo.streamlit.app

## Structure du projet

```bash
SHIPMARK/                               # Répertoire du projet Shipmark
├── img_app/                            # Répertoire contenant les images de l'application
├── test_demo/                          # Répertoire contenant des images de test pour le modèle
│          
├── .gitattributes                      # Fichier .gitattributes du projet
├── Model_Shipmark.pt                   # Modèle YOLO entraîné pour la détection de bateaux
├── packages.txt                        # Fichier contenant les dépendances pour le déploiement cloud
├── README.md                           # Fichier README du projet
├── requirements.tx                     # Fichier contenant les dépendances à installer
└── Shipmark_demo.py                    # Fichier python pour l'application Streamlit
```

## Auteurs

- **© 2024 Shipmark** : 
    - Anne-Julie HOTTIN
    - Maël GUEGUEN
    - Mike LEVELEUX
    - Théo MASSON
    - Nicolas ROUSSELOT
    - Cédric Song
