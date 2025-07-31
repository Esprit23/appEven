Plateforme de Gestion des Événements Universitaires
Description du Projet
Ce projet implémente une plateforme de gestion des événements universitaires en utilisant Python et Tkinter pour l'interface graphique. L'objectif principal est de démontrer l'application de plusieurs design patterns pour construire une architecture logicielle robuste, flexible et maintenable, capable de gérer la création d'événements, l'inscription des participants, la visualisation des informations et la communication des mises à jour.

Fonctionnalités
La plateforme offre les fonctionnalités suivantes :

Création d'événements variés : Permet de créer différents types d'événements (Conférences, Hackathons, Séminaires) avec des attributs spécifiques.

Gestion des inscriptions : Facilite l'inscription des participants aux événements, avec des règles de validation dynamiques.

Système de notification : Envoie des notifications automatiques aux participants et organisateurs en cas de mises à jour ou de changements de statut d'inscription.

Visualisation flexible des événements : Affiche les informations des événements de différentes manières (simple, détaillée) et s'adapte à diverses plateformes (web, mobile).

Sécurisation des accès : Contrôle l'accès aux détails sensibles des événements en fonction du rôle de l'utilisateur ou de son statut d'inscription.

Design Patterns Utilisés
Ce projet met en œuvre les design patterns suivants pour adresser les besoins du système :

Factory Method (Création) : Pour la création flexible et découplée des différents types d'événements.

Bridge (Structurel) : Pour découpler l'abstraction de l'affichage des événements de son implémentation sur diverses plateformes.

Proxy (Structurel) : Pour contrôler et sécuriser l'accès aux détails des événements.

Observer (Comportemental) : Pour la gestion des notifications automatiques lors des changements d'état des événements ou des inscriptions.

Strategy (Comportemental) : Pour encapsuler et rendre interchangeables les différentes règles de validation d'inscription.

Template Method (Comportemental) : Pour définir le squelette d'un processus d'inscription standardisé tout en permettant la personnalisation de certaines étapes.

Comment Exécuter l'Application
Prérequis
Python 3.x installé.

Étapes
Téléchargez le code :
Clonez ce dépôt ou téléchargez les fichiers du projet. Assurez-vous d'avoir le fichier event_app.py (ou le nom de votre fichier principal).

Naviguez vers le répertoire du projet :
Ouvrez votre terminal ou invite de commande et accédez au dossier où se trouve le fichier event_app.py.

cd chemin/vers/votre/dossier/projet

Exécutez l'application :
Lancez l'application en exécutant le script Python.

python event_app.py

Utilisation de l'Application
L'application s'ouvrira avec une interface graphique Tkinter divisée en plusieurs onglets :

Créer Événement : Permet aux organisateurs de définir de nouveaux événements en spécifiant leur nom, description, date, type et les attributs spécifiques à chaque type (places, speaker, sponsor, durée, domaine).

Gérer Inscriptions : Permet de créer des participants, de les inscrire à des événements et de valider leurs inscriptions selon des règles spécifiques.

Voir Événements : Permet de consulter les détails des événements avec différentes options d'affichage (simple/détaillé) et de plateforme (web/mobile).

Proxy & Notifications : Permet de simuler la connexion d'utilisateurs, de tester l'accès sécurisé aux détails des événements via le Proxy, et d'observer le journal des notifications en temps réel.

Dépendances
Ce projet utilise les modules standards de Python :

tkinter (pour l'interface graphique)

tkinter.ttk (pour les widgets thématiques modernes)

tkinter.messagebox (pour les boîtes de dialogue)

tkinter.scrolledtext (pour les zones de texte défilantes)

abc (pour les classes abstraites)

datetime (pour la gestion des dates)

Aucune installation supplémentaire de bibliothèques externes n'est requise.
