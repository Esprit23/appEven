# 🎓 Plateforme de Gestion des Événements Universitaires

Ce projet est une **application de bureau Python (Tkinter)** permettant de gérer des événements universitaires. Elle met en œuvre plusieurs **design patterns** pour garantir une architecture solide, flexible et facilement maintenable.

---

## 🚀 Fonctionnalités Principales

- **Création d’événements variés** : conférences, hackathons, séminaires, avec attributs spécifiques.
- **Gestion des inscriptions** : système dynamique de validation selon des règles définies.
- **Système de notifications** : envoi automatique de notifications aux participants/organisateurs.
- **Affichage multi-plateforme** : visualisation simple ou détaillée, adaptable à différents supports (web/mobile).
- **Contrôle d’accès sécurisé** : affichage conditionnel des détails sensibles selon le rôle ou le statut d’inscription.

---

## 🧠 Design Patterns Utilisés

| Pattern              | Catégorie       | Utilisation |
|----------------------|------------------|-------------|
| Factory Method        | Création         | Création flexible d’événements selon leur type. |
| Bridge                | Structurel       | Découplage de l'affichage de l’événement de son implémentation. |
| Proxy                 | Structurel       | Contrôle d’accès aux détails sensibles des événements. |
| Observer              | Comportemental   | Notifications automatiques des changements d’état. |
| Strategy              | Comportemental   | Règles de validation d’inscription interchangeables. |
| Template Method       | Comportemental   | Définition d’un processus d’inscription standardisé. |

---

## 💻 Interface Utilisateur

L’interface graphique est construite avec **Tkinter** et divisée en 4 onglets :

1. **Créer Événement** : saisie des informations de l’événement.
2. **Gérer Inscriptions** : ajout de participants et validation des inscriptions.
3. **Voir Événements** : consultation des événements sous différents formats.
4. **Proxy & Notifications** : test d’accès sécurisé et affichage des notifications en temps réel.

---

## 🛠️ Pré-requis

- **Python 3.x** installé sur votre machine.
- Aucun module externe requis.

---

## ▶️ Lancer l’Application

1. Clonez le dépôt :

```bash
git clone https://github.com/votre-utilisateur/nom-du-repo.git
cd nom-du-repo
