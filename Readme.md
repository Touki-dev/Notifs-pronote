# Notif Pronote
Ce repo contient un code qui permet l'accès automatique à pronote

## Démarer pour la première fois
Installer les dépendances nécessaires :
``` pip install selenium discord flask ```
Construire le projet :
``` python3 Build.py ```

## Utiliser un bot discord (opt1)
Créer un bot discord : https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro
Enregistrer le TOKEN du bot dans le fichier Variables.py créé par Build.py
Exécuter cette commande pour lancer le bot :
``` python3 BotDiscord.py ```

## Utilser une API (opt2)
Démarer l'API avec la commande :
``` python3 API.py ```
> Vous pouvez maintenant envoyer des requète a cette API,ex
> 127.0.0.1/crawl?user_id=votre_ID