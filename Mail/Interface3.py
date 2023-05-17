#!####################################################################################################
#!------------------------------------------LIBRAIRIES-------------------------------------------#
#!####################################################################################################

import os
import csv
import sys
import random
import smtplib
import numpy as np
import tkinter as tk
import mysql.connector
from tkinter import ttk
from datetime import date
import matplotlib.pyplot as plt
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#!####################################################################################################
#!------------------------------------------FONCTIONS-------------------------------------------#
#!####################################################################################################

#* Cette fonction permet de se connecter à la base de donnée et de créer un curseur qui permettra de 
#* de lire les données de celle-ci.
#* Elle retourne les éléments du curseur.
def connexion_BDD():
    # Connexion à la base de données MySQL.
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="phishing_rapport"
    )

    # Création d'un curseur pour exécuter des requêtes SQL.
    mycursor = mydb.cursor()

    return mydb, mycursor

#* Cette fonction teste directement la BDD pour savoir si elle est vide ou non.
#* Elle prend en argument le curseur créer lors de la connexion à la BDD.
#* Elle retourne un booléan en fonction du nombre de ligne.
def BDD_nonVide(mycursor):
    
    # Récupère le nombre de ligne dans la BDD.
    nb_lignes = mycursor.rowcount
    
    # Teste pour savoir si elle est vide ou non.
    if (nb_lignes > 0 ):
        return False
    else:
        return True

#* Cette fonction peremt de récupérer les lignes de la BDD qui ont été ajouté à la date actuelle.
#* Autrement dit, elle récupère les informations (l'adresse mail) des personnes piégées.
#* Elle prend en argument les éléments du curseur.
#* Et retourne une liste contenant les lignes qui nous intéressent.
def todayData(mydb, mycursor):
    
    # Tester si la connexion est active, sinon la rétablir.
    if not mydb.is_connected():
        mydb.reconnect()

    # Exécution de la requête pour récupérer toutes les lignes avec la date actuelle.
    today = date.today().strftime("%Y-%m-%d")
    mycursor.execute("SELECT * FROM Menace WHERE date_detection=%s", (today,))
    
    # Récupération des résultats.
    resultats = mycursor.fetchall()
    
    return resultats

#* Cette fonction permet d'actualiser l'histpgramme en interrogeant la BDD.
def update_data():
    
    # Vide le tableau qui contient les données.
    pourcentage_pieges.clear()
    
    # Récupère les infos en fonction de leur date pour contabiliser les utilisateurs selon le mois.
    for i in range(1, 13):
        cursor.execute(f"SELECT COUNT(*) FROM menace WHERE YEAR(date_detection) = '{year}' AND MONTH(date_detection) = '{i:02}'")
        result = cursor.fetchone()[0]
        pourcentage_pieges.append(result)
    
    # Reset les éléments de l'histogramme qui vont être modifiés.
    ax.clear()
    
    # Modifications des éléments de l'histogramme avec les nouvelles données et reconstruction des 
    # éléments effacés.
    ax.set_ylim(0, 100)
    ax.bar(mois, pourcentage_pieges, color='red', label='Nombre de personnes piégées')
    ax.legend(fontsize=15)
    for i in range(len(mois)):
        ax.text(i, pourcentage_pieges[i], f"{pourcentage_pieges[i]}", ha='center', va='bottom', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xticks(rotation=90)

    canvas.draw()
    
#* Cette fonction permet de séléctionner un certain nombre d'adresses aléatoirement selon l'option
#* choisie par l'utilisateur.
#* Elle retourne une liste d'adresses.
def select_email_addresses():
    global selected_addresses
    
    # Ouverture du fichier csv contenant les adresses
    with open('liste_mails.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            selected_addresses.append((row[0],"?"))
    
    # Récupère le mode choisi par l'utilisateur 
    selection_mode = selection_mode_var.get()
    
    # Mode 2 = nombre d'adresses spécifié
    if selection_mode == 2:
        
        # Sélection aléatoire d'un nombre spécifié d'adresses
        num_addresses = int(num_addresses_entry.get())
        selected_addresses = random.sample(selected_addresses, num_addresses)
 # Modification de la liste d'adresses sélectionnées
    return selected_addresses

#* Cette fonction permet d'afficher les adresses séléctionnées dans le tableau.
#* Elle prend en arguement la liste des adresses séléectionnées aléatoirement.
#* Elle retourne le tableau pour pouvoir le modifier ultérieurement.
def display_email_addresses(selected_addresses):
    global table 
    
    # Suppression des anciens widgets dans la frame 4.
    for widget in frame1.winfo_children():
        if isinstance(widget, ttk.Treeview):
            widget.destroy()
        if isinstance(widget, ttk.Treeview) and widget._name == "tree":
            widget.destroy()

    # Ajout du tableau pour afficher les adresses sélectionnées.
    table = ttk.Treeview(frame1, columns=("col1", "col2"), show="headings")

    # Ajout des colonnes.
    table.heading("col1", text="Adresse", anchor="center")
    table.heading("col2", text="Résultat", anchor="center")

    # Ajout des lignes avec les adresses sélectionnées.
    for i, address in enumerate(selected_addresses):
        values = (address[0], address[1])
        table.insert("", "end", values=values)

    # Centrage des colonnes dans leur cellule.
    for col in table["columns"]:
        table.column(col, anchor="center")

    # Configuration des poids des colonnes pour les centrer dans la frame.
    for i, col in enumerate(table["columns"]):
        frame1.columnconfigure(i, weight=1)

    # Ajout de l'espace autour du tableau.
    table.grid(row=0, column=0,padx=10, pady=10)

    # Centrage du tableau horizontalement dans sa frame.
    table.grid(sticky="ew", columnspan=3)

    # Replacer les autres éléments de l'interface utilisateur à leur position initiale.
    all_addresses_rb.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    random_addresses_rb.grid(row=1, column=0, sticky="w", padx=10, pady=10)
    num_addresses_label.grid(row=1, column=1, padx=(0, 10), pady=10)
    num_addresses_entry.grid(row=1, column=2, sticky="w", padx=10, pady=10)
    select_button.grid(row=3, column=0, sticky="w", padx=10, pady=5)
    send_button.grid(row=4, column=0, sticky="w", padx=10, pady=5)

    return table

#* Cette fonction permet d'appeler les deux fonctions ci-dessus lorsque le bouton est cliqué.
#* Elle retourne le tableau pour pouvoir le modifier ultérieurement.
def select_and_display_email_addresses():
    global table
    selected_addresses = select_email_addresses()
    table = display_email_addresses(selected_addresses)
    return table
        
#* Cette fonction permet d'envoyer un type de mail séléctionné aléatoirement à l'ensemble des adresses
#* de la liste.
def send_mail():
    
    global selected_addresses
    
    # Parcours de chaque ligne du tableau.
    i = 0
    for adresse in selected_addresses:
        # La première colonne contient les adresses mail.
        adr = adresse[0]

        # Définir les informations de l'e-mail.
        sender = 'no-reply-serviceInfo@gmail.com'
        recipient = adresse[0]
        subject = 'Urgent'

        # Créer un objet MIMEMultipart avec le corps de l'e-mail.
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        # Séléction aléatoire d'un dossier dans le répertoire courant.
        # Chaque dossier contient le code html et les images nécesaire pour la construction de l'email.
        with open(chemin_html, 'rb') as f:
            code_HTML = f.read().decode('utf-8')
            # Remplacer "{adr}" par le contenu de la variable recipient.
            code_HTML = code_HTML.replace('{adr}', adr)

        # Ajouter une partie texte.
        texte = MIMEText(code_HTML, 'html')
        msg.attach(texte)
        
        # Ajouter une partie image en utilisant CID pour référencer l'image dans le HTML.
        with open(chemin_image, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<image1>')
            msg.attach(img)

        # Si une image "alerte.jpg" est présente on l'ajoute.
        # (Elle n'est pas systématiquement présente dans tous les mails)
        if (os.path.exists(chemin_alerte)):
            with open(chemin_alerte, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<image2>')
                msg.attach(img)
        
        # Établir une connexion avec le serveur SMTP.
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        
        # Envoyer l'e-mail.
        server.sendmail(sender, recipient, msg.as_string())
        
        # Modifie la colonne "Résulat" du tableau pour signaler que le mail a bien été envoyé.
        selected_addresses[i] = (adresse[0], "✔️")
        i += 1
        
        # Afficher le tableau pour mettre à jour la colonne résultat.
        display_email_addresses(selected_addresses)
        
        # Rafraichir la fenêtre.
        root.update()
        
        # Fermer la connexion.
        server.quit()

#* Cette fonction permet de récupérer les données de la BDD et de les comparer à la liste d'adresses
#* qui auquelles ont été envoyé un mail afin de savoir quel utilisateur s'est fait avoir.
def testAdresse(data,table):
    global pourcentage_pieges
    
    # Récupération de la première colonne du tableau.
    adresse_column = []
    for row_id in table.get_children():
        row = table.item(row_id)["values"]
        adresse_column.append(row[0])

    # Pour chaque ligne de la BDD.
    for row in data:
        
        # On enlève les espaces au début et à la fin.
        chaine = row[1]
        row_strip = chaine.strip()
        
        # Pour chaque adresse du tableau.
        for adr in adresse_column:
            
            # On enlève les espaces au début et à la fin.
            adr_strip = adr.strip()
            
            # On test si les deux adresses correspondent.
            if row_strip == adr_strip:
                i = 0 # Compteur pour retrouver la ligne dans le tableau.
                
                # Pour chaque adresse dans la liste des adresses séléctionnées.
                for line in selected_addresses:
                    
                    # Si l'adresse de la ligne correspond à l'adresse de la BDD.
                    if line[0] == row_strip:
                        
                        # On modifie le statue pour indiquer que cet utilisateur s'est fait piéger.
                        selected_addresses[i] = (row_strip, "❌")
                        
                        # On relance l'affichage du tableau pour afficher la modification.
                        display_email_addresses(selected_addresses)
                    i += 1
    
    # On modifie aussi les données de l'histogramme 
    update_data()

#* Cette fonction permet de fermer toutes les fenêtres et/ou sessions ouverte pour fermer corectement
#* le programme.
def on_closing():
    root.destroy()  # Fermer la fenêtre tkinter
    plt.close()     # Fermer la fenêtre matplotlib
    sys.exit()      # Quitter le programme
#!####################################################################################################
#!------------------------------------------BASE DE DONNEE-------------------------------------------#
#!####################################################################################################

# Connexion à la base de données.
mydb, cursor = connexion_BDD()

# Test base de donnée.
BDD_nonVide(cursor)

# Récupère les données de la date actuelle.
data = todayData(mydb, cursor)

#!####################################################################################################
#!----------------------------------------------INTERFACE--------------------------------------------#
#!####################################################################################################

# Création de la fenêtre principale.
root = tk.Tk()
root.title("Gestion Phishing")

# Définir les informations de connexion au serveur SMTP.
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = '' #! Mettre l'adresse mail du compte quue vous souhaitez utiliser pour envoyer les mails
smtp_password = '' #! Mettre le MDP pour se connecter à se compte

# Choisir aléatoirement un dossier dans le répertoire courant des mails prédéfinis.
dossiers = os.listdir()
dossier_aleatoire = random.choice([d for d in dossiers if os.path.isdir(d)])

# Définir les chemins vers les fichiers HTML et image.
chemin_html = os.path.join(dossier_aleatoire, 'file.html')
chemin_image = os.path.join(dossier_aleatoire, 'mon_image.jpg')
chemin_alerte = os.path.join(dossier_aleatoire, 'alerte.jpg')

# Configuration de la taille de la fenêtre.
window_width = 1000
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_pos = int((screen_width - window_width) / 2)
y_pos = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
root.resizable(width=False, height=False)

# Création des trois frames.
frame1 = tk.Frame(root, bg="#D3D3D3", height=500, width=500)
frame2 = tk.Frame(root, bg="#D3D3D3",borderwidth=2, highlightthickness=2, highlightbackground="grey", height=500, width=500)

# Positionnement des frames dans la fenêtre.
frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=1, sticky="nsew")

# Définition de la taille minimale et maximale de la frame.
frame1.config(width=500, height=500, highlightthickness=0)
frame1.grid_propagate(False)

# Récupère l'année en cours pour afficher l'histogramme en fonction de celle-ci.
year = date.today().strftime("%Y")

# Première affichage (à l'ouverture) de l'histogramme.
pourcentage_pieges = [] 

# Récupère les infos en fonction de leur date pour contabiliser les utilisateurs selon le mois.
for i in range(1, 13):
    new_date = f"{year}-{i:02}"
    cursor.execute(f"SELECT COUNT(*) FROM menace WHERE YEAR(date_detection) = '{year}' AND MONTH(date_detection) = '{i:02}'")
    result = cursor.fetchone()[0]
    pourcentage_pieges.append(result)

# Données de pourcentage de personnes par jour sur 7 jours.
mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

# Création de la figure avec une taille personnalisée.
fig = plt.figure(figsize=(10, 10), dpi=50)
fig.subplots_adjust(top=0.95, bottom=0.2)

# Création du diagramme en barres avec les données générées.
ax = fig.add_subplot(111)
ax.set_ylim(0, 100)
ax.bar(mois, pourcentage_pieges, color='red', label='Nombre de personnes piégées')

# Ajout de la légende.
ax.legend(fontsize=15)

# Ajout des étiquettes de pourcentage au-dessus de chaque barre.
for i in range(len(mois)):
    ax.text(i,  pourcentage_pieges[i], f"{pourcentage_pieges[i]}", ha='center', va='bottom', fontsize=15)

# Agrandissement de la taille de la police des étiquettes.
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(rotation=90)

# Affichage du graphique dans la frame.
canvas = FigureCanvasTkAgg(fig, master=frame2)
canvas.draw()
canvas.get_tk_widget().pack()

# Création du tableau déroulant.
table = ttk.Treeview(frame1, columns=("col1", "col2"), show="headings")

# Ajout des colonnes.
table.heading("col1", text="Adresse",anchor="center")
table.heading("col2", text="Résultat", anchor="center")

# Centrage des colonnes dans leur cellule.
for col in table["columns"]:
    table.column(col, anchor="center")

# Configuration des poids des colonnes pour les centrer dans la frame.
for i, col in enumerate(table["columns"]):
    frame1.columnconfigure(i, weight=1)

# Ajout de l'espace autour du tableau.
table.grid(padx=10, pady=10)

# Centrage du tableau horizontalement dans sa frame.
table.grid(sticky="ew", columnspan=3)

# Variables global.
selected_addresses = []
table = []

# Ajout des widgets à la première frame.
selection_mode_var = tk.IntVar()
selection_mode_var.set(2) # Option par défaut.
all_addresses_rb = tk.Radiobutton(frame1, bg="#D3D3D3",text="Toutes les adresses", variable=selection_mode_var, value=1)
random_addresses_rb = tk.Radiobutton(frame1, bg="#D3D3D3",text="Sélection aléatoire", variable=selection_mode_var, value=2)
num_addresses_label = tk.Label(frame1, bg="#D3D3D3",text="Nombre d'adresses à sélectionner :")
num_addresses_entry = tk.Entry(frame1)
num_addresses_entry.insert(0, "20")
select_button = tk.Button(frame1, text="Sélectionner les adresses ", command=select_and_display_email_addresses)
send_button = tk.Button(frame1, text="Envoyer aux adresses", command=send_mail)

# Placement des widgets dans leur frame.
all_addresses_rb.grid(row=2, column=0, sticky="w", padx=10, pady=5)
random_addresses_rb.grid(row=1, column=0, sticky="w", padx=10, pady=10)
num_addresses_label.grid(row=1, column=1, sticky="w", padx=10, pady=10)
num_addresses_entry.grid(row=1, column=2, sticky="w", padx=10, pady=10)
select_button.grid(row=3, column=0, sticky="w", padx=10, pady=5)
send_button.grid(row=4, column=0, sticky="w", padx=10, pady=5)

# Créer un bouton pour lancer testAdresse.
button = tk.Button(frame1, text="Actualiser", command=lambda: testAdresse(data, table))
button.grid(row=5, column=0,sticky="w", padx=10, pady=5 )

# Ajouter le gestionnaire d'événements pour la fermeture de la fenêtre.
root.protocol("WM_DELETE_WINDOW", on_closing)  

# Boucle principale.
root.mainloop()
