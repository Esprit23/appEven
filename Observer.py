# --- Interfaces Sujet et Observateur ---
from abc import ABC, abstractmethod
from Factory_Method import EvenementFactory

class ISubject(ABC):
    
    @abstractmethod
    def ajouter_observateur(self, observateur):
        pass

    @abstractmethod
    def retirer_observateur(self, observateur):
        pass

    @abstractmethod
    def notifier_observateurs(self):
        pass

class IObserver(ABC):
    
    @abstractmethod
    def mettre_a_jour(self, sujet):
        pass



class Evenement(ABC):

    def __init__(self, nom, description, date):
        self.nom = nom
        self.description = description
        self.date = date
        self._observateurs = []

    def ajouter_observateur(self, observateur: IObserver):
        self._observateurs.append(observateur)

    def retirer_observateur(self, observateur: IObserver):
        self._observateurs.remove(observateur)

    def notifier_observateurs(self):
        for obs in self._observateurs:
            obs.mettre_a_jour(self)

    @abstractmethod
    def get_details(self):
        pass

    def mettre_a_jour_evenement(self, nouvelle_description):
        self.description = nouvelle_description
        print(f"\nÉvénement '{self.nom}' mis à jour. Notification des observateurs...")
        self.notifier_observateurs()

class Inscription: 
   
    def __init__(self, participant, evenement, regle_validation):
        self.participant = participant
        self.evenement = evenement
        self.regle_validation = regle_validation
        self.est_validee = False
        self._observateurs = []

    def ajouter_observateur(self, observateur: IObserver):
        self._observateurs.append(observateur)

    def retirer_observateur(self, observateur: IObserver):
        self._observateurs.remove(observateur)

    def notifier_observateurs(self):
        for obs in self._observateurs:
            obs.mettre_a_jour(self)

    def valider(self):
        
        ancienne_validation = self.est_validee
        self.est_validee = self.regle_validation.valider(self)
        if self.est_validee != ancienne_validation:
            print(f"Statut d'inscription de {self.participant.nom} changé. Notification des observateurs...")
            self.notifier_observateurs()
        return self.est_validee

# --- Observateurs (qui réagissent aux changements) ---
class NotificationService(IObserver):
   
    def mettre_a_jour(self, sujet):
        if isinstance(sujet, Evenement):
            print(f"[NotificationService] Événement '{sujet.nom}' a été mis à jour: {sujet.description}")
            self.envoyer_email(f"Mise à jour de l'événement: {sujet.nom}", f"Le sujet '{sujet.nom}' a été mis à jour.")
        elif isinstance(sujet, Inscription):
            statut = "validée" if sujet.est_validee else "en attente"
            print(f"[NotificationService] Inscription de '{sujet.participant.nom}' pour '{sujet.evenement.nom}' est maintenant {statut}.")
            self.envoyer_sms(sujet.participant.email, f"Votre inscription à {sujet.evenement.nom} est {statut}.")
        else:
            print(f"[NotificationService] Un sujet inconnu a été mis à jour.")

    def envoyer_email(self, sujet, message):
        print(f"  --> EMAIL envoyé: Sujet='{sujet}', Message='{message}'")

    def envoyer_sms(self, destinataire, message):
        print(f"  --> SMS envoyé à {destinataire}: '{message}'")



# --- Exemple d'utilisation ---
if __name__ == "__main__":
    from datetime import date
    # Initialisation
    factory = EvenementFactory()
    notification_service = NotificationService()

   
    conf_dev = factory.creer_evenement("Conference", "Conférence Dev", "Les bases du développement", date(2025, 8, 1),
                                      nombre_places=100, speaker_principal="M. Codeur")
    conf_dev.ajouter_observateur(notification_service)

    # Création d'un participant
    chloe = Participant("Chloé Durand", "chloe@example.com")

   
    inscription_chloe_dev = Inscription(chloe, conf_dev, RegleValidationConference())
    inscription_chloe_dev.ajouter_observateur(notification_service)

    # Simuler des actions
    print("\n--- Scénario 1: Mise à jour de l'événement ---")
    conf_dev.mettre_a_jour_evenement("Les bases du développement web et mobile")

    print("\n--- Scénario 2: Validation de l'inscription ---")
    inscription_chloe_dev.valider() # Cette action devrait notifier

    print("\n--- Scénario 3: Changement d'état sans notification ---")
    # Si la validation ne change pas l'état, pas de notification
    conf_dev.description = "Nouvelle description interne"
    print(f"Description mise à jour en interne: {conf_dev.description}")