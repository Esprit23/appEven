# --- Interface Sujet ---
from abc import ABC, abstractmethod

class IEvenementService(ABC):
    """Interface commune pour le service d'événement et le proxy."""
    @abstractmethod
    def get_details_evenement(self, evenement_id, utilisateur=None):
        """Retourne les détails d'un événement, potentiellement avec contrôle d'accès."""
        pass

# --- Sujet Réel ---
class EvenementServiceReel(IEvenementService):
    """Le service réel qui fournit les détails des événements."""
    def __init__(self, evenements_db):
        self._evenements_db = evenements_db 

    def get_details_evenement(self, evenement_id, utilisateur=None):
        print(f"  [Service Réel] Récupération des détails pour l'événement ID: {evenement_id}")
        # Simuler la récupération des détails complets
        evenement = self._evenements_db.get(evenement_id)
        if evenement:
            return evenement.get_details()
        return "Événement non trouvé."

# --- Proxy ---
class EvenementServiceProxy(IEvenementService):
    """Proxy pour contrôler l'accès au service d'événement réel."""
    def __init__(self, evenements_db, authentification_service):
        self._evenement_service_reel = EvenementServiceReel(evenements_db)
        self._authentification_service = authentification_service

    def get_details_evenement(self, evenement_id, utilisateur=None):
        print(f"[Proxy] Demande de détails pour l'événement ID: {evenement_id}")

        evenement = self._evenement_service_reel._evenements_db.get(evenement_id) 
        
        if evenement:
            if evenement.nom == "Conférence Secrète" and not self._authentification_service.est_connecte(utilisateur):
                print(f"[Proxy] Accès refusé: {evenement.nom} nécessite une connexion.")
                return "Veuillez vous connecter pour voir les détails de cet événement."
            
            if isinstance(evenement, Hackathon) and not self._authentification_service.est_inscrit(utilisateur, evenement_id):
                print(f"[Proxy] Accès refusé: {evenement.nom} est limité aux participants inscrits.")
                return "Vous devez être inscrit à cet hackathon pour voir les détails complets."
        else:
            return "Événement non trouvé." 

        print("[Proxy] Accès autorisé. Délégation au service réel.")
        return self._evenement_service_reel.get_details_evenement(evenement_id, utilisateur)

# --- Service d'Authentification  ---
class AuthentificationService:
    """Service simulé pour la gestion de l'authentification et des inscriptions."""
    def __init__(self):
        self.utilisateurs_connectes = set() 
        self.inscriptions = {}

    def connecter_utilisateur(self, utilisateur_id):
        self.utilisateurs_connectes.add(utilisateur_id)
        print(f"  [Auth Service] Utilisateur {utilisateur_id} connecté.")

    def est_connecte(self, utilisateur):
        return utilisateur and utilisateur.id in self.utilisateurs_connectes

    def inscrire_participant(self, utilisateur, evenement_id):
        if utilisateur.id not in self.inscriptions:
            self.inscriptions[utilisateur.id] = []
        self.inscriptions[utilisateur.id].append(evenement_id)
        print(f"  [Auth Service] {utilisateur.nom} inscrit à l'événement {evenement_id}.")

    def est_inscrit(self, utilisateur, evenement_id):
        return utilisateur and utilisateur.id in self.inscriptions and evenement_id in self.inscriptions[utilisateur.id]


class Evenement(ABC):
    def __init__(self, id, nom, description, date):
        self.id = id
        self.nom = nom
        self.description = description
        self.date = date
        self._observateurs = [] 

    @abstractmethod
    def get_details(self) -> str:
        pass

    def afficher_info_base(self):
        return f"ID: {self.id}, Nom: {self.nom}, Description: {self.description}, Date: {self.date.strftime('%Y-%m-%d')}"

# --- Classes concrètes d'événements ---
class Conference(Evenement):
    def __init__(self, id, nom, description, date, nombre_places, speaker_principal):
        super().__init__(id, nom, description, date)
        self.nombre_places = nombre_places
        self.speaker_principal = speaker_principal
    def get_details(self) -> str:
        return f"Conférence: {self.nom}, {self.description}, {self.date.strftime('%Y-%m-%d')}, Places: {self.nombre_places}, Speaker: {self.speaker_principal}"

class Hackathon(Evenement):
    def __init__(self, id, nom, description, date, sponsor, duree_heures):
        super().__init__(id, nom, description, date)
        self.sponsor = sponsor
        self.duree_heures = duree_heures
    def get_details(self) -> str:
        return f"Hackathon: {self.nom}, {self.description}, {self.date.strftime('%Y-%m-%d')}, Sponsor: {self.sponsor}, Durée: {self.duree_heures}h"

class Seminaire(Evenement):
    def __init__(self, id, nom, description, date, domaine):
        super().__init__(id, nom, description, date)
        self.domaine = domaine
    def get_details(self) -> str:
        return f"Séminaire: {self.nom}, {self.description}, {self.date.strftime('%Y-%m-%d')}, Domaine: {self.domaine}"

# Modifier EvenementFactory pour inclure l'ID
class EvenementFactory:
    _current_id = 0
    def _generer_id(self):
        EvenementFactory._current_id += 1
        return f"EV{EvenementFactory._current_id:03d}"

    def creer_evenement(self, type_evenement, nom, description, date, **kwargs):
        event_id = self._generer_id()
        if type_evenement == "Conference":
            return Conference(event_id, nom, description, date, kwargs.get('nombre_places'), kwargs.get('speaker_principal'))
        elif type_evenement == "Hackathon":
            return Hackathon(event_id, nom, description, date, kwargs.get('sponsor'), kwargs.get('duree_heures'))
        elif type_evenement == "Seminaire":
            return Seminaire(event_id, nom, description, date, kwargs.get('domaine'))
        else:
            raise ValueError(f"Type d'événement inconnu: {type_evenement}")

# Ajouter un ID à la classe Participant
class Participant:
    _current_id = 0
    def __init__(self, nom, email, est_etudiant=True):
        Participant._current_id += 1
        self.id = f"P{Participant._current_id:03d}"
        self.nom = nom
        self.email = email
        self.est_etudiant = est_etudiant

# --- Exemple d'utilisation ---
if __name__ == "__main__":
    from datetime import date

    # Initialisation
    factory = EvenementFactory()
    auth_service = AuthentificationService()
    
    # Création d'événements
    conf_secrete = factory.creer_evenement("Conference", "Conférence Secrète", "Top secret sur la cyberdéfense", date(2025, 12, 1),
                                           nombre_places=50, speaker_principal="Agent X")
    hack_web = factory.creer_evenement("Hackathon", "Hackathon WebDev", "Construire des apps web", date(2025, 11, 15),
                                      sponsor="DevNet", duree_heures=24)
    sem_public = factory.creer_evenement("Seminaire", "Séminaire Ouvert", "Présentation générale", date(2025, 10, 1),
                                        domaine="Général")

    evenements_db = {
        conf_secrete.id: conf_secrete,
        hack_web.id: hack_web,
        sem_public.id: sem_public
    }

    # Création du proxy
    service_evenement = EvenementServiceProxy(evenements_db, auth_service)

    # Participants
    user_guest = Participant("Visiteur Non Connecté", "guest@example.com")
    user_connected = Participant("Utilisateur Connecté", "user@example.com")
    user_participant = Participant("Participant Hackathon", "participant@example.com")

    # --- Scénarios de test ---
    print("\n--- Scénario 1: Accès à un événement public (Séminaire Ouvert) ---")
    print(service_evenement.get_details_evenement(sem_public.id, user_guest))

    print("\n--- Scénario 2: Accès à une Conférence Secrète sans être connecté ---")
    print(service_evenement.get_details_evenement(conf_secrete.id, user_guest))

    print("\n--- Scénario 3: Accès à une Conférence Secrète en étant connecté ---")
    auth_service.connecter_utilisateur(user_connected.id)
    print(service_evenement.get_details_evenement(conf_secrete.id, user_connected))

    print("\n--- Scénario 4: Accès à un Hackathon sans être inscrit ---")
    print(service_evenement.get_details_evenement(hack_web.id, user_connected))

    print("\n--- Scénario 5: Accès à un Hackathon en étant inscrit ---")
    auth_service.inscrire_participant(user_participant, hack_web.id)
    auth_service.connecter_utilisateur(user_participant.id) # Un inscrit est souvent connecté
    print(service_evenement.get_details_evenement(hack_web.id, user_participant))