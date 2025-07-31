# --- Interface / Classe Abstraite pour la Stratégie de Validation ---

from Factory_Method import EvenementFactory
from abc import ABC, abstractmethod

class IRegleValidation(ABC):

    @abstractmethod
    def valider(self, inscription):
        pass

# --- Stratégies Concrètes de Validation ---
class RegleValidationHackathon(IRegleValidation):
    def valider(self, inscription):
        print(f"Validation spécifique Hackathon pour {inscription.participant.nom}...")
        # Simuler une logique de validation complexe (ex: vérification manuelle)
        est_valide = inscription.participant.est_etudiant and inscription.evenement.nom == "Hackathon Cybersécurité"
        return est_valide 

class RegleValidationConference(IRegleValidation):
    def valider(self, inscription):
        print(f"Validation spécifique Conférence pour {inscription.participant.nom}...")
        return inscription.evenement.nombre_places > 0 

class RegleValidationGenerale(IRegleValidation):
    def valider(self, inscription):
        print(f"Validation générale pour {inscription.participant.nom}...")
        return True 

# --- Contexte : La classe Inscription ---
class Participant:
    def __init__(self, nom, email, est_etudiant=True):
        self.nom = nom
        self.email = email
        self.est_etudiant = est_etudiant

class Inscription:
    def __init__(self, participant, evenement, regle_validation: IRegleValidation):
        self.participant = participant
        self.evenement = evenement
        self.regle_validation = regle_validation
        self.est_validee = False

    def valider(self):
        self.est_validee = self.regle_validation.valider(self)
        print(f"Inscription de {self.participant.nom} pour '{self.evenement.nom}' est {'validée' if self.est_validee else 'en attente/refusée'}.")
        return self.est_validee

    def set_regle_validation(self, regle_validation: IRegleValidation):
        self.regle_validation = regle_validation

# --- Exemple d'utilisation ---
if __name__ == "__main__":
    from datetime import date

    factory = EvenementFactory()
    conf_ai = factory.creer_evenement("Conference", "Conférence IA", "IA et avenir", date(2025, 9, 15),
                                       nombre_places=150, speaker_principal="Dr. AI")
    hack_cyber = factory.creer_evenement("Hackathon", "Hackathon Cybersécurité", "Défi de sécurité", date(2025, 10, 20),
                                         sponsor="SecurCo", duree_heures=24)
    sem_info = factory.creer_evenement("Seminaire", "Séminaire Info", "Introduction", date(2025, 11, 5),
                                      domaine="Informatique")

    # Participants
    alice = Participant("Alice Dubois", "alice@example.com", est_etudiant=True)
    bob = Participant("Bob Martin", "bob@example.com", est_etudiant=False)

    # Inscription de Alice au Hackathon avec la règle spécifique
    inscription_alice_hack = Inscription(alice, hack_cyber, RegleValidationHackathon())
    inscription_alice_hack.valider()

   
    inscription_bob_conf = Inscription(bob, conf_ai, RegleValidationConference())
    inscription_bob_conf.valider()

    
    inscription_alice_sem = Inscription(alice, sem_info, RegleValidationGenerale())
    inscription_alice_sem.valider()

    print("\n--- Changement de stratégie ---")
    conf_ai.nombre_places = 0 
    inscription_bob_conf.set_regle_validation(RegleValidationConference()) 
    inscription_bob_conf.valider() 