Plugin_QGIS_SICEN
=================
Etant donné que nous considérons l’application SICEN seulement comme une interface de saisie, nous avons mis en place cette extension pour faciliter la visualisation et l’interrogation des données naturalistes saisies dans SICEN sur QGIS.

# I. Ouverture des données SICEN
La première partie du plugin va permettre d'ouvrir les données d'observation saisies dans SICEN, sur QGIS,  pour les visualiser et effectuer des analyses. L’avantage du plugin est qu’il permet de filtrer les données en fonction de plusieurs critères avant l’ouverture.

Pour réaliser le filtre il faut choisir des critères en fonction des 4 pages présentées ci-dessous, puis cliquer sur « OK ».

## Page 1 : Généralités
 - Par observateur(s)  : En fonction d’une liste déroulante générée automatiquement, avec « OU » comme critère.
 - Par localisation : En fonction d’une liste de communes prédéfinies, avec « OU » comme critère aussi.
 - Par Date : A vous de choisir vos dates dans le calendrier. Si vous choisissez la date du jour dans le calendrier elle sera ignorée.

		Exemple : Pour avoir les observations réalisées avant le 15 septembre 2013 vous devez sélectionner :
		            - Supérieur à date du jour (qui sera ignorée)
		            - Inférieur à 15 septembre 2013
 
## Page 2 : Filtre par Taxons
 - Par règne : Animal ou Végétal.
 - Par ordre : En fonction d’une liste déroulante générée automatiquement.
 - Par espèces : Sur le Nom vernaculaire ou le nom complet.

## Page 3 : Filtre par patrimonialité et statuts de protection
Sur cette page on retrouvera 3 onglets avec des cases à cocher pour faire des choix.

 - Onglet 3.1 : Présence sur une liste rouge
 - Onglet 3.2 : Espèces patrimoniales
 - Onglet 3.3 : Les différents statuts de protection


## Page 4 : Filtre par emprise
Cette page permet d’afficher les observations faites sur un polygone précis. Pour cela il faut avoir au préalable sélectionner une table et un polygone dans l’interface « carte » de QGIS. Déterminer une zone tampon autour du polygone puis cocher la case.


		NOTE : Les filtres des 3 pages précédentes seront aussi pris en compte !

# II. Export d’une liste d’espèces
La deuxième partie de l’extension permet d’exporter au format .csv (ouvrable directement dans Excel) une liste des espèces observées dans un polygone choisi.

Le fonctionnement est sensiblement le même que pour la page 4 de la première partie :

1. Sélectionnez une table et un polygone dans l’interface « carte » de QGIS.
2. Cliquez sur le bouton « Export liste d’espèces ».
3. Choisissez le lieu d’enregistrement et un nom de fichier.
4. Un petit message vous confirmera l’enregistrement.