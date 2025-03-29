# Notif Pronote
### Ce repo contient un code qui permet l'accès automatique à pronote

## Démarer pour la première fois
- Installer les dépendances nécessaires :
```shell
pip install selenium discord flask 
```
- Installer geckodriver et le placer à la racine du projet : https://github.com/mozilla/geckodriver/releases
- Construire le projet :
```shell
python3 Build.py 
```

## Utiliser un bot discord (opt1)
- Créer un bot discord : https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro
- Enregistrer le TOKEN du bot dans le fichier `Variables.py` créé par Build.py
- Exécuter cette commande pour lancer le bot :
```shell
python3 BotDiscord.py 
```

## Utilser une API (opt2)
Démarer l'API avec la commande :
```shell
python3 API.py 
```
> Vous pouvez maintenant envoyer des requète a cette API

> Exemple : `127.0.0.1/crawl?user_id=votre_ID`