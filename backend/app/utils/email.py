"""
Utilitaires pour l'envoi d'emails
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from app.clients.models import Client

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_email(to: str, subject: str, body: str, html_body: str = None) -> bool:
    """
    Envoie un email
    
    Args:
        to: Destinataire
        subject: Sujet
        body: Corps du message (texte)
        html_body: Corps du message (HTML, optionnel)
        
    Returns:
        True si l'email a été envoyé avec succès, False sinon
    """
    # Vérification des paramètres SMTP
    if not all([settings.SMTP_SERVER, settings.SMTP_PORT, settings.SMTP_USERNAME, settings.SMTP_PASSWORD, settings.EMAIL_FROM]):
        logger.warning("Paramètres SMTP incomplets, impossible d'envoyer l'email")
        return False
    
    try:
        # Création du message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = to
        
        # Ajout du corps du message (texte)
        part1 = MIMEText(body, 'plain')
        msg.attach(part1)
        
        # Ajout du corps du message (HTML, si fourni)
        if html_body:
            part2 = MIMEText(html_body, 'html')
            msg.attach(part2)
        
        # Connexion au serveur SMTP
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        
        # Envoi de l'email
        server.sendmail(settings.EMAIL_FROM, to, msg.as_string())
        server.quit()
        
        logger.info(f"Email envoyé à {to}")
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email: {str(e)}")
        return False

async def send_quota_alert_email(client: Client) -> bool:
    """
    Envoie un email d'alerte lorsque le quota d'un client est dépassé
    
    Args:
        client: Client dont le quota est dépassé
        
    Returns:
        True si l'email a été envoyé avec succès, False sinon
    """
    subject = f"[IAfluence] Alerte quota dépassé - {client.name}"
    
    body = f"""
Bonjour,

Le quota mensuel de requêtes LLM pour le client {client.name} (ID: {client.client_id}) a été dépassé.

Quota mensuel: {client.monthly_quota} requêtes
    
Le système a automatiquement basculé vers le LLM de secours pour assurer la continuité du service.

Pour augmenter le quota ou discuter des options disponibles, veuillez contacter le client.

Cordialement,
L'équipe IAfluence
"""
    
    html_body = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4f46e5; color: white; padding: 10px 20px; border-radius: 5px 5px 0 0; }}
        .content {{ padding: 20px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 5px 5px; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #777; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Alerte quota dépassé</h2>
        </div>
        <div class="content">
            <p>Bonjour,</p>
            <p>Le quota mensuel de requêtes LLM pour le client <strong>{client.name}</strong> (ID: <code>{client.client_id}</code>) a été dépassé.</p>
            <p><strong>Quota mensuel:</strong> {client.monthly_quota} requêtes</p>
            <p>Le système a automatiquement basculé vers le LLM de secours pour assurer la continuité du service.</p>
            <p>Pour augmenter le quota ou discuter des options disponibles, veuillez contacter le client.</p>
            <p>Cordialement,<br>L'équipe IAfluence</p>
        </div>
        <div class="footer">
            <p>Cet email a été envoyé automatiquement par le système IAfluence. Merci de ne pas y répondre.</p>
        </div>
    </div>
</body>
</html>
"""
    
    return await send_email(settings.ADMIN_EMAIL, subject, body, html_body)
