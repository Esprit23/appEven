# --- Classe Abstraite / Interface pour les Événements ---
from abc import ABC, abstractmethod

class Evenement(ABC):
    def __init__(self, nom, description, date):
        self.nom = nom
        self.description = description
        self.date = date

    @abstractmethod
    def get_details(self):
        pass

    def afficher_info_base(self):
        return f"Nom: {self.nom}, Description: {self.description}, Date: {self.date.strftime('%Y-%m-%d')}"

# --- Classes Concrètes d'Événements ---
class Conference(Evenement):
    def __init__(self, nom, description, date, nombre_places, speaker_principal):
        super().__init__(nom, description, date)
        self.nombre_places = nombre_places
        self.speaker_principal = speaker_principal

    def get_details(self):
        return f"{self.afficher_info_base()}, Places: {self.nombre_places}, Speaker: {self.speaker_principal}"

class Hackathon(Evenement):
    def __init__(self, nom, description, date, sponsor, duree_heures):
        super().__init__(nom, description, date)
        self.sponsor = sponsor
        self.duree_heures = duree_heures

    def get_details(self):
        return f"{self.afficher_info_base()}, Sponsor: {self.sponsor}, Durée: {self.duree_heures} heures"

class Seminaire(Evenement):
    def __init__(self, nom, description, date, domaine):
        super().__init__(nom, description, date)
        self.domaine = domaine

    def get_details(self):
        return f"{self.afficher_info_base()}, Domaine: {self.domaine}"

# --- Classe Fabrique (Factory) ---
class EvenementFactory:
    def creer_evenement(self, type_evenement, nom, description, date, **kwargs):
        if type_evenement == "Conference":
            return Conference(nom, description, date, kwargs.get('nombre_places'), kwargs.get('speaker_principal'))
        elif type_evenement == "Hackathon":
            return Hackathon(nom, description, date, kwargs.get('sponsor'), kwargs.get('duree_heures'))
        elif type_evenement == "Seminaire":
            return Seminaire(nom, description, date, kwargs.get('domaine'))
        else:
            raise ValueError(f"Type d'événement inconnu: {type_evenement}")

# --- Exemple d'utilisation ---
if __name__ == "__main__":
    from datetime import date

    factory = EvenementFactory()

    # Création d'une conférence
    conf = factory.creer_evenement("Conference", "Conférence IA", "Dernières avancées en IA", date(2025, 9, 15),
                                   nombre_places=200, speaker_principal="Dr. Elara Vance")
    print(conf.get_details())

    # Création d'un hackathon
    hack = factory.creer_evenement("Hackathon", "Hackathon Cybersécurité", "Développez des solutions de sécurité", date(2025, 10, 20),
                                   sponsor="TechCorp", duree_heures=48)
    print(hack.get_details())

    # Création d'un séminaire
    sem = factory.creer_evenement("Seminaire", "Séminaire Blockchain", "Introduction aux technologies blockchain", date(2025, 11, 5),
                                  domaine="Finance")
    print(sem.get_details())

    # Tenter de créer un type inconnu
    try:
        unknown_event = factory.creer_evenement("Atelier", "Atelier Dessin", "Apprendre à dessiner", date(2025, 12, 1))
    except ValueError as e:
        print(f"\nErreur attendue: {e}")