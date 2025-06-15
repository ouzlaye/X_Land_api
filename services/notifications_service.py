def envoyer_notification_banque(contactBanque: str, titre: dict):
    """
    Simule l'envoi d'une notification à la banque en cas de changement de statut du titre foncier.
    """
    message = f"⚠️ [ALERTE FONCIÈRE] Le titre {titre['numeroTitre']} ({titre['situation']}) a changé de statut : {titre['statut']}."
    print(f"📩 Notification envoyée à {contactBanque}: {message}")  # Simulé, remplacé par un vrai email/webhook plus tard
