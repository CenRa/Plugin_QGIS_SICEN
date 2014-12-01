# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SICEN
                                 A QGIS plugin
 Filtre sur données SICEN
                              -------------------
        begin                : 2014-10-17
        copyright            : (C) 2014 by Guillaume COSTES (CENRA)
        email                : guillaume.costes@espaces-naturels.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import iface

# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from sicendialog import SICENDialog

import os.path
import psycopg2
import qgis
import datetime
import csv

class SICEN:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'sicen_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = SICENDialog()

    def initGui(self):
        self.toolBar = self.iface.addToolBar("SICEN")
        self.toolBar.setObjectName("SICEN")

        ## Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/sicen/sicen.png"),
            u"Ouverture des données SICEN", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.ouverture)

        # Add toolbar button and menu item
        self.toolBar.addAction(self.action)     
        self.iface.addPluginToMenu(u"SICEN", self.action)

        ## Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/sicen/sicen_export.png"),
            u"Export liste d'espèces", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.export)

        # Add toolbar button and menu item
        self.toolBar.addAction(self.action)
        self.iface.addPluginToMenu(u"SICEN", self.action)

        self.menu = QMenu()
        self.menu.setTitle( QCoreApplication.translate( "SICEN","&SICEN" ) )

        self.sicen_ouverture = QAction( QIcon(":/plugins/SICEN/sicen.png"), QCoreApplication.translate("SICEN", u"Ouverture des données SICEN" ), self.iface.mainWindow() )
        self.sicen_export = QAction( QIcon(":/plugins/SICEN/sicen_export.png"), QCoreApplication.translate("SICEN", u"Export liste d'espèces" ), self.iface.mainWindow() )
        
        self.menu.addActions( [self.sicen_ouverture, self.sicen_export] )
        
        menu_bar = self.iface.mainWindow().menuBar()
        actions = menu_bar.actions()
        lastAction = actions[ len( actions ) - 1 ]
        menu_bar.insertMenu( lastAction, self.menu )
        
        self.sicen_ouverture.triggered.connect(self.ouverture)
        self.sicen_export.triggered.connect(self.export)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&SICEN", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def ouverture(self):

        ### config.txt
        config = "//chemin_du_fichier/config.txt" # Chemin du fichier config

            # Fonction de lecture des lignes du fichier config
        def readline(n):
          with open(config, "r") as f:
            for lineno, line in enumerate(f):
              if lineno == n:
                return line.strip() # Permet d'enlever les retours chariots

            # Recuperation des donnees
        host = readline(10)
        port = readline(12)
        dbname = readline(14)
        user = readline(16)
        password = readline(18)
		
        # Connexion a la BD
        con = psycopg2.connect("dbname="+ dbname + " user=" + user + " host=" + host + " password=" + password + " port=" + port)
        cur = con.cursor()
		
        ## Creation des listes deroulantes
            # Listing de valeur des champs
        SQL_observateur = u"""SELECT DISTINCT observateur FROM _agregation_ra.observations ORDER BY observateur"""
        SQL_nom_com = u"""SELECT DISTINCT nom FROM saisie.commune ORDER BY nom"""
        SQL_nom_vern = u"""SELECT DISTINCT nom_vern FROM _agregation_ra.observations ORDER BY nom_vern"""
        SQL_nom_complet = u"""SELECT DISTINCT nom_complet FROM _agregation_ra.observations ORDER BY nom_complet"""
        SQL_ordre = u"""SELECT DISTINCT ordre FROM _agregation_ra.observations ORDER BY ordre"""

            # Generation des listes
        cur.execute(SQL_observateur)
        list_observateur = cur.fetchall()

        cur.execute(SQL_nom_com)
        list_nom_com = cur.fetchall()

        cur.execute(SQL_nom_vern)
        list_nom_vern = cur.fetchall()

        cur.execute(SQL_nom_complet)
        list_nom_complet = cur.fetchall()

        cur.execute(SQL_ordre)
        list_ordre = cur.fetchall()

        con.close()
            
            # Ajout des items dans les combobox
        self.dlg.observateur_1.clear()
        i = 0
        while i < len(list_observateur):
			self.dlg.observateur_1.addItems(list_observateur[i])
			i=i+1			
        self.dlg.observateur_1.setCurrentIndex(-1) # Pour ne pas commencer la liste au premier item

        self.dlg.observateur_2.clear()
        i = 0
        while i < len(list_observateur):
			self.dlg.observateur_2.addItems(list_observateur[i])
			i=i+1			
        self.dlg.observateur_2.setCurrentIndex(-1)
		
        self.dlg.observateur_3.clear()
        i = 0
        while i < len(list_observateur):
			self.dlg.observateur_3.addItems(list_observateur[i])
			i=i+1			
        self.dlg.observateur_3.setCurrentIndex(-1)
		
        self.dlg.observateur_4.clear()
        i = 0
        while i < len(list_observateur):
			self.dlg.observateur_4.addItems(list_observateur[i])
			i=i+1			
        self.dlg.observateur_4.setCurrentIndex(-1)

        self.dlg.nom_com_1.clear()
        i = 0
        while i < len(list_nom_com):
            self.dlg.nom_com_1.addItems(list_nom_com[i])
            i=i+1           
        self.dlg.nom_com_1.setCurrentIndex(-1)

        self.dlg.nom_com_2.clear()
        i = 0
        while i < len(list_nom_com):
            self.dlg.nom_com_2.addItems(list_nom_com[i])
            i=i+1           
        self.dlg.nom_com_2.setCurrentIndex(-1)

        self.dlg.nom_vern.clear()
        i = 0
        while i < len(list_nom_vern):
            self.dlg.nom_vern.addItems(list_nom_vern[i])
            i=i+1           
        self.dlg.nom_vern.setCurrentIndex(-1)

        self.dlg.nom_complet.clear()
        i = 0
        while i < len(list_nom_complet):
            self.dlg.nom_complet.addItems(list_nom_complet[i])
            i=i+1           
        self.dlg.nom_complet.setCurrentIndex(-1)

        self.dlg.ordre.clear()
        i = 0
        while i < len(list_ordre):
            self.dlg.ordre.addItems(list_ordre[i])
            i=i+1           
        self.dlg.ordre.setCurrentIndex(-1)

	# show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
		
            ### config.txt
            config = "//chemin_du_fichier/config.txt" # Chemin du fichier config

                # Fonction de lecture des lignes du fichier config
            def readline(n):
              with open(config, "r") as f:
                for lineno, line in enumerate(f):
                  if lineno == n:
                    return line.strip() # Permet d'enlever les retours chariots

                # Recuperation des donnees
            host = readline(10)
            port = readline(12)
            dbname = readline(14)
            user = readline(16)
            password = readline(18)
			
            # Requete filtre observateur
            if self.dlg.observateur_1.currentIndex() != -1 :
				sql_obs1 = """"observateur" = '""" + self.dlg.observateur_1.currentText() + "'"
            else :
                sql_obs1 = ''

            if self.dlg.observateur_2.currentIndex() != -1 :
                sql_obs2 = """"observateur" = '""" + self.dlg.observateur_2.currentText() + "'"
            else :
                sql_obs2 = ''

            if self.dlg.observateur_3.currentIndex() != -1 :
                sql_obs3 = """"observateur" = '""" + self.dlg.observateur_3.currentText() + "'"
            else :
                sql_obs3 = ''

            if self.dlg.observateur_4.currentIndex() != -1 :
                sql_obs4 = """"observateur" = '""" + self.dlg.observateur_4.currentText() + "'"
            else :
                sql_obs4 = ''

            reqwhere_obs = sql_obs1 + 'OR' + sql_obs2 + 'OR' + sql_obs3 + 'OR' + sql_obs4

            while reqwhere_obs[-2:] == 'OR' :
                reqwhere_obs = reqwhere_obs[:-2]
            while reqwhere_obs[:2] == 'OR' :
                reqwhere_obs = reqwhere_obs[2:]

            # Requete communes
                # Connexion a la BD
            con = psycopg2.connect("dbname="+ dbname + " user=" + user + " host=" + host + " password=" + password + " port=" + port)
            cur = con.cursor()

            if self.dlg.nom_com_1.currentIndex() != -1 :
                nom_com = self.dlg.nom_com_1.currentText()
                SQL_code_INSEE = u"""SELECT DISTINCT code_insee FROM saisie.commune WHERE nom = '""" + nom_com + "'"
                cur.execute(SQL_code_INSEE)
                list_code_INSEE = cur.fetchall()
                code_INSEE = list_code_INSEE[0][0]

                sql_insee_1 = """"code_insee" = '""" + code_INSEE + "'"
            else :
                sql_insee_1 = ''

            if self.dlg.nom_com_2.currentIndex() != -1 :
                nom_com = self.dlg.nom_com_2.currentText()
                SQL_code_INSEE = u"""SELECT DISTINCT code_insee FROM saisie.commune WHERE nom = '""" + nom_com + "'"
                cur.execute(SQL_code_INSEE)
                list_code_INSEE = cur.fetchall()
                code_INSEE = list_code_INSEE[0][0]

                sql_insee_2 = """"code_insee" = '""" + code_INSEE + "'"
            else :
                sql_insee_2 = ''

            reqwhere_insee = sql_insee_1 + 'OR' + sql_insee_2

            while reqwhere_insee[-2:] == 'OR' :
                reqwhere_insee = reqwhere_insee[:-2]
            while reqwhere_insee[:2] == 'OR' :
                reqwhere_insee = reqwhere_insee[2:]

            con.close()

            # Requete date
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            date_min = self.dlg.date_min.selectedDate().toString("yyyy-MM-dd")
            date_max = self.dlg.date_max.selectedDate().toString("yyyy-MM-dd")

            if date_min != today :
                sql_date_min = """"date_obs" >= '""" + date_min + "'"
            else :
                sql_date_min = ''

            if date_max != today :
                sql_date_max = """"date_obs" <= '""" + date_max + "'"
            else :
                sql_date_max = ''

            reqwhere_date = sql_date_min + 'AND' + sql_date_max

            while reqwhere_obs[-3:] == 'AND' :
                reqwhere_obs = reqwhere_obs[:-3]
            while reqwhere_obs[:3] == 'AND' :
                reqwhere_obs = reqwhere_obs[3:]

            # Requete regne
            if self.dlg.Animalia.isChecked() == 1 :
                sql_Animalia = """"regne" = 'Animalia'"""
            else :
                sql_Animalia = ''           

            if self.dlg.Plantae.isChecked() == 1 :
                sql_Plantae = """"regne" = 'Plantae'"""
            else :
                sql_Plantae = '' 

            reqwhere_regne = sql_Animalia + 'OR' + sql_Plantae

            while reqwhere_regne[-2:] == 'OR' :
                reqwhere_regne = reqwhere_regne[:-2]
            while reqwhere_regne[:2] == 'OR' :
                reqwhere_regne = reqwhere_regne[2:]

            # Requete ordre
            if self.dlg.ordre.currentIndex() != -1 :
                reqwhere_ordre = """"ordre" = '""" + self.dlg.ordre.currentText() + "'"
            else :
                reqwhere_ordre = ''

            # Requete sp
            if self.dlg.nom_vern.currentIndex() != -1 :
                sql_nom_vern = """"nom_vern" = '""" + self.dlg.nom_vern.currentText() + "'"
            else :
                sql_nom_vern = ''

            if self.dlg.nom_complet.currentIndex() != -1 :
                sql_nom_complet = """"nom_complet" = '""" + self.dlg.nom_complet.currentText() + "'"
            else :
                sql_nom_complet = ''

            reqwhere_sp = sql_nom_vern + 'OR' + sql_nom_complet

            while reqwhere_sp[-2:] == 'OR' :
                reqwhere_sp = reqwhere_sp[:-2]
            while reqwhere_sp[2:] == 'OR' :
                reqwhere_sp = reqwhere_sp[:2]

            # Requete filtre patrimonialite
            if self.dlg.LRD_01.isChecked() == 1 :
                sql_LRD_01 = """"LRD_01" IS NOT NULL """
            else :
                sql_LRD_01 = ''
                
            if self.dlg.LRD_07.isChecked() == 1 :
                sql_LRD_07 = """"LRD_07" IS NOT NULL """
            else :
                sql_LRD_07 = ''
                
            if self.dlg.LRD_26.isChecked() == 1 :
                sql_LRD_26 = """"LRD_26" IS NOT NULL """
            else :
                sql_LRD_26 = ''

            if self.dlg.LRD_38.isChecked() == 1 :
                sql_LRD_38 = """"LRD_38" IS NOT NULL """
            else :
                sql_LRD_38 = ''

            if self.dlg.LRD_42.isChecked() == 1 :
                sql_LRD_42 = """"LRD_42" IS NOT NULL """
            else :
                sql_LRD_42 = ''
                
            if self.dlg.LRD_69.isChecked() == 1 :
                sql_LRD_69 = """"LRD_69" IS NOT NULL """
            else :
                sql_LRD_69 = ''
                
            if self.dlg.LRD_73.isChecked() == 1 :
                sql_LRD_73 = """"LRD_73" IS NOT NULL """
            else :
                sql_LRD_73 = ''

            if self.dlg.LRD_74.isChecked() == 1 :
                sql_LRD_74 = """"LRD_74" IS NOT NULL """
            else :
                sql_LRD_74 = ''
                
            if self.dlg.LRR_Flore.isChecked() == 1 :
                sql_LRR_Flore = """"LRR_Flore" IS NOT NULL """
            else :
                sql_LRR_Flore = ''
                
            if self.dlg.LRR_Oiseaux.isChecked() == 1 :
                sql_LRR_Oiseaux = """"LRR_Oiseaux" IS NOT NULL """
            else :
                sql_LRR_Oiseaux = ''
                
            if self.dlg.LRR_Autre.isChecked() == 1 :
                sql_LRR_Autre = """"LRR_Autre" IS NOT NULL """
            else :
                sql_LRR_Autre = ''

            if self.dlg.LRN_Flore.isChecked() == 1 :
                sql_LRN_Flore = """"LRN_Flore" IS NOT NULL """
            else :
                sql_LRN_Flore = ''
                
            if self.dlg.LRN_Oiseaux.isChecked() == 1 :
                sql_LRN_Oiseaux = """"LRN_Oiseaux" IS NOT NULL """
            else :
                sql_LRN_Oiseaux = ''

            if self.dlg.LRN_Ortho.isChecked() == 1 :
                sql_LRN_Ortho = """"LRN_Ortho" IS NOT NULL """
            else :
                sql_LRN_Ortho = ''

            if self.dlg.LRN_Autre.isChecked() == 1 :
                sql_LRN_Autre = """"LRN_Autre" IS NOT NULL """
            else :
                sql_LRN_Autre = ''

            if self.dlg.LRE.isChecked() == 1 :
                sql_LRE = """"LRE" IS NOT NULL """
            else :
                sql_LRE = ''
                
            if self.dlg.UICN.isChecked() == 1 :
                sql_UICN = """"UICN" IS NOT NULL """
            else :
                sql_UICN = ''


            if self.dlg.PATRIMONIALITE.isChecked() == 1 :
                sql_PATRIMONIALITE = """"PATRIMONIALITE" IS NOT NULL """
            else :
                sql_PATRIMONIALITE = ''

            if self.dlg.PATRI01.isChecked() == 1 :
                sql_PATRI01 = """"PATRI01" IS NOT NULL """
            else :
                sql_PATRI01 = ''
                
            if self.dlg.PATRI07.isChecked() == 1 :
                sql_PATRI07 = """"PATRI07" IS NOT NULL """
            else :
                sql_PATRI07 = ''
                
            if self.dlg.PATRI26.isChecked() == 1 :
                sql_PATRI26 = """"PATRI26" IS NOT NULL """
            else :
                sql_PATRI26 = ''

            if self.dlg.PATRI38.isChecked() == 1 :
                sql_PATRI38 = """"PATRI38" IS NOT NULL """
            else :
                sql_PATRI38 = ''

            if self.dlg.PATRI42.isChecked() == 1 :
                sql_PATRI42 = """"PATRI42" IS NOT NULL """
            else :
                sql_PATRI42 = ''
                
            if self.dlg.PATRI69.isChecked() == 1 :
                sql_PATRI69 = """"PATRI69" IS NOT NULL """
            else :
                sql_PATRI69 = ''
                
            if self.dlg.PATRI73.isChecked() == 1 :
                sql_PATRI73 = """"PATRI73" IS NOT NULL """
            else :
                sql_PATRI73 = ''

            if self.dlg.PATRI74.isChecked() == 1 :
                sql_PATRI74 = """"PATRI74" IS NOT NULL """
            else :
                sql_PATRI74 = ''
                          

            if self.dlg.ZNIEFF.isChecked() == 1 :
                sql_ZNIEFF = """"ZNIEFF" IS NOT NULL """
            else :
                sql_ZNIEFF = ''           

            if self.dlg.DH_AnnII.isChecked() == 1 :
                sql_DH_AnnII = """"DH_AnnII" IS NOT NULL """
            else :
                sql_DH_AnnII = ''           

            if self.dlg.PD_38.isChecked() == 1 :
                sql_PD_38 = """"PD_38" IS NOT NULL """
            else :
                sql_PD_38 = ''           

            if self.dlg.PD_42.isChecked() == 1 :
                sql_PD_42 = """"PD_42" IS NOT NULL """
            else :
                sql_PD_42 = ''           

            if self.dlg.PN.isChecked() == 1 :
                sql_PN = """"PN" IS NOT NULL """
            else :
                sql_PN = ''           

            if self.dlg.PR.isChecked() == 1 :
                sql_PR = """"PR" IS NOT NULL """
            else :
                sql_PR = ''       

            reqwhere_pat = sql_LRD_01 + 'OR' + sql_LRD_07 + 'OR' + sql_LRD_26 + 'OR' + sql_LRD_38 + 'OR' + sql_LRD_42 + 'OR' + sql_LRD_69 + 'OR' + sql_LRD_73 + 'OR' + sql_LRD_74 + 'OR' + sql_LRE + 'OR' + sql_LRN_Flore + 'OR' + sql_LRN_Oiseaux + 'OR' + sql_LRN_Ortho + 'OR' + sql_LRN_Autre + 'OR' + sql_LRR_Flore + 'OR' + sql_LRR_Oiseaux + 'OR' + sql_LRR_Autre + 'OR' + sql_UICN + 'OR' + sql_PD_38 + 'OR' + sql_PD_42 + 'OR' + sql_PN + 'OR' + sql_PR + 'OR' + sql_DH_AnnII + 'OR' + sql_PATRI01 + 'OR' + sql_PATRI07 + 'OR' + sql_PATRI26 + 'OR' + sql_PATRI38 + 'OR' + sql_PATRI42 + 'OR' + sql_PATRI69 + 'OR' + sql_PATRI73 + 'OR' + sql_PATRI74 + 'OR' + sql_PATRIMONIALITE

            while reqwhere_pat.find('OROR') != -1 :
                reqwhere_pat = reqwhere_pat.replace('OROR','OR')
            while reqwhere_pat[-2:] == 'OR' :
                reqwhere_pat = reqwhere_pat[:-2]
            while reqwhere_pat[:2] == 'OR' :
                reqwhere_pat = reqwhere_pat[2:]

            # Requete geom
            if self.dlg.bouton_geom.isChecked() == 1 :

                layer = self.iface.activeLayer()
                if layer == None :
                    self.iface.messageBar().pushMessage(u"Vous devez sélectionner une table !", level=QgsMessageBar.WARNING, duration=5)

                else :                    
                    selection = layer.selectedFeatures()
                    if layer.selectedFeatureCount() == 1 :
                        for feature in selection:
                            geom = feature.geometry()
                            poly = geom.exportToWkt()
                    
                        buffer = self.dlg.buffer.text()
                        reqwhere_geom = " ST_intersects(geometrie,ST_Buffer(ST_geomFromText('" + poly + "',2154), " + buffer + " ))"

                        # Requete finale
                        reqwhere_final = '(' + reqwhere_obs + ')' + 'AND' + reqwhere_insee + 'AND' + reqwhere_ordre + 'AND' + reqwhere_sp + 'AND' + reqwhere_pat + 'AND' + reqwhere_regne + 'AND' + reqwhere_date + 'AND' + reqwhere_geom

                        # Nettoyage de la requete finale
                        while reqwhere_final.find('ANDAND') != -1 :
                            reqwhere_final = reqwhere_final.replace('ANDAND','AND')            
                        while reqwhere_final[-3:] == 'AND' :
                            reqwhere_final = reqwhere_final[:-3]
                        while reqwhere_final[:5] == '()AND' :
                            reqwhere_final = reqwhere_final[5:]
                        while reqwhere_final[:3] == 'AND' :
                            reqwhere_final = reqwhere_final[3:]

                        reqwhere_final = '(' + reqwhere_final + ')'
                        while reqwhere_final == '(())' :
                            reqwhere_final = ''           

                        ## Affichage de la table
                        table_name = 'observations_filtre'

                        uri = QgsDataSourceURI()
                        uri.setConnection(host ,port ,dbname ,user ,password)
                        uri.setDataSource("_agregation_ra", "observations", "geometrie", reqwhere_final, "gid")
                        layer = self.iface.addVectorLayer(uri.uri(), table_name, "postgres")

                        iface.messageBar().pushMessage(u"Extraction réussie : ", u" Pensez à renommer votre couches pour plus de lisibilité.", level=QgsMessageBar.INFO, duration=10)                        

                    elif layer.selectedFeatureCount() == 0 :
                        self.iface.messageBar().pushMessage(u"Vous devez sélectionner au moins un polygone !", level=QgsMessageBar.WARNING, duration=5)
                        reqwhere_geom = ''

                    else : 
                        self.iface.messageBar().pushMessage(u"Vous devez sélectionner qu'un seul polygone !", level=QgsMessageBar.WARNING, duration=5)
                        reqwhere_geom = ''                            
            else :
                # Requete finale
                reqwhere_final = '(' + reqwhere_obs + ')' + 'AND' + reqwhere_insee + 'AND' + reqwhere_ordre + 'AND' + reqwhere_sp + 'AND' + reqwhere_pat + 'AND' + reqwhere_regne + 'AND' + reqwhere_date

                # Nettoyage de la requete finale
                while reqwhere_final.find('ANDAND') != -1 :
                    reqwhere_final = reqwhere_final.replace('ANDAND','AND')            
                while reqwhere_final[-3:] == 'AND' :
                    reqwhere_final = reqwhere_final[:-3]
                while reqwhere_final[:5] == '()AND' :
                    reqwhere_final = reqwhere_final[5:]
                while reqwhere_final[:3] == 'AND' :
                    reqwhere_final = reqwhere_final[3:]

                reqwhere_final = '(' + reqwhere_final + ')'
                while reqwhere_final == '(())' :
                    reqwhere_final = '' 

                ## Affichage de la table
                table_name = 'observations_filtre'

                uri = QgsDataSourceURI()
                uri.setConnection(host ,port ,dbname ,user ,password)
                uri.setDataSource("_agregation_ra", "observations", "geometrie", reqwhere_final, "gid")
                layer = self.iface.addVectorLayer(uri.uri(), table_name, "postgres")

                self.iface.messageBar().pushMessage(u"Extraction réussie : ", u" Pensez à renommer votre couches pour plus de lisibilité.", level=QgsMessageBar.INFO, duration=10)
            pass

    def export(self):

        ### config.txt
        config = "//chemin_du_fichier/config.txt" # Chemin du fichier config

            # Fonction de lecture des lignes du fichier config
        def readline(n):
          with open(config, "r") as f:
            for lineno, line in enumerate(f):
              if lineno == n:
                return line.strip() # Permet d'enlever les retours chariots

            # Recuperation des donnees
        host = readline(10)
        port = readline(12)
        dbname = readline(14)
        user = readline(16)
        password = readline(18)

        layer = self.iface.activeLayer()

        if layer == None :
            self.iface.messageBar().pushMessage(u"Vous devez sélectionner une table !", level=QgsMessageBar.WARNING, duration=5)

        else :
            selection = layer.selectedFeatures()
            if (layer.selectedFeatureCount() == 1) :
                for feature in selection:
                    geom = feature.geometry()
                    poly = geom.exportToWkt()
                
                buffer = '100'

                con = psycopg2.connect("dbname="+ dbname + " user=" + user + " host=" + host + " password=" + password + " port=" + port)
                cur = con.cursor()

                SQL_list_sp = u"""SELECT DISTINCT classe::text, ordre::text, nom_complet::text, nom_vern::text, max(date_obs)::text AS derniere_obs FROM _agregation_ra.observations WHERE ST_intersects(geometrie,ST_Buffer(ST_geomFromText('""" + poly + "',2154), " + buffer + " )) GROUP BY classe, ordre, nom_complet, nom_vern ORDER BY nom_vern"""
                cur.execute(SQL_list_sp)
                data_sp = cur.fetchall()
                
                chemin_fichier = QFileDialog.getSaveFileName(None, 'Enregistrer sous...', "C:\Users\\" + str(os.environ.get("USERNAME")) + '\Desktop\liste_sp.csv', "Fichiers CSV (*.csv)")
                file = open(chemin_fichier, 'wb')
                file.write(u'\ufeff'.encode('utf8')) # BOM (optionel...Permet a Excel d'ouvrir proprement le fichier en UTF-8)
                writer = csv.writer(file, delimiter = ';') # délimiteur ';' pour faciliter l'ouverture avec Excel
                writer.writerow(['Classe', 'Ordre', 'Nom Complet', 'Nom Vernaculaire', u'Date Derniere Observation']) # Création des entêtes
               
                for row in data_sp : # Boucle d'écriture ligne par ligne dans le csv
                    list_sp = []
                    list_sp.append(row[0].encode('utf-8'))
                    list_sp.append(row[1].encode('utf-8'))
                    list_sp.append(row[2].encode('utf-8'))
                    if row[3] == None : # Si la valeur est 'None' l'encodage ne peut se faire donc boucle d'évitement
                        row3 = str(row[3])
                        row3 = ''
                    else :
                        row3 = row[3]
                    list_sp.append(row3.encode('utf-8'))
                    if row[4] == None :
                        row4 = str(row[3])
                        row4 = ''
                    else :
                        row4 = row[4]
                    list_sp.append(row4.encode('utf-8'))        
                    writer.writerow(list_sp)
                    
                file.close()
                self.iface.messageBar().pushMessage(u"Export réussi dans " + chemin_fichier , level=QgsMessageBar.INFO, duration=5)
                
            elif  (layer.selectedFeatureCount() == 0) :
                self.iface.messageBar().pushMessage(u"Vous devez sélectionner au moins un polygone !", level=QgsMessageBar.WARNING, duration=5)
                
            else :
                self.iface.messageBar().pushMessage(u"Vous devez sélectionner qu'un seul polygone !", level=QgsMessageBar.WARNING, duration=5)