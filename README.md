# 🔴 DIFF-tool Discord Nuker

## 📋 Description

DIFF-tool est un outil de test de sécurité Discord permettant d'évaluer la robustesse des permissions et des protections d'un serveur. Il offre des fonctionnalités de:
- Suppression massive de channels/rôles
- Bannissement de membres
- Création en masse de channels/rôles
- Spam via webhooks
- Mode bot automatisé avec commandes Discord

## ⚙️ Fonctionnalités

### Menu Principal
```
modules/ui.py
```

### Mode Bot Discord
Le mode bot offre des commandes avancées:
- `!nuke` - Destruction complète du serveur (6 phases)
- `!spam [amount]` - Spam de messages
- `!massban` - Bannissement massif
- `!delchannels` - Suppression de tous les channels
- `!delroles` - Suppression de tous les rôles
- `!admin` : Donne les permissions administrateur à absolument tout le monde.
- `!nickall` : Change le pseudonyme de tous les membres.
- `!logspam` : Inonde l'Audit Log pour masquer les actions en cours.

## 🔧 Installation

### Prérequis
- Python 3.8+
- Compte Discord avec un bot configuré
- Token de bot Discord valide

### Dépendances

pip install -r requirements.txt
```

### Configuration

1. **Créer un Bot Discord**:
   - Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
   - Créez une nouvelle application
   - Activez l'onglet "Bot"
   - Copiez le token du bot
   - Activez les **Privileged Gateway Intents**: `PRESENCE`, `SERVER MEMBERS`, `MESSAGE CONTENT`

2. **Inviter le bot**:
   - OAuth2 → URL Generator
   - Sélectionnez les scopes: `bot`, `applications.commands`
   - Permissions requises:
     - Administrator (ou permissions granulaires)
     - Manage Channels
     - Manage Roles
     - Ban Members
     - Manage Webhooks

3. **Premier lancement**:
   ```bash
   python DIFF-tool.py ou depuis le fichier
   ```
   - Le script créera automatiquement le dossier `data/`
   - Entrez votre token de bot (sans le préfixe "Bot ")
   - Entrez l'ID du serveur cible

## 📁 Structure des Fichiers

```
DIFF-tool/
├── DIFF-tool.py          # Script principal
├── data/
│   ├── token.txt          # Tokens sauvegardés (format: token|note)
│   └── guild.txt          # Guild IDs sauvegardés (format: id|note)
├── LICENSE                # Licence MIT
├── modules/configs/
│   ├── __init__.py        # Initialisation des modules
│   ├── api_functions.py   # Module pour les appels API
│   ├── bot_nuker.py       # Bot nuker
│   ├── config.py          # Configuration générale
│   └── ui.py              # Interface du menu
├── README.md
└── requirements.txt       # Liste des dépendances
```

## 🚀 Utilisation

### Lancement Basique
```bash
python DIIF-tool.py
```

### Workflow Typique

1. **Sélection du Token**:
   - Choisissez un token existant ou ajoutez-en un nouveau
   - Les tokens sont masqués pour la sécurité

2. **Sélection du Serveur**:
   - Choisissez un Guild ID existant ou ajoutez-en un nouveau

3. **Utilisation du Menu**:
   - Options 1-6: Opérations directes via API
   - Option 7: Mode bot Discord avec commandes

### Exemple: Mode Bot
```
[07] Bot nuker
> Entrer prefix: !
> Entrer message spam: Test de sécurité
> Nom des channels: test-channel
> Nom des rôles: test-role
> Ban tous les membres ? (y/n): n
> Nombre de channels à créer: 10
> Nombre de rôles à créer: 5
> Messages spam par channel: 20
```

Ensuite, dans Discord:
```
!nuke  # Lance la destruction complète
!nuke - Nuke complet (6 phases)
!massban - Bannir tous les membres
!delchannels - Supprimer tous les channels
!delroles - Supprimer tous les rôles
!spam - Spammer des messages
! = prefixe du bot

```

## 🛡️ Considérations de Sécurité

### ⚠️ IMPORTANT - Légalité

**Utilisation AUTORISÉE**:
- ✅ Tests sur VOS PROPRES serveurs
- ✅ Environnements de test contrôlés
- ✅ Audits de sécurité avec autorisation écrite
- ✅ Recherche académique avec consentement

**Utilisation INTERDITE**:
- ❌ Serveurs dont vous n'êtes pas propriétaire
- ❌ Serveurs sans autorisation explicite
- ❌ Attaques malveillantes ou vengeance
- ❌ Harcèlement ou perturbation de communautés

### Conséquences Légales
L'utilisation non autorisée peut entraîner:
- Bannissement permanent de Discord
- Poursuites judiciaires (Computer Fraud and Abuse Act, RGPD)
- Amendes et peines de prison selon la juridiction

### Protection de vos Tokens
- ⚠️ **Ne partagez JAMAIS vos tokens**
- Les tokens sont stockés en clair dans `data/token.txt`
- Utilisez des permissions minimales nécessaires
- Régénérez les tokens après utilisation

## 🔍 Détails Techniques

### Rate Limiting
L'outil gère automatiquement les limites de débit Discord:
- Retry automatique avec délais exponentiels
- Messages d'avertissement lors de rate limits

### Gestion d'Erreurs
- Validation des tokens avant utilisation
- Try-catch sur toutes les opérations API
- Logs détaillés avec timestamps

### Optimisation
- Utilisation d'`asyncio` pour les opérations parallèles
- Session HTTP réutilisable via `aiohttp`
- Traitement par batch des opérations massives

## 🐛 Dépannage

### Erreur: "Token validation failed"
- Vérifiez que le token est correct
- Assurez-vous que le bot n'est pas désactivé
- Vérifiez que les Intents sont activés

### Erreur: "Permissions insuffisantes"
- Le bot nécessite les permissions Administrator
- Ou configurez manuellement les permissions requises

### Rate Limits Fréquents
- Discord limite à ~50 requêtes/seconde
- L'outil gère automatiquement, patience !

## 📊 Phases du Nuke (Commande !nuke)

1. **Phase 1**: Bannissement des membres (si activé)
2. **Phase 2**: Suppression de tous les rôles
3. **Phase 3**: Suppression de tous les channels
4. **Phase 4**: Création de 20 nouveaux rôles
5. **Phase 5**: Création de 50 nouveaux channels (avec auto-spam)
6. **Phase 6**: Renommage du serveur

## 🤝 Contribution

Ce projet est à but **éducatif uniquement**. Les contributions doivent respecter cette philosophie.

## 📜 Disclaimer

```
CE LOGICIEL EST FOURNI "TEL QUEL", SANS GARANTIE D'AUCUNE SORTE.
L'AUTEUR NE PEUT ÊTRE TENU RESPONSABLE DES DOMMAGES RÉSULTANT
DE L'UTILISATION DE CET OUTIL.

EN UTILISANT CE CODE, VOUS ACCEPTEZ L'ENTIÈRE RESPONSABILITÉ
DE VOS ACTIONS ET VOUS ENGAGEZ À RESPECTER:
- Les lois locales et internationales
- Les Conditions d'Utilisation de Discord
- Les règles d'éthique en sécurité informatique
```

## 📞 Support

Pour des questions légitimes sur la sécurité Discord:
- [Discord Security](https://discord.com/security)
- [Bug Bounty Program](https://discord.com/security)

---

**Version**: 1.0  
**Développeur**: Slender  
**Dernière mise à jour**: 2025

> ⚠️ **RAPPEL FINAL**: Utilisez cet outil de manière responsable et éthique. La cybersécurité commence par le respect et le consentement.

### PLUS DE CONFIGURATION :

**Vous pouvez également configurer le code :**


**LIGNE 29 de "bot_nuker.py" :**
activity = discord.Game(name=f"**{ta config}**", type=3)

**LIGNE 132 de "bot_nuker.py" :**
await guild.edit(name="**{ton nom de serveur a changer}**"

**LIGNE 148 de "bot_nuker.py" :**
await guild.ban(member, reason="**{ta raison}**") **c'est le message qui apparaitra quand on sera banni**

**LIGNE 18 de "DIFF-tool.py" :**
nom = **"ton nom"** **replace par ton pseudo**


**MERCI A TOI :)**

## CREDIT :
# Slender

*
