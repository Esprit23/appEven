import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk # Ensure ttk is imported
from abc import ABC, abstractmethod
from datetime import date

# --- 1. Factory Method (Création des événements) ---
class Evenement(ABC):
    def __init__(self, id, nom, description, date):
        self.id = id
        self.nom = nom
        self.description = description
        self.date = date
        self._observateurs = []

    @abstractmethod
    def get_details(self):
        pass

    def afficher_info_base(self):
        return f"ID: {self.id}, Nom: {self.nom}, Date: {self.date.strftime('%Y-%m-%d')}"

    def ajouter_observateur(self, observateur):
        if observateur not in self._observateurs:
            self._observateurs.append(observateur)

    def retirer_observateur(self, observateur):
        if observateur in self._observateurs:
            self._observateurs.remove(observateur)

    def notifier_observateurs(self, message_type):
        for obs in self._observateurs:
            obs.mettre_a_jour(self, message_type)

    def mettre_a_jour_description(self, nouvelle_description):
        self.description = nouvelle_description
        self.notifier_observateurs("mise_a_jour_evenement")

class Conference(Evenement):
    def __init__(self, id, nom, description, date, nombre_places, speaker_principal):
        super().__init__(id, nom, description, date)
        self.nombre_places = nombre_places
        self.speaker_principal = speaker_principal

    def get_details(self):
        return f"{self.afficher_info_base()}\n  Type: Conférence\n  Places: {self.nombre_places}\n  Speaker: {self.speaker_principal}\n  Description: {self.description}"

class Hackathon(Evenement):
    def __init__(self, id, nom, description, date, sponsor, duree_heures):
        super().__init__(id, nom, description, date)
        self.sponsor = sponsor
        self.duree_heures = duree_heures

    def get_details(self):
        return f"{self.afficher_info_base()}\n  Type: Hackathon\n  Sponsor: {self.sponsor}\n  Durée: {self.duree_heures}h\n  Description: {self.description}"

class Seminaire(Evenement):
    def __init__(self, id, nom, description, date, domaine):
        super().__init__(id, nom, description, date)
        self.domaine = domaine

    def get_details(self):
        return f"{self.afficher_info_base()}\n  Type: Séminaire\n  Domaine: {self.domaine}\n  Description: {self.description}"

class EvenementFactory:
    _current_id = 0
    def _generer_id(self):
        EvenementFactory._current_id += 1
        return f"EV{EvenementFactory._current_id:03d}"

    def creer_evenement(self, type_evenement, nom, description, date_obj, **kwargs):
        event_id = self._generer_id()
        if type_evenement == "Conference":
            return Conference(event_id, nom, description, date_obj, kwargs.get('nombre_places'), kwargs.get('speaker_principal'))
        elif type_evenement == "Hackathon":
            return Hackathon(event_id, nom, description, date_obj, kwargs.get('sponsor'), kwargs.get('duree_heures'))
        elif type_evenement == "Seminaire":
            return Seminaire(event_id, nom, description, date_obj, kwargs.get('domaine'))
        else:
            raise ValueError(f"Type d'événement inconnu: {type_evenement}")

# --- 2. Strategy (Règles de validation d'inscription) ---
class Participant:
    _current_id = 0
    def __init__(self, nom, email, est_etudiant=True):
        Participant._current_id += 1
        self.id = f"P{Participant._current_id:03d}"
        self.nom = nom
        self.email = email
        self.est_etudiant = est_etudiant

class IRegleValidation(ABC):
    @abstractmethod
    def valider(self, inscription):
        pass

class RegleValidationHackathon(IRegleValidation):
    def valider(self, inscription):
        return inscription.participant.est_etudiant

class RegleValidationConference(IRegleValidation):
    def valider(self, inscription):
        return inscription.evenement.nombre_places > 0

class RegleValidationGenerale(IRegleValidation):
    def valider(self, inscription):
        return True

class Inscription:
    def __init__(self, participant, evenement, regle_validation: IRegleValidation):
        self.participant = participant
        self.evenement = evenement
        self.regle_validation = regle_validation
        self.est_validee = False
        self._observateurs = []

    def ajouter_observateur(self, observateur):
        if observateur not in self._observateurs:
            self._observateurs.append(observateur)

    def retirer_observateur(self, observateur):
        if observateur in self._observateurs:
            self._observateurs.remove(observateur)

    def notifier_observateurs(self, message_type):
        for obs in self._observateurs:
            obs.mettre_a_jour(self, message_type)

    def valider_inscription(self):
        ancienne_validation = self.est_validee
        self.est_validee = self.regle_validation.valider(self)
        if self.est_validee != ancienne_validation:
            self.notifier_observateurs("inscription_validee" if self.est_validee else "inscription_en_attente")
        return self.est_validee

    def set_regle_validation(self, regle_validation: IRegleValidation):
        self.regle_validation = regle_validation

# --- 3. Observer (Notifications) ---
class IObserver(ABC):
    @abstractmethod
    def mettre_a_jour(self, sujet, message_type):
        pass

class NotificationService(IObserver):
    def __init__(self, log_output):
        self.log_output = log_output

    def mettre_a_jour(self, sujet, message_type):
        msg = ""
        if isinstance(sujet, Evenement):
            if message_type == "mise_a_jour_evenement":
                msg = f"[NOTIFICATION] L'événement '{sujet.nom}' a été mis à jour: {sujet.description}"
            else:
                msg = f"[NOTIFICATION] Un événement ({sujet.nom}) a notifié un changement de type: {message_type}"
        elif isinstance(sujet, Inscription):
            statut = "validée" if sujet.est_validee else "en attente"
            msg = f"[NOTIFICATION] L'inscription de '{sujet.participant.nom}' à '{sujet.evenement.nom}' est maintenant {statut}."
        
        self.log_output.config(state='normal')
        self.log_output.insert(tk.END, msg + "\n")
        self.log_output.see(tk.END)
        self.log_output.config(state='disabled')

    def envoyer_email(self, destinataire, sujet, message):
        self.log_output.config(state='normal')
        self.log_output.insert(tk.END, f"  --> EMAIL envoyé à {destinataire}: Sujet='{sujet}', Message='{message}'\n")
        self.log_output.see(tk.END)
        self.log_output.config(state='disabled')

    def envoyer_sms(self, destinataire, message):
        self.log_output.config(state='normal')
        self.log_output.insert(tk.END, f"  --> SMS envoyé à {destinataire}: '{message}'\n")
        self.log_output.see(tk.END)
        self.log_output.config(state='disabled')

# --- 4. Bridge (Affichage des événements) ---
class AffichageEvenement(ABC):
    def __init__(self, evenement, implementateur_affichage):
        self._evenement = evenement
        self._implementateur_affichage = implementateur_affichage

    @abstractmethod
    def afficher(self):
        pass

class AffichageSimpleEvenement(AffichageEvenement):
    def afficher(self):
        return self._implementateur_affichage.afficher_evenement_simple(self._evenement)

class AffichageDetailleEvenement(AffichageEvenement):
    def afficher(self):
        return self._implementateur_affichage.afficher_evenement_detaille(self._evenement)

class IImplementateurAffichage(ABC):
    @abstractmethod
    def afficher_evenement_simple(self, evenement):
        pass

    @abstractmethod
    def afficher_evenement_detaille(self, evenement):
        pass

class AffichageWeb(IImplementateurAffichage):
    def afficher_evenement_simple(self, evenement):
        return f"<div class='card'><h3>{evenement.nom}</h3><p>{evenement.date.strftime('%Y-%m-%d')}</p></div>"

    def afficher_evenement_detaille(self, evenement):
        return f"<div class='page'><h1>{evenement.nom}</h1><p>{evenement.get_details()}</p></div>"

class AffichageMobile(IImplementateurAffichage):
    def afficher_evenement_simple(self, evenement):
        return f"--- {evenement.nom} ---\nDate: {evenement.date.strftime('%Y-%m-%d')}\n"

    def afficher_evenement_detaille(self, evenement):
        return f"--- DÉTAILS {evenement.nom.upper()} ---\n{evenement.get_details()}\n--- FIN ---\n"

# --- 5. Proxy (Sécurisation de l'accès) ---
class IEvenementService(ABC):
    @abstractmethod
    def get_details_evenement(self, evenement_id, utilisateur=None):
        pass

class EvenementServiceReel(IEvenementService):
    def __init__(self, evenements_db):
        self._evenements_db = evenements_db

    def get_details_evenement(self, evenement_id, utilisateur=None):
        evenement = self._evenements_db.get(evenement_id)
        if evenement:
            return evenement.get_details()
        return "Événement non trouvé."

class AuthentificationService:
    def __init__(self):
        self.utilisateurs_connectes = set()
        self.inscriptions = {}

    def connecter_utilisateur(self, utilisateur_id):
        self.utilisateurs_connectes.add(utilisateur_id)

    def est_connecte(self, utilisateur_id):
        return utilisateur_id in self.utilisateurs_connectes

    def inscrire_participant_auth(self, participant_id, evenement_id):
        if participant_id not in self.inscriptions:
            self.inscriptions[participant_id] = []
        self.inscriptions[participant_id].append(evenement_id)

    def est_inscrit(self, participant_id, evenement_id):
        return participant_id in self.inscriptions and evenement_id in self.inscriptions[participant_id]

class EvenementServiceProxy(IEvenementService):
    def __init__(self, evenements_db, authentification_service):
        self._evenement_service_reel = EvenementServiceReel(evenements_db)
        self._authentification_service = authentification_service

    def get_details_evenement(self, evenement_id, utilisateur=None):
        evenement = self._evenement_service_reel._evenements_db.get(evenement_id)
        
        if evenement:
            if "Secrète" in evenement.nom and (not utilisateur or not self._authentification_service.est_connecte(utilisateur.id)):
                return "ACCÈS REFUSÉ: Cet événement est secret et nécessite une connexion."
            
            if isinstance(evenement, Hackathon) and (not utilisateur or not self._authentification_service.est_inscrit(utilisateur.id, evenement_id)):
                return "ACCÈS REFUSÉ: Détails du Hackathon réservés aux participants inscrits."

        return self._evenement_service_reel.get_details_evenement(evenement_id, utilisateur)

# --- Application Tkinter ---
class EventApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plateforme de Gestion des Événements Universitaires")
        self.geometry("1000x750") # Slightly larger window

        # --- Apply a modern theme ---
        self.style = ttk.Style(self)
        self.style.theme_use('clam') # 'clam', 'alt', 'default', 'classic' are good options.
                                     # 'clam' is generally clean and modern.
        # Further customizations for a modern look
        self.style.configure('TFrame', background='#e0e0e0') # Light grey background for frames
        self.style.configure('TLabel', background='#e0e0e0', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6, background='#007bff', foreground='white')
        self.style.map('TButton', background=[('active', '#0056b3')]) # Darker blue on hover
        self.style.configure('TEntry', padding=4, font=('Segoe UI', 10))
        self.style.configure('TCombobox', padding=4, font=('Segoe UI', 10))
        self.style.configure('TCheckbutton', background='#e0e0e0', font=('Segoe UI', 10))
        self.style.configure('TNotebook', background='#c0c0c0') # Notebook tab area background
        self.style.configure('TNotebook.Tab', padding=[10, 5], font=('Segoe UI', 10, 'bold')) # Tab padding and font
        self.style.map('TNotebook.Tab', background=[('selected', '#ffffff')], foreground=[('selected', 'black')]) # Selected tab color

        # --- Initialisation des Services et Données ---
        self.evenement_factory = EvenementFactory()
        self.evenements = {}  # Stockage des événements créés: {id: Evenement_obj}
        self.participants = {} # Stockage des participants: {id: Participant_obj}
        self.inscriptions = [] # Stockage des inscriptions: [Inscription_obj, ...]

        self.auth_service = AuthentificationService()
        self.notification_log = scrolledtext.ScrolledText(self, width=80, height=8, state='disabled', wrap=tk.WORD, font=('Consolas', 9))
        self.notification_service = NotificationService(self.notification_log)
        self.evenement_service_proxy = EvenementServiceProxy(self.evenements, self.auth_service)

        self.current_user = None

        self._create_widgets()

    def _create_widgets(self):
        # --- Main frame for tabs (Notebook) ---
        self.notebook = ttk.Notebook(self) # Use ttk.Notebook
        self.notebook.pack(expand=True, fill="both", padx=15, pady=15) # Add more padding

        # Onglet "Créer Événement"
        self._create_event_tab()
        # Onglet "Gérer Inscriptions"
        self._create_inscription_tab()
        # Onglet "Voir Événements"
        self._create_view_events_tab()
        # Onglet "Proxy & Notifications"
        self._create_proxy_notification_tab()

        # Notification Log at the bottom
        log_frame = ttk.LabelFrame(self, text="Journal des Notifications") # Use ttk.LabelFrame
        log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=5)
        self.notification_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notification_log.config(state='normal')
        self.notification_log.delete(1.0, tk.END)
        self.notification_log.config(state='disabled')

    def _create_event_tab(self):
        frame = ttk.Frame(self.notebook, padding="15 15 15 15") # Use ttk.Frame with padding
        self.notebook.add(frame, text="Créer Événement")

        # Use ttk.Label and ttk.Entry for consistent styling
        ttk.Label(frame, text="Nom:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.event_name_entry = ttk.Entry(frame)
        self.event_name_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(frame, text="Description:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.event_desc_entry = ttk.Entry(frame)
        self.event_desc_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(frame, text="Date (AAAA-MM-JJ):").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.event_date_entry = ttk.Entry(frame)
        self.event_date_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        
        ttk.Label(frame, text="Type d'Événement:").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.event_type_var = tk.StringVar(self)
        self.event_type_var.set("Conference")
        event_type_options = ["Conference", "Hackathon", "Seminaire"]
        self.event_type_menu = ttk.Combobox(frame, textvariable=self.event_type_var, values=event_type_options, state="readonly")
        self.event_type_menu.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
        self.event_type_menu.bind("<<ComboboxSelected>>", self._update_event_specific_fields)

        self.specific_frame = ttk.Frame(frame, padding="10 0 0 0") # Padding for nested frame
        self.specific_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)
        self._update_event_specific_fields()

        ttk.Button(frame, text="Créer Événement", command=self._create_event, style='Accent.TButton').grid(row=5, column=0, columnspan=2, pady=15, padx=5)

        frame.columnconfigure(1, weight=1)

    def _update_event_specific_fields(self, event=None):
        for widget in self.specific_frame.winfo_children():
            widget.destroy()

        event_type = self.event_type_var.get()
        if event_type == "Conference":
            ttk.Label(self.specific_frame, text="Nombre de places:").grid(row=0, column=0, sticky="w", pady=2, padx=5)
            self.conf_places_entry = ttk.Entry(self.specific_frame)
            self.conf_places_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
            ttk.Label(self.specific_frame, text="Speaker Principal:").grid(row=1, column=0, sticky="w", pady=2, padx=5)
            self.conf_speaker_entry = ttk.Entry(self.specific_frame)
            self.conf_speaker_entry.grid(row=1, column=1, sticky="ew", pady=2, padx=5)
        elif event_type == "Hackathon":
            ttk.Label(self.specific_frame, text="Sponsor:").grid(row=0, column=0, sticky="w", pady=2, padx=5)
            self.hack_sponsor_entry = ttk.Entry(self.specific_frame)
            self.hack_sponsor_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
            ttk.Label(self.specific_frame, text="Durée (heures):").grid(row=1, column=0, sticky="w", pady=2, padx=5)
            self.hack_duree_entry = ttk.Entry(self.specific_frame)
            self.hack_duree_entry.grid(row=1, column=1, sticky="ew", pady=2, padx=5)
        elif event_type == "Seminaire":
            ttk.Label(self.specific_frame, text="Domaine:").grid(row=0, column=0, sticky="w", pady=2, padx=5)
            self.sem_domaine_entry = ttk.Entry(self.specific_frame)
            self.sem_domaine_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        self.specific_frame.columnconfigure(1, weight=1)

    def _create_event(self):
        try:
            name = self.event_name_entry.get()
            desc = self.event_desc_entry.get()
            date_str = self.event_date_entry.get()
            event_type = self.event_type_var.get()
            
            if not all([name, desc, date_str, event_type]):
                raise ValueError("Tous les champs de base doivent être remplis.")
            
            event_date = date.fromisoformat(date_str)

            kwargs = {}
            if event_type == "Conference":
                kwargs['nombre_places'] = int(self.conf_places_entry.get())
                kwargs['speaker_principal'] = self.conf_speaker_entry.get()
            elif event_type == "Hackathon":
                kwargs['sponsor'] = self.hack_sponsor_entry.get()
                kwargs['duree_heures'] = int(self.hack_duree_entry.get())
            elif event_type == "Seminaire":
                kwargs['domaine'] = self.sem_domaine_entry.get()

            new_event = self.evenement_factory.creer_evenement(event_type, name, desc, event_date, **kwargs)
            self.evenements[new_event.id] = new_event
            new_event.ajouter_observateur(self.notification_service)

            messagebox.showinfo("Succès", f"Événement '{new_event.nom}' créé avec l'ID: {new_event.id}")
            self._update_event_lists()
            self._clear_event_form()

        except ValueError as e:
            messagebox.showerror("Erreur de création", f"Veuillez vérifier les entrées: {e}")
        except Exception as e:
            messagebox.showerror("Erreur inattendue", f"Une erreur s'est produite: {e}")

    def _clear_event_form(self):
        self.event_name_entry.delete(0, tk.END)
        self.event_desc_entry.delete(0, tk.END)
        self.event_date_entry.delete(0, tk.END)
        self.event_type_var.set("Conference")
        self._update_event_specific_fields()


    def _create_inscription_tab(self):
        frame = ttk.Frame(self.notebook, padding="15 15 15 15")
        self.notebook.add(frame, text="Gérer Inscriptions")

        ttk.Label(frame, text="--- Créer un Participant ---", font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Label(frame, text="Nom Participant:").grid(row=1, column=0, sticky="w", pady=2, padx=5)
        self.part_name_entry = ttk.Entry(frame)
        self.part_name_entry.grid(row=1, column=1, sticky="ew", pady=2, padx=5)
        ttk.Label(frame, text="Email Participant:").grid(row=2, column=0, sticky="w", pady=2, padx=5)
        self.part_email_entry = ttk.Entry(frame)
        self.part_email_entry.grid(row=2, column=1, sticky="ew", pady=2, padx=5)
        self.part_is_student_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Est étudiant?", variable=self.part_is_student_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=5, padx=5)
        ttk.Button(frame, text="Créer Participant", command=self._create_participant).grid(row=4, column=0, columnspan=2, pady=10, padx=5)

        ttk.Label(frame, text="--- Inscrire un Participant ---", font=('Segoe UI', 11, 'bold')).grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Label(frame, text="Participant:").grid(row=6, column=0, sticky="w", pady=2, padx=5)
        self.participant_id_var = tk.StringVar(self)
        self.participant_menu = ttk.Combobox(frame, textvariable=self.participant_id_var, state="readonly")
        self.participant_menu.grid(row=6, column=1, sticky="ew", pady=2, padx=5)

        ttk.Label(frame, text="Événement:").grid(row=7, column=0, sticky="w", pady=2, padx=5)
        self.event_id_var = tk.StringVar(self)
        self.event_menu_inscription = ttk.Combobox(frame, textvariable=self.event_id_var, state="readonly")
        self.event_menu_inscription.grid(row=7, column=1, sticky="ew", pady=2, padx=5)

        ttk.Button(frame, text="Inscrire", command=self._inscrire_participant, style='Accent.TButton').grid(row=8, column=0, columnspan=2, pady=15, padx=5)

        ttk.Label(frame, text="--- Inscriptions Actuelles ---", font=('Segoe UI', 11, 'bold')).grid(row=9, column=0, columnspan=2, sticky="ew", pady=10)
        # Use ttk.Treeview for a more modern listbox look and feel
        self.inscription_tree = ttk.Treeview(frame, columns=('Participant', 'Event', 'Status'), show='headings', height=8)
        self.inscription_tree.heading('Participant', text='Participant')
        self.inscription_tree.heading('Event', text='Événement')
        self.inscription_tree.heading('Status', text='Statut')
        self.inscription_tree.column('Participant', width=150, anchor='center')
        self.inscription_tree.column('Event', width=150, anchor='center')
        self.inscription_tree.column('Status', width=100, anchor='center')
        self.inscription_tree.grid(row=10, column=0, columnspan=2, sticky="nsew", pady=5, padx=5)

        # Add a scrollbar to the Treeview
        tree_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.inscription_tree.yview)
        tree_scrollbar.grid(row=10, column=2, sticky="ns")
        self.inscription_tree.configure(yscrollcommand=tree_scrollbar.set)

        ttk.Button(frame, text="Valider Inscription Sélectionnée", command=self._validate_selected_inscription).grid(row=11, column=0, columnspan=2, pady=10, padx=5)

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(10, weight=1) # Allow treeview to expand


    def _create_participant(self):
        try:
            name = self.part_name_entry.get()
            email = self.part_email_entry.get()
            is_student = self.part_is_student_var.get()
            
            if not name or not email:
                raise ValueError("Nom et email du participant sont requis.")

            new_participant = Participant(name, email, is_student)
            self.participants[new_participant.id] = new_participant
            messagebox.showinfo("Succès", f"Participant '{new_participant.nom}' créé avec l'ID: {new_participant.id}")
            self._update_participant_list()
            self.part_name_entry.delete(0, tk.END)
            self.part_email_entry.delete(0, tk.END)
            self.part_is_student_var.set(True)
        except Exception as e:
            messagebox.showerror("Erreur participant", str(e))

    def _update_participant_list(self):
        self.participant_menu['values'] = [f"{p.id} - {p.nom}" for p in self.participants.values()]
        if self.participants:
            self.participant_id_var.set(self.participant_menu['values'][0])
        else:
            self.participant_id_var.set("")
        
    def _inscrire_participant(self):
        try:
            selected_participant_id = self.participant_id_var.get().split(" - ")[0]
            selected_event_id = self.event_id_var.get().split(" - ")[0]

            participant = self.participants.get(selected_participant_id)
            evenement = self.evenements.get(selected_event_id)

            if not participant or not evenement:
                raise ValueError("Veuillez sélectionner un participant et un événement valides.")

            regle = RegleValidationGenerale() # Default
            if isinstance(evenement, Hackathon):
                regle = RegleValidationHackathon()
            elif isinstance(evenement, Conference):
                regle = RegleValidationConference()

            new_inscription = Inscription(participant, evenement, regle)
            new_inscription.ajouter_observateur(self.notification_service)
            self.inscriptions.append(new_inscription)
            
            self.auth_service.inscrire_participant_auth(participant.id, evenement.id)

            messagebox.showinfo("Succès", f"Inscription de {participant.nom} à '{evenement.nom}' ajoutée. Validation en attente.")
            self._update_inscription_listbox()
        except Exception as e:
            messagebox.showerror("Erreur Inscription", str(e))

    def _update_inscription_listbox(self):
        # Clear existing items in Treeview
        for i in self.inscription_tree.get_children():
            self.inscription_tree.delete(i)
        
        for inscr in self.inscriptions:
            status = "Validée" if inscr.est_validee else "En attente"
            self.inscription_tree.insert('', tk.END, values=(inscr.participant.nom, inscr.evenement.nom, status))

    def _validate_selected_inscription(self):
        try:
            selected_item_id = self.inscription_tree.selection()
            if not selected_item_id:
                messagebox.showerror("Validation", "Veuillez sélectionner une inscription à valider.")
                return

            # Get the index of the selected item in the original inscriptions list
            # This is a bit indirect, but necessary because Treeview doesn't store object references directly
            selected_values = self.inscription_tree.item(selected_item_id[0])['values']
            
            inscription_obj = None
            for inscr in self.inscriptions:
                if inscr.participant.nom == selected_values[0] and \
                   inscr.evenement.nom == selected_values[1] and \
                   ("Validée" if inscr.est_validee else "En attente") == selected_values[2]:
                   inscription_obj = inscr
                   break
            
            if not inscription_obj:
                messagebox.showerror("Validation", "Inscription introuvable.")
                return

            if inscription_obj.valider_inscription():
                messagebox.showinfo("Validation", f"Inscription de {inscription_obj.participant.nom} à '{inscription_obj.evenement.nom}' validée avec succès !")
            else:
                messagebox.showwarning("Validation", f"Validation de l'inscription de {inscription_obj.participant.nom} à '{inscription_obj.evenement.nom}' a échoué selon les règles spécifiques.")
            
            self._update_inscription_listbox()
        except Exception as e:
            messagebox.showerror("Erreur Validation", str(e))


    def _create_view_events_tab(self):
        frame = ttk.Frame(self.notebook, padding="15 15 15 15")
        self.notebook.add(frame, text="Voir Événements")

        ttk.Label(frame, text="Sélectionner un Événement:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.event_view_id_var = tk.StringVar(self)
        self.event_menu_view = ttk.Combobox(frame, textvariable=self.event_view_id_var, state="readonly")
        self.event_menu_view.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        self.event_menu_view.bind("<<ComboboxSelected>>", self._display_selected_event)

        ttk.Label(frame, text="Type d'Affichage:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.display_type_var = tk.StringVar(self)
        self.display_type_var.set("Simple")
        display_options = ["Simple", "Détaillé"]
        ttk.Combobox(frame, textvariable=self.display_type_var, values=display_options, state="readonly").grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(frame, text="Plateforme d'Affichage:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.platform_type_var = tk.StringVar(self)
        self.platform_type_var.set("Web")
        platform_options = ["Web", "Mobile"]
        ttk.Combobox(frame, textvariable=self.platform_type_var, values=platform_options, state="readonly").grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        ttk.Button(frame, text="Afficher Événement", command=self._display_selected_event, style='Accent.TButton').grid(row=3, column=0, columnspan=2, pady=15, padx=5)

        self.event_display_output = scrolledtext.ScrolledText(frame, width=60, height=15, state='disabled', wrap=tk.WORD, font=('Consolas', 10))
        self.event_display_output.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=5, padx=5)

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

    def _display_selected_event(self, event=None):
        self.event_display_output.config(state='normal')
        self.event_display_output.delete(1.0, tk.END)

        selected_event_id = self.event_view_id_var.get().split(" - ")[0]
        evenement = self.evenements.get(selected_event_id)

        if not evenement:
            self.event_display_output.insert(tk.END, "Veuillez sélectionner un événement.")
            self.event_display_output.config(state='disabled')
            return

        display_type = self.display_type_var.get()
        platform_type = self.platform_type_var.get()

        implementateur = AffichageWeb() # Default
        if platform_type == "Mobile":
            implementateur = AffichageMobile()

        affichage_strategy = AffichageSimpleEvenement(evenement, implementateur) # Default
        if display_type == "Détaillé":
            affichage_strategy = AffichageDetailleEvenement(evenement, implementateur)

        rendered_output = affichage_strategy.afficher()
        self.event_display_output.insert(tk.END, rendered_output)
        self.event_display_output.config(state='disabled')

    def _create_proxy_notification_tab(self):
        frame = ttk.Frame(self.notebook, padding="15 15 15 15")
        self.notebook.add(frame, text="Proxy & Notifications")

        ttk.Label(frame, text="--- Gérer l'Utilisateur Actuel (pour Proxy) ---", font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Label(frame, text="Utilisateur:").grid(row=1, column=0, sticky="w", pady=2, padx=5)
        self.current_user_var = tk.StringVar(self)
        self.current_user_menu = ttk.Combobox(frame, textvariable=self.current_user_var, state="readonly")
        self.current_user_menu.grid(row=1, column=1, sticky="ew", pady=2, padx=5)
        self.current_user_menu.bind("<<ComboboxSelected>>", self._set_current_user)

        ttk.Button(frame, text="Se Connecter", command=self._login_current_user).grid(row=2, column=0, sticky="ew", pady=5, padx=5)
        ttk.Button(frame, text="Se Déconnecter", command=self._logout_current_user).grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        self.login_status_label = ttk.Label(frame, text="Statut: Non connecté", font=('Segoe UI', 9, 'italic'))
        self.login_status_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=5, padx=5)

        ttk.Label(frame, text="--- Accéder aux Détails via Proxy ---", font=('Segoe UI', 11, 'bold')).grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Label(frame, text="Sélectionner Événement:").grid(row=5, column=0, sticky="w", pady=2, padx=5)
        self.event_proxy_id_var = tk.StringVar(self)
        self.event_menu_proxy = ttk.Combobox(frame, textvariable=self.event_proxy_id_var, state="readonly")
        self.event_menu_proxy.grid(row=5, column=1, sticky="ew", pady=2, padx=5)
        ttk.Button(frame, text="Voir Détails (via Proxy)", command=self._get_event_details_via_proxy, style='Accent.TButton').grid(row=6, column=0, columnspan=2, pady=15, padx=5)
        self.proxy_output = scrolledtext.ScrolledText(frame, width=60, height=8, state='disabled', wrap=tk.WORD, font=('Consolas', 10))
        self.proxy_output.grid(row=7, column=0, columnspan=2, sticky="nsew", pady=5, padx=5)

        ttk.Label(frame, text="--- Mettre à Jour Événement (pour Observer) ---", font=('Segoe UI', 11, 'bold')).grid(row=8, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Label(frame, text="Sélectionner Événement:").grid(row=9, column=0, sticky="w", pady=2, padx=5)
        self.event_update_id_var = tk.StringVar(self)
        self.event_menu_update = ttk.Combobox(frame, textvariable=self.event_update_id_var, state="readonly")
        self.event_menu_update.grid(row=9, column=1, sticky="ew", pady=2, padx=5)

        ttk.Label(frame, text="Nouvelle Description:").grid(row=10, column=0, sticky="w", pady=2, padx=5)
        self.new_description_entry = ttk.Entry(frame)
        self.new_description_entry.grid(row=10, column=1, sticky="ew", pady=2, padx=5)

        ttk.Button(frame, text="Mettre à Jour et Notifier", command=self._update_and_notify_event, style='Accent.TButton').grid(row=11, column=0, columnspan=2, pady=15, padx=5)

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(7, weight=1)

    def _set_current_user(self, event=None):
        selected_user_id = self.current_user_var.get().split(" - ")[0]
        self.current_user = self.participants.get(selected_user_id)
        if self.current_user:
            self.login_status_label.config(text=f"Statut: Utilisateur sélectionné: {self.current_user.nom}")
        else:
            self.login_status_label.config(text="Statut: Aucun utilisateur sélectionné")

    def _login_current_user(self):
        if self.current_user:
            self.auth_service.connecter_utilisateur(self.current_user.id)
            self.login_status_label.config(text=f"Statut: Connecté en tant que {self.current_user.nom}")
            messagebox.showinfo("Connexion", f"{self.current_user.nom} est maintenant connecté.")
        else:
            messagebox.showwarning("Connexion", "Veuillez sélectionner un utilisateur à connecter.")

    def _logout_current_user(self):
        if self.current_user and self.auth_service.est_connecte(self.current_user.id):
            self.auth_service.utilisateurs_connectes.remove(self.current_user.id)
            self.login_status_label.config(text=f"Statut: Déconnecté.")
            messagebox.showinfo("Déconnexion", f"{self.current_user.nom} est déconnecté.")
            self.current_user = None # Clear current user
            self.current_user_var.set("") # Clear combobox selection
        else:
            messagebox.showwarning("Déconnexion", "Aucun utilisateur connecté à déconnecter.")

    def _get_event_details_via_proxy(self):
        self.proxy_output.config(state='normal')
        self.proxy_output.delete(1.0, tk.END)

        selected_event_id = self.event_proxy_id_var.get().split(" - ")[0]
        
        details = self.evenement_service_proxy.get_details_evenement(selected_event_id, self.current_user)
        self.proxy_output.insert(tk.END, details)
        self.proxy_output.config(state='disabled')

    def _update_and_notify_event(self):
        try:
            selected_event_id = self.event_update_id_var.get().split(" - ")[0]
            new_desc = self.new_description_entry.get()

            evenement = self.evenements.get(selected_event_id)
            if not evenement:
                raise ValueError("Veuillez sélectionner un événement.")
            if not new_desc:
                raise ValueError("La nouvelle description ne peut pas être vide.")

            evenement.mettre_a_jour_description(new_desc)
            messagebox.showinfo("Mise à Jour", f"L'événement '{evenement.nom}' a été mis à jour et les observateurs notifiés.")
            self.new_description_entry.delete(0, tk.END)
            self._update_event_lists()
        except Exception as e:
            messagebox.showerror("Erreur Mise à Jour", str(e))

    def _update_event_lists(self):
        event_options = [f"{e.id} - {e.nom}" for e in self.evenements.values()]
        
        self.event_menu_inscription['values'] = event_options
        self.event_menu_view['values'] = event_options
        self.event_menu_proxy['values'] = event_options
        self.event_menu_update['values'] = event_options

        # Set default selections if events exist
        if event_options:
            self.event_id_var.set(event_options[0])
            self.event_view_id_var.set(event_options[0])
            self.event_proxy_id_var.set(event_options[0])
            self.event_update_id_var.set(event_options[0])
        else:
            self.event_id_var.set("")
            self.event_view_id_var.set("")
            self.event_proxy_id_var.set("")
            self.event_update_id_var.set("")

        self._update_inscription_listbox()
        self.after(100, self._update_participant_list)

# --- Point d'entrée de l'application ---
if __name__ == "__main__":
    _factory_demo = EvenementFactory()
    evenements_db = {
        "EV001": _factory_demo.creer_evenement("Conference", "Conférence Secrète sur la Quantum", "Conférence très confidentielle sur les dernières découvertes de la physique quantique.", date(2025, 8, 20),
                                               nombre_places=50, speaker_principal="Dr. Elara Vance"),
        "EV002": _factory_demo.creer_evenement("Hackathon", "Hackathon Blockchain", "Défi de développement d'applications décentralisées (DApps) sur la blockchain Ethereum.", date(2025, 9, 10),
                                              sponsor="CryptoCorp Solutions", duree_heures=36),
        "EV003": _factory_demo.creer_evenement("Seminaire", "Séminaire d'Introduction à Python", "Les bases de la programmation en Python, idéal pour les débutants.", date(2025, 10, 5),
                                              domaine="Programmation"),
        "EV004": _factory_demo.creer_evenement("Conference", "Conférence Ouverte sur l'IA", "Introduction à l'intelligence artificielle et ses applications dans le monde réel.", date(2025, 11, 1),
                                              nombre_places=500, speaker_principal="Mme. Ada Lovelace")
    }
    
    app = EventApp()
    app.evenements.update(evenements_db)
    app._update_event_lists()

    p1 = Participant("Alice Dupont", "alice@univ.com", True)
    p2 = Participant("Bob Le Prof", "bob@univ.com", False)
    p3 = Participant("Charlie Etudiant", "charlie@univ.com", True)
    app.participants[p1.id] = p1
    app.participants[p2.id] = p2
    app.participants[p3.id] = p3
    app._update_participant_list()

    app.mainloop()