# --- Abstraction de l'Affichage ---
from abc import ABC, abstractmethod
from Factory_Method import EvenementFactory


class AffichageEvenement(ABC):
    def __init__(self, evenement, implementateur_affichage):
        self._evenement = evenement
        self._implementateur_affichage = implementateur_affichage

    @abstractmethod
    def afficher(self):
        pass

class AffichageSimpleEvenement(AffichageEvenement):
    def afficher(self):
        print("--- Affichage Simple ---")
        return self._implementateur_affichage.afficher_evenement_simple(self._evenement)

class AffichageDetailleEvenement(AffichageEvenement):
    def afficher(self):
        print("--- Affichage Détaillé ---")
        return self._implementateur_affichage.afficher_evenement_detaille(self._evenement)

# --- Implémentation de l'Affichage ---
class IImplementateurAffichage(ABC):
    @abstractmethod
    def afficher_evenement_simple(self, evenement):
        pass

    @abstractmethod
    def afficher_evenement_detaille(self, evenement):
        pass

class AffichageWeb(IImplementateurAffichage):
    def afficher_evenement_simple(self, evenement):
        return (f"<div class='evenement-card'><h2>{evenement.nom}</h2><p>{evenement.date.strftime('%Y-%m-%d')}</p></div>")

    def afficher_evenement_detaille(self, evenement):
        details = evenement.get_details()
        return (f"<div class='evenement-page'><h1>{evenement.nom}</h1><p>Description: {evenement.description}</p>"
                f"<p>Date: {evenement.date.strftime('%Y-%m-%d')}</p><p>Spécificités: {details}</p></div>")

class AffichageMobile(IImplementateurAffichage):
    def afficher_evenement_simple(self, evenement):
        return (f"--- {evenement.nom} ---\nDate: {evenement.date.strftime('%Y-%m-%d')}\n")

    def afficher_evenement_detaille(self, evenement):
        details = evenement.get_details()
        return (f"--- DÉTAILS {evenement.nom.upper()} ---\nDescription: {evenement.description}\n"
                f"Date: {evenement.date.strftime('%Y-%m-%d')}\nSpécificités: {details}\n--- FIN ---")



# --- Exemple d'utilisation ---
if __name__ == "__main__":
    from datetime import date

    factory = EvenementFactory()
    conf_data = factory.creer_evenement("Conference", "Conférence Data Science", "Exploration des Big Data", date(2025, 9, 1),
                                        nombre_places=300, speaker_principal="Dr. Data")
    hack_iot = factory.creer_evenement("Hackathon", "Hackathon IoT", "Construire des objets connectés", date(2025, 10, 10),
                                        sponsor="IoT Solutions", duree_heures=36)

    # Affichage Web
    affichage_web = AffichageWeb()
    simple_web_conf = AffichageSimpleEvenement(conf_data, affichage_web)
    detail_web_hack = AffichageDetailleEvenement(hack_iot, affichage_web)

    print("\n--- Affichage Web ---")
    print(simple_web_conf.afficher())
    print(detail_web_hack.afficher())

    # Affichage Mobile
    affichage_mobile = AffichageMobile()
    simple_mobile_conf = AffichageSimpleEvenement(conf_data, affichage_mobile)
    detail_mobile_hack = AffichageDetailleEvenement(hack_iot, affichage_mobile)

    print("\n--- Affichage Mobile ---")
    print(simple_mobile_conf.afficher())
    print(detail_mobile_hack.afficher())