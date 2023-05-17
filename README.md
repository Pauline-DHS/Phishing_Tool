# 🎣 Phishing Tool

## 📙 Description
Le Phishing Tool est un outil permettant de mener une campagne de phishing, afin de sensibiliser les utilisateurs à la sécurité informatique.

L'interface est divisée en deux frames : la partie de gauche permet de gérer l'envoi de mails et la sélection des adresses, et la partie de droite affiche un histogramme qui rend compte du nombre de personnes piégées par la campagne de mails par mois sur l'année.

L'utilisateur peut sélectionner toutes les adresses présentes dans le fichier CSV, ou indiquer un nombre d'adresses, dans les deux cas celles-ci seront tirées aléatoirement. Les données nécessaires à l'histogramme sont stockées dans une base de données à laquelle le script se connecte automatiquement au lancement du programme.

## 📧 Mails
Les codes HTML des corps des mails sont classés dans des dossiers avec leurs images. Il existe quatre types de mails : Google, Microsoft, Soissons et Gmail. Lors de l'envoi de mail, le programme sélectionne aléatoirement un de ces dossiers pour construire le mail à envoyer. Ainsi, il y a au total onze types de mails mélangés.

## 🌐 Pages web
Les boutons dans les mails redirigent les utilisateurs sur la page du prétendu organisme qui l'envoie. Il y a donc une page de connexion pour Google (incluant les mails Google mais aussi Gmail), une page de connexion Microsoft et une page de connexion Soissons. Une fois sur la page, si l'utilisateur rentre ses informations de connexion et clique sur le bouton de connexion, sur la page rien ne se passe mais une requête SQL se lance pour ajouter l'adresse mail de l'utilisateur à la base de données.

## ⬇️ Installation

### 📝 Prérequis
-> Héberger les pages web sur un serveur de sorte à ce que les agents puissent y accéder.

-> Héberger une base de données de type MySQL sur ce même serveur afin d'avoir accès à ses données, nommer la table "phishing_rapport" et la table "menace".

-> Création d'un faux compte mail (Gmail est recommandé).

-> Installer les librairies python nécessaire avec pip.

### ⚙️ Configuration
La base de données est protégée par un identifiant et un mot de passe qu'il faut renseigner dans le script du programme, dans la fonction "connexion_BDD", à la ligne 29 en renseignant l'hôte qui héberge la base de données (l'adresse IP), le user (l'identifiant), le password (le mot de passe) et la database (le nom de la base de données qui doit être "phishing_rapport").

Afin d'avoir la bonne redirection, il est nécessaire de changer l'url de redirection de chaque fichier html.

Il faut créer une clé d'application avec le faux compte Gmail et renseigner celle-ci à la ligne 329 (smtp_password) du programme, ainsi que l'adresse du compte à la ligne 328.

### 👨‍💻 Utilisation
Une fois les prérequis et la configuration effectués, lancer l'interface du Phishing Tool. Sélectionner les adresses souhaitées, choisir le nombre de mails à envoyer, puis cliquer sur "Envoyer". Les destinataires recevront alors un mail de phishing personnalisé, avec un bouton les redirigeant vers la page web de connexion. Si l'utilisateur entre ses informations de connexion, l'adresse mail de celui-ci sera enregistrée dans la base de données. Il suffira alors d'appuyer sur le bouton "actualiser" pour voir les résultats.

### ⚠️ Avertissement
L'utilisation de cet outil dans un contexte réel peut être illégale. Le Phishing Tool est destiné à un usage éducatif et doit être utilisé à des fins de sensibilisation.
