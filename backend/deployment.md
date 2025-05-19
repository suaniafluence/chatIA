# Instructions de déploiement - IAfluence

Ce document détaille les étapes nécessaires pour déployer l'application IAfluence sur un serveur EC2 Ubuntu via GitHub Actions.

## Prérequis

- Un compte AWS avec accès à EC2
- Un compte GitHub avec le dépôt https://github.com/suaniafluence/chatIA.git
- Un nom de domaine (optionnel mais recommandé)
- Un compte MongoDB Atlas (ou un serveur MongoDB)

## Configuration de l'environnement

### 1. Configuration de MongoDB Atlas

1. Créez un compte sur [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) si vous n'en avez pas déjà un
2. Créez un nouveau cluster (l'option gratuite est suffisante pour commencer)
3. Configurez l'accès réseau pour autoriser les connexions depuis n'importe où (0.0.0.0/0) ou depuis l'adresse IP de votre serveur EC2
4. Créez un utilisateur de base de données avec les droits de lecture/écriture
5. Notez l'URI de connexion, qui sera de la forme : `mongodb+srv://<username>:<password>@<cluster>.mongodb.net/iafluence`

### 2. Configuration de l'instance EC2

1. Connectez-vous à la console AWS et accédez au service EC2
2. Lancez une nouvelle instance avec les caractéristiques suivantes :
   - Ubuntu Server 22.04 LTS
   - Type d'instance : t2.micro (pour commencer, à ajuster selon les besoins)
   - Stockage : 20 Go minimum
   - Groupe de sécurité : ouvrir les ports 22 (SSH), 80 (HTTP), 443 (HTTPS)
3. Créez ou utilisez une paire de clés existante pour vous connecter à l'instance
4. Connectez-vous à l'instance via SSH :
   ```
   ssh -i votre-cle.pem ubuntu@votre-ip-ec2
   ```
5. Mettez à jour le système :
   ```
   sudo apt update && sudo apt upgrade -y
   ```
6. Installez les dépendances nécessaires :
   ```
   sudo apt install -y python3-pip python3-venv nodejs npm nginx certbot python3-certbot-nginx
   ```
7. Installez Docker (optionnel, si vous préférez déployer avec Docker) :
   ```
   sudo apt install -y docker.io docker-compose
   sudo systemctl enable docker
   sudo systemctl start docker
   sudo usermod -aG docker ubuntu
   ```

### 3. Configuration des secrets GitHub

1. Dans votre dépôt GitHub, accédez à Settings > Secrets and variables > Actions
2. Ajoutez les secrets suivants :
   - `AWS_SSH_KEY` : contenu de votre clé privée SSH pour accéder à l'instance EC2
   - `EC2_HOST` : adresse IP publique de votre instance EC2
   - `EC2_USERNAME` : nom d'utilisateur pour la connexion SSH (généralement "ubuntu")
   - `MONGODB_URL` : URI de connexion MongoDB Atlas
   - `SECRET_KEY` : clé secrète pour l'application (générez une chaîne aléatoire)
   - `OPENAI_API_KEY` : votre clé API OpenAI (si vous utilisez GPT)
   - `ANTHROPIC_API_KEY` : votre clé API Anthropic (si vous utilisez Claude)
   - `ADMIN_USERNAME` : nom d'utilisateur admin (par défaut : suan.tay@iafluence.fr)
   - `ADMIN_PASSWORD` : mot de passe admin (par défaut : motdepassefort)

## Déploiement

### Option 1 : Déploiement automatique via GitHub Actions

Le workflow GitHub Actions est déjà configuré dans le dépôt. À chaque push sur la branche main, le déploiement sera automatiquement déclenché.

1. Clonez le dépôt localement :
   ```
   git clone https://github.com/suaniafluence/chatIA.git
   cd chatIA
   ```

2. Vérifiez que le fichier `.github/workflows/deploy.yml` est présent et correctement configuré

3. Effectuez un push sur la branche main pour déclencher le déploiement :
   ```
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

4. Suivez l'avancement du déploiement dans l'onglet "Actions" de votre dépôt GitHub

### Option 2 : Déploiement manuel

Si vous préférez déployer manuellement, suivez ces étapes :

1. Clonez le dépôt sur votre serveur EC2 :
   ```
   git clone https://github.com/suaniafluence/chatIA.git
   cd chatIA
   ```

2. Créez un fichier `.env` à la racine du projet backend :
   ```
   cd backend
   cp .env.example .env
   nano .env
   ```

3. Remplissez les variables d'environnement dans le fichier `.env` :
   ```
   DEBUG=False
   SECRET_KEY=votre_cle_secrete
   MONGODB_URL=votre_uri_mongodb
   MONGODB_DB_NAME=iafluence
   OPENAI_API_KEY=votre_cle_api_openai
   ANTHROPIC_API_KEY=votre_cle_api_anthropic
   OLLAMA_API_URL=http://localhost:11434
   ADMIN_USERNAME=suan.tay@iafluence.fr
   ADMIN_PASSWORD=motdepassefort
   ```

4. Installez les dépendances backend :
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. Installez les dépendances frontend :
   ```
   cd ../frontend
   npm install
   ```

6. Construisez le frontend :
   ```
   npm run build
   ```

7. Configurez Nginx :
   ```
   sudo nano /etc/nginx/sites-available/iafluence
   ```

8. Ajoutez la configuration suivante :
   ```
   server {
       listen 80;
       server_name votre-domaine.com;  # Remplacez par votre domaine ou IP

       location / {
           root /home/ubuntu/chatIA/frontend/build;
           try_files $uri /index.html;
       }

       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /docs {
           proxy_pass http://localhost:8000/docs;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /widgets {
           alias /home/ubuntu/chatIA/widgets;
       }
   }
   ```

9. Activez la configuration Nginx :
   ```
   sudo ln -s /etc/nginx/sites-available/iafluence /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

10. Configurez SSL avec Certbot (si vous avez un domaine) :
    ```
    sudo certbot --nginx -d votre-domaine.com
    ```

11. Créez un service systemd pour le backend :
    ```
    sudo nano /etc/systemd/system/iafluence.service
    ```

12. Ajoutez la configuration suivante :
    ```
    [Unit]
    Description=IAfluence FastAPI Backend
    After=network.target

    [Service]
    User=ubuntu
    Group=ubuntu
    WorkingDirectory=/home/ubuntu/chatIA/backend
    Environment="PATH=/home/ubuntu/chatIA/backend/venv/bin"
    EnvironmentFile=/home/ubuntu/chatIA/backend/.env
    ExecStart=/home/ubuntu/chatIA/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

    [Install]
    WantedBy=multi-user.target
    ```

13. Activez et démarrez le service :
    ```
    sudo systemctl enable iafluence
    sudo systemctl start iafluence
    ```

## Vérification du déploiement

1. Vérifiez que le backend fonctionne :
   ```
   curl http://localhost:8000/health
   ```
   Vous devriez obtenir : `{"status":"ok"}`

2. Accédez à l'interface d'administration via votre navigateur :
   ```
   http://votre-domaine.com/admin
   ```
   ou
   ```
   http://votre-ip-ec2/admin
   ```

3. Connectez-vous avec les identifiants administrateur configurés

## Mise à jour de l'application

### Via GitHub Actions

Pour mettre à jour l'application, il suffit de pousser les modifications sur la branche main du dépôt GitHub. Le workflow de déploiement s'exécutera automatiquement.

### Mise à jour manuelle

1. Connectez-vous à votre serveur EC2
2. Accédez au répertoire du projet :
   ```
   cd ~/chatIA
   ```
3. Tirez les dernières modifications :
   ```
   git pull origin main
   ```
4. Mettez à jour les dépendances backend :
   ```
   cd backend
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. Mettez à jour les dépendances frontend et reconstruisez :
   ```
   cd ../frontend
   npm install
   npm run build
   ```
6. Redémarrez le service backend :
   ```
   sudo systemctl restart iafluence
   ```

## Dépannage

### Le backend ne démarre pas

Vérifiez les logs du service :
```
sudo journalctl -u iafluence -f
```

### Problèmes de connexion à MongoDB

Vérifiez que l'URI de connexion est correct et que l'adresse IP de votre serveur est autorisée dans les paramètres de sécurité de MongoDB Atlas.

### Problèmes avec Nginx

Vérifiez la configuration Nginx :
```
sudo nginx -t
```

Consultez les logs Nginx :
```
sudo tail -f /var/log/nginx/error.log
```

### Problèmes avec GitHub Actions

Vérifiez les logs d'exécution dans l'onglet Actions de votre dépôt GitHub pour identifier les erreurs potentielles.
