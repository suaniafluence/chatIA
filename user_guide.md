# Guide d'utilisation - IAfluence

Ce guide détaille l'utilisation de la plateforme IAfluence pour la génération, le déploiement et la gestion de chatbots personnalisés.

## Table des matières

1. [Interface d'administration](#interface-dadministration)
2. [Gestion des clients](#gestion-des-clients)
3. [Configuration des chatbots](#configuration-des-chatbots)
4. [Intégration des widgets](#intégration-des-widgets)
5. [Consultation des conversations](#consultation-des-conversations)
6. [Gestion des LLMs](#gestion-des-llms)
7. [Rapports et statistiques](#rapports-et-statistiques)

## Interface d'administration

### Connexion

1. Accédez à l'interface d'administration via l'URL : `https://votre-domaine.com/admin`
2. Connectez-vous avec vos identifiants administrateur :
   - Nom d'utilisateur : `suan.tay@iafluence.fr` (par défaut)
   - Mot de passe : `motdepassefort` (par défaut)

### Navigation

L'interface d'administration est organisée en plusieurs sections accessibles via le menu latéral :

- **Tableau de bord** : Vue d'ensemble des statistiques et activités
- **Clients** : Gestion des clients et de leurs quotas
- **Chatbots** : Configuration des chatbots pour chaque client
- **Conversations** : Historique des échanges entre utilisateurs et chatbots
- **LLMs** : Configuration des modèles de langage
- **Utilisateurs** : Gestion des utilisateurs administrateurs
- **Paramètres** : Configuration générale de la plateforme

## Gestion des clients

### Création d'un nouveau client

1. Dans le menu latéral, cliquez sur **Clients**
2. Cliquez sur le bouton **Ajouter un client**
3. Remplissez le formulaire avec les informations du client :
   - **Nom** : Nom de l'entreprise ou de l'organisation
   - **Identifiant client** : Identifiant unique (généré automatiquement, mais modifiable)
   - **Domaine** : Domaine web principal du client
   - **Email de contact** : Email principal pour les communications
   - **Nom du contact** : Personne à contacter
   - **Téléphone du contact** : Numéro de téléphone
   - **Quota mensuel** : Nombre de requêtes LLM autorisées par mois
4. Cliquez sur **Créer**

### Modification d'un client

1. Dans la liste des clients, cliquez sur le client à modifier
2. Modifiez les informations souhaitées
3. Cliquez sur **Enregistrer**

### Suppression d'un client

1. Dans la liste des clients, cliquez sur le client à supprimer
2. Cliquez sur le bouton **Supprimer**
3. Confirmez la suppression

## Configuration des chatbots

### Création d'un nouveau chatbot

1. Dans le menu latéral, cliquez sur **Chatbots**
2. Cliquez sur le bouton **Ajouter un chatbot**
3. Remplissez le formulaire avec les informations du chatbot :
   - **Nom** : Nom du chatbot
   - **Client** : Sélectionnez le client propriétaire
   - **Message de bienvenue** : Message affiché à l'ouverture du chatbot
   - **Couleur principale** : Couleur principale du chatbot
   - **Couleur secondaire** : Couleur secondaire du chatbot
   - **Position** : Position du bouton sur la page
   - **Logo** : URL du logo (optionnel)
   - **Afficher le branding** : Afficher "Propulsé par IAfluence"
   - **Ouverture automatique** : Ouverture automatique du chatbot
   - **Délai avant ouverture** : Délai en millisecondes
   - **LLM par défaut** : Modèle de langage principal
   - **LLM de secours** : Modèle de langage en cas de dépassement de quota
   - **Instructions personnalisées** : Instructions spécifiques pour le LLM
   - **Code personnalisé** : Code Python à exécuter pour enrichir les réponses
4. Cliquez sur **Créer**

### Personnalisation avancée

#### Instructions personnalisées

Les instructions personnalisées permettent d'orienter le comportement du LLM. Exemple :

```
Tu es un assistant commercial spécialisé dans les produits de la marque XYZ.
Réponds de manière concise et professionnelle.
Ne mentionne jamais les produits de la concurrence.
Si on te demande des informations sur les prix, invite toujours l'utilisateur à contacter le service commercial.
```

#### Code personnalisé

Le code personnalisé permet d'enrichir les réponses avec des données externes. Exemple :

```python
import json

# Exemple de récupération de données produits
products = {
    "smartphone": {"name": "XPhone Pro", "price": 999, "stock": 42},
    "laptop": {"name": "XBook Air", "price": 1299, "stock": 15},
    "tablet": {"name": "XPad", "price": 499, "stock": 8}
}

# Analyse du message pour détecter les mentions de produits
product_keywords = ["smartphone", "laptop", "tablet", "téléphone", "ordinateur", "tablette"]
mentioned_products = []

for keyword in product_keywords:
    if keyword in message.lower():
        if keyword == "téléphone":
            keyword = "smartphone"
        elif keyword == "ordinateur":
            keyword = "laptop"
        elif keyword == "tablette":
            keyword = "tablet"
        
        if keyword in products and keyword not in mentioned_products:
            mentioned_products.append(keyword)

# Préparation des données pour le LLM
result = {}
if mentioned_products:
    result["products"] = [products[p] for p in mentioned_products]

# Le résultat sera automatiquement ajouté au contexte du LLM
```

### Prévisualisation du chatbot

1. Dans la liste des chatbots, cliquez sur le chatbot à prévisualiser
2. Cliquez sur l'onglet **Prévisualisation**
3. Testez le chatbot dans l'environnement de prévisualisation

## Intégration des widgets

### WordPress

1. Dans la liste des chatbots, cliquez sur le chatbot à intégrer
2. Cliquez sur l'onglet **Intégration**
3. Téléchargez le plugin WordPress
4. Installez le plugin sur le site WordPress du client :
   - Connectez-vous à l'administration WordPress
   - Accédez à **Extensions > Ajouter**
   - Cliquez sur **Téléverser une extension**
   - Sélectionnez le fichier ZIP du plugin
   - Cliquez sur **Installer maintenant**
   - Activez le plugin
5. Configurez le plugin dans **Réglages > IAfluence Chatbot**

### Autres plateformes

1. Dans la liste des chatbots, cliquez sur le chatbot à intégrer
2. Cliquez sur l'onglet **Intégration**
3. Copiez le snippet HTML
4. Collez le snippet juste avant la balise de fermeture `</body>` du site web du client

## Consultation des conversations

### Recherche de conversations

1. Dans le menu latéral, cliquez sur **Conversations**
2. Utilisez les filtres pour affiner votre recherche :
   - **Client** : Sélectionnez un client spécifique
   - **Période** : Sélectionnez une période
   - **Recherche** : Entrez des mots-clés
   - **LLM** : Filtrez par modèle de langage utilisé

### Analyse d'une conversation

1. Dans la liste des conversations, cliquez sur une conversation
2. Consultez l'historique complet des échanges
3. Visualisez les métadonnées associées à chaque message :
   - LLM utilisé
   - Indice de confiance
   - Temps de réponse
   - Nombre de tokens

### Export des données

1. Dans la liste des conversations, sélectionnez les conversations à exporter
2. Cliquez sur le bouton **Exporter**
3. Choisissez le format d'export (CSV ou JSON)
4. Téléchargez le fichier d'export

## Gestion des LLMs

### Configuration des LLMs

1. Dans le menu latéral, cliquez sur **LLMs**
2. Pour chaque LLM, vous pouvez configurer :
   - **Statut** : Actif ou inactif
   - **Température** : Niveau de créativité (0.0 à 1.0)
   - **Tokens maximum** : Limite de tokens par requête
   - **Coût** : Coût par 1000 tokens

### Suivi de l'utilisation

1. Dans le menu latéral, cliquez sur **LLMs**
2. Cliquez sur l'onglet **Utilisation**
3. Consultez les statistiques d'utilisation par client et par LLM :
   - Nombre de requêtes
   - Nombre de tokens
   - Coût estimé

## Rapports et statistiques

### Tableau de bord

Le tableau de bord présente une vue d'ensemble des statistiques clés :

- Nombre total de clients
- Nombre total de chatbots
- Nombre total de conversations
- Utilisation des LLMs
- Activité récente

### Rapports par client

1. Dans la liste des clients, cliquez sur un client
2. Cliquez sur l'onglet **Rapports**
3. Sélectionnez la période souhaitée
4. Consultez les statistiques détaillées :
   - Nombre de conversations
   - Nombre de messages
   - Utilisation des LLMs
   - Temps de réponse moyen
   - Répartition par jour/semaine/mois

### Alertes et notifications

Le système envoie automatiquement des alertes par email dans les cas suivants :

- Dépassement du quota mensuel d'un client
- Basculement vers un LLM de secours
- Erreurs répétées dans la génération de réponses

## Assistance et support

Pour toute question ou assistance, contactez le support IAfluence :

- Email : support@iafluence.fr
- Téléphone : +33 (0)1 23 45 67 89
- Horaires : Du lundi au vendredi, de 9h à 18h (CET)
