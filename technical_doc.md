# Documentation Technique - IAfluence

Cette documentation technique détaille l'architecture, les composants et les choix d'implémentation de la plateforme IAfluence pour la génération, le déploiement et la gestion de chatbots personnalisés.

## Architecture globale

L'application IAfluence est construite selon une architecture moderne et modulaire, avec une séparation claire entre le frontend et le backend :

```
iafluence/
│
├── backend/                      # Backend FastAPI
│   ├── app/                      # Code source principal
│   │   ├── main.py               # Point d'entrée
│   │   ├── config.py             # Configuration
│   │   ├── auth/                 # Authentification
│   │   ├── clients/              # Gestion des clients
│   │   ├── chatbots/             # Gestion des chatbots
│   │   ├── conversations/        # Gestion des conversations
│   │   ├── llm/                  # Intégration des LLMs
│   │   ├── sandbox/              # Exécution sécurisée de code
│   │   ├── utils/                # Utilitaires
│   │   └── widgets/              # Génération de widgets
│   ├── tests/                    # Tests unitaires et d'intégration
│   └── requirements.txt          # Dépendances Python
│
├── frontend/                     # Frontend TypeScript/React
│   ├── public/                   # Fichiers statiques
│   ├── src/                      # Code source
│   │   ├── components/           # Composants React
│   │   ├── pages/                # Pages de l'application
│   │   ├── api/                  # Clients API
│   │   └── ...                   # Autres modules
│   └── package.json              # Dépendances Node.js
│
└── widgets/                      # Widgets pour les clients
    ├── js/                       # Scripts JavaScript
    ├── css/                      # Styles CSS
    └── templates/                # Templates d'intégration
```

## Backend (FastAPI)

### Structure et organisation

Le backend est développé avec FastAPI, un framework Python moderne et performant. Il est organisé en modules fonctionnels :

- **app/main.py** : Point d'entrée de l'application, configuration des middlewares et des routes
- **app/config.py** : Configuration centralisée de l'application
- **app/auth/** : Gestion de l'authentification et des utilisateurs
- **app/clients/** : Gestion des clients et de leurs quotas
- **app/chatbots/** : Configuration et personnalisation des chatbots
- **app/conversations/** : Traitement des conversations et historisation
- **app/llm/** : Intégration avec différents modèles de langage
- **app/sandbox/** : Exécution sécurisée de code personnalisé
- **app/utils/** : Fonctions utilitaires (base de données, email, sécurité)
- **app/widgets/** : Génération des widgets d'intégration

### Modèle de données

#### Utilisateurs

```python
class User:
    id: str                # Identifiant unique
    email: str             # Email (utilisé comme identifiant de connexion)
    full_name: str         # Nom complet
    hashed_password: str   # Mot de passe haché
    is_admin: bool         # Statut administrateur
    created_at: datetime   # Date de création
    updated_at: datetime   # Date de dernière mise à jour
```

#### Clients

```python
class Client:
    id: str                # Identifiant MongoDB
    client_id: str         # Identifiant unique (utilisé dans les URLs)
    name: str              # Nom du client
    domain: str            # Domaine principal
    contact_email: str     # Email de contact
    contact_name: str      # Nom du contact
    contact_phone: str     # Téléphone du contact
    monthly_quota: int     # Quota mensuel de requêtes
    active: bool           # Statut d'activation
    created_at: datetime   # Date de création
    updated_at: datetime   # Date de dernière mise à jour
```

#### Chatbots

```python
class Chatbot:
    id: str                # Identifiant MongoDB
    client_id: str         # Identifiant du client propriétaire
    name: str              # Nom du chatbot
    welcome_message: str   # Message de bienvenue
    primary_color: str     # Couleur principale
    secondary_color: str   # Couleur secondaire
    position: str          # Position sur la page
    logo_url: str          # URL du logo
    show_branding: bool    # Afficher le branding IAfluence
    auto_open: bool        # Ouverture automatique
    delay_auto_open: int   # Délai avant ouverture (ms)
    active: bool           # Statut d'activation
    custom_instructions: str # Instructions personnalisées pour le LLM
    custom_code: str       # Code personnalisé à exécuter
    default_llm: str       # LLM par défaut
    fallback_llm: str      # LLM de secours
    created_at: datetime   # Date de création
    updated_at: datetime   # Date de dernière mise à jour
```

#### Conversations

```python
class Message:
    id: str                # Identifiant unique du message
    sender: str            # Expéditeur (user ou bot)
    content: str           # Contenu du message
    timestamp: datetime    # Horodatage
    llm_used: str          # LLM utilisé (si bot)
    confidence: float      # Indice de confiance (si bot)
    response_time: float   # Temps de réponse en ms (si bot)
    tags: List[str]        # Tags associés
    metadata: Dict         # Métadonnées supplémentaires

class Conversation:
    id: str                # Identifiant MongoDB
    client_id: str         # Identifiant du client
    chatbot_id: str        # Identifiant du chatbot
    session_id: str        # Identifiant de session unique
    messages: List[Message] # Liste des messages
    user_info: Dict        # Informations sur l'utilisateur
    timestamp: datetime    # Date de création
    updated_at: datetime   # Date de dernière mise à jour
```

#### LLMs

```python
class LLMConfig:
    name: str              # Nom du LLM
    provider: str          # Fournisseur (openai, anthropic, ollama)
    model: str             # Modèle spécifique
    api_key_env: str       # Variable d'environnement pour la clé API
    api_url: str           # URL de l'API
    max_tokens: int        # Nombre maximum de tokens
    temperature: float     # Température (créativité)
    is_fallback: bool      # S'il s'agit d'un LLM de secours
    cost_per_1k_tokens: float # Coût par 1000 tokens
    active: bool           # Statut d'activation
```

### API REST

L'API REST est organisée selon les principes RESTful, avec des endpoints pour chaque ressource :

#### Authentification

- `POST /api/auth/token` : Obtention d'un token JWT
- `GET /api/auth/me` : Informations sur l'utilisateur courant
- `POST /api/auth/register` : Création d'un nouvel utilisateur (admin)

#### Clients

- `GET /api/clients/` : Liste des clients
- `POST /api/clients/` : Création d'un client
- `GET /api/clients/{client_id}` : Détails d'un client
- `PUT /api/clients/{client_id}` : Mise à jour d'un client
- `DELETE /api/clients/{client_id}` : Suppression d'un client
- `GET /api/clients/{client_id}/stats` : Statistiques d'un client
- `GET /api/clients/{client_id}/report` : Rapport détaillé d'un client

#### Chatbots

- `GET /api/chatbots/` : Liste des chatbots
- `POST /api/chatbots/` : Création d'un chatbot
- `GET /api/chatbots/client/{client_id}` : Chatbots d'un client
- `GET /api/chatbots/{id}` : Détails d'un chatbot
- `PUT /api/chatbots/{id}` : Mise à jour d'un chatbot
- `DELETE /api/chatbots/{id}` : Suppression d'un chatbot
- `GET /api/chatbots/{id}/stats` : Statistiques d'un chatbot

#### Conversations

- `GET /api/conversations/` : Liste des conversations
- `POST /api/conversations/` : Création d'une conversation
- `GET /api/conversations/{id}` : Détails d'une conversation
- `POST /api/conversations/chat` : Traitement d'une requête de chat
- `GET /api/conversations/search/` : Recherche de conversations

#### LLMs

- `GET /api/llm/` : Liste des LLMs disponibles
- `PUT /api/llm/{name}` : Mise à jour de la configuration d'un LLM
- `GET /api/llm/usage` : Statistiques d'utilisation des LLMs

### Sécurité

#### Authentification JWT

L'authentification utilise des tokens JWT (JSON Web Tokens) avec les caractéristiques suivantes :

- Durée de validité : 24 heures par défaut
- Algorithme de signature : HS256
- Informations encodées : email, statut administrateur, expiration

#### Hachage des mots de passe

Les mots de passe sont hachés avec bcrypt, une fonction de hachage sécurisée avec sel intégré.

#### Isolation des données

Chaque client dispose d'un espace isolé dans MongoDB, garantissant la séparation stricte des données.

#### Exécution sécurisée de code

Le code personnalisé est exécuté dans un environnement restreint grâce à RestrictedPython, avec :

- Accès limité aux modules Python
- Isolation des variables globales
- Restrictions sur les opérations dangereuses

## Frontend (TypeScript/React)

### Structure et organisation

Le frontend est développé avec React et TypeScript, organisé selon une architecture modulaire :

- **src/App.tsx** : Composant principal et routage
- **src/api/** : Clients API pour communiquer avec le backend
- **src/components/** : Composants réutilisables
- **src/contexts/** : Contextes React (authentification, thème)
- **src/hooks/** : Hooks personnalisés
- **src/pages/** : Pages de l'application
- **src/styles/** : Styles globaux et thème
- **src/types/** : Types TypeScript
- **src/utils/** : Fonctions utilitaires

### Gestion d'état

La gestion d'état utilise plusieurs approches complémentaires :

- **Contextes React** : Pour l'état global (authentification, thème)
- **React Query** : Pour la gestion des données serveur (cache, invalidation)
- **État local** : Pour l'état spécifique aux composants

### Interface utilisateur

L'interface utilisateur est construite avec Material-UI, offrant :

- Design responsive pour tous les appareils
- Thème personnalisable
- Composants accessibles
- Mode sombre/clair

### Visualisation des données

Les données sont visualisées avec Recharts, permettant de créer :

- Graphiques d'utilisation des LLMs
- Statistiques de conversations
- Évolution des métriques dans le temps

## Widgets d'intégration

### Plugin WordPress

Le plugin WordPress est généré dynamiquement pour chaque client, avec :

- Fichier PHP principal avec les métadonnées du plugin
- Interface d'administration pour la configuration
- Chargement automatique des ressources JS/CSS
- Intégration du chatbot sur toutes les pages

### Snippet HTML générique

Pour les plateformes autres que WordPress, un snippet HTML est généré :

- Code JavaScript auto-exécutable
- Chargement asynchrone des ressources
- Configuration intégrée
- Compatible avec tous les sites web modernes

### Widget JavaScript

Le widget JavaScript est responsable de :

- Affichage de l'interface utilisateur du chatbot
- Communication avec le backend via API
- Gestion de l'historique de conversation local
- Personnalisation visuelle selon la configuration

## Base de données

### MongoDB

MongoDB est utilisé comme base de données principale, avec les collections suivantes :

- **users** : Utilisateurs administrateurs
- **clients** : Informations sur les clients
- **chatbots** : Configuration des chatbots
- **conversations** : Historique des conversations
- **llm_usage** : Statistiques d'utilisation des LLMs

### Indexation

Des index sont créés pour optimiser les requêtes fréquentes :

- Index unique sur `client_id` dans la collection `clients`
- Index sur `client_id` dans la collection `chatbots`
- Index composé sur `client_id` et `timestamp` dans la collection `conversations`
- Index sur `session_id` dans la collection `conversations`
- Index unique sur `email` dans la collection `users`
- Index composé sur `client_id` et `date` dans la collection `llm_usage`

## Intégration LLM

### Fournisseurs supportés

La plateforme supporte plusieurs fournisseurs de LLM :

- **OpenAI** : GPT-4, GPT-3.5-Turbo
- **Anthropic** : Claude 3
- **Ollama** : Modèles open-source locaux (Llama 3)

### Gestion des quotas

Le système gère automatiquement les quotas d'utilisation :

- Suivi de l'utilisation par client et par mois
- Basculement automatique vers un LLM de secours en cas de dépassement
- Alertes par email aux administrateurs

### Personnalisation des réponses

Les réponses peuvent être personnalisées via :

- Instructions spécifiques pour orienter le comportement du LLM
- Code Python personnalisé pour enrichir les réponses avec des données externes
- Ajustement de la température pour contrôler la créativité

## Déploiement

### GitHub Actions

Le déploiement est automatisé via GitHub Actions :

- Déclenchement automatique à chaque push sur la branche main
- Tests automatiques avant déploiement
- Déploiement sur EC2 via SSH
- Configuration automatique de Nginx

### Infrastructure AWS

L'application est déployée sur AWS EC2 :

- Instance Ubuntu 22.04
- Nginx comme serveur web et proxy inverse
- Certificats SSL via Let's Encrypt
- Service systemd pour le backend FastAPI

## Performances et scalabilité

### Optimisations

Plusieurs optimisations sont mises en place :

- Mise en cache des réponses API avec React Query
- Indexation MongoDB pour les requêtes fréquentes
- Chargement asynchrone des ressources du widget
- Pagination des résultats pour les grandes collections

### Scalabilité

L'architecture permet une scalabilité horizontale :

- Backend stateless facilitant la réplication
- MongoDB supportant le sharding
- Séparation claire frontend/backend

## Sécurité

### HTTPS

Toutes les communications sont sécurisées via HTTPS :

- Certificats SSL/TLS via Let's Encrypt
- Renouvellement automatique des certificats
- HSTS pour forcer les connexions sécurisées

### Protection contre les attaques courantes

Des mesures sont en place contre les attaques courantes :

- Protection CSRF via tokens
- Protection XSS via échappement des données
- Rate limiting pour prévenir les attaques par force brute
- Validation des entrées côté serveur

## Maintenance et monitoring

### Logs

Les logs sont centralisés et structurés :

- Logs d'application via le logger Python
- Logs d'accès Nginx
- Logs systemd pour le service backend

### Alertes

Des alertes sont configurées pour :

- Dépassement de quota
- Erreurs serveur répétées
- Problèmes d'authentification
- Indisponibilité du service

## Évolutions futures

### Fonctionnalités planifiées

Plusieurs évolutions sont envisagées :

- Support de modèles multimodaux (texte + images)
- Intégration avec des bases de connaissances externes
- Analyse de sentiment des conversations
- Interface d'administration mobile
- Support multi-langues pour l'interface d'administration
- Intégration avec des plateformes CRM
