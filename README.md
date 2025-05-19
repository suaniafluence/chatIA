# Architecture Globale - IAfluence

## Structure des dossiers et fichiers

```
iafluence/
│
├── backend/                      # Backend FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # Point d'entrée de l'application FastAPI
│   │   ├── config.py             # Configuration de l'application
│   │   ├── auth/                 # Gestion de l'authentification
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py   # Dépendances pour l'authentification
│   │   │   ├── models.py         # Modèles pour l'authentification
│   │   │   └── router.py         # Routes pour l'authentification
│   │   ├── clients/              # Gestion des clients
│   │   │   ├── __init__.py
│   │   │   ├── models.py         # Modèles pour les clients
│   │   │   ├── router.py         # Routes pour les clients
│   │   │   └── service.py        # Services pour les clients
│   │   ├── chatbots/             # Gestion des chatbots
│   │   │   ├── __init__.py
│   │   │   ├── models.py         # Modèles pour les chatbots
│   │   │   ├── router.py         # Routes pour les chatbots
│   │   │   └── service.py        # Services pour les chatbots
│   │   ├── conversations/        # Gestion des conversations
│   │   │   ├── __init__.py
│   │   │   ├── models.py         # Modèles pour les conversations
│   │   │   ├── router.py         # Routes pour les conversations
│   │   │   └── service.py        # Services pour les conversations
│   │   ├── llm/                  # Gestion des LLMs
│   │   │   ├── __init__.py
│   │   │   ├── models.py         # Modèles pour les LLMs
│   │   │   ├── router.py         # Routes pour les LLMs
│   │   │   └── service.py        # Services pour les LLMs
│   │   ├── sandbox/              # Environnement sécurisé pour l'exécution de code
│   │   │   ├── __init__.py
│   │   │   └── executor.py       # Exécuteur de code sécurisé
│   │   ├── utils/                # Utilitaires
│   │   │   ├── __init__.py
│   │   │   ├── db.py             # Utilitaires pour la base de données
│   │   │   ├── email.py          # Utilitaires pour l'envoi d'emails
│   │   │   └── security.py       # Utilitaires pour la sécurité
│   │   └── widgets/              # Gestion des widgets
│   │       ├── __init__.py
│   │       ├── models.py         # Modèles pour les widgets
│   │       ├── router.py         # Routes pour les widgets
│   │       ├── service.py        # Services pour les widgets
│   │       └── templates/        # Templates pour les widgets
│   │           ├── wordpress.php # Template pour WordPress
│   │           └── generic.html  # Template générique
│   ├── tests/                    # Tests unitaires et d'intégration
│   │   ├── __init__.py
│   │   ├── conftest.py           # Configuration des tests
│   │   ├── test_auth.py          # Tests pour l'authentification
│   │   ├── test_clients.py       # Tests pour les clients
│   │   ├── test_chatbots.py      # Tests pour les chatbots
│   │   └── test_conversations.py # Tests pour les conversations
│   ├── .env.example              # Exemple de fichier d'environnement
│   ├── Dockerfile                # Dockerfile pour le backend
│   ├── requirements.txt          # Dépendances Python
│   └── README.md                 # Documentation du backend
│
├── frontend/                     # Frontend TypeScript
│   ├── public/                   # Fichiers statiques
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   └── assets/
│   │       └── images/
│   ├── src/
│   │   ├── App.tsx               # Composant principal
│   │   ├── index.tsx             # Point d'entrée
│   │   ├── api/                  # Appels API
│   │   │   ├── index.ts
│   │   │   ├── auth.ts           # API pour l'authentification
│   │   │   ├── clients.ts        # API pour les clients
│   │   │   ├── chatbots.ts       # API pour les chatbots
│   │   │   └── conversations.ts  # API pour les conversations
│   │   ├── components/           # Composants réutilisables
│   │   │   ├── common/           # Composants communs
│   │   │   ├── auth/             # Composants pour l'authentification
│   │   │   ├── clients/          # Composants pour les clients
│   │   │   ├── chatbots/         # Composants pour les chatbots
│   │   │   ├── conversations/    # Composants pour les conversations
│   │   │   └── dashboard/        # Composants pour le dashboard
│   │   ├── contexts/             # Contextes React
│   │   │   ├── AuthContext.tsx   # Contexte pour l'authentification
│   │   │   └── ThemeContext.tsx  # Contexte pour le thème
│   │   ├── hooks/                # Hooks personnalisés
│   │   │   ├── useAuth.ts        # Hook pour l'authentification
│   │   │   └── useApi.ts         # Hook pour les appels API
│   │   ├── pages/                # Pages de l'application
│   │   │   ├── Login.tsx         # Page de connexion
│   │   │   ├── Dashboard.tsx     # Page de tableau de bord
│   │   │   ├── Clients/          # Pages pour les clients
│   │   │   ├── Chatbots/         # Pages pour les chatbots
│   │   │   └── Conversations/    # Pages pour les conversations
│   │   ├── styles/               # Styles
│   │   │   ├── global.css        # Styles globaux
│   │   │   └── theme.ts          # Thème de l'application
│   │   ├── types/                # Types TypeScript
│   │   │   ├── auth.ts           # Types pour l'authentification
│   │   │   ├── client.ts         # Types pour les clients
│   │   │   ├── chatbot.ts        # Types pour les chatbots
│   │   │   └── conversation.ts   # Types pour les conversations
│   │   └── utils/                # Utilitaires
│   │       ├── format.ts         # Formatage de données
│   │       └── validation.ts     # Validation de formulaires
│   ├── .env.example              # Exemple de fichier d'environnement
│   ├── Dockerfile                # Dockerfile pour le frontend
│   ├── package.json              # Dépendances Node.js
│   ├── tsconfig.json             # Configuration TypeScript
│   └── README.md                 # Documentation du frontend
│
├── widgets/                      # Widgets pour les clients
│   ├── js/
│   │   ├── chatbot-widget.js     # Script JS du widget
│   │   └── chatbot-widget.min.js # Version minifiée
│   ├── css/
│   │   ├── chatbot-widget.css    # Styles du widget
│   │   └── chatbot-widget.min.css # Version minifiée
│   └── templates/
│       ├── wordpress/            # Templates pour WordPress
│       │   └── xxx-widget.php    # Template de plugin WordPress
│       └── generic/              # Templates génériques
│           └── snippet.html      # Snippet HTML générique
│
├── .github/                      # Configuration GitHub
│   └── workflows/
│       ├── backend-ci.yml        # CI pour le backend
│       ├── frontend-ci.yml       # CI pour le frontend
│       └── deploy.yml            # Déploiement sur EC2
│
├── docker-compose.yml            # Configuration Docker Compose
├── .gitignore                    # Fichiers à ignorer par Git
└── README.md                     # Documentation principale
```

## Choix technologiques

### Backend

1. **FastAPI** : Framework Python moderne, rapide et asynchrone
   - Performances élevées grâce à Starlette et Pydantic
   - Documentation automatique avec Swagger UI
   - Validation des données intégrée
   - Support natif des opérations asynchrones

2. **MongoDB** : Base de données NoSQL orientée documents
   - Flexibilité du schéma pour l'évolution des données
   - Performances élevées pour les opérations de lecture/écriture
   - Scalabilité horizontale
   - Support natif du format JSON
   - MongoDB Atlas pour le cloud

3. **PyMongo** : Driver MongoDB officiel pour Python
   - Support complet des fonctionnalités MongoDB
   - Intégration avec FastAPI via motor (client asynchrone)

4. **JWT** : JSON Web Tokens pour l'authentification
   - Stateless, idéal pour les API RESTful
   - Sécurité et extensibilité

5. **RestrictedPython** : Pour l'exécution sécurisée de code
   - Sandbox pour l'exécution de code Python personnalisé
   - Restrictions configurables pour la sécurité

6. **Jinja2** : Moteur de templates
   - Génération dynamique des widgets et plugins
   - Flexibilité et puissance pour les templates complexes

### Frontend

1. **TypeScript** : Superset typé de JavaScript
   - Typage statique pour réduire les erreurs
   - Meilleure autocomplétion et refactoring
   - Documentation intégrée via les types

2. **React** : Bibliothèque UI pour construire des interfaces
   - Composants réutilisables
   - Virtual DOM pour des performances optimales
   - Large écosystème et communauté

3. **React Router** : Routage côté client
   - Navigation fluide entre les pages
   - Gestion des paramètres d'URL

4. **Axios** : Client HTTP
   - Promesses pour les requêtes asynchrones
   - Intercepteurs pour la gestion globale des requêtes/réponses
   - Annulation des requêtes

5. **Material-UI** : Bibliothèque de composants React
   - Design moderne et responsive
   - Personnalisation via le système de thèmes
   - Composants accessibles

6. **React Query** : Gestion des états serveur
   - Mise en cache et invalidation automatiques
   - Gestion des erreurs et des retries
   - Pagination et infinite scrolling

7. **Recharts** : Bibliothèque de graphiques pour React
   - Visualisation des données du dashboard
   - Composants responsives et personnalisables

### Déploiement

1. **Docker** : Conteneurisation
   - Isolation des environnements
   - Reproductibilité des déploiements
   - Scaling horizontal facilité

2. **GitHub Actions** : CI/CD
   - Intégration native avec GitHub
   - Automatisation des tests et du déploiement
   - Configuration flexible via YAML

3. **AWS EC2** : Serveur cloud
   - Scalabilité à la demande
   - Haute disponibilité
   - Intégration avec d'autres services AWS

4. **Nginx** : Serveur web et proxy inverse
   - Haute performance
   - Gestion du SSL/TLS
   - Load balancing
   - Mise en cache

5. **Certbot** : Gestion automatique des certificats SSL
   - Certificats Let's Encrypt gratuits
   - Renouvellement automatique

## Dépendances principales

### Backend (Python)

```
fastapi>=0.95.0
uvicorn>=0.22.0
motor>=3.1.1
pymongo>=4.3.3
python-jose>=3.3.0
passlib>=1.7.4
python-multipart>=0.0.6
pydantic>=2.0.0
jinja2>=3.1.2
aiofiles>=23.1.0
python-dotenv>=1.0.0
httpx>=0.24.0
restrictedpython>=6.0
pytest>=7.3.1
pytest-asyncio>=0.21.0
```

### Frontend (TypeScript/Node.js)

```json
{
  "dependencies": {
    "@emotion/react": "^11.11.0",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.11.16",
    "@mui/material": "^5.13.0",
    "@tanstack/react-query": "^4.29.5",
    "axios": "^1.4.0",
    "date-fns": "^2.30.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-hook-form": "^7.43.9",
    "react-router-dom": "^6.11.1",
    "recharts": "^2.6.2",
    "zod": "^3.21.4"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/react": "^14.0.0",
    "@testing-library/user-event": "^14.4.3",
    "@types/node": "^20.1.3",
    "@types/react": "^18.2.6",
    "@types/react-dom": "^18.2.4",
    "@typescript-eslint/eslint-plugin": "^5.59.5",
    "@typescript-eslint/parser": "^5.59.5",
    "eslint": "^8.40.0",
    "eslint-plugin-react": "^7.32.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "typescript": "^5.0.4",
    "vite": "^4.3.5",
    "vitest": "^0.31.0"
  }
}
```

## Flux de données et interactions

1. **Intégration du widget**
   - Le client intègre le widget généré sur son site
   - Le widget charge le script JS depuis le serveur IAfluence
   - Le script initialise le chatbot avec l'ID client

2. **Conversation utilisateur-chatbot**
   - L'utilisateur envoie une question via le widget
   - Le widget transmet la question au backend via API
   - Le backend traite la question avec le LLM approprié
   - La réponse est renvoyée au widget et affichée à l'utilisateur
   - La conversation est historisée dans MongoDB

3. **Administration**
   - L'admin se connecte à l'interface d'administration
   - Il peut consulter les clients, chatbots et conversations
   - Il peut configurer les chatbots (style, comportement, etc.)
   - Il peut analyser les statistiques d'utilisation
   - Il peut exporter les données

4. **Gestion des LLMs**
   - Le système utilise le LLM configuré par défaut
   - Si le quota est dépassé, bascule automatique vers un LLM alternatif
   - Notification à l'admin en cas de basculement
   - Suivi des coûts et de l'utilisation

## Sécurité

1. **Authentification**
   - JWT pour l'API backend
   - Sessions sécurisées pour l'interface admin
   - Stockage sécurisé des mots de passe (hachage + sel)

2. **Isolation des données**
   - Séparation stricte des données par client dans MongoDB
   - Validation des accès à chaque requête

3. **Exécution sécurisée de code**
   - Sandbox pour l'exécution du code personnalisé
   - Limitations des ressources et des accès
   - Validation et nettoyage des entrées/sorties

4. **Communication**
   - HTTPS obligatoire
   - En-têtes de sécurité (CORS, CSP, etc.)
   - Protection contre les attaques courantes (XSS, CSRF, etc.)

## Scalabilité

1. **Architecture modulaire**
   - Séparation claire des responsabilités
   - Facilité d'ajout de nouvelles fonctionnalités

2. **Conteneurisation**
   - Déploiement facile de nouvelles instances
   - Scaling horizontal automatique possible

3. **Base de données**
   - MongoDB supporte le sharding pour la scalabilité horizontale
   - Indexation optimisée pour les requêtes fréquentes

4. **Mise en cache**
   - Cache Redis pour les données fréquemment accédées
   - Réduction de la charge sur la base de données et les LLMs
