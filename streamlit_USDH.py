# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 12:03:36 2022

@author: licke
"""

####################################################################################################
####################################################################################################
####################################################################################################

###                                         IMPORTATION DES MODULES NECESSAIRES :
    
    
# Data-viz :
    

import numpy as np
import pandas as pd


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import seaborn as sns


import plotly.express as px





# Traitement d'images : 
    
    
    
# Chargement d'images : 
    
from PIL import Image

import imageio






# Pour éviter d'avoir les messages warning : 

import warnings
warnings.filterwarnings('ignore')




# Streamlit :

import streamlit as st






##################################################################################################################### 
#####################################################################################################################
#####################################################################################################################

# Code pour avoir un écran large sur l'application Streamlit : 

    
st.set_page_config(layout = "wide", 
                   page_title = "Application statistiques USDH" , 
                   page_icon = "🤾")




#####################################################################################################################
#####################################################################################################################
#####################################################################################################################

### DICTIONNAIRE DES RENCONTRES déjà DISPUTEES PAR LES SM1 DE L'USDH EN 2022-2023 : 
    
dico_rencontres_USDH = {"J1" : ("Pouzauges" , "USDH") ,  
                        "J2" : ("USDH" , "Ligné") , 
                        "J3" : ("Authion" , "USDH") , 
                        "J4" : ("Connerre" , "USDH") , 
                        "J5" : ("USDH" , "St Berthevin") , 
                        "J6" : ("USDH" , "Pouzauges") , 
                        "J7" : ("Ligné" , "USDH") , 
                        "J8" : ("USDH" , "Authion") , 
                        "J9" : ("USDH" , "Connerre") , 
                        "J10" : ("St Berthevin" , "USDH") , 
                        "J12" : ("USDH" , "St Nazaire") , 
                        "J13" : ("Talmont" , "USDH")}







### DICTIONNAIRE DES COULEURS ASSOCIEES A CHAQUE EQUIPE DU CHAMPIONNAT SM1 2022-2023 : 

dico_couleurs = {"USDH" : "red" ,
                 "Pouzauges" : "#252522" , # noir et blanc
                 "Ligné" : "#E8E217" ,  # jaune
                 "Authion" : "#AD15C8" , # violet
                 "Connerre" : "#1957DB" ,   # bleu
                 "St Berthevin" : "#387A2D" ,  # vert foncé
                 "Clisson" : "#D205AD" ,  # noir et rose foncé
                 "RACC Nantes" : "#37B921" , # vert 
                 "Chabossière" : "#CA0924" , # rouge et noir
                 "St Nazaire" : "#FB0426" , # rouge et blanc
                 "Talmont" : "#D205AD",  # noir et rose 
                 "La Ferrière" : "#E8E217"}  # jaune







### DICTIONNAIRE DES LIENS VERS LES PHOTOS DES LOGOS ASSOCIEES A CHAQUE EQUIPE DU CHAMPIONNAT SM1 2022-2023 : 

dico_logos = {"USDH" : "./Logos/USDH.png" ,
              "Pouzauges" : "./Logos/pouzauges.png" ,
              "Ligné" : "./Logos/ligne.png" ,  
              "Authion" : "./Logos/authion.png" , 
              "Connerre" : "./Logos/la_ferte.png" ,
              "St Berthevin" : "./Logos/saint_berthevin.png" ,  
              "Clisson" : "./Logos/clisson.png" ,  
              "RACC Nantes" : "./Logos/racc_nantes.png" , 
              "Chabossière" : "./Logos/la_chabossiere.png" , 
              "St Nazaire" : "./Logos/saint_nazaire.png" , 
              "Talmont" : "./Logos/talmont.png", 
              "La Ferrière" : "./Logos/la_ferriere.png"} 




#####################################################################################################################
#####################################################################################################################
#####################################################################################################################


###                                                     FONCTIONS DE BASE :



## Fonction permettant de lire une image prise sur internet :

def load_image(file):

    image = imageio.imread(file)

    return image






    
    
## Fonction permettant d'importer la base de données des SM1 de l'USDH et de la nettoyer pour analyse : 
    
def importation_et_nettoyage(link = "https://github.com/jujuHandF144/streamlit-USDH-/blob/main/base_de_donnees_feuilles_de_match_SM1.xlsx?raw=true") : 
    
    """Importe et nettoie rapidement la base de données des matchs de championnat des SM1 de l'USDH en 2022-2023."""
    
    
    
    # 1) Importation du fichier excel : 
    
    df = pd.read_excel(link)
    
    
    
    
    
    
    # 2) Nettoyage : 
    
    
    # a) Suppression de la colonne 'Unnamed: 0' : 
    
    df = df.drop(columns = ['Unnamed: 0'])
    
    
    
    
    
    
    # b) Conversion de type de la colonne 'intervalle de temps' :   'object' --> 'intervalles' : 
    
    
    df["intervalle de temps"] = pd.cut(x = df["temps"] ,             # on catégorise la variable 'temps'
                                       bins = list(range(0,61,5)) ,  # on créer des intervalles d'amplitude 5 minutes entre 0 et 60
                                       include_lowest = True)        # on inclut la borne inférieure (0)
    







    return df





######################################################################################################################
######################################################################################################################

###                                                FONTIONS D'ANALYSE

######################################################################################################################
######################################################################################################################

## FONCTIONS LIEES A LA SITUATION NUMERIQUE D'UNE EQUIPE LORS D'1 MATCH PARTICULIER : 
    
######################################################################################################################
   
    
## Fonction permettant de retourner les périodes d'infériorité / d'égalité / de supériorité numérique de l'USDH lors d'un match précis (récupérées à l'oeil grâce à un graphique des périodes d'exclusion de l'USDH et de son adversaire lors de ce match) :
    
def periodes_situation_numerique_USDH(data , journee = "J1" , situation = "infériorité numérique" , format_dates = "float") :
    
    
    """Retourne la liste de TOUTES les périodes (date_debut , date_fin) jouées par l'USDH dans le type de situation numérique 
       (supériorité / infériorité / égalité numérique) renseigné en argument, au cours du match de championnat ayant eu lieu 
       lors de la journée renseignée."""
    
    
    
    # Fonction de conversion d'une date du format str au format float, exprimée en minutes : 
    
    en_minutes = lambda temps : int(temps.split(sep = ":")[0]) + (int(temps.split(sep = ":")[1])/60)

    
    
    
    # SI la journée de championnat renseignée a bien déjà eu lieu :

    if journee in dico_rencontres_USDH.keys() :
        
        
        
        
        # Journée 1 : Pouzauges - USDH

        if journee == "J1" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = [('13:40' , '14:05') , ('28:39' , '30:39') , ('37:27' , '39:27') , ('41:42' , '41:53') , 
                                ('41:53' , '43:53') , ('54:30' , '54:40') , ('54:40' , '56:40')]






                elif situation == "supériorité numérique" : 

                    periodes = [('4:37' , '6:37') , ('11:40' , '13:40') , ('33:55' , '35:55') , ('39:42' , '41:42') , ('52:30' , '54:30')]





                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '4:37') , ('6:37' , '11:40') , ('14:05' , '28:39') , ('30:39' , '33:55') , ('35:55' , '37:27') , 
                                ('39:27' , '39:42') , ('43:53' , '52:30') , ('56:40' , '60:00')]




                if format_dates == "str" : 

                    return periodes


                elif format_dates == "float" : 


                    # Conversion des dates données en minutes :

                    periodes = [(en_minutes(periode[0]) , en_minutes(periode[1])) for periode in periodes]

                    return periodes


                else : 

                    raise ValueError("paramètre attendu pour l'argument 'format_dates' : 'float' ou 'str'.")






            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")










        # Journée 2 : USDH - Ligné

        elif journee == "J2" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = [('27:59' , '29:59') , ('44:49' , '46:49')]







                elif situation == "supériorité numérique" : 

                    periodes = [('13:57' , '15:57') , ('32:54' , '34:54')]





                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '13:57') , ('15:57' , '27:59') , ('29:59' , '32:54') , ('34:54' , '44:49') , 
                                ('46:49' , '60:00')]




                if format_dates == "str" : 

                    return periodes


                elif format_dates == "float" : 


                    # Conversion des dates données en minutes :

                    periodes = [(en_minutes(periode[0]) , en_minutes(periode[1])) for periode in periodes]

                    return periodes


                else : 

                    raise ValueError("paramètre attendu pour l'argument 'format_dates' : 'float' ou 'str'.")






            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")









        # Journée 3 : Authion - USDH

        elif journee == "J3" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = [('18:41' , '20:16') , ('56:22' , '57:52')]





                elif situation == "supériorité numérique" : 

                    periodes = [('2:23' , '4:23') , ('10:42' , '12:42') , ('16:41' , '18:16') , ('48:18' , '50:18') , 
                                ('58:22' , '60:00')]





                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '2:23') , ('4:23' , '10:42') , ('12:42' , '16:41') , ('18:16' , '18:41') , ('20:16' , '48:18') , 
                                ('50:18' , '56:22') , ('57:52' , '58:22')]

                    


            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")









        # Journée 4 : Connerre - USDH

        elif journee == "J4" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = [('17:23' , '18:11') , ('24:24' , '27:49') , ('30:36' , '31:59') , ('44:32' , '46:32') , 
                                ('49:53' , '51:53') , ('56:17' , '58:17')]




                elif situation == "supériorité numérique" : 

                    periodes = [('3:27' , '5:27') , ('15:23' , '16:11') , ('19:25' , '21:25') , ('28:36' , '29:59') , 
                                ('41:45' , '43:45')]




                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '3:27') , ('5:27' , '15:23') , ('16:11' , '17:23') , ('18:11' , '19:25') , ('21:25' , '24:24') , 
                                ('27:49' , '28:36') , ('29:59' , '30:36') , ('31:59' , '41:45') , ('43:45' , '44:32') , ('46:32' , '49:53') , 
                                ('51:53' , '56:17') , ('58:17' , '60:00')]

                    

            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")









        # Journée 5 : USDH - St Berthevin

        elif journee == "J5" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = [('24:57' , '26:25') , ('58:29' , '60:00')]






                elif situation == "supériorité numérique" : 

                    periodes = [('19:53' , '21:53') , ('22:57' , '24:25') , ('39:51' , '41:51') , ('43:05' , '45:05')]





                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '19:53') , ('21:53' , '22:57') , ('24:25' , '24:57') , ('26:25' , '39:51') , 
                                ('41:51' , '43:05') , ('45:05' , '58:29')]





            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")











        # Journée 6 : USDH - Pouzauges (match retour)

        elif journee == "J6" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = [('8:00' , '10:00') , ('22:25' , '26:09') , ('47:24' , '49:24') , ('56:17' , '58:04') , ('59:15' , '60:00')]





                elif situation == "supériorité numérique" : 

                    periodes = [('19:22' , '21:22') , ('28:27' , '30:27') , ('51:24' , '53:24') , ('54:17' , '56:04')]





                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '8:00') , ('10:00' , '19:22') , ('21:22' , '22:25') , ('26:09' , '28:27') , 
                                ('30:27' , '47:24') , ('49:24' , '51:24') , ('53:24' , '54:17') , ('56:04' , '56:17') , 
                                ('58:04' , '59:15')]

                    

            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")


    
    
    
    
    
 

    
    
    
        # Journée 7 : Ligné - USDH (match retour)

        elif journee == "J7" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = []





                elif situation == "supériorité numérique" : 

                    periodes = [('5:56' , '7:56') , ('33:26' , '35:26')]





                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '5:56') , ('7:56' , '33:26') , ('35:26' , '60:00')]

                    

            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")

    
    
    
    
    
    
    
    
    
    
    
        # Journée 8 : USDH - Authion (retour)

        elif journee == "J8" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = []


                    

                elif situation == "supériorité numérique" : 

                    periodes = [('23:02' , '25:02') , ('50:31' , '52:31') , ('54:23' , '56:23') , ('58:53' , '60:00')]





                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '23:02') , ('25:02' , '50:31') , ('52:31' , '54:23') , ('56:23' , '58:53')]

                    

            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")
    
    
    
    
    
    

    
    

        # Journée 9 : USDH - Connerre (retour)

        elif journee == "J9" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = [('21:43' , '22:46') , ('32:44' , '34:44') , ('38:37' , '40:37') , ('55:21' , '57:21')]


                    

                elif situation == "supériorité numérique" : 

                    periodes = [('19:43' , '20:46') , ('28:12' , '30:12') , ('45:00' , '47:00') , ('58:56' , '60:00')]





                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '19:43') , ('20:46' , '21:43') , ('22:46' , '28:12') , ('30:12' , '32:44') , 
                                ('34:44' , '38:37') , ('40:37' , '45:00') , ('47:00' , '55:21') , ('57:21' , '58:56')]

                    

            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")
    
    
    
    
        
        
        
        
        # Journée 10 : USDH - St Berthevin

        elif journee == "J10" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = [('4:16' , '6:16') , ('23:29' , '25:43') , ('46:51' , '48:51')]





                elif situation == "supériorité numérique" : 

                    periodes = [('14:29' , '16:29') , ('27:22' , '27:43') , ('48:53' , '50:53') , ('56:23' , '58:23')]





                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '4:16') , ('6:16' , '14:29') , ('16:29' , '23:29') , ('25:43' , '27:22') ,  
                                ('27:43' , '46:51') , ('48:51' , '48:53') , ('50:53' , '56:23') , ('58:23' , '60:00')]

                    

                    
            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")
    

        
        
        
        

        
        # Journée 11 : RACC Nantes - USDH (la feuille de match n'a pas été enregistrée !)

        elif journee == "J11" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                periodes = []

                
                
                
            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")
        
        
        
        
        

        
        
        # Journée 12 : USDH - St Nazaire

        elif journee == "J12" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = [('5:49' , '7:49') , ('43:31' , '45:31')]





                elif situation == "supériorité numérique" : 

                    periodes = [('46:58' , '48:58') , ('56:59' , '58:59')]





                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '5:49') , ('7:49' , '43:31') , ('45:31' , '46:58') , ('48:58' , '56:59') ,  ('58:59' , '60:00')]

                    

                    
            else : 

                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique' , 'égalité numérique' ou 'supériorité numérique'.")
        
        
        
        
        
        
        
        # Journée 13 : Talmont - USDH

        elif journee == "J13" : 


            if situation in ["infériorité numérique" , "égalité numérique" , "supériorité numérique"] :


                if situation == "infériorité numérique" : 

                    periodes = [('13:42' , '15:42') , ('42:14' , '44:14')]





                elif situation == "supériorité numérique" : 

                    periodes = [('21:12' , '23:12') , ('23:23' , '25:23') , ('35:48' , '37:48') , ('54:15' , '56:15') ,  
                                ('58:52' , '60:00')]





                else :   # situation == "égalité numérique" : 

                    periodes = [('0:00' , '13:42') , ('15:42' , '21:12') , ('23:12' , '23:23') , ('25:23' , '35:48') , 
                                ('37:48' , '42:14') , ('44:14' , '54:15') , ('56:15' , '58:52')]
        
        
        
        
        
    
    
    
    
        if format_dates == "str" : 

            return periodes
        

        
        
        

        elif format_dates == "float" : 


            # Conversion des dates données en minutes :

            periodes = [(en_minutes(periode[0]) , en_minutes(periode[1])) for periode in periodes]

            return periodes
        
        
        


        else : 

            raise ValueError("paramètre attendu pour l'argument 'format_dates' : 'float' ou 'str'.")
            
            
            
            

    
    
    
    # SINON, si la journée de championnat renseignée n'a pas encore eu lieu :
    
    else : 
        
        raise ValueError(f"A ce stade de la saison, seules {len(dico_rencontres_USDH)} journées de championnat ont été disputées par l'USDH !")
    















## Fonction permettant de retourner les périodes d'infériorité / d'égalité / de supériorité numérique de l'équipe VOULUE lors d'un match bien précis :

def periodes_situation_numerique_equipe(data , journee = "J1" , situation = "infériorité numérique" , equipe = "USDH" , 
                                        format_dates = "float") :
    
    
    """Retourne la liste de TOUTES les périodes (date_debut , date_fin) jouées par l'équipe renseignée dans le type de situation numérique 
       (supériorité / infériorité / égalité numérique) renseigné en argument, au cours du match de championnat ayant eu lieu 
       lors de la journée renseignée."""
    
    
    
    # SI l'équipe renseignée jouait bel et bien lors de la journée de championnat renseignée :
    
    if equipe in data[data["journée"] == journee]["équipe"].unique() :
        
        
        # CAS 1 : si l'équipe renseignée est l'USDH, aucun soucis :
        
        if equipe == "USDH" : 
            
            situation_a_considerer = situation   # les situations numériques de l'équipe renseignée en argument sont celles de l'USDH
            
            
            
            
            
            
        # CAS 2 : si l'équipe renseignée N'est PAS l'USDH, attention : cette équipe est en infériorité (resp. supériorité) numérique lorsque l'USDH est en supériorité (rest.infériorité) numérique !
        
        else : 
            
            
            
            # Si je souhaite obtenir les périodes de SUPERIORITE numérique de cette équipe QUI N'EST PAS L'USDH...
            
            if situation == "supériorité numérique" : 
                
                situation_a_considerer = "infériorité numérique"   # ... Je dois regarder les périodes d'INFERIORITE numérique de l'USDH !
                
                
                
            
            # Si, à contrario, je souhaite obtenir les périodes d'INFERIORITE numérique de cette équipe QUI N'EST PAS L'USDH...
            
            elif situation == "infériorité numérique" : 
                
                situation_a_considerer = "supériorité numérique"   # ... Je dois regarder les périodes de SUPERIORITE numérique de l'USDH !
            
            
            
             
            # Sinon, si je souhaite obtenir les périodes d'EGALITE numérique de cette équipe QUI N'EST PAS L'USDH, rien à faire de différent car les 2 équipes sont à égalité numériques simultanément...
            
            else :   # situation == "égalité numérique" : 
                
                situation_a_considerer = "égalité numérique"   # Les périodes d'égalité numériques de cette équipe sont aussi celles de l'USDH, et réciproquement
            
            
            
            
            
         
        
        # On récupère la liste des périodes jouées par cette équipe dans ce type de situation numérique : 

        L_periodes_situation = periodes_situation_numerique_USDH(data = data , journee = journee , 
                                                                 situation = situation_a_considerer , 
                                                                 format_dates = format_dates)
        
        
        
        
        return L_periodes_situation
    
    
    
    
    
    
    
    
    # SINON, si l'équipe renseignée NE jouait PAS lors de la journée de championnat renseignée :
    
    else :
        
        
        # On récupère la liste des 2 équipes qui jouaient ce jour-là :
        
        L_equipes = [equipe for equipe in data[data["journée"] == journee]["équipe"].unique() if equipe != " "]
        
        
        
        
        if journee == "J1" : 
        
            raise ValueError(f"{equipe} ne jouait pas lors de la {journee[-1]}ère journée : les 2 équipes opposées ce jour-là étaient {L_equipes[0]} et {L_equipes[1]}")
                             
                             
                             
                             
        else : 
                             
            raise ValueError(f"{equipe} ne jouait pas lors de la {journee[-1]}ème journée : les 2 équipes opposées ce jour-là étaient {L_equipes[0]} et {L_equipes[1]}")
                             
                             
















## Fonction permettant de récupérer le nombre de buts marqués / encaissés + le différentiel de buts de l'équipe renseignée lors de CHAQUE période jouée par cette équipe dans la situation numérique voulue, au cours d'un match bien précis :
    
def bilan_situation_numerique_equipe(data , journee = "J5" , equipe = "USDH" , situation = "infériorité numérique") :
    
    """Retourne un dictionnaire indiquant, pour chaque période jouée par l'équipe renseignée dans le type de situation numérique 
       renseigné lors de la journée de championnat renseignée, le nombre buts marqués et encaissés + le différentiel de buts."""
    
    
    
    # SI l'équipe renseignée jouait bel et bien lors de la journée de championnat renseignée :
    
    if equipe in data[data["journée"] == journee]["équipe"].unique() :
        
        
        
        # On commence par récupérer le nom de l'adveraire de l'équipe renseignée lors de cette journée de championnat : 
        
        adversaire = [e for e in data[data["journée"] == journee]["équipe"].unique() if e not in [" " , equipe]]
        adversaire = adversaire[0]
        
        
        
        # On récupère, pour CHAQUE type de situation numérique possible (infériorité / supérorité / égalité numérique), la liste de TOUTES les périodes jouées par cette équipe au cours de ce match :
        
        L_periodes_inf = periodes_situation_numerique_equipe(data = data , journee = journee , situation = "infériorité numérique" , equipe = equipe , format_dates = "float")  # la liste des périodes d'INFERIORITE numérique de ette équipe
        L_periodes_sup = periodes_situation_numerique_equipe(data = data , journee = journee , situation = "supériorité numérique" , equipe = equipe , format_dates = "float")  # la liste des périodes de SUPERIORITE numérique de cette équipe
        L_periodes_ega = periodes_situation_numerique_equipe(data = data , journee = journee , situation = "égalité numérique" , equipe = equipe , format_dates = "float")      # la liste des périodes d'EGALITE numérique de cette équipe




        # 2) On regroupe à présent TOUTES ces périodes dans 1 seul et même dictionnaire d'associations (periode , situation_num_periode) , avec 'periode' un tuple des dates de début et de fin de la période : 

        dico_periodes = dict([(periode , "infériorité numérique") for periode in L_periodes_inf] + [(periode , "supériorité numérique") for periode in L_periodes_sup] + [(periode , "égalité numérique") for periode in L_periodes_ega])




        # 3) On récupère la LISTE triée en ordre croissant de ces périodes disjointes :

        L_periodes_triees = sorted(dico_periodes)  




        # 4) On instancie un dictionnaire initialement vide, destiné à contenir les associations (periode , bilan_periode) , avec 'bilan_periode' un dictionnaire lui aussi qui contiendra le nombre de buts marqués par l'USDH sur cette période, le nombre de buts encaissés ainsi que le différentiel de buts : 

        dico_bilan_periodes_equipe = {}




        # 5) Pour chacune des périodes de la liste L_periodes_triees, on récupère le nombre de buts marqués + le nombre de buts encaissés + le différentiel de buts en faveur de l'USDH :

        for periode , num_periode in zip(L_periodes_triees , range(len(L_periodes_triees))) : 


            date_debut = periode[0]  # date à laquelle débute la période
            date_fin = periode[1]    # date à laquelle se termine la période



            # Si l'on est en train de regarder la toute dernière période ==> il faut inclure les bornes inférieure ET supérieure.

            if num_periode == len(L_periodes_triees)-1 :


                # Filtrage des actions de jeu ayant eu lieu lors de cette période :

                data_periode = data[(data["journée"] == journee) & (data["temps"] >= date_debut) & (data["temps"] <= date_fin)]  # on INCLU la borne supérieure de la période





            # SINON, si l'on regarde n'importe quelle AUTRE période QUE la dernière => il faut inclure la borne inférieure MAIS exclure la borne supérieure (car le match débute forcément à égalité numérique, et que la 1ère exclusion survient et débute à la date de début de la 2ème période de la liste triée) :

            else : 


                # Filtrage des actions de jeu ayant eu lieu lors de cette période :

                data_periode = data[(data["journée"] == journee) & (data["temps"] >= date_debut) & (data["temps"] < date_fin)]  # on EXCLU la borne supérieure de la période





            # Récupération du nombre de buts marqués + encaissés par l'USDH  + du différentiel de buts de l'USDH sur cette période : 

            nbr_buts_marques_equipe_periode = len(data_periode[(data_periode["équipe"] == equipe) & (data_periode["action"].isin(["but" , "but 7m"]))])
            nbr_buts_encaisses_equipe_periode = len(data_periode[(data_periode["équipe"] == adversaire) & (data_periode["action"].isin(["but" , "but 7m"]))])
            differentiel_buts_equipe_periode = nbr_buts_marques_equipe_periode - nbr_buts_encaisses_equipe_periode



            # Stockage de la période et de son bilan dans le dictionnaire dédié : 

            dico_bilan_periodes_equipe[periode] = {f"buts marqués {equipe}" : nbr_buts_marques_equipe_periode , 
                                                   f"buts encaissés {equipe}" : nbr_buts_encaisses_equipe_periode , 
                                                   f"différentiel de buts {equipe}" : differentiel_buts_equipe_periode}
                                                   







        # 6) On N'extrait du dictionnaire dico_bilan_periodes_equipe QUE les périodes de la situation numérique souhaitée : 

        dico_bilan_periodes_situation = {}  # On instancie un dictionnaire initialement vide destiné à contenir le bilan de chaque période jouée par cette équipe UNIQUEMENT dans le type de situation numérique renseigné :

        
        # Pour chaque période (tous types de situations numériques confondus) :
        
        for periode , situation_numerique_periode in dico_periodes.items() : 
            
            
            # Si la situation numérique de l'équipe lors de cette période est celle que l'on souhaite voir :

            if situation_numerique_periode == situation : 


                dico_bilan_periodes_situation[periode] = dico_bilan_periodes_equipe[periode]  # on ajoute la période et son bilan au dictionnaire final qui sera retourné




                
                

        return dico_bilan_periodes_situation
    
    
    
    
    
    
    
    # SINON, si l'équipe renseignée ne jouait pas lors de la journée de championnat renseignée : 
    
    else : 
        
        
        # On récupère la liste des 2 équipes qui jouaient ce jour-là :
        
        L_equipes = [equipe for equipe in data[data["journée"] == journee]["équipe"].unique() if equipe != " "]
        
        
        
        
        if journee == "J1" : 
        
            raise ValueError(f"{equipe} ne jouait pas lors de la {journee[-1]}ère journée : les 2 équipes opposées ce jour-là étaient {L_equipes[0]} et {L_equipes[1]}.")
                             
                             
                             
                             
        else : 
                             
            raise ValueError(f"{equipe} ne jouait pas lors de la {journee[-1]}ème journée : les 2 équipes opposées ce jour-là étaient {L_equipes[0]} et {L_equipes[1]}.")
                             
                             





















## Fonction retournant une figure sur laquelle est tracée la droite des 60 minutes du match, découpée selon les périodes d'infériorité / de supériorité / d'égalité numérique de l'équipe renseignée lors de la journée de championnat renseignée :
    
def droite_sup_inf_numeriques_equipe(fig , ax , data , journee = "J1" , equipe = "USDH" , afficher_scores = True , 
                                     afficher_differentiels = True , afficher_bilan = True , show_title = True , 
                                     text_color = "black") :
    
    
    
    """Trace une droite des 60 minutes de match découpées et colorées selon la situation numérique dans laquelle se trouve
       l'équipe renseignée en argument, lors de la journée de championnat voulue."""
    
    
    
    
    if text_color == "white" : 
        
        fig.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")
    
    
    
    
    
    # SI l'équipe renseignée en argument jouait bel et bien lors de la journée de championnat renseignée :
    
    if equipe in data[data["journée"] == journee]["équipe"].unique() :
        
        
        
        # On commence par récupérer le nom de l'adveraire de l'équipe renseignée lors de cette journée de championnat : 
        
        adversaire = [e for e in data[data["journée"] == journee]["équipe"].unique() if e not in [" " , equipe]]
        adversaire = adversaire[0]
        
        
        
        # On récupére à présent, pour chaque type de situation numérique possible (infériorité / supériorité / égalité numérique), le dictionnaire du bilan de cette équipe lors de chaqué période jouée dans ce type de situation numérique :

        dico_bilan_periodes_inf_equipe = bilan_situation_numerique_equipe(data = data , journee = journee , equipe = equipe , situation = "infériorité numérique")
        dico_bilan_periodes_sup_equipe = bilan_situation_numerique_equipe(data = data , journee = journee , equipe = equipe , situation = "supériorité numérique")
        dico_bilan_periodes_ega_equipe = bilan_situation_numerique_equipe(data = data , journee = journee , equipe = equipe , situation = "égalité numérique")


        # A partir des clés de ces 3 dictionnaires, on récupèe pour chaque type de situation numérique possible, la liste des périodes jouées par cette équipe dans ce type de situation numérique :
        
        L_periodes_inf_equipe = list(dico_bilan_periodes_inf_equipe.keys())
        L_periodes_sup_equipe = list(dico_bilan_periodes_sup_equipe.keys())
        L_periodes_ega_equipe = list(dico_bilan_periodes_ega_equipe.keys())
        
        
        
        # On stocke les 3 listes dans une liste L_periodes_equipe : 

        L_periodes_equipe = [L_periodes_inf_equipe , L_periodes_ega_equipe , L_periodes_sup_equipe]
        
        
        
        # On définit les graduations en abscisses --> 1 graduation à chaque début / fin de période (avec comme texte, la date exprimée au format 'str') :

        xtick_couples = L_periodes_inf_equipe + L_periodes_ega_equipe + L_periodes_sup_equipe
        xticklabel_couples = periodes_situation_numerique_equipe(data = data , journee = journee , equipe = equipe , situation = "infériorité numérique" , format_dates = "str") + periodes_situation_numerique_equipe(data = data , journee = journee , equipe = equipe , situation = "égalité numérique" , format_dates = "str") + periodes_situation_numerique_equipe(data = data , journee = journee , equipe = equipe ,  situation = "supériorité numérique" , format_dates = "str") 


        
        
        # On personnalise la figure renseignée : 

        ax.spines["top"].set_color(None)
        ax.spines["left"].set_color(None)
        ax.spines["right"].set_color(None)
        ax.spines["bottom"].set_position(("data" , 0.4995))
        ax.spines["bottom"].set_color(text_color)

        ax.set_yticks([])
        ax.set_xticks([couple[0] for couple in xtick_couples] + [60.0])
        ax.tick_params(axis = 'x', colors = text_color)   # couleur des graduations
        ax.set_xticklabels([couple[0] for couple in xticklabel_couples] + ['60:00'] , rotation = 90)

        ax.set_xlim([0,60])
        ax.set_ylim([0.4995 , 0.5004])




        # Ligne symbolisant la mi-temps : 

        ax.plot([30 , 30] , 
                [0.4995 , 0.500405] , 
                ls = "--" , 
                color = "red")
        
        
        
        ax.text(x = 30 , 
                y = 0.50041 , 
                horizontalalignment = "center" , 
                s = "mi-temps" , 
                fontsize = 12 ,
                color = "red")



        


        # Pour chaque type de situation numérique possible (infériorité / supériorité / égalité numérique) : 

        k = 0

        for L_periodes_situations_nums_equipe , couleur in zip(L_periodes_equipe , ["red" , "#00D1FF" , "lime"]) : 

            
            if k == 0 : 

                situation_num = "infériorité numérique"

                

            elif k == 1 : 

                situation_num = "égalité numérique"


                
            elif k == 2 : 

                situation_num = "supériorité numérique"
                
                
                
                
            
            # Récupération du dictionnaire des bilans de cette équipe sur chaque période qu'elle a jouée dans ce type de situation numérique :

            dico_scores_situation_num = bilan_situation_numerique_equipe(data = data , journee = journee , equipe = equipe , situation = situation_num)




                

            # Pour chaque période jouée dans cette situation numérique, on trace le segment correspondant à la période dans la couleur adéquate :

            for periode in L_periodes_situations_nums_equipe : 

                
                # On dessine un rectangle pour cette période-là :
                
                x = periode
                y1 = [0.5 , 0.5]
                y2 = [0.50025 , 0.50025]
                
                
                # bord horizontal INFERIEUR du rectangle :

                ax.plot(list(periode) , 
                        [0.5 , 0.5] , 
                        color = couleur , 
                        lw = 1)
                
                
                
                # bord horizontal SUPERIEUR du rectangle :

                ax.plot(list(periode) , 
                        [0.50025 , 0.50025] , 
                        color = couleur , 
                        lw = 1)

                
                
                # bord vertical GAUCHE du rectangle :

                ax.plot(2*[periode[0]] , 
                        [0.5 , 0.50025] , 
                        color = couleur , 
                        lw = 1)


                
                # bord vertical DROIT du rectangle :

                ax.plot(2*[periode[1]] , 
                        [0.5 , 0.50025] , 
                        color = couleur , 
                        lw = 1)




                # On colorie la surface entre les 4 bornes du rectangle :

                ax.fill_between(x = x , 
                                y1 = y1 , 
                                y2 = y2 , 
                                color = couleur)





                
                
                # SI on souhaite afficher, pour cette période, le score ET/OU le différentiel de buts : 

                if (afficher_scores == True) or (afficher_differentiels == True) : 
                    

                    # Récupération du score des 2 équipes sur cette période : 

                    score_equipe_periode = dico_scores_situation_num[periode][f"buts marqués {equipe}"]
                    score_adversaire_periode = dico_scores_situation_num[periode][f"buts encaissés {equipe}"]
                    differentiel_periode = dico_scores_situation_num[periode][f"différentiel de buts {equipe}"]
                    
                    
                    
                    
                    
                    
                    # SI on souhaite afficher le score sur cette période : 
                        
                    if afficher_scores == True : 


                        # Annotation du score sur la figure au-dessus de la période correspondante :

                        ax.text(x = (periode[0] + periode[1])/1.995 , 
                                y = (0.5 + 0.50025)/2 , 
                                color = "black" , 
                                s = f"{score_equipe_periode} - {score_adversaire_periode}" , 
                                horizontalalignment = "center" , 
                                verticalalignment = "center" ,
                                fontsize = 11.75 , 
                                rotation = 90)





                    # Si on souhaite afficher le différentiels de buts sur cette période :

                    if afficher_differentiels == True :
                        
                        
                        
                        # Gestion de l'affichage du différentiel de buts, suivant son signe :

                    
                        if differentiel_periode > 0 :

                            differentiel_txt = "+ " + str(differentiel_periode)
                            color_differentiel = "green"



                        elif differentiel_periode == 0 : 

                            differentiel_txt = str(differentiel_periode)
                            color_differentiel = "orange"



                        else : 

                            differentiel_txt = "- " + str(abs(differentiel_periode))
                            color_differentiel = "red"

                        
                        
                        


                        # Annotation du différentiel de buts sur la figure au-dessus de la période correspondante :

                        ax.text(x = (periode[0] + periode[1])/2 , 
                                y = 0.500305 , 
                                color = color_differentiel , 
                                s = differentiel_txt , 
                                horizontalalignment = "center" , 
                                fontsize = 13.5)



                    
            
            
            # SI on souhaite afficher le bilan de cette équipe sur ce type de situation numérique : 
                        
            if afficher_bilan == True : 


                score_equipe_type_situation = sum([dico_scores_situation_num[periode][f"buts marqués {equipe}"] for periode in dico_scores_situation_num.keys()])         # le nbr de buts marqués par cette équipe dans ce type de situation numérique
                score_adversaire_type_situation = sum([dico_scores_situation_num[periode][f"buts encaissés {equipe}"] for periode in dico_scores_situation_num.keys()])   # le nbr de buts encaissés par cette équipe dans ce type de situation numérique
                differentiel_type_situation = score_equipe_type_situation - score_adversaire_type_situation   # le différentiel de buts de cette équipe sur ce type de situation numérique

                
                # Gestion de l'affichage des scores selon leur signe (signe + couleur) :
                
                if differentiel_type_situation > 0 :
                        
                    color_differentiel = "lime"
                    differentiel_text = "+ " + str(differentiel_type_situation)


                elif differentiel_type_situation == 0 : 

                    color_differentiel = "orange"
                    differentiel_text = str(differentiel_type_situation)


                else : 

                    color_differentiel = "red"
                    differentiel_text = "- " + str(abs(differentiel_type_situation))
                        
                        
                        
                

                # Annotation du bilan en bas à gauche de la figure :

                ax.text(x = 0 , 
                        y = 0.49965 - k*0.00005 , 
                        color = couleur , 
                        s = f"BILAN {situation_num} {equipe} :" ,
                        fontsize = 13)
                
                
                
                ax.text(x = 17.5 , 
                        y = 0.49965 - k*0.00005 , 
                        color = couleur , 
                        s = f"{score_equipe_type_situation} - {score_adversaire_type_situation}" , 
                        fontsize = 13)
                
                
                
                
                ax.text(x = 21.5 , 
                        y = 0.49965 - k*0.00005 , 
                        color = color_differentiel , 
                        s = f"({differentiel_text})"  , 
                        fontsize = 13)
                
                

            
            
            k += 1
            
            
            
            
                
            

        # Création manuelle de la légende à afficher :
        

        legende_inf = mpatches.Patch(color = "red" ,
                                     label = "infériorité numérique USDH")

        legende_sup = mpatches.Patch(color = "lime" , 
                                     label = "supériorité numérique USDH")

        legende_ega = mpatches.Patch(color = "#00D1FF" ,
                                     label = "égalité numérique")


        ax.legend(handles = [legende_inf , legende_sup , legende_ega] , 
                  loc = "lower right")




        

        # SI l'on souhaite ajouter un titre au graphique : 

        if show_title == True :

            fig.suptitle(f"{journee} : découpage du match {dico_rencontres_USDH[journee][0]} - {dico_rencontres_USDH[journee][1]} suivant la situation numérique de {equipe}." , 
                         fontsize = 21 , 
                         family = "serif" , 
                         color = text_color) 
            
            
            



















## Fonction permettant de calculer la durée totale passée par une équipe en supériorité / infériorité / égalité numérique (au choix) lors d'un match donné :
    
def duree_passee_situation_numerique_equipe(data , journee = "J1" , equipe = "USDH" , format_duree = "float" , 
                                            situation = "infériorité numérique") :
    
    
    """Retourne le temps passé par l'équipe renseignée en argument dans la situation numérique voulue, lors du match renseigné."""
    
    
    
    # SI l'équipe renseignée en argument jouait bel et bien lors de la journée de championnat renseignée :
    
    if equipe in data[data["journée"] == journee]["équipe"].unique() :
        
        
        
        # On récupère la liste de TOUTES les périodes que cette équipe a joué dans le type de situation numérique renseigné :
        
        L_periodes_situation_num_equipe = periodes_situation_numerique_equipe(data = data , journee = journee , equipe = equipe , situation = situation , format_dates = "float")




        # A partir de la liste ci-dessus, on récupère à présent la liste des durées de chaque période que cette équipe a joué dans le type de situation numérique renseigné : 

        L_durees_periodes_sitation_num_equipe = [periode[1] - periode[0] for periode in L_periodes_situation_num_equipe]




        # On calcule alors le temps TOTAL que cette équipe a joué dans ce type de situation numérique en sommant les durées contenues dans la liste ci-dessus :

        duree_totale_situation_num_equipe = sum(L_durees_periodes_sitation_num_equipe)




        # CAS 1 : SI je souhaite avoir cette durée au format float (en minutes) : 

        if format_duree == "float" :

            return duree_totale_situation_num_equipe
        
        


        # CAS 2 : SI je souhaite avoir cette durée en pourcentage des 60 minutes du match : 

        elif format_duree in ["pct" , "pourcentage" , "%"] :

            return (duree_totale_situation_num_equipe/60)*100



        else : 

            raise ValueError("paramètre attendu pour l'argument 'format_duree' : 'float' , 'pct' , 'pourcentage' ou '%'.")
            
            
            

            
            
            
            
            
            
    # SINON, si l'équipe renseignée ne jouait pas lors de la journée de championnat renseignée : 
    
    else : 
        
        
        # On récupère la liste des 2 équipes qui jouaient ce jour-là :
        
        L_equipes = [equipe for equipe in data[data["journée"] == journee]["équipe"].unique() if equipe != " "]
        
        
        
        
        if journee == "J1" : 
        
            raise ValueError(f"{equipe} ne jouait pas lors de la {journee[-1]}ère journée : les 2 équipes opposées ce jour-là étaient {L_equipes[0]} et {L_equipes[1]}.")
                             
                             
                             
                             
        else : 
                             
            raise ValueError(f"{equipe} ne jouait pas lors de la {journee[-1]}ème journée : les 2 équipes opposées ce jour-là étaient {L_equipes[0]} et {L_equipes[1]}.")
                             
                             
                             
                             
                             





######################################################################################################################

## FONCTIONS LIEES A LA SITUATION AU SCORE D'UNE EQUIPE LORS D'1 MATCH PARTICULIER : 
    
######################################################################################################################


## Fonction permettant de calculer le temps passé par une l'USDH derrière / à égalité / devant au score :

def duree_situation_score(data , journee = "J5") : 
    
    """Calcule et retourne dans un dictionnaire le temps passé par l'USDH à mener, à égalité et à être mené au score lors 
       de la journée renseignée en argument."""
    
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    # Création d'un dictionnaire destiné à recevoir les bornes des deltas à calculer :
    
    dates = {"USDH mène" : [] , 
             "égalité" : [] , 
             "adversaire mène" : []}
    
    
    
    
    # Création d'un dictionnaire destiné à recevoir les durées calculées :
    
    durees = {"USDH mène" : [] , 
              "égalité" : [] , 
              "adversaire mène" : []}
    
    
    
    
    # Création d'un dictionnaire destiné à recevoir les durées totales (= somme des durées calculées) :
    
    durees_totales = {"USDH mène" : [] , 
                      "égalité" : [] , 
                      "adversaire mène" : []}
    
    
    
    
    # Création d'un dictionnaire destiné à recevoir les % du temps du match (60 minutes) :
    
    pct_duree_totale = {"USDH mène" : [] , 
                        "égalité" : [] , 
                        "adversaire mène" : []}
    
    
    
    
    
    
    
    
    # On part du haut du DataFrame 'data' : 
    
    i = data_filtre.index[0]
    
    
    
    
    # GESTION DU 1ER INDICE (égalité 0-0 jusqua'au 1er but) : 
    
    couple = (0 , data_filtre["temps"].loc[i])

    duree = couple[1] - couple[0]
    
    
    dates["égalité"].append(couple)

    durees["égalité"].append(duree)
        
        
        
    
    
    
    
    # On parcourt le DataFrame 'data' dans son ensemble : pour chaque ligne de 'data' ...
    
    while i < data_filtre.index[-1] :
        
        
        
        # CAS 1 : SI la différence en faveur de l'USDH est STRICTEMENT POSITIVE (= USDH mène) : 
        
        if data_filtre["différence de buts"].loc[i] > 0 :
            
            # On passe à la ligne suivante :
            
            i += 1
            

            # Tant que la différence de buts en faveur de l'USDH reste STRICTEMENT POSITIVE (et que l'indice ne dépasse pas l'indice final) :
            
            while (data_filtre["différence de buts"].loc[i] > 0) and (i < data_filtre.index[-1]) :

                couple = (data_filtre["temps"].loc[i-1] , data_filtre["temps"].loc[i])

                dates["USDH mène"].append(couple)
                
                
                duree = couple[1] - couple[0]
                
                durees["USDH mène"].append(duree)

                
                i += 1
                
                
                
                
            couple = (data_filtre["temps"].loc[i-1] , data_filtre["temps"].loc[i])
                
            dates["USDH mène"].append(couple)
            
            
            duree = couple[1] - couple[0]
                
            durees["USDH mène"].append(duree)
            
            
            
            if i == data_filtre.index[-1] :
                
                couple = (data_filtre["temps"].loc[i] , 60)
            
                dates["USDH mène"].append(couple)


                duree = couple[1] - couple[0]

                durees["USDH mène"].append(duree)
            
            
            
                
                
     

    
    
    
    

        # CAS 2 : SI la différence en faveur de l'USDH est NULLE (= égalité) : 
        
        elif data_filtre["différence de buts"].loc[i] == 0 :
            
            # On passe à la ligne suivante :
            
            i += 1
            

            # Tant que la différence de buts en faveur de l'USDH reste NULLE (et que l'indice ne dépasse pas l'indice final) :
            
            while (data_filtre["différence de buts"].loc[i] == 0) and (i < data_filtre.index[-1]) :

                couple = (data_filtre["temps"].loc[i-1] , data_filtre["temps"].loc[i])
                
                dates["égalité"].append(couple)
                
                
                duree = couple[1] - couple[0]
                
                durees["égalité"].append(duree)

                
                i += 1
                
                
                
                
            couple = (data_filtre["temps"].loc[i-1] , data_filtre["temps"].loc[i])
            
            dates["égalité"].append(couple)
            
            
            duree = couple[1] - couple[0]
                
            durees["égalité"].append(duree)
            
            
            
            if i == data_filtre.index[-1] :
                
                couple = (data_filtre["temps"].loc[i] , 60)
            
                dates["égalité"].append(couple)


                duree = couple[1] - couple[0]

                durees["égalité"].append(duree)
            
            
            
                
                
                
                
                
                
        # CAS 3 : SI la différence en faveur de l'USDH est STRICTEMENT NEGATIVE (= adversaire mène) : 
        
        else :   # data_filtre["différence de buts"].loc[i] < 0 :
            
            # On passe à la ligne suivante :
            
            i += 1
            

            # Tant que la différence de buts en faveur de l'USDH reste STRICTEMENT NEGATIVE (et que l'indice ne dépasse pas l'indice final) :
            
            while (data_filtre["différence de buts"].loc[i] < 0) and (i < data_filtre.index[-1]) :

                couple = (data_filtre["temps"].loc[i-1] , data_filtre["temps"].loc[i])
                
                dates["adversaire mène"].append(couple)
                
                
                duree = couple[1] - couple[0]
                
                durees["adversaire mène"].append(duree)
                

                i += 1
                
                
                
                
            couple = (data_filtre["temps"].loc[i-1] , data_filtre["temps"].loc[i])
            
            dates["adversaire mène"].append(couple)
            
            
            duree = couple[1] - couple[0]
                
            durees["adversaire mène"].append(duree)
            
            
            
            if i == data_filtre.index[-1] :
                
                couple = (data_filtre["temps"].loc[i] , 60)
            
                dates["adversaire mène"].append(couple)


                duree = couple[1] - couple[0]

                durees["adversaire mène"].append(duree)
                
                
                
                
         
        
        # On calcule la durée totale en sommant les durées calculés et stockées dans des listes :
        
        for cle in durees_totales.keys() : 
            
            durees_totales[cle] = sum(durees[cle]) 
            
            pct_duree_totale[cle] = (durees_totales[cle]/60)*100
                
                
            
            
            
            
   
            
    return dates , durees , durees_totales , pct_duree_totale

















## Fonction permettant de récupérer les périodes l'USDH durant lesquelles l'USDH a mené / a été mené / a été à égalité au score lors d'un match précis :
    
def periodes_situation_score(data , situation = "USDH mène" , journee = "J5") :
    
    
    # On commence par récupérer les 4 dictionnaires retournés via la fonction 'duree_situation_score' ci-dessus :
    
    dates , durees , durees_totales , pct = duree_situation_score(data = data , journee = journee)
    
    
    
    
    
    # On s'intéresse uniquement à celui contenant les dates (date_debut , date_fin) des périodes de situations au score voulues :
 
    L = dates[situation]   # L est une liste de tuples (date_debut , date_fin)
    
    
    periodes = []   # la liste des périodes (date_debut , date_fin) qui sera retournée à la fin.
    
    
    # SI L est non vide : 
    
    if L != [] : 
        

        i = 0


        borne_inf = L[i][0]
        borne_sup = L[i][1]


        while i < len(L) :


            while (i < len(L)-1) and (borne_sup == L[i+1][0]) :

                borne_sup = L[i+1][1]

                i += 1




            periode = (borne_inf , borne_sup)

            periodes.append(periode)



            i += 1



            if i < len(L) :

                borne_inf = L[i][0]
                borne_sup = L[i][1]
                
                
             
        
        
            
    return periodes



















## Fonction permettant de connaître la dynamique (= nbr de buts marqués / encaissés) de jeu de l'USDH lors des x dernières minutes précédant la date t, lors de la journée précisée :
    
def dynamique_equipe(data , date = 29 , x_dernieres_minutes = 5 , journee = "J5" , equipe = "USDH") :
    
    """Retourne le différentiel des buts marqués / encaissés par l'équipe renseignée sur les x_dernieres_minutes précédant la 
       date renseignée, lors de la journée de championnat voulue."""
    
    
    
    # On commence par filtrer les données : 
    
    data_filtre = data[(data["journée"] == journee) & (data["temps"] <= date) & (data["temps"] >= date-x_dernieres_minutes)]
    
    
    
    
    
    # On compte à présent le nombre de buts marqués et encaissés par l'USDH lors de cette période du match : 
    
    buts_USDH = len(data_filtre[(data_filtre["équipe"] == "USDH") & (data_filtre["action"].isin(["but" , "but 7m"]))])
    buts_adv = len(data_filtre[(data_filtre["équipe"] != "USDH") & (data_filtre["action"].isin(["but" , "but 7m"]))])
    
    
    if equipe == "USDH" :
    
        differentiel = buts_USDH - buts_adv     # en faveur de l'USDH
        
    else : 
        
        differentiel = buts_adv - buts_USDH     # en faveur de l'équipe adverse
    
    
    
    
    
    
    
    return differentiel


















## Fonction permettant de connaître la dynamique (= nbr de buts marqués / encaissés) de jeu d'une équipe autour de la date des temps morts posés, lors de la journée précisée :
    
def dynamique_autour_TM(data , x_minutes_avant_apres = 5 , avant_ou_apres = "après" , journee = "J5" , 
                        equipe = "USDH" , TM_de = "USDH") :
    
    """Retourne le différentiel des buts marqués / encaissés par l'équipe renseignée sur les x_minutes_avant_apres 
       avant / après la (les) date(s) des temps morts posés par l'équipe 'TM_de', lors de la journée de championnat voulue."""
    
    
    # On commence par filtrer les données de la journée de championnat renseignée :
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    # On récupère la liste des 2 équipes opposées lors de cette journée :
    
    L_equipes = [e for e in data_filtre["équipe"].unique() if e != " "]
    
    
    
    
    
    # CAS 1 : l'équipe dont je souhaite connaître la dynamique (argument 'equipe') jouait bel et bien ce jour-là :
    
    if equipe in L_equipes :
        
        
        
        # CAS 1-a) : l'équipe dont je souhaite regarder les temps morts posés (argument 'TM_de') jouait bel et bien ce jour-là : 
        
        if TM_de in L_equipes :
    
    
    
    
            # On commence par récupèrer la (les) date(s) des éventuels temps morts posés par l'équipe voulue lors de cette rencontre : 

            L_dates_TM = [t for t in data_filtre[(data_filtre["équipe"] == TM_de) & (data_filtre["action"].isin(["temps mort d'équipe recevant" , "temps mort d'équipe visiteur"]))]["temps"].unique()]




            # Création d'un dictionnaire (initialement vide) destiné à contenir la dynamique de l'équipe 'equipe' : 

            dico_dynamique_TM = {}




            # SI l'équipe renseignée via le paramètre 'TM_de' a posé au moins un temps mort durant le match : 

            if L_dates_TM != [] : 


                # Pour chacune de ces dates de TM :

                for date in L_dates_TM : 



                    # On filtre UNIQUEMENT les actions de jeu de ce match ayant eu lieu x minutes après la date du TM : 

                    # SI on souhaite regarder les x minutes APRES le temps mort posé :
                    
                    if avant_ou_apres == "après" :

                        data_periode = data[(data["journée"] == journee) & (data["temps"] >= date) & (data["temps"] <= date + x_minutes_avant_apres)]




                    # SI on souhaite regarder les x minutes AVANT le temps mort posé :
                    
                    elif avant_ou_apres == "avant" :
                 

                        data_periode = data[(data["journée"] == journee) & (data["temps"] >= date - x_minutes_avant_apres) & (data["temps"] <= date)]




                    else : 
                        
                        raise ValueError("paramètre attendu pour l'argument 'x_minutes_avant_apres' : 'avant' ou 'après'.")






                    # On compte à présent le nombre de buts marqués et encaissés par l'équipe 'equipe' lors de cette période suivant le TM : 
                    
                    
                    # Buts marqués : 
                    
            
                    buts_marques_equipe = len(data_periode[(data_periode["équipe"] == equipe) & (data_periode["action"].isin(["but" , "but 7m"]))])

                    
                    
                    
                    
                    # Buts encaissés : 

                    
                    buts_marques_adv = len(data_periode[(data_periode["équipe"] != equipe) & (data_periode["action"].isin(["but" , "but 7m"]))])



                    
                    
                    
                    
                    differentiel = buts_marques_equipe - buts_marques_adv    # en faveur de l'équipe 'equipe'







                    # On stocke la dynamique dans le dictionnaire dédié : 

                    dico_dynamique_TM[(date , x_minutes_avant_apres)] = {f"buts marqués {equipe}" : buts_marques_equipe , 
                                                                         f"buts encaissés {equipe}" : buts_marques_adv , 
                                                                         "différentiel de buts" : differentiel}






            return dico_dynamique_TM
        
        
        
        
        
        # CAS 1-b) : l'équipe dont je souhaite regarder les temps morts posés (argument 'TM_de') NE jouait PAS ce jour-là : 
        
        else :  # TM_de not in L_equipes :
            
            
            raise ValueError(f"{TM_de} ne jouait pas lors de la {journee} : les 2 équipes opposées ce jour-là étaient {L_equipes[0]} et {L_equipes[1]}")
            
            
            

            
            
    # CAS 2 : l'équipe dont je souhaite regarder la dynamique (argument 'equipe') NE jouait PAS ce jour-là : 
        
    else :  # equipe not in L_equipes :


        raise ValueError(f"{equipe} ne jouait pas lors de la {journee} : les 2 équipes opposées ce jour-là étaient {L_equipes[0]} et {L_equipes[1]}")




        
        
        
        
        
        


















## Fonction permettant de récupérer le score de l'USDH à la date souhaitée, lors d'une journée au choix :
    
def score_USDH(data , journee = "J5" , temps = 29) : 
    
    """Retourne le score de l'USDH lors du match de la journée renseignée, au temps renseigné."""
    
    
    # On récupère le nom de l'adversaire de l'USDH lors de cette journée : 
    
    adv = [equipe for equipe in data[data["journée"] == journee]["équipe"].unique() if equipe not in ["USDH" , " "]]
    adv = adv[0]
    
    
    
    data_filtre = data[(data["journée"] == journee) & (data["équipe"] == "USDH")]
    
    
    
    # CAS 1 : le temps voulu est déjà renseigné dans data_filtre : 
    
    if temps in data_filtre["temps"].unique() : 
        
        
        return data_filtre[data_filtre["temps"] == temps]["score USDH"].loc[data_filtre[data_filtre["temps"] == temps].index[0]]
    
    
    
    
    
    
    # CAS 2 : sinon, on retourne le score au dernier pointage (SSI il y en avait un !!) avant le temps demandé :
    
    else : 
        
        
        # S'il y avait un pointage précédent : 
        
        if temps > data_filtre["temps"].min() :
        
            return data_filtre[data_filtre["temps"] <= temps]["score USDH"].loc[data_filtre[data_filtre["temps"] <= temps].index[-1]]
    
    
    
    
        # Sinon, c'est que le score de l'adversaire était nul :
        
        else : 
            
            return 0
        




















## Fonction permettant de récupérer le score de l'adversaire de l'USDH à la date souhaitée, lors d'une journée au choix :
    
def score_adversaire(data , journee = "J5" , temps = 29) : 
    
    """Retourne le score de l'adversaire de l'USDH lors du match de la journée renseignée, au temps renseigné."""
    
    
    # On récupère le nom de l'adversaire de l'USDH lors de cette journée : 
    
    adv = [equipe for equipe in data[data["journée"] == journee]["équipe"].unique() if equipe not in ["USDH" , " "]]
    adv = adv[0]
    
    
    
    data_filtre = data[(data["journée"] == journee) & (data["équipe"] == adv)]
    
    
    
    # CAS 1 : le temps voulu est déjà renseigné dans data_filtre : 
    
    if temps in data_filtre["temps"].unique() : 
        
        
        return data_filtre[data_filtre["temps"] == temps]["score adversaire"].loc[data_filtre[data_filtre["temps"] == temps].index[0]]
    
    
    
    
    
    
    # CAS 2 : sinon, on retourne le score au dernier pointage (SSI il y en avait un !!) avant le temps demandé :
    
    else : 
        
        
        # S'il y avait un pointage précédent : 
        
        if temps > data_filtre["temps"].min() :
        
            return data_filtre[data_filtre["temps"] <= temps]["score adversaire"].loc[data_filtre[data_filtre["temps"] <= temps].index[-1]]
    
    
    
        # Sinon, c'est que le score de l'adversaire était nul :
        
        else : 
            
            return 0
        
        
        
        
        
        
        
        
        








## Fonction permettant de repérer les séries de buts consécutifs encaissés d'une équipe, lors d'une rencontre donnée : 
    
def series_buts_encaisses(data , journee = "J5" , equipe = "USDH") : 
    
    """Retourne un dictionnaire des séries de buts consécutifs encaissés SANS MARQUER LE MOINDRE BUT par l'équipe renseignée 
       en argument, lors de la rencontre voulue."""
    
    
    
    # On commence par filtrer les données : 
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    dico_series = {}  # le dictionnaire des séries de buts consécutifs encaissés par l'équipe choisie (initialement vide).
    
    
    
    
    # Repérages des colonnes à utiliser : 
    
    if equipe == "USDH" : 
        
        col_score_equipe = "score USDH"
        col_score_adv = "score adversaire"
       
    
    else : 
        
        col_score_equipe = "score adversaire"
        col_score_adv = "score USDH"
        
        
    
    
    
    # On démarre au 1er indice :
    
    i = data_filtre.index[0]
    
    serie_en_cours = 0                                 # la série de buts consécutifs encaissés
    date_debut_serie = data_filtre["temps"].loc[i]     # la date du début de cette série
    date_fin_serie = data_filtre["temps"].loc[i]       # la date de la fin de cette série
    
    
    
    
    
    # On parcourt data_filtre de haut en bas, dans son ensemble : 
    
    while i < data_filtre.index[-1] :
    
        
        score_equipe_actuel = data_filtre[col_score_equipe].loc[i]     # score de l'équipe à l'issue de l'action de jeu en cours
        score_adv_actuel = data_filtre[col_score_adv].loc[i]           # score de l'équipe adverse à l'issue de l'action de jeu en cours
        
        score_equipe_suivant = data_filtre[col_score_equipe].loc[i+1]  # score de l'équipe à l'issue de l'action de jeu suivante
        score_adv_suivant =data_filtre[col_score_adv].loc[i+1]         # score de l'équipe adverse à l'issue de l'action de jeu suivante
        
        
        
        
        # Tant que le nombre de buts MARQUES de l'équipe reste identique ET QUE le nombre de buts ENCAISSES augmente :
        
        while (i+1 < data_filtre.index[-1]) and ((score_equipe_actuel == score_equipe_suivant) and (score_adv_suivant == score_adv_actuel + 1)) :
            

            
            serie_en_cours += 1   # la série de buts encaissés par cette équipe décrémente d'1 unité
            
            # On passe à l'action suivante :
            
            i += 1
            
            date_fin_serie = data_filtre["temps"].loc[i]  # On met à jour la date de la fin de la série en cours
            
            score_equipe_actuel = data_filtre[col_score_equipe].loc[i]     # score de l'équipe à l'issue de l'action de jeu en cours
            score_adv_actuel = data_filtre[col_score_adv].loc[i]           # score de l'équipe adverse à l'issue de l'action de jeu en cours

            score_equipe_suivant = data_filtre[col_score_equipe].loc[i+1]  # score de l'équipe à l'issue de l'action de jeu suivante
            score_adv_suivant =data_filtre[col_score_adv].loc[i+1]         # score de l'équipe adverse à l'issue de l'action de jeu suivante

        
        
        # On ajoute la série au dictionnaire dédié SSI IL Y A EU UNE SERIE DE BUTS CONSECUTIFS (= SSI serie_en_cours > 1) : 
        
        
        if serie_en_cours > 1 : 
        
            dico_series[(date_debut_serie , date_fin_serie)] = (0 , serie_en_cours)
        
        
        
        # On débute une nouvelle série : 
        
        i += 1
        
        # Mise à jour : 
        
        date_debut_serie = data_filtre["temps"].loc[i]
        date_fin_serie = data_filtre["temps"].loc[i]
        serie_en_cours = 0
        
        
        
    return dico_series






















## Fonction permettant de repérer les séries de buts consécutifs marqués d'une équipe, lors d'une rencontre donnée :
        
def series_buts_marques(data , journee = "J5" , equipe = "USDH") : 
    
    """Retourne un dictionnaire des séries de buts consécutifs marqués SANS ENCAISSER LE MOINDRE BUT par l'équipe renseignée 
       en argument, lors de la rencontre voulue."""
    
    
    # On récupère le nom de l'adversaire de l'équipe renseignée en argument : 
    
    adv = [e for e in data[data["journée"] == journee]["équipe"].unique() if e not in [equipe , " "]]
    adv = adv[0]
    
    
    
    # On récupère le dictionnaire des séries de buts encaissés par l'ADVERSAIRE DE L'USDH lors de cette même rencontre à l'aide de la fonction 'series_buts_encaisses' créée ci-dessus : 
    
    dico_series_encaisses_adv = series_buts_encaisses(data = data , journee = journee , equipe = adv)
    
    
    
    # On en déduit alors le dictionnaire des séries de buts marqués par l'équipe souhaitée, en inverssant l'ordre des éléments de chaque tuple du dictionnaire : 
    
    dico_serie_marques_equipe = {}
    

    
    for serie , score in dico_series_encaisses_adv.items() : 
        
        dico_serie_marques_equipe[serie] = (score[1] , score[0])    # inversion de l'ordre des buts
        
        
        
        

        
    
    return dico_serie_marques_equipe








#####################################################################################################################
#####################################################################################################################

###                                               FONCTIONS GRAPHIQUES :
 
#####################################################################################################################
#####################################################################################################################


## Fonction permettant de tracer l'évolution du score (de manière STATIQUE) des 2 équipes lors d'une rencontre précise :
    
def evolution_score(fig , ax , data , journee = "J5" , annotations  = "2min" , show_title = True , 
                    afficher_points = False , par_but_ou_par_minute = "par but" , colorer_gap = True , 
                    text_color = "black") :

    
    
    
    # SI on souhaite écrire le texte (graduations, titre, ...) en BLANC : 
    
    if text_color == "white" : 
        
        
        # Alors on ajoute un fond NOIR à la figure :
        
        fig.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")
        
        
        
        
        
    
    
    # On filtre UNIQUEMENT les données de la journée de championnat voulue : 
    
    data_filtre = data[data["journée"] == journee]
    

    
    
    # récupération du nom de l'équipe adverse : 

    adv = [equipe for equipe in data_filtre["équipe"].unique() if equipe not in ["USDH" , " "]]
    adv = adv[0]  


        
        


    
    scores = []  # la liste destinée à contenir la liste des scores minute par minute de l'USDH et celle de son adversaire.
    

        
    # Tracer de la courbe de score pour chacune des 2 équipes : 

    for equipe in ["USDH" , adv] :

        # SI on regarde l'USDH : 

        if equipe == "USDH" : 

            # la colonne de data_filtre indiquant le score de l'équipe est 'score_USDH' :

            col_score = "score USDH"
            col_score_adv = "score adversaire"
            
            linecolor = dico_couleurs[equipe]
            



        # SINON : 

        else : 

            # la colonne de data_filtre indiquant le score de l'équipe est 'score adversaire' :

            col_score = "score adversaire"
            col_score_adv = "score USDH"
            
    
            
            # SI la couleur de fond de la figure est le NOIR :
                
            if text_color == "white" : 
            
                
                # SI l'équipe est Pouzauges OU St Berthevin ==> la couleur associée à cette équipe est proche du noir, donc il faut une couleur flashy sur un fond noir :
                    
                if equipe in ["Pouzauges" , "St Berthevin"] : 
                
                    if equipe == "Pouzauges" : 
                        
                        linecolor = "white"
                        
                    else : 
                        
                        linecolor = "#16BD26"
                    
                    
                else : 
                    
                    linecolor = dico_couleurs[equipe]
        
        
            else : 
                
                linecolor = dico_couleurs[equipe]






        # SI je souhaite afficher l'évolution du score but par but :

        if par_but_ou_par_minute == "par but" :

            ax.plot(data_filtre[(data_filtre["équipe"].isin([equipe , " "])) & (data_filtre["action"].isin([" " , "but" , "but 7m"]))]["temps"] , 
                    data_filtre[(data_filtre["équipe"].isin([equipe , " "])) & (data_filtre["action"].isin([" " , "but" , "but 7m"]))][col_score] , 
                    color = linecolor , 
                    label = equipe , 
                    lw = 2)





            # SI je souhaite afficher les points EN PLUS des courbes : 

            if afficher_points == True : 


                ax.scatter(data_filtre[(data_filtre["équipe"].isin([equipe , " "])) & (data_filtre["action"].isin([" " , "but" , "but 7m"]))]["temps"] , 
                           data_filtre[(data_filtre["équipe"].isin([equipe , " "])) & (data_filtre["action"].isin([" " , "but" , "but 7m"]))][col_score] , 
                           color = linecolor)







        # SI je souhaite afficher l'évolution du score touts les minutes :

        elif par_but_ou_par_minute == "par minute" :


            # On récupère le score de l'équipe minute par minute (de la 0ème à la 60ème) grâce à la fonction 'score' :

            # SI l'équipe est l'USDH ==> fonction score_USDH pour récupérer le score de l'équipe :

            if equipe == "USDH" :

                scores_equipe = [score_USDH(data = data , journee = journee , temps = t) for t in range(0,61)]



            # SINON ==> fonction score_adversaire pour récupérer le score de l'équipe :

            else : 

                scores_equipe = [score_adversaire(data = data , journee = journee , temps = t) for t in range(0,61)]



            scores.append(np.array(scores_equipe))   # on stocke chaque liste de scores dans la liste 'scores'.



            # On trace alors le graphe obtenu :

            ax.plot(list(range(0,61)) , 
                    scores_equipe , 
                    color = linecolor , 
                    label = equipe)
            
        


        else : 

            raise ValueError("paramètre attendu pour l'argument 'par_but_ou_par_minute' : 'par but' ou 'par minute'.")








        # Ajout des annotations demandées : 

        for j in data_filtre[(data_filtre["équipe"] == equipe) & (data_filtre["action"] == annotations)].index : 
            
            # SI le score de l'équipe est SUPERIEUR à celui de l'adversaire (= courbe au-dessus) : 
            
            if data_filtre[col_score].loc[j] > data_filtre[col_score_adv].loc[j] :
            
                y_text = data_filtre[(data_filtre["équipe"] == equipe) & (data_filtre["action"] == annotations)][col_score].loc[j] + 2
                
            else : 
                
                y_text = data_filtre[(data_filtre["équipe"] == equipe) & (data_filtre["action"] == annotations)][col_score].loc[j] - 2
                

            ax.annotate(xy = (data_filtre[(data_filtre["équipe"].isin([equipe , " "])) & (data_filtre["action"] == annotations)]["temps"].loc[j] , data_filtre[(data_filtre["équipe"] == equipe) & (data_filtre["action"] == annotations)][col_score].loc[j]) ,
                        xytext = (data_filtre[(data_filtre["équipe"].isin([equipe , " "])) & (data_filtre["action"] == annotations)]["temps"].loc[j] , y_text) ,
                        color = text_color , 
                        text = annotations , 
                        horizontalalignment = "center" , 
                        verticalalignment = "center" , 
                        arrowprops = {"facecolor" : text_color , 
                                      "shrink" : 0.05})
            
            
            
            
            
            
            
            
    # Remplissage du gap entre les 2 courbes SSI on regarde le score minute par minute : 
    
    if par_but_ou_par_minute == "par minute" : 
        
        
        # SI je souhaite colorer l'espace séparant les 2 courbes :
        
        if colorer_gap == True :
        
        
            # On colorie le gap entre les courbes selon le signe du gap en faveur de l'USDH (devant = vert , derrière = orange) : 

            ax.fill_between(list(range(0,61)) , 
                            scores[0] ,          # array des scores de l'USDH 
                            scores[1] ,          # array des scores de l'adversaire 
                            where = (scores[0] > scores[1]) ,
                            color = "lime")


            ax.fill_between(list(range(0,61)) , 
                            scores[0] ,          # array des scores de l'USDH  
                            scores[1] ,          # array des scores de l'adversaire 
                            where = (np.array(scores[0]) < np.array(scores[1])) ,
                            color = "orange")





                
                
                


    # Personnalisation de la figure :        
            

    ax.legend(loc = "center right")


    ax.set_xlabel("minute" , fontsize = 15 , family = "serif" , color = text_color)
    ax.set_ylabel("score" , fontsize = 15 , family = "serif" , color = text_color)


    ax.set_xticks(range(0 , 61 , 2))
    ax.tick_params(axis = 'x', colors = text_color)   # couleur des graduations
    ax.set_xticklabels(range(0 , 61 , 2) , color = text_color)
    
    
    # yticks : 
    
    score_final_USDH = data_filtre[data_filtre["action"].isin([" " , "but" , "but 7m"])]["score USDH"].max()
    score_final_opposant = data_filtre[data_filtre["action"].isin([" " , "but" , "but 7m"])]["score adversaire"].max()
    
    
    ax.set_yticks(range(0 , max(score_final_USDH , score_final_opposant) , 2))
    ax.tick_params(axis = 'y', colors = text_color)   # couleur des graduations
    ax.set_yticklabels(range(0 , max(score_final_USDH , score_final_opposant) , 2) , color = text_color)
    
    

    ax.spines["top"].set_color(None)
    ax.spines["right"].set_color(None)
    ax.spines["bottom"].set_position(("data" , 0))
    ax.spines["left"].set_position(("data" , 0))
    
    ax.spines["bottom"].set_color(text_color)
    ax.spines["left"].set_color(text_color)

    
    


    # Ajout d'une grille en pointillés :

    
    if text_color == "black" :

        ax.grid(ls = ":" , color = text_color)


    
    



    # ligne symbolisant la mi-temps :

    ax.plot([30 , 30] , 
            [0 , max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 4.5] , 
            color = "#14A2D7" , 
            ls = "--" , 
            lw = 1.5)


    ax.text(x = 30 ,
            y = max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 4.85 ,
            s = "mi-temps" ,
            color = "#14A2D7" , 
            fontsize = 13 , 
            horizontalalignment = "center")
    
    

    
    
    
    
    
    
    
    # Récupération du bilan de l'USDH sur chaque période jouée dans chaque type de situation numérique + annotations du différentiel au-dessus de chaque période correspondante : 
    
    dico_bilans_inferiorite_num_USDH = bilan_situation_numerique_equipe(data = data , journee = journee , 
                                                                        equipe = "USDH" ,
                                                                        situation = "infériorité numérique")  # infériorité
    
    
    dico_bilans_superiorite_num_USDH = bilan_situation_numerique_equipe(data = data , journee = journee , 
                                                                        equipe = "USDH" ,
                                                                        situation = "supériorité numérique")  # supériotité
    
    
    
    
    
    # a) Pour chaque période d'INFERIORITE NUMERIQUE : 
    
    for periode_inferiorite in dico_bilans_inferiorite_num_USDH.keys() :
        
        debut_periode = periode_inferiorite[0]  # date de début de la période 
        fin_periode = periode_inferiorite[1]    # date de fin de la période
        differentiel = dico_bilans_inferiorite_num_USDH[periode_inferiorite]["différentiel de buts USDH"]  # le différentiel de buts sur cette période
        
        if differentiel > 0 : 
            
            c = "lime"
            differentiel = "+" + str(differentiel)
            
            
        elif differentiel == 0 : 
            
            c = "orange"
            
            
        else : 
            
            c = "red"
            differentiel = "- " + str((-1)*differentiel)
            
            
        
        # On trace un crochet ROUGE du début à la fin de la période, indiquant une période d'infériorité numérique de l'USDH :
        
        # ligne horizontale : 
        
        ax.plot([debut_periode , fin_periode] , 
                2*[max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 2] , 
                color = "red" , 
                lw = 2)
        
        
        # bornes verticales du crochet : 
        # borne gauche :
        
        ax.plot([debut_periode , debut_periode] , 
                [max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 1.8 , max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 2.2] , 
                color = "red" , 
                lw = 2)
        
        
        # borne droite :
        
        ax.plot([fin_periode , fin_periode] , 
                [max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 1.8 , max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 2.2] , 
                color = "red" , 
                lw = 2)
        
        
        
        # On inscrit au-dessus de cette ligne ROUGE le différentiel de buts EN FAVEUR DE L'USDH sur cette période : 
        
        ax.text(x = (debut_periode + fin_periode)/2 , 
                y = max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 2.75 , 
                s = differentiel,
                color = c , 
                fontsize = 14 , 
                horizontalalignment = "center")
        
        
        
        # On inscrit en-dessous de cette ligne ROUGE la mention "inf" : 

        ax.text(x = (debut_periode + fin_periode)/2 , 
                y = max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 1 , 
                s = "inf",
                color = "red" , 
                fontsize = 12 , 
                horizontalalignment = "center")
        
        
        
        
    
    
    # b) Pour chaque période de SUPERIORITE NUMERIQUE : 
    
    for periode_superiorite in dico_bilans_superiorite_num_USDH.keys() :
        
        debut_periode = periode_superiorite[0]  # date de début de la période 
        fin_periode = periode_superiorite[1]    # date de fin de la période
        differentiel = dico_bilans_superiorite_num_USDH[periode_superiorite]["différentiel de buts USDH"]  # le différentiel de buts sur cette période
        
        if differentiel > 0 : 
            
            c = "lime"
            differentiel = "+" + str(differentiel)
            
            
        elif differentiel == 0 : 
            
            c = "orange"  
            
        
            
        else : 
            
            c = "red"
            differentiel = "- " + str((-1)*differentiel)
            
            
    
    
        # On trace un crochet VERT du début à la fin de la période, indiquant une période de supériorité numérique de l'USDH :

        # ligne horizontale : 

        ax.plot([debut_periode , fin_periode] , 
                2*[max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 2] , 
                color = "#51E31F" , 
                lw = 2)


        # bornes verticales du crochet : 
        # borne gauche :

        ax.plot([debut_periode , debut_periode] , 
                [max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 1.8 , max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 2.2] , 
                color = "#51E31F" , 
                lw = 2)
        
    

        
        # borne droite :

        ax.plot([fin_periode , fin_periode] , 
                [max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 1.8 , max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 2.2] , 
                color = "#51E31F" , 
                lw = 2)
        
        
       



        # On inscrit au-dessus de cette ligne VERTE le différentiel de buts EN FAVEUR DE L'USDH sur cette période : 

        ax.text(x = (debut_periode + fin_periode)/2 , 
                y = max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 2.75 , 
                s = differentiel,
                color = c , 
                fontsize = 14 , 
                horizontalalignment = "center")
        
        
        
        # On inscrit en-dessous de cette ligne VERTE la mention "sup" : 

        ax.text(x = (debut_periode + fin_periode)/2 , 
                y = max(data_filtre["score USDH"].max() , data_filtre["score adversaire"].max()) + 1 , 
                s = "sup",
                color = "#46CF17" , 
                fontsize = 12 , 
                horizontalalignment = "center")


    
    
    
    
    
    
    # Affichage du titre (si souhaité) :
    
    if show_title == True : 
        
        
        if dico_rencontres_USDH[journee][0] == "USDH" :
        
            fig.suptitle(f"{journee} ({dico_rencontres_USDH[journee][0]} - {dico_rencontres_USDH[journee][1]}) : évolution du score au fil de la rencontre ({score_final_USDH} - {score_final_opposant})." , 
                         fontsize = 22.5 , family = "serif" , 
                         color = text_color)
            
            
            
        else :
        
            fig.suptitle(f"{journee} ({dico_rencontres_USDH[journee][0]} - {dico_rencontres_USDH[journee][1]}) : évolution du score au fil de la rencontre ({score_final_opposant} - {score_final_USDH})." , 
                         fontsize = 22.5 , family = "serif" , 
                         color = text_color)
        
        
        
        
        
        
        
    return ax






















## Fonction permettant de tracer l'évolution du GAP entre les 2 équipes lors d'une rencontre précise :
    
def evolution_gap_score(fig , ax , data , journee = "J5" , show_title = True , afficher_points = False , 
                        par_but_ou_par_minute = "par but") :

    
    
    # On filtre UNIQUEMENT les données de la journée de championnat voulue : 
    
    data_filtre = data[data["journée"] == journee]
    

    
    
    # récupération du nom de l'équipe adverse : 

    adv = [equipe for equipe in data_filtre["équipe"].unique() if equipe not in ["USDH" , " "]]
    adv = adv[0]  

        
    
    
    
    # SI je souhaite afficher l'évolution du score but par but :

    if par_but_ou_par_minute == "par but" :
        
        
        serie_dates = data_filtre[data_filtre["action"].isin([" " , "but" , "but 7m"])]["temps"]
        serie_dates.index = data_filtre[data_filtre["action"].isin([" " , "but" , "but 7m"])].index

        serie_buts_USDH = data_filtre[data_filtre["action"].isin([" " , "but" , "but 7m"])]["score USDH"]
        serie_buts_USDH.index = data_filtre[data_filtre["action"].isin([" " , "but" , "but 7m"])].index
        
        serie_buts_adv = data_filtre[data_filtre["action"].isin([" " , "but" , "but 7m"])]["score adversaire"]
        serie_buts_adv.index = data_filtre[data_filtre["action"].isin([" " , "but" , "but 7m"])].index
        
        
        serie_difference_buts = serie_buts_USDH - serie_buts_adv  # la liste des différences de buts en faveur de l'USDH
        
        

        
        ax.plot(serie_dates , 
                serie_difference_buts , 
                color = "red")
        
        
        
        
        # Annotation des PLUS GRAND et PLUS PETIT gaps enregistrés lors de cette rencontre : 
    
        # a) Recherche de l'indice du PLUS GRAND gap en faveur de l'USDH : 

        plus_grand_gap_en_faveur = serie_difference_buts.max()
        id_plus_grand_gap_en_faveur = serie_difference_buts.idxmax()


        # annotation du point sur la courbe : 

        ax.annotate(xy = (data_filtre["temps"].loc[id_plus_grand_gap_en_faveur] , plus_grand_gap_en_faveur) ,
                    xytext = (data_filtre["temps"].loc[id_plus_grand_gap_en_faveur] + 0.5 , plus_grand_gap_en_faveur + 1.5) ,
                    fontsize = 14 ,
                    s = f"retard MIN : {plus_grand_gap_en_faveur}" ,
                    color = "green" ,
                    horizontalalignment = "center" , 
                    arrowprops = {"color" : "black"})




        
        
        

        # b) Recherche de l'indice du PLUS GRAND gap en défaveur de l'USDH : 

        plus_grand_gap_subbis = serie_difference_buts.min()
        id_plus_grand_gap_subbis = serie_difference_buts.idxmin()


        # annotation du point sur la courbe : 

        ax.annotate(xy = (data_filtre["temps"].loc[id_plus_grand_gap_subbis] , plus_grand_gap_subbis) ,
                    xytext = (data_filtre["temps"].loc[id_plus_grand_gap_subbis] + 0.5 , plus_grand_gap_subbis - 1.5) ,
                    fontsize = 14 ,
                    s = f"retard MAX : {plus_grand_gap_subbis}" ,
                    color = "red" ,
                    horizontalalignment = "center" , 
                    arrowprops = {"color" : "black"})
        
        
        
        ax.fill_between(serie_dates , 
                        serie_difference_buts ,          # série des différences de buts en faveur de l'USDH 
                        where = (serie_difference_buts > 0) ,
                        color = "lime")
        
        
        
        ax.fill_between(serie_dates , 
                        serie_difference_buts ,          # série des différences de buts en faveur de l'USDH 
                        where = (serie_difference_buts < 0) ,
                        color = "orange")

        
        
        
        
        
        
        
    # SI je souhaite afficher l'évolution du score toutes les minutes :

    elif par_but_ou_par_minute == "par minute" :


        # On récupère le score de l'équipe minute par minute (de la 0ème à la 60ème) grâce à la fonction 'score' :

        serie_dates = pd.Series(list(range(61)))
        
        
        # fonction score_USDH pour récupérer le score de l'équipe :

        serie_buts_USDH = pd.Series([score_USDH(data = data , journee = journee , temps = t) for t in range(0,61)])

        
        # fonction score_adversaire pour récupérer le score de l'équipe :

        serie_buts_adv = pd.Series([score_adversaire(data = data , journee = journee , temps = t) for t in range(0,61)])



        # Calcul des différences de buts en faveur de l'USDH, minute par minute : 

        serie_difference_buts = serie_buts_USDH - serie_buts_adv
        
        
        
        
        # On trace la courbe du gap entre l'USDH et son adversaire : 
        
        ax.plot(serie_dates , 
                serie_difference_buts , 
                color = "red")
        
        
        
        
        
        
        
        
        # On colorie le gap entre les courbes selon le signe du gap en faveur de l'USDH (devant = vert , derrière = orange) : 

        ax.fill_between(serie_dates , 
                        serie_difference_buts ,          # série des différences de buts en faveur de l'USDH 
                        where = (serie_difference_buts > 0) ,
                        color = "lime")


        ax.fill_between(serie_dates , 
                        serie_difference_buts ,          # série des différences de buts en faveur de l'USDH 
                        where = (serie_difference_buts < 0) ,
                        color = "orange")
        
        
        
        
        
        
        
        
        # a) Recherche de l'indice du PLUS GRAND gap en faveur de l'USDH : 

        
        d = pd.DataFrame(data = data_filtre["score USDH"] - data_filtre["score adversaire"] , columns = ["gap"])
        
        
        plus_grand_gap_en_faveur = serie_difference_buts.max()
        id_plus_grand_gap_en_faveur = d[d["gap"] == plus_grand_gap_en_faveur].index[0]
        date_plus_grand_gap_en_faveur = data_filtre["temps"].loc[id_plus_grand_gap_en_faveur] # date exacte du plus grand gap en faveur de l'USDH
        
        
       
        
        
        
        
        
        
        
        
        # b) Recherche de l'indice du PLUS GRAND gap en défaveur de l'USDH : 

        plus_grand_gap_subbis = serie_difference_buts.min()
        id_plus_grand_gap_subbis = d[d["gap"] == plus_grand_gap_subbis].index[0]
        date_plus_grand_gap_subbis = data_filtre["temps"].loc[id_plus_grand_gap_subbis]
        
        
        
        
        
        

        
        
        
    else : 

        raise ValueError("paramètre attendu pour l'argument 'par_but_ou_par_minute' : 'par but' ou 'par minute'.")




            
            


    # SI je souhaite afficher les points EN PLUS des courbes : 

    if afficher_points == True : 


        ax.scatter(serie_dates , 
                   serie_difference_buts , 
                   color = "red")

        
    
    
    
    
    
    # Ligne horizontale en pointillés pour une différence de 0 but : 
    
    ax.plot([0 , 60] , 
            [0 , 0] , 
            color = "blue" , 
            ls = "--" , 
            lw = 2)





    # ligne verticale symbolisant la mi-temps :
    
    
    ax.plot([30 , 30] , 
            [serie_difference_buts.min() - 1 , serie_difference_buts.max() + 2] , 
            color = "green" , 
            ls = "--" , 
            lw = 3)
    
    

    
    
   
    
    
    

    # Annotations des périodes de supériorité numérique et des périodes d'infériorité numérique de l'USDH : 
    
    
    # On commence par récupérer le dictionnaire des bilans de l'USDH lors de chaque période qu'elle a joué pour chaque type de situation numérique possible (supériorité / infériorité / égalité numérique) :
    
    dico_bilans_inferiorite_num_USDH = bilan_situation_numerique_equipe(data = data , journee = journee , equipe = "USDH" ,
                                                                        situation = "infériorité numérique")  # infériorité
    
    
    dico_bilans_superiorite_num_USDH = bilan_situation_numerique_equipe(data = data , journee = journee , equipe = "USDH" ,
                                                                        situation = "supériorité numérique")  # supériorité
    
    
    dico_bilans_egalite_num_USDH = bilan_situation_numerique_equipe(data = data , journee = journee , equipe = "USDH" ,
                                                                    situation = "égalité numérique")  # égalité
    
    
    
    
    
    # a) Pour chaque période d'INFERIORITE NUMERIQUE : 
    
    for periode_inferiorite in dico_bilans_inferiorite_num_USDH.keys() :
        
        debut_periode = periode_inferiorite[0]  # date de début de la période 
        fin_periode = periode_inferiorite[1]    # date de fin de la période
        differentiel = dico_bilans_inferiorite_num_USDH[periode_inferiorite]["différentiel de buts USDH"]  # le différentiel de buts sur cette période
        
        if differentiel > 0 : 
            
            c = "green"
            differentiel = "+" + str(differentiel)
            
            
            
        elif differentiel == 0 : 
            
            c = "orange"
            differentiel = str(differentiel)
            
            
            
        else : 
            
            c = "red"
            differentiel = "- " + str((-1)*differentiel)
            
            
        
        # On trace un crochet ORANGE du début à la fin de la période, indiquant une période d'infériorité numérique de l'USDH :
        
        # ligne horizontale : 
        
        ax.plot([debut_periode , fin_periode] , 
                2*[plus_grand_gap_en_faveur + 3] , 
                color = "#E32121" , 
                lw = 4)
        
        
                    
                                       
        ax.text(x = (debut_periode + fin_periode)/2 , 
                y = plus_grand_gap_en_faveur + 2.5 , 
                s = differentiel,
                color = c , 
                fontsize = 14 , 
                horizontalalignment = "center")
        
        
        
        
    
    
    # b) Pour chaque période de SUPERIORITE NUMERIQUE : 
    
    for periode_superiorite in dico_bilans_superiorite_num_USDH.keys() :
        
        debut_periode = periode_superiorite[0]  # date de début de la période 
        fin_periode = periode_superiorite[1]    # date de fin de la période
        differentiel = dico_bilans_superiorite_num_USDH[periode_superiorite]["différentiel de buts USDH"]  # le différentiel de buts sur cette période
        
        if differentiel > 0 : 
            
            c = "green"
            differentiel = "+" + str(differentiel)
            
            
            
        elif differentiel == 0 : 
            
            c = "orange"
            differentiel = str(differentiel)
            
            

        else : 
            
            c = "red"
            differentiel = "- " + str((-1)*differentiel)
    
    
    
    
    
        # On trace un crochet VERTE du début à la fin de la période, indiquant une période de supériorité numérique de l'USDH :

        # ligne horizontale : 

        ax.plot([debut_periode , fin_periode] , 
                2*[plus_grand_gap_en_faveur + 3] , 
                color = "#28F011" , 
                lw = 4)


               
            
        # On inscrit au-dessus de cette ligne VERTE le différentiel de buts EN FAVEUR DE L'USDH sur cette période : 

        ax.text(x = (debut_periode + fin_periode)/2 , 
                y = plus_grand_gap_en_faveur + 2.5 , 
                s = differentiel,
                color = c , 
                fontsize = 14 , 
                horizontalalignment = "center")
        
        
        
        
        
        
        
        
     # c) Pour chaque période d'EGALITE NUMERIQUE : 
    
    for periode_egalite in dico_bilans_egalite_num_USDH.keys() :
        
        debut_periode = periode_egalite[0]  # date de début de la période 
        fin_periode = periode_egalite[1]    # date de fin de la période
        differentiel = dico_bilans_egalite_num_USDH[periode_egalite]["différentiel de buts USDH"]  # le différentiel de buts sur cette période
        
        if differentiel > 0 : 
            
            c = "green"
            differentiel = "+" + str(differentiel)
            
            
            
        elif differentiel == 0 : 
            
            c = "orange"
            differentiel = str(differentiel)
        
            
            
        else : 
            
            c = "red"
            differentiel = "- " + str((-1)*differentiel)
            
            
            
            
        
        # On trace un crochet ORANGE du début à la fin de la période, indiquant une période d'infériorité numérique de l'USDH :
        
        # ligne horizontale : 
        
        ax.plot([debut_periode , fin_periode] , 
                2*[plus_grand_gap_en_faveur + 3] , 
                color = "grey" , 
                lw = 4)
        
        
           
        
        # On inscrit au-dessus de cette ligne ORANGE le différentiel de buts EN FAVEUR DE L'USDH sur cette période : 
        
        ax.text(x = (debut_periode + fin_periode)/2 , 
                y = plus_grand_gap_en_faveur + 3.2 , 
                s = differentiel,
                color = c , 
                fontsize = 14 , 
                horizontalalignment = "center")
        
        
        
        
        
    
    
    

    
    # Affichage du titre (si souhaité) :
    
    if show_title == True : 
        
        fig.suptitle(f"{journee} : évolution du gap en faveur de l'USDH au fil de la rencontre." , 
                     fontsize = 28 , family = "serif")
        
        
        
        
        
        
        
        
        
        
    # Personnalisation de la figure :

    ax.set_xlabel("minute" , fontsize = 15 , family = "serif")
    ax.set_ylabel("gap" , fontsize = 15 , family = "serif")


    ax.set_xticks(range(0,61,2))


    ax.spines["top"].set_color(None)
    ax.spines["right"].set_color(None)
    ax.spines["bottom"].set_color(None)
    ax.spines["left"].set_position(("data" , 0))



    ax.grid(ls = "--")    
        
    
        
        
  
        
        
    return ax   


















## Fonction retournant un double histogramme VERTICAL des buts marqués / tirs tentés / arrêts / 2min / avertissements par tranche de 5 minutes d'une rencontre précise :
    
def double_vertical_histogram(fig , ax , data , type_action = ["but" , "but 7m"] , journee = "J1" , 
                              show_title = False , nbr_tranches = 12 , text_color = "black") : 
    
    
    
    from itertools import permutations
    
    
    
    # SI l'utilisateur souhaite écrire les textes (graduations, noms des axes, titre, ...) en BLANC : 
    
    if text_color == "white" : 
        
        
        # Alors la couleur de fond du graphique st NOIRE :
        
        fig.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")
    
    
    
    
    
    
    # Filtrage des données concernées : 

    data_filtre = data[(data["journée"] == journee) & (data["action"].isin(type_action))]
        
        
        
        


    # Récupération de l'adversaire de l'USDH ce jour-là : 

    adv = [equipe for equipe in data_filtre["équipe"].unique() if equipe != "USDH"]
    adv = adv[0]

    
    

        
    if nbr_tranches in [3 , 4 , 5 , 6 , 10 , 12, 15, 20, 30, 60] :
        
        
        if nbr_tranches != 12 : 
            
            data_filtre["intervalle de temps"] = pd.cut(df["temps"] , bins = np.arange(0 , 61 , 60//nbr_tranches) , 
                                                        include_lowest = True)
            
            

        
            
        # diagramme en barres verticales de l'USDH (vers le haut  ==>  height >= 0) :

        ax.bar(x = range(1, nbr_tranches + 1) ,   # car si on découpe les 60 minutes en intervalle de 5 minutes, on trouve 12 intervalles (5 x 12 = 60).
               height = data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index() , 
               align = 'center' , 
               color = dico_couleurs["USDH"] , 
               label = "USDH")



        # Idem pour son adversaire (vers le bas  ==>  height <= 0): 
        
        # Si l'adversaire est Pouzauges OU St Berthevin --> sa couleur associée est proche du noir ==> colorer les bordures des barres en blanc !
        
        if adv in ["Pouzauges" , "St Berthevin"] : 
            
            edgecolor = "white"
        
        
        else : 
            
            edgecolor = dico_couleurs[adv]
            
            
            
        ax.bar(x = range(1, nbr_tranches + 1) , 
               height = (-1)*data_filtre[data_filtre["équipe"] == adv]["intervalle de temps"].value_counts().sort_index() , 
               align = 'center' , 
               color = dico_couleurs[adv] , 
               label = adv , 
               edgecolor = edgecolor)   
            
            

        



        # 3) Personnalisation : 

        ax.spines["top"].set_color(None)
        ax.spines["right"].set_color(None)
        ax.spines["bottom"].set_position(("data" , 0))
        ax.spines["left"].set_position(("data" , 0.5))
        
        ax.spines["left"].set_color(text_color)
        ax.spines["bottom"].set_color(text_color)
        

        ax.set_xlim([0.5 , nbr_tranches + 0.5])
        
        


        # ticks : 

        # yticks : 

        max_action_USDH = data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().max()    # le plus grand nbr de 'type_action' effectués par l'USDH dans un intervalle de 5 minutes
        max_action_adv = data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().max()     # le plus grand nbr de 'type_action' effectués par l'adversaire dans un intervalle de 5 minutes


        ytick_inf = (-1)*max_action_adv   # borne inférieure des xticks
        ytick_sup = max_action_USDH + 1   # borne supérieure des xticks (+1 car un range s'arrête une unité avant la valeur spécifiée)


        yticks = list(np.arange(ytick_inf , 0 , 2)) + list(np.arange(0 , ytick_sup , 2))
        
        ax.set_yticks(yticks)
        ax.tick_params(axis = 'y', colors = text_color)   # couleur des graduations
        ax.set_yticklabels([abs(tick) for tick in yticks] , 
                            fontsize = 12 , 
                            color = text_color)
        
        
        
        





        # xticks :


        for tick in range(1 , nbr_tranches + 1) :
            
            

            ax.text(x = tick , 
                    y = ytick_inf + ytick_inf/1.15 - 1  ,       # ytick_inf - (9/10)*data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().mean() ,
                    s = f"{int(data_filtre['intervalle de temps'].value_counts().sort_index().index[tick-1].left)}ème - {int(data_filtre['intervalle de temps'].value_counts().sort_index().index[tick-1].right)}ème" ,
                    fontsize = 11 , 
                    rotation = 90 , 
                    color = text_color ,
                    verticalalignment = "center" , 
                    horizontalalignment = "center")


        ax.set_xticks(list(range(1 , nbr_tranches + 1)))
        ax.tick_params(axis = 'x', colors = text_color)   # couleur des graduations
        ax.set_xticklabels(nbr_tranches*[" "] , color = text_color)




        
        
        
        # titre du graphique ET label de l'axe des ordonnées : 

        
        # Si l'on regarde les tirs pris :

        if tuple(type_action) in list(permutations(["tir" , "but" , "but 7m"])) :

            if show_title == True :
                
                titre = f"{journee} ({dico_rencontres_USDH[journee][0]} - {dico_rencontres_USDH[journee][1]}) : répartition des tirs par tranche de 5 minutes"
                ax.set_title(titre , fontsize = 27 , family = "serif" , color = text_color , pad = 75)
                
            ylabel = "nombre de tirs tentés"
            ax.set_ylabel(ylabel , fontsize = 15 , family = "serif" , color = text_color)
        



        # Si l'on regarde les buts marqués :

        elif tuple(type_action) in list(permutations(["but" , "but 7m"])) :
            
            if show_title == True :
            
                titre = f"{journee} ({dico_rencontres_USDH[journee][0]} - {dico_rencontres_USDH[journee][1]}) : répartition des buts par tranche de 5 minutes"
                ax.set_title(titre , fontsize = 27 , family = "serif" , color = text_color , pad = 75)
                
            ylabel = "nombre de buts inscrits"
            ax.set_ylabel(ylabel , fontsize = 15 , family = "serif" , color = text_color)
        
            
            
            
        # Si l'on regarde les buts marqués DANS LE JEU :

        elif type_action == ["but"] :

            if show_title == True :
                
                titre = f"{journee} ({dico_rencontres_USDH[journee][0]} - {dico_rencontres_USDH[journee][1]}) : répartition des buts marqués dans le jeu par tranche de 5 minutes"
                ax.set_title(titre , fontsize = 27 , family = "serif" , color = text_color , pad = 75)
                
            ylabel = "nombre de buts inscrits dans le jeu"
            ax.set_ylabel(ylabel , fontsize = 15 , family = "serif" , color = text_color)
        
            
            
            
            
        # Si l'on regarde les buts marqués SUR 7M :

        elif type_action == ["but 7m"] :

            if show_title == True :
                
                titre = f"{journee} ({dico_rencontres_USDH[journee][0]} - {dico_rencontres_USDH[journee][1]}) : répartition des buts marqués sur 7m par tranche de 5 minutes"
                ax.set_title(titre , fontsize = 27 , family = "serif" , color = text_color , pad = 75)
                
            ylabel = "nombre de buts inscrits sur 7m"
            ax.set_ylabel(ylabel , fontsize = 15 , family = "serif" , color = text_color)
        
            
            
            
        # Si l'on regarde les punitions (cartons jaunes + exclusions) :

        elif tuple(type_action) in list(permutations(["avertissement" , "2min"])) :

            if show_title == True :
            
                titre = f"{journee} ({dico_rencontres_USDH[journee][0]} - {dico_rencontres_USDH[journee][1]}) : répartition des punitions reçues par tranche de 5 minutes"
                ax.set_title(titre , fontsize = 27 , family = "serif" , color = text_color , pad = 75)
                
            ylabel = "nombre de punitions"
            ax.set_ylabel(ylabel , fontsize = 15 , family = "serif" , color = text_color)
        
            
            
            
        
        # Si l'on regarde les avertissements (cartons jaunes) :

        elif type_action == ["avertissement"] :

            if show_title == True :
                
                titre = f"{journee} ({dico_rencontres_USDH[journee][0]} - {dico_rencontres_USDH[journee][1]}) : répartition des cartons jaunes reçus par tranche de 5 minutes"
                ax.set_title(titre , fontsize = 27 , family = "serif" , color = text_color , pad = 75)
                
            ylabel = "nombre de cartons jaunes"
            ax.set_ylabel(ylabel , fontsize = 15 , family = "serif" , color = text_color)
        

            
            
            
        # Si l'on regarde les exclusions (2 minutes) :

        elif type_action == ["2min"] :
            
            if show_title == True :
            
                titre = f"{journee} ({dico_rencontres_USDH[journee][0]} - {dico_rencontres_USDH[journee][1]}) : répartition des 2mins reçus par tranche de 5 minutes"
                ax.set_title(titre , fontsize = 27 , family = "serif" , color = text_color , pad = 75)
                
            ylabel = "nombre de 2min"
            ax.set_ylabel(ylabel , fontsize = 15 , family = "serif" , color = text_color)
            
            
            
            
        else : 
            
            raise ValueError("Erreur : type d'action INCONNU !")
        





        ax.set_xlabel(" ")







        # 4) Annotation des effectifs en face de chaque barre verticale (SSI effectif NON NUL) :

        # Pour chacune des 2 équipes : 

        for filtre in [data_filtre["équipe"] == "USDH" , data_filtre["équipe"] != "USDH"] :


            # Pour chaque intervalle de temps (12 au total) :

            for i , intervalle in zip(list(range(1,nbr_tranches + 1)) , data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index().index) :

                
                # CAS 1 : si le nombre de tranches souhaité vaut 3, 5 ou 15 --> la ligne de la mi-temps coupe la tranche du milieu et passe en plein sur le texte de l'effectif de cette tranche ==> décalage du texte sur un côté !
                
                if nbr_tranches in [3,5,15] : 
                    
                    if i == nbr_tranches//2 + 1 :  # S'il s'agit de la tranche du milieu :
                        
                        x = i + 0.075   # on décale le texte vers la droite
                        
                        
                    else : # SINON, s'il s'agit d'une autre tranche quelconque :
                        
                        x = i  # pas de soucis, on écrit le texte au milieu
                
                
                
                # CAS 2 : 
                
                else : 
                    
                    x = i

                

                # CAS 1 : s'il s'agit des barres de l'USDH : 
                    
                if False not in (filtre == (data_filtre["équipe"] == "USDH")).unique() : 

                    y = (7/6)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index().loc[intervalle]   #  data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index().loc[intervalle] + (1.25/10)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().mean()
                    color = dico_couleurs["USDH"]
                    txt = data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index().loc[intervalle]

                



                # CAS 2 : s'il s'agit des barres de l'adversaire de l'USDH : 

                else :

                    y = (10/9)*(-1)*data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().sort_index().loc[intervalle] - (1.25/10)*data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().mean()
                    color = edgecolor
                    txt = data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().sort_index().loc[intervalle]



                    
                # SI l'effectif de la barre est NON NUL ==> on l'écrit en face de sa barre :

                if txt != 0 : 
                    
                    ax.text(x = x , 
                            y = y , 
                            s = txt , 
                            horizontalalignment = "center" , 
                            verticalalignment = "center" , 
                            color = color , 
                            fontsize = 16)








        # 5) Ligne symbolisant la mi-temps :


        ord_mi_temps_1 = (4/3)*ytick_sup  # (5/4)*ytick_inf     # ytick_inf - 0.5
        ord_mi_temps_2 = (4/3)*ytick_inf  # (5/4)*ytick_sup     # (ytick_sup-1) + (ytick_sup-1)/5

        abs_mi_temps = (nbr_tranches + 1)/2


        ax.plot([abs_mi_temps , abs_mi_temps] , 
                [ord_mi_temps_1 , ord_mi_temps_2] , 
                 color = "#00D1FF" , 
                 ls = "--" , 
                 lw = 2)


        ax.text(x = abs_mi_temps , 
                y = (3/2)*ytick_sup ,   # (ytick_sup-1) + (ytick_sup-1)/5 + (4/10)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().mean() , 
                color = "#00D1FF" , 
                fontsize = 12 , 
                s = "mi-temps" , 
                verticalalignment = "center" , 
                horizontalalignment = "center")




        ax.legend(loc = "upper left")







        # 6) Inscription du score des 2 équipes lors de chaque période : 
        
        

            
        # SI on regarde les buts marqués :

        if (type_action == ["but" , "but 7m"]) or (type_action == ["but 7m" , "but"]) :

            score_M1_USDH = score_USDH(data = data , journee = journee , temps = 30)
            score_final_USDH = score_USDH(data = data , journee = journee , temps = 60)
            score_M2_USDH = score_final_USDH - score_M1_USDH   # nbr de buts inscrits en 2ème période par l'USDH

            score_M1_adv = score_adversaire(data = data , journee = journee , temps = 30)
            score_final_adv = score_adversaire(data = data , journee = journee , temps = 60)
            score_M2_adv = score_final_adv - score_M1_adv   # nbr de buts inscrits en 2ème période par l'adversaire de l'USDH





        else :

            score_M1_USDH = len(data_filtre[(data_filtre["équipe"] == "USDH") & (data_filtre["temps"] <= 30)])
            score_final_USDH = len(data_filtre[data_filtre["équipe"] == "USDH"])
            score_M2_USDH = score_final_USDH - score_M1_USDH   # nbr d'actions de ce type réalisées en 2ème période par l'USDH

            score_M1_adv = len(data_filtre[(data_filtre["équipe"] == adv) & (data_filtre["temps"] <= 30)])
            score_final_adv = len(data_filtre[data_filtre["équipe"] == adv])
            score_M2_adv = score_final_adv - score_M1_adv   # nbr d'actions de ce type réalisées en 2ème période par l'adversaire de l'USDH




        # SCORE M1 : 

        # USDH : 

        ax.text(y = (4/3)*ytick_sup ,   # (ytick_sup-1) + (ytick_sup-1)/5 + (4/10)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().mean() , 
                x = (1 + nbr_tranches/2)/2 - 2*nbr_tranches/50 ,   # (nbr_tranches + 0.5)/4 , 
                s = score_M1_USDH , 
                color = dico_couleurs["USDH"] , 
                fontsize = 30 , 
                verticalalignment = "center")


        # tiret : 

        ax.text(y = (4/3)*ytick_sup ,    # (ytick_sup-1) + (ytick_sup-1)/5 + (4/10)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().mean() , 
                x = (1 + nbr_tranches/2)/2 ,  # (nbr_tranches + 0.5)/4 + nbr_tranches/30 , 
                s = " -" , 
                color = text_color , 
                fontsize = 30 , 
                verticalalignment = "center")



        # adv : 

        ax.text(y = (4/3)*ytick_sup ,    # (ytick_sup-1) + (ytick_sup-1)/5 + (4/10)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().mean() , # ytick_inf + ytick_inf/5 + 0.1  , 
                x = (1 + nbr_tranches/2)/2 + 2*nbr_tranches/50 ,   # (nbr_tranches + 0.5)/4 + 2*nbr_tranches/30 , 
                s = score_M1_adv , 
                color = edgecolor , 
                fontsize = 30 , 
                verticalalignment = "center")







        # score M2 : 

        # USDH : 

        ax.text(y = (4/3)*ytick_sup ,    #(ytick_sup-1) + (ytick_sup-1)/5 + (4/10)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().mean() , 
                x = (nbr_tranches + 0.25)/2 + (0.25 + nbr_tranches/2)/2 - 2*nbr_tranches/50 , 
                s = score_M2_USDH , 
                color = dico_couleurs["USDH"] , 
                fontsize = 30 , 
                verticalalignment = "center")


        # tiret : 

        ax.text(y = (4/3)*ytick_sup ,    # (ytick_sup-1) + (ytick_sup-1)/5 + (4/10)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().mean() , 
                x = (nbr_tranches + 0.25)/2 + (0.25 + nbr_tranches/2)/2  ,     # 2.5*(nbr_tranches + 0.5)/4 + nbr_tranches/30 , 
                s = " -" , 
                color = text_color , 
                fontsize = 30 , 
                verticalalignment = "center")





        # adv : 

        ax.text(y = (4/3)*ytick_sup ,    # (ytick_sup-1) + (ytick_sup-1)/5 + (4/10)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().mean() , # ytick_inf + ytick_inf/5 + 0.1 , 
                x = (nbr_tranches + 0.25)/2 + (0.25 + nbr_tranches/2)/2 + 2*nbr_tranches/50 , 
                s = score_M2_adv , 
                color = edgecolor , 
                fontsize = 30 , 
                verticalalignment = "center")

            
            


        

        return ax
    
    
    
    
    
    
    else : 
        
        
        raise ValueError("nombre de tranches attendu : 3, 4, 5, 6, 10, 12, 15, 20, 30 ou 60.")





















## Fonction retourant un histogramme des différentiels de buts entre les 2 équipes par tranche de 5 minutes :
    
def histogram_differentiel_buts(fig , ax , data , journee = "J5" , show_title = False) : 
    
    
    
    # Filtrage des données concernées : 

    data_filtre = data[(data["journée"] == journee) & (data["action"].isin(["but" , "but 7m"]))]
        
        
        
        


    # Récupération de l'adversaire de l'USDH ce jour-là : 

    adv = [equipe for equipe in data_filtre["équipe"].unique() if equipe != "USDH"]
    adv = adv[0]


    
    
    
    # diagramme en barres verticales des différentiels de buts :
    
    # On calcule le DataFrame (à 1 seule colonne : 'intervalle de temps') des différentiels de buts en faveur de l'USDH : 
    
    data_differentiel = pd.DataFrame(data = data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index() - data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().sort_index()) 
    
    
    
    
    # CAS 1 : histogramme des différentiels positifs (en VERT) :
    
    data_differentiel_pos = data_differentiel[data_differentiel["intervalle de temps"] > 0]
    
    ax.bar(x = np.arange(1,13)[data_differentiel["intervalle de temps"] > 0] ,   # car si on découpe les 60 minutes en intervalle de 5 minutes, on trouve 12 intervalles (5 x 12 = 60).
           height = data_differentiel_pos["intervalle de temps"] , 
           align = 'center' , 
           color = '#1FBF28')
    
    
    
    
    
    # CAS 2 : histogramme des différentiels negatifs (en ROUGE) :
    
    data_differentiel_neg = data_differentiel[data_differentiel["intervalle de temps"] < 0]
    
    
    ax.bar(x = np.arange(1,13)[data_differentiel["intervalle de temps"] < 0] ,   # car si on découpe les 60 minutes en intervalle de 5 minutes, on trouve 12 intervalles (5 x 12 = 60).
           height = data_differentiel_neg["intervalle de temps"] , 
           align = 'center' , 
           color = 'red')





    # 3) Personnalisation : 

    ax.spines["top"].set_color(None)
    ax.spines["right"].set_color(None)
    ax.spines["bottom"].set_position(("data" , 0))
    ax.spines["left"].set_position(("data" , 0))
    



    # ticks : 

    # yticks : 
    
    min_diff = (data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index() - data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().sort_index()).min()
    max_diff = (data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index() - data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().sort_index()).max()

    
    ytick_inf = min_diff       # borne inférieure des yticks
    ytick_sup = max_diff + 1   # borne supérieure des yticks (+1 car un range s'arrête une unité avant la valeur spécifiée)



    ax.set_yticks(np.arange(ytick_inf , ytick_sup , 1))
    ax.set_yticklabels([abs(tick) for tick in np.arange(ytick_inf , ytick_sup , 1)] , 
                        fontsize = 12)



    
    # xticks :
    
    
    for tick in range(1,13) :
        
        ax.text(x = tick , 
                y = ytick_inf - 1.75 ,
                s = f"{int(data_filtre['intervalle de temps'].value_counts().sort_index().index[tick-1].left)}ème - {int(data_filtre['intervalle de temps'].value_counts().sort_index().index[tick-1].right)}ème" ,
                fontsize = 11 , 
                rotation = 90 ,
                verticalalignment = "center" , 
                horizontalalignment = "center")
        
        
    ax.set_xticks([])
    

    
    
    
    
    # titre du graphique : 
    

    # SI l'USDH joue à domicile :

    if "USDH" in data[data["journée"] == journee]["domicile"].unique() :

        titre = f"{journee} : USDH - {adv} (différence de buts par tranche de 5 minutes)"



    else : 

        titre = f"{journee} : {adv} - USDH (différence de buts par tranche de 5 minutes)"


    

    

    if show_title == True : 

        fig.suptitle(titre , fontsize = 35 , family = "serif" , fontweight = "bold")
        
        
    
    
    
    ax.set_ylabel("différence de buts" , fontsize = 15 , family = "serif")
    ax.set_xlabel(" ")
    
    
    
    



    # 4) Annotation des effectifs en face de chaque barre :

   

    # Pour chaque intervalle de temps (12 au total) :

    for i , intervalle in zip(list(range(1,13)) , data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index().index) :


        x = i
        
        differentiel_buts = data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index().loc[intervalle] - data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().sort_index().loc[intervalle]


        if differentiel_buts > 0 :
            
            couleur = "#1FBF28"
            txt = "+ " + str(differentiel_buts)
            
        elif differentiel_buts == 0 : 
            
            couleur = "orange"
            txt = "0"
            
        else : 
            
            couleur = "red"
            txt = "- " + str(abs(differentiel_buts))
            
            
        if differentiel_buts >= 0 :
            
            y = differentiel_buts + 0.2
            
        else : 
            
            y = differentiel_buts - 0.2
        
        
    




        ax.text(x = x , 
                y = y , 
                s = txt , 
                horizontalalignment = "center" , 
                verticalalignment = "center" , 
                color = couleur , 
                fontsize = 16)








    # 5) Ligne symbolisant la mi-temps :


    ord_mi_temps_1 = ytick_inf - 0.5
    ord_mi_temps_2 = ytick_sup - 0.5  # car on avait déjà ajouté + 1 dans le range des xticks

    abs_mi_temps = 6.5


    ax.plot(2*[abs_mi_temps] , [ord_mi_temps_1 , ord_mi_temps_2] , 
            color = "green" , 
            ls = "--" , 
            lw = 2)


    ax.text(x = abs_mi_temps , 
            y = ord_mi_temps_2 + 0.55 , 
            color = "green" , 
            fontsize = 12 , 
            s = "mi-temps" , 
            verticalalignment = "center" , 
            horizontalalignment = "center")









    # 6) Inscription du score des 2 équipes lors de chaque période : 

    score_M1_USDH = data[(data["journée"] == journee) & (data["temps"] <= 30)]["score USDH"].loc[data[(data["journée"] == journee) & (data["temps"] <= 30)].index[-1]]
    score_final_USDH = data[data["journée"] == journee]["score USDH"].max()
    score_M2_USDH = score_final_USDH - score_M1_USDH   # nbr de buts inscrits en 2ème période par l'USDH

    score_M1_adv = data[(data["journée"] == journee) & (data["temps"] <= 30)]["score adversaire"].loc[data[(data["journée"] == journee) & (data["temps"] <= 30)].index[-1]]
    score_final_adv = data[data["journée"] == journee]["score adversaire"].max()
    score_M2_adv = score_final_adv - score_M1_adv   # nbr de buts inscrits en 2ème période par les adversaires



    # SCORE M1 : 

    # USDH : 

    ax.text(y = (ytick_sup-1) + (ytick_sup-1)/5 + 0.25 , 
            x = 2.75 , 
            s = score_M1_USDH , 
            color = "#BE1717" , 
            fontsize = 30 , 
            verticalalignment = "center")
    
    
    # tiret : 

    ax.text(y = (ytick_sup-1) + (ytick_sup-1)/5 + 0.25 , 
            x = 3.25 , 
            s = " -" , 
            color = "black" , 
            fontsize = 30 , 
            verticalalignment = "center")



    # adv : 

    ax.text(y = (ytick_sup-1) + (ytick_sup-1)/5 + 0.25 , # ytick_inf + ytick_inf/5 + 0.1  , 
            x = 3.75 , 
            s = score_M1_adv , 
            color = dico_couleurs[adv] , 
            fontsize = 30 , 
            verticalalignment = "center")



    
    
    

    # score M2 : 

    # USDH : 

    ax.text(y = (ytick_sup-1) + (ytick_sup-1)/5 + 0.25 , 
            x = 9 , 
            s = score_M2_USDH , 
            color = "#BE1717" , 
            fontsize = 30 , 
            verticalalignment = "center")
    
    
    # tiret : 
    
    ax.text(y = (ytick_sup-1) + (ytick_sup-1)/5 + 0.25 , 
            x = 9.5 , 
            s = " -" , 
            color = "black" , 
            fontsize = 30 , 
            verticalalignment = "center")
    
    



    # adv : 

    ax.text(y = (ytick_sup-1) + (ytick_sup-1)/5 + 0.25 , # ytick_inf + ytick_inf/5 + 0.1 , 
           x = 10 , 
           s = score_M2_adv , 
           color = dico_couleurs[adv] , 
           fontsize = 30 , 
           verticalalignment = "center")
    
    
    
    
    
    
    return ax


















## Fonction retournant un diagramme en barres des buts marqués par joueur d'une équipe précise, lors d'une rencontre précise :
    
def diagramme_barres_buts_equipe(fig , ax , data , journee = "J5" , equipe = "USDH" , show_title = True) :
    
    """Retourne une figure contenant le diagramme en barres des buts marqués par joueur de l'équipe renseignée, lors du match 
       de championnat précisé."""
    
    
    # Filtrage des données qui nous intéressent :
    
    data_filtre = data[(data["journée"] == journee) & (data["équipe"] == equipe) & data["action"].isin(["but" , "but 7m"])]
    
    
    
    # Graphique : 
    
    sns.countplot(data = data_filtre , 
                  x = "joueur" , 
                  order = data_filtre["joueur"].value_counts().index ,
                  ax = ax)


    ax.grid(ls = "--" , alpha = 0.7)

    ax.set_ylabel("tirs tentés")
    
    
    if show_title == True : 
        
        fig.suptitle(f"Buts marqués par joueur de {equipe}, {journee}" , fontsize = 30 , family = "serif")
        
        
    
    ax.set_xticklabels(labels = data_filtre["joueur"].value_counts().index , 
                       rotation = 35)
    
    
    ax.spines["top"].set_color(None)
    ax.spines["right"].set_color(None)
    
    
    
    
    
    
    
    # Ajout des effectifs au-dessus des barres : 
    
    for joueur , position in zip(list(data_filtre["joueur"].value_counts().index) , list(range(len(data_filtre["joueur"].value_counts().index)))) :
        
        ax.text(x = position , 
                y = data_filtre["joueur"].value_counts().loc[joueur] + 0.3 , 
                s = data_filtre["joueur"].value_counts().loc[joueur] , 
                fontsize = 16 , 
                color = "red" , 
                horizontalalignment = "center")
    
    
    
    
    
    return ax





















## Fonction retournant un camembert du type d'actions souhaité, par joueur d'une équipe précise, lors d'une rencontre précise :
    
def camembert_type_action_equipe(fig , ax , data , journee = "J5" , equipe = "USDH" , show_title = True , 
                                 type_action = ["but" , "but 7m"]) : 
    
    
    """Retourne un diagramme circulaire du type d'action voulu, par joueur de l'équipe renseignée en argument, lors de la rencontre 
       précisée."""
    
    
    
    # Filtrage des données qui nous intéressent :
    
    data_filtre = data[(data["journée"] == journee) & (data["équipe"] == equipe) & data["action"].isin(type_action)]
    
    
    
    # Graphique : 
    
    ax.pie(x = data_filtre["joueur"].value_counts() , 
           labels = data_filtre["joueur"].value_counts().index , 
           autopct = lambda pct : str(np.round(pct , 2)) + " %" , 
           pctdistance = 0.5 , 
           labeldistance = 1.05 , 
           shadow = True , 
           startangle = 90 , 
           radius = 1.35)


    
    
    
    if show_title == True : 
        
        if len(type_action) == 2 : 
            
            if "but" in type_action : 
        
                fig.suptitle(f"Proportion des buts de {equipe} marqués par joueur, {journee}" , fontsize = 30 , family = "serif")
        
        
            else : 
                
                fig.suptitle(f"Proportion des avertissements + 2min de {equipe} par joueur, {journee}" , fontsize = 30 , family = "serif")
        
        
        else : 
            
            fig.suptitle(f"Proportion des {type_action[0]} de {equipe} marqués par joueur, {journee}" , fontsize = 30 , family = "serif")
        
                
                
    
    ax.legend(loc = (1.35 , 0.5))
    
    
    
    return ax  





















## Fonction retournant un camembert PLOTLY du nombre d'actions du type d'action renseigné réalisées par joueur d'une équipe, lors d'un match bien précis :
    
def camembert_type_action_equipe_plotly(data , journee = "J5" , equipe = "USDH" , show_title = True , 
                                        type_action = ["but" , "but 7m"]) : 
    
    
    """Retourne un diagramme circulaire du type d'actions voulu, par joueur de l'équipe renseignée en argument, lors de la rencontre 
       précisée."""
    
    
    
    # Filtrage des données qui nous intéressent :
    
    data_filtre = data[(data["journée"] == journee) & (data["équipe"] == equipe) & data["action"].isin(type_action)]
    
    
    
    # Graphique : 
    
    fig = px.pie(values = data_filtre["joueur"].value_counts() , 
                 names = data_filtre["joueur"].value_counts(normalize = True).index , 
                 color_discrete_sequence=px.colors.sequential.RdBu , 
                 hole = 1/5)
    
    
    
    fig.update_traces(textposition = "inside" , 
                      textinfo = "percent+label")


    
    
    
    if show_title == True : 
        
        if len(type_action) == 2 : 
            
            if "but" in type_action : 
        
                fig.update_layout(title_text = f"Proportion des buts de {equipe} marqués par joueur, {journee}")
        
        
            else : 
                
                fig.update_layout(title_text = f"Proportion des avertissements + 2min de {equipe} par joueur, {journee}")
        
        
        else : 
            
            fig.update_layout(title_text = f"Proportion des {type_action[0]} de {equipe} marqués par joueur, {journee}")
        
        
    
    
    
    
    
    
    return fig







#####################################################################################################################
#####################################################################################################################

###                                 FONCTIONS SPECIFIQUES A L'APPLICATION STREAMLIT :
    
#####################################################################################################################
#####################################################################################################################



## Fonction permettant de récupérer, pour une journée de championnat donnée, le score de l'équipe jouant à domicile :
    
def score_domicile(data , journee = "J1" , periode = "final") : 
    
    
    """Retourne le score de l'équipe jouant à domicile lors de la journée renseignée.
       Au choix : retourne le score en 1ère mi-temps ('M1') , en 2ème mi-temps ('M2') ou le score final ('final') de l'équipe."""
    
    
    
    # 0) On commence par filtrer les données : 
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à domicile lors de cette rencontre : 
    
    equipe_domicile = dico_rencontres_USDH[journee][0]
    
    
    
    
    
    # 2) On peut donc en déduire le score de l'équipe à domicile :
    
    
    # a) On identifie la colonne indiquant le score de cette équipe (2 choix possibles : 'score_USDH' ou 'score_adversaire').
    
    # CAS 1 : l'équipe à domicile est l'USDH ==> la colonne indiquant le score de l'équiupe est 'score_USDH' : 
    
    if equipe_domicile == "USDH" : 
        
        col_score = "score USDH"
        
        
        
    # CAS 2 : l'équipe à domicile N'est PAS l'USDH ==> la colonne indiquant le score de l'équiupe est 'scorz_adversaire' : 
        
    else : 
        
        col_score = "score adversaire"
        
        
        
        
        
        
    # b) On récupère le score de l'équipe en fonction de la période souhaitée : 
    
    if periode == "M1" :
        
        score_equipe = data_filtre[data_filtre["temps"] <= 30][col_score].max()
        
        return score_equipe
        
        
        
    elif periode == "M2" : 
        
        score_final = data_filtre[col_score].max()  # le score final de l'équipe
        score_M1 = data_filtre[data_filtre["temps"] <= 30][col_score].max()  # le score de l'équipe en M1
        
        score_equipe = score_final - score_M1  # score M2 = score final - score M1
        
        
        return score_equipe
        
        
         
    elif periode in ["final" , "score final"] :
        
        score_equipe = data_filtre[col_score].max()
        
        return score_equipe
        
        
        
        
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'periode' : 'M1' , 'M2' , 'final' , ou 'score final'.")
    
        
    
    
    
    
    
    
    
    
    




## Fonction permettant de récupérer, pour une journée de championnat donnée, le score de l'équipe jouant à l'extérieur :
    
def score_exterieur(data , journee = "J1" , periode = "final") : 
    
    
    """Retourne le score de l'équipe jouant à l'extérieur lors de la journée renseignée.
       Au choix : retourne le score en 1ère mi-temps ('M1') , en 2ème mi-temps ('M2') ou le score final ('final') de l'équipe."""
    
    
    
    # 0) On commence par filtrer les données : 
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à l'extérieur lors de cette rencontre : 
    
    equipe_exterieur = dico_rencontres_USDH[journee][1]
    
    
    
    
    
    # 2) On peut donc en déduire le score de l'équipe à l'extérieur :
    
    
    # a) On identifie la colonne indiquant le score de cette équipe (2 choix possibles : 'score_USDH' ou 'score_adversaire').
    
    # CAS 1 : l'équipe à l'extérieur est l'USDH ==> la colonne indiquant le score de l'équiupe est 'score_USDH' : 
    
    if equipe_exterieur == "USDH" : 
        
        col_score = "score USDH"
        
        
        
    # CAS 2 : l'équipe à l'extérieur N'est PAS l'USDH ==> la colonne indiquant le score de l'équiupe est 'scorz_adversaire' : 
        
    else : 
        
        col_score = "score adversaire"
        
        
        
        
        
        
    # b) On récupère le score de l'équipe en fonction de la période souhaitée : 
    
    if periode == "M1" :
        
        score_equipe = data_filtre[data_filtre["temps"] <= 30][col_score].max()
        
        return score_equipe
        
        
        
    elif periode == "M2" : 
        
        score_final = data_filtre[col_score].max()  # le score final de l'équipe
        score_M1 = data_filtre[data_filtre["temps"] <= 30][col_score].max()  # le score de l'équipe en M1
        
        score_equipe = score_final - score_M1  # score M2 = score final - score M1
        
        
        return score_equipe
        
        
         
    elif periode in ["final" , "score final"] :
        
        score_equipe = data_filtre[col_score].max()
        
        return score_equipe
        
        
        
        
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'periode' : 'M1' , 'M2' , 'final' , ou 'score final'.")















## Fonction récapitulative permettant de retourner AU CHOIX le score de l'équipe jouant à domicile OU de celle jouant à l'extérieur, lors de la journée de championnat voulue :

def score(data , journee = "J5" , periode = "final" , equipe = "domicile") :
    
    """Retourne le score de l'équipe voulue, lors de la journée de championnat renseignée.
       Au choix : retourne le score en 1ère mi-temps ('M1') , en 2ème mi-temps ('M2') ou le score final ('final') de l'équipe."""
    
    
    # CAS 1 : si je souhaite obtenir le score de l'équipe à DOMICILE ==> j'utilise la fonction 'score_domicile' :
    
    if equipe in ["domicile" , "dom"] :
        
        
        return score_domicile(data = data , journee = journee , periode = periode)
    
    
    
    
    # CAS 2 : si je souhaite obtenir le score de l'équipe à L'EXTERIEUR ==> j'utilise la fonction 'score_exterieur' :
    
    elif equipe in ["extérieur" , "ext"] :
        
        
        return score_exterieur(data = data , journee = journee , periode = periode)
    
    
    
    
    else : 
        
        raise ValueError("patramètre attendu pour l'argument 'equipe' : 'domicile' , 'dom' , 'extérieur' ou 'ext'.")

















## Fonction permettant de récupérer, pour une journée de championnat donnée, le nombre de punitions (avertissements OU 2min, au choix) reçus l'équipe jouant à domicile :
    
def nbr_punitions_domicile(data , journee = "J1" , type_punition = "avertissement") : 
    
    
    """Retourne le nbr de punitions (soit avertissement, soit 2min) reçus par l'équipe jouant à domicile lors de la journée 
       renseignée."""
    
    

    if type_punition in ["avertissement" , "2min"] :
        
        
        
        # 0) On commence par récupérer le nom de l'équipe jouant à domicile lors de cette rencontre : 

        equipe_domicile = dico_rencontres_USDH[journee][0]





        # 1) On filtre à présent les données : 

        data_filtre = data[(data["journée"] == journee) & (data["équipe"] == equipe_domicile) & (data["action"] == type_punition)]





        # 2) On peut donc en déduire le nbr de punitions reçues par l'équipe jouant à domicile :

        nbr_punitions = len(data_filtre)
        
        
        return nbr_punitions
    
    
    
    
    
        
        
        
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'type_punition' : 'avertissement' ou '2min'.")
        
        
        
        












## Fonction permettant de récupérer, pour une journée de championnat donnée, le nombre de punitions (avertissements OU 2min, au choix) reçus l'équipe jouant à l'extérieur :
    
def nbr_punitions_exterieur(data , journee = "J1" , type_punition = "avertissement") : 
    
    
    """Retourne le nbr de punitions (soit avertissement, soit 2min) reçus par l'équipe jouant à l'extérieur lors de la journée 
       renseignée."""
    
    

    if type_punition in ["avertissement" , "2min"] :
        
        
        
        # 0) On commence par récupérer le nom de l'équipe jouant à l'extérieur lors de cette rencontre : 

        equipe_exterieur = dico_rencontres_USDH[journee][1]





        # 1) On filtre à présent les données : 

        data_filtre = data[(data["journée"] == journee) & (data["équipe"] == equipe_exterieur) & (data["action"] == type_punition)]





        # 2) On peut donc en déduire le nbr de punitions reçues par l'équipe jouant à domicile :

        nbr_punitions = len(data_filtre)
        
        
        return nbr_punitions
    
    
    
    
    
        
        
        
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'type_punition' : 'avertissement' ou '2min'.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
## Fonction récapitulative permettant, au choix, de retourner le nombre de punitions subbies par l'équipe jouant à domicile OU à l'extérieur lors de la journée de championnat renseignée :
    
def nbr_punitions(data , journee = "J5" , type_punition = "avertissement" , equipe = "domicile") :
    
    """Retourne le nombre de punitions du type mentionné reçues par l'équipe voulue, lors de la journée renseignée."""
    
    
    # CAS 1 : si l'équipe voulue est celle jouant à domicile ==> on utilise la fonction 'nbr_punitions_domicile' : 
    
    if equipe in ["domicile" , "dom"] :  
        
        return nbr_punitions_domicile(data = data , journee = journee , type_punition = type_punition)
    
    
    
    
    
    # CAS 2 : si l'équipe voulue est celle jouant à l'extérieur ==> on utilise la fonction 'nbr_punitions_exterieur' : 
    
    if equipe in ["extérieur" , "ext"] :  
        
        return nbr_punitions_exterieur(data = data , journee = journee , type_punition = type_punition)
        
        
        
        
        
        
    else : 
        
        
        raise ValueError("paramètre attendu pour l'argument 'equipe' : 'domicile' , 'dom' , 'extérieur' ou 'ext'.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


## Fonction permettant de récupérer, pour une journée de championnat donnée, le TEMPS PASSE EN TÊTE par l'équipe jouant à domicile :
    
def temps_en_tete_domicile(data , journee = "J5" , duree_en = "pct") :
    
    """Retourne la durée (sous forme de pourcentage des 60 minutes de jeu du match OU exprimé en minutes) pendant laquelle 
       l'équipe à domicile a mené au score, durant la journée de championnat renseignée en argument."""
    
    
    # 0) On commence par filtrer les données : 
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à domicile : 
    
    equipe_domicile = dico_rencontres_USDH[journee][0]
    
    
    
    
    
    # 2) On récupère le dictionaire des durées passés par l'USDH à mener / à égalité / à être mené au score : 
    
    dates , durees , durees_totales , pct = duree_situation_score(data = data , journee = journee)
    
    
    
    # CAS 1 : je souhaite ces durées en MINUTES ==> je regarde le dictionnaire 'durees_totales' : 
    
    if duree_en in ["minutes"] :
        
        
        # SI l'équipe jouant à domicile est l'USDH ==> son temps passé en tête est associé à la clé 'USDH mène'
        
        if equipe_domicile == "USDH" :
        
            duree_en_tete = durees_totales["USDH mène"]
            
            
            
        # SINON, si l'équipe jouant à domicile est l'adversaire de l'USDH ==> son temps passé en tête est associé à la clé 'adversaire mène'
        
        else : 
            
            duree_en_tete = durees_totales["adversaire mène"] 
    
    
    
    
    
    
        return duree_en_tete
    
    
    
    
    
    
    # CAS 2 : je souhaite ces durées en POURCENTAGE DES 60 MINUTES ==> je regarde le dictionnaire 'pct' :
    
    elif duree_en in ["pct" , "%" , "pourcentage"] :
        
        
        # SI l'équipe jouant à domicile est l'USDH ==> son temps passé en tête est associé à la clé 'USDH mène'
        
        if equipe_domicile == "USDH" :
        
            duree_en_tete = pct["USDH mène"]
            
            
            
        # SINON, si l'équipe jouant à domicile est l'adversaire de l'USDH ==> son temps passé en tête est associé à la clé 'adversaire mène'
        
        else : 
            
            duree_en_tete = pct["adversaire mène"] 
    
    
    
    
    
    
        return duree_en_tete
    
    
    
    
    
    
    
    
    
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'duree_en' : 'minutes' , 'pct' , '%' ou 'pourcentage'.")
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
## Fonction permettant de récupérer, pour une journée de championnat donnée, le TEMPS PASSE EN TÊTE par l'équipe jouant à l'extérieur :
    
def temps_en_tete_exterieur(data , journee = "J5" , duree_en = "pct") :
    
    """Retourne la durée (sous forme de pourcentage des 60 minutes de jeu du match OU exprimé en minutes) pendant laquelle 
       l'équipe à l'extérieur a mené au score, durant la journée de championnat renseignée en argument."""
    
    
    # 0) On commence par filtrer les données : 
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à l'extérieur : 
    
    equipe_exterieur = dico_rencontres_USDH[journee][1]
    
    
    
    
    
    # 2) On récupère le dictionaire des durées passés par l'USDH à mener / à égalité / à être mené au score : 
    
    dates , durees , durees_totales , pct = duree_situation_score(data = data , journee = journee)
    
    
    
    # CAS 1 : je souhaite ces durées en MINUTES ==> je regarde le dictionnaire 'durees_totales' : 
    
    if duree_en in ["minutes"] :
        
        
        # SI l'équipe jouant à l'extérieur est l'USDH ==> son temps passé en tête est associé à la clé 'USDH mène'
        
        if equipe_exterieur == "USDH" :
        
            duree_en_tete = durees_totales["USDH mène"]
            
            
            
        # SINON, si l'équipe jouant à l'extérieur est l'adversaire de l'USDH ==> son temps passé en tête est associé à la clé 'adversaire mène'
        
        else : 
            
            duree_en_tete = durees_totales["adversaire mène"] 
    
    
    
    
    
    
        return duree_en_tete
    
    
    
    
    
    
    # CAS 2 : je souhaite ces durées en POURCENTAGE DES 60 MINUTES ==> je regarde le dictionnaire 'pct' :
    
    elif duree_en in ["pct" , "%" , "pourcentage"] :
        
        
        # SI l'équipe jouant à domicile est l'USDH ==> son temps passé en tête est associé à la clé 'USDH mène'
        
        if equipe_exterieur == "USDH" :
        
            duree_en_tete = pct["USDH mène"]
            
            
            
        # SINON, si l'équipe jouant à domicile est l'adversaire de l'USDH ==> son temps passé en tête est associé à la clé 'adversaire mène'
        
        else : 
            
            duree_en_tete = pct["adversaire mène"] 
    
    
    
    
    
    
        return duree_en_tete
    
    
    
    
    
    
    
    
    
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'duree_en' : 'minutes' , 'pct' , '%' ou 'pourcentage'.")
        
        
        
        
        
        
        
        
    















## Fonction récapitulative permettant de récupérer, AU CHOIX et pour une journée de championnat donnée, le TEMPS PASSE EN TÊTE par l'équipe jouant à domicile OU à l'extérieur :

def temps_en_tete(data , journee = "J5" , duree_en = "pct" , equipe = "domicile") :
    
    """Retourne la durée (sous forme de pourcentage des 60 minutes de jeu du match OU exprimé en minutes) pendant laquelle 
       l'équipe renseignée a mené au score, durant la journée de championnat renseignée en argument."""
    
    
    
    # SI je souhaite retourner le temps passé en tête par l'équipe à DOMICILE ==> j'utilise la fonction 'temps_en_tete_domicile'
    
    if equipe in ["domicile" , "dom"] : 
        
        
        return temps_en_tete_domicile(data = data , journee = journee , duree_en = duree_en)
    
    
    
    
    
    # SI je souhaite retourner le temps passé en tête par l'équipe à L'EXTERIEUR ==> j'utilise la fonction 'temps_en_tete_exterieur'
    
    elif equipe in ["extérieur" , "ext"] : 
        
        
        return temps_en_tete_exterieur(data = data , journee = journee , duree_en = duree_en)
    
    
    

    
    else : 
        
        
        raise ValueError("paramètre attendu pour l'argument 'equipe' : 'domicile' , 'dom' , 'extérieur' ou 'ext'.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

## Fonction permettant de récupérer, pour une journée de championnat donnée, le TEMPS PASSE EN SUPERIORITE NUMERIQUE par l'équipe jouant à domicile :
    
def temps_en_superiorite_domicile(data , journee = "J5" , format_duree = "pct") :
    
    """Retourne la durée (sous forme de pourcentage des 60 minutes de jeu du match OU exprimé en minutes) pendant laquelle 
       l'équipe à domicile a joué en supériorité numérique, durant la journée de championnat renseignée en argument."""
    
    
    # 0) On commence par filtrer les données : 
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à domicile : 
    
    equipe_domicile = dico_rencontres_USDH[journee][0]
    
    
    
    
    
    # 2) On récupère le temps total passé par cette équipe dans cette situation numérique grâce à la fonction 'duree_passee_situation_numerique_equipe' :
    

    temps_en_situation_num = duree_passee_situation_numerique_equipe(data = data , journee = journee , 
                                                                     equipe = equipe_domicile , format_duree = format_duree , 
                                                                     situation = 'supériorité numérique') 
    
    
    
    
    
    
    return temps_en_situation_num
    




















## Fonction permettant de récupérer, pour une journée de championnat donnée, le TEMPS PASSE EN SUPERIORITE NUMERIQUE par l'équipe jouant à l'extérieur :
    
def temps_en_superiorite_exterieur(data , journee = "J5" , format_duree = "pct") :
    
    """Retourne la durée (sous forme de pourcentage des 60 minutes de jeu du match OU exprimé en minutes) pendant laquelle 
       l'équipe à l'extérieur a joué en supériorité numérique, durant la journée de championnat renseignée en argument."""
    
    
    # 0) On commence par filtrer les données : 
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à l'extérieur : 
    
    equipe_exterieur = dico_rencontres_USDH[journee][1]
    
    
    
    
    
    # 2) On récupère le temps total passé par cette équipe dans cette situation numérique grâce à la fonction 'duree_totale_situation_numerique' :
    

    temps_en_situation_num = duree_passee_situation_numerique_equipe(data = data , journee = journee , 
                                                                     equipe = equipe_exterieur , format_duree = format_duree , 
                                                                     situation = 'supériorité numérique')  
    
    
    
    
    
    
    return temps_en_situation_num
    



















## Fonction récapitulative permettant de récupérer, pour une journée de championnat donnée, le TEMPS PASSE EN SUPERIORITE NUMERIQUE par l'équipe renseignée :

def temps_en_superiorite(data , journee = "J5" , format_duree = "pct" , equipe = "domicile") :
    
    """Retourne la durée (sous forme de pourcentage des 60 minutes de jeu du match OU exprimé en minutes) pendant laquelle 
       l'équipe renseignée a joué en supériorité numérique, durant la journée de championnat renseignée en argument."""
    
    
    # SI je souhaite connaître le temps passé en supériorité par l'équipe jouant à DOMICILE ==> fonction 'temps_en_superiorite_domicile'
    
    if equipe in ["domicile" , "dom"] : 
        
        
        return temps_en_superiorite_domicile(data = data , journee = journee , format_duree = format_duree)
        
        
        
        
        
        
    # SI je souhaite connaître le temps passé en supériorité par l'équipe jouant à L'EXTERIEUR ==> fonction 'temps_en_superiorite_exterieur'
    
    elif equipe in ["extérieur" , "ext"] :
    
    
        return temps_en_superiorite_exterieur(data = data , journee = journee , format_duree = format_duree)
    
    
    
    
    
    
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'equipe' : 'domicile' , 'dom' , 'extérieur' ou' ext'.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        




## Fonction permettant de récupérer, pour une journée de championnat donnée, le DIFFERENTIEL DE BUTS sur les périodes de SUPERIORITE NUMERIQUE par l'équipe jouant à domicile :
    
def differentiel_superiorite_domicile(data , journee = "J5" , differentiel_en = "buts") :
    
    
    """Retourne le différentiel diff = buts marqués - buts encaissés de l'équipe jouant à domicile LORS DES PHASES QU'ELLE 
       JOUE EN SUPERIORITE NUMERIQUE, au cours de la journée de championnat renseignée."""
    
    
    
    
    # 0) On commence par filtrer les données : 
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à domicile : 
    
    equipe_domicile = dico_rencontres_USDH[journee][0]
    
    
    
    
    
    
    # 2) On récupère le dictionaire des buts marqués / encaissés / différentiel de l'équipe jouant à domicile lors de CHAQUE période de supériorité numérique : 
    
    dico_bilans_superiorites_domicile = bilan_situation_numerique_equipe(data = data , journee = journee , equipe = equipe_domicile , 
                                                                         situation = "supériorité numérique")
    
    
    
    
    
    # On extrait de ce dictionnaire la liste des différentiels de buts de cette équipe lors de chaque période qu'elle a joué en supériorité numérique :
    
    L_differentiels = [dico_bilans_superiorites_domicile[periode][f"différentiel de buts {equipe_domicile}"] for periode in dico_bilans_superiorites_domicile.keys()]
        
        
                       
                       
                       
    # On calcule le différentiel TOTAL sur l'ensemble du temps passé en supériorité numérique en sommant les différentiels de chaque période de supériorité jouée par l'équipe :

    differentiel_total = sum(L_differentiels)  
    
    

                       
                       

    # SI je souhaite retourner le différentiel TOTAL (exprimé en buts) : 

    if differentiel_en == "buts" :


        return differentiel_total
    
    
    

    # SI je souhaite ramener ce différentiel PAR MINUTE JOUEE EN SUPERIORITE NUMERIQUE (exprimé en buts / minute) :

    elif differentiel_en == "buts / minute" : 


        # On récupère le temps passé par l'équipe jouant à domicile en supériorité numérique : 

        temps_superiorite = temps_en_superiorite(data = data , journee = journee , format_duree = "float" , equipe = "domicile")


        # On effectue le quotient : 

        return differentiel_total / temps_superiorite




    else : 

        raise ValueError("paramètre attendu pour l'argument 'differentiel_en' : 'buts' ou 'buts / minute'.")






















## Fonction permettant de récupérer, pour une journée de championnat donnée, le DIFFERENTIEL DE BUTS sur les périodes de SUPERIORITE NUMERIQUE par l'équipe jouant à l'extérieur :
    
def differentiel_superiorite_exterieur(data , journee = "J5" , differentiel_en = "buts") :
    
    
    """Retourne le différentiel diff = buts marqués - buts encaissés de l'équipe jouant à l'extérieur LORS DES PHASES QU'ELLE 
       JOUE EN SUPERIORITE NUMERIQUE, au cours de la journée de championnat renseignée."""
    
    
    
    
    # 0) On commence par filtrer les données : 
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à l'extérieur : 
    
    equipe_exterieur = dico_rencontres_USDH[journee][1]
    
    
    
    
    
    
    # 2) On récupère le dictionaire des buts marqués / encaissés / différentiel de l'équipe jouant à l'extérieur lors de CHAQUE période de supériorité numérique : 
    
    dico_bilans_superiorites_domicile = bilan_situation_numerique_equipe(data = data , journee = journee , equipe = equipe_exterieur , 
                                                                         situation = "supériorité numérique")
    
    
    
    
    
    # On extrait de ce dictionnaire la liste des différentiels de buts de cette équipe lors de chaque période qu'elle a joué en supériorité numérique :
    
    L_differentiels = [dico_bilans_superiorites_domicile[periode][f"différentiel de buts {equipe_exterieur}"] for periode in dico_bilans_superiorites_domicile.keys()]
        
        
        
        
        
        
    # On calcule le différentiel TOTAL sur l'ensemble du temps passé en supériorité numérique en sommant les différentiels de chaque période de supériorité jouée par l'équipe :

    differentiel_total = sum(L_differentiels)  
    
    


    # SI je souhaite retourner le différentiel TOTAL (exprimé en buts) : 

    if differentiel_en == "buts" :


        return differentiel_total
    
    
    

    # SI je souhaite ramener ce différentiel PAR MINUTE JOUEE EN SUPERIORITE NUMERIQUE (exprimé en buts / minute) :

    elif differentiel_en == "buts / minute" : 


        # On récupère le temps passé par l'équipe jouant à l'extérieur en supériorité numérique : 

        temps_superiorite = temps_en_superiorite(data = data , journee = journee , format_duree = "float" , equipe = "extérieur")


        # On effectue le quotient : 

        return differentiel_total / temps_superiorite


    
    
    


    else : 

        raise ValueError("paramètre attendu pour l'argument 'differentiel_en' : 'buts' ou 'buts / minute'.")
        
        
        
        
        
        
        
        
        
        













## Fonction récapitulative permettant de récupérer, pour une journée de championnat donnée, le DIFFERENTIEL DE BUTS sur les périodes de SUPERIORITE NUMERIQUE par l'équipe renseignée (domicile ou extérieur) :
    
def differentiel_superiorite(data , journee = "J5" , differentiel_en = "buts" , equipe = "domicile") :
    
    
    """Retourne le différentiel diff = buts marqués - buts encaissés de l'équipe renseignée en argiment LORS DES PHASES QU'ELLE 
       JOUE EN SUPERIORITE NUMERIQUE, au cours de la journée de championnat renseignée."""
    
    
    
    # SI je souhaite connaître le différentiel de buts sur les supériorités numériques de l'équipe jouant à DOMICILE ==> j'utilise la fonction 'differentiel_superiorite_domicile' :
    
    if equipe in ["domicile" , "dom"] : 
        
           
            return differentiel_superiorite_domicile(data = data , journee = journee , differentiel_en = differentiel_en)
        
        
        
        
        
        
        
    # SI je souhaite connaître le différentiel de buts sur les supériorités numériques de l'équipe jouant à L'EXTERIEUR ==> j'utilise la fonction 'differentiel_superiorite_exterieur' :
    
    elif equipe in ["extérieur" , "ext"] : 
        
           
            return differentiel_superiorite_exterieur(data = data , journee = journee , differentiel_en = differentiel_en)
        
        
        
        
        
    else : 
        
        
        raise ValueError("paramètre attendu pour l'argument 'equipe' : 'domicile' , 'dom' , 'extérieur' ou 'ext'.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
       
        
        
        
        
        
## Fonction permettant de récupérer, pour une journée de championnat donnée, le NOMBRE de périodes de SUPERIORITE NUMERIQUE jouées par l'équipe jouant à domicile :
    
def nbr_periodes_superiorite_domicile(data , journee = "J5") :
    
    
    """Retourne le nombre de périodes de supériorités numériques jouées par l'équipe à domicile lors de la rencontre renseigée."""
    
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à domicile lors de cette journée de championnat : 
    
    equipe_domicile = dico_rencontres_USDH[journee][0]
    
    
    
    
    
    
    
    # 2) On récupère la liste des périodes de supériorité numérique de l'équipe à domicile :
    
    
    periodes_sup_equipe_dom = periodes_situation_numerique_equipe(data = data , journee = journee , 
                                                                  equipe = equipe_domicile , situation = "supériorité numérique")

        
        
        
    
        
        
        
    # 3) On calcule alors le nombre de périodes de supériorité en calculant la longueur de la liste 'periodes_sup_equipe_dom' : 
    
    
    return len(periodes_sup_equipe_dom)





















## Fonction permettant de récupérer, pour une journée de championnat donnée, le NOMBRE de périodes de SUPERIORITE NUMERIQUE jouées par l'équipe jouant à l'extérieur :
    
def nbr_periodes_superiorite_exterieur(data , journee = "J5") :
    
    
    """Retourne le nombre de périodes de supériorités numériques jouées par l'équipe à l'extérieur lors de la rencontre renseigée."""
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à l'extérieur : 
    
    equipe_exterieur = dico_rencontres_USDH[journee][1]
    
    
    
    
    
    
    
    # 2) On récupère la liste des périodes de supériorité numérique de l'équipe à l'extérieur :
    
    
    periodes_sup_equipe_ext = periodes_situation_numerique_equipe(data = data , journee = journee , 
                                                                  equipe = equipe_exterieur , situation = "supériorité numérique")

        
        

        
        
        
    # 3) On calcule alors le nombre de périodes de supériorité en calculant la longueur de la liste 'periodes_sup_equipe_ext' : 
    
    
    return len(periodes_sup_equipe_ext)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
## Fonction récapitulative permettant de récupérer, pour une journée de championnat donnée, le NOMBRE de périodes de SUPERIORITE NUMERIQUE jouées par l'équipe souhaitée (domicile ou extérieur) :
    
def nbr_periodes_superiorite(data , journee = "J5" , equipe = "domicile") :
    
    
    """Retourne le nombre de périodes de supériorités numériques jouées par l'équipe renseignée lors de la rencontre précisée."""
    
    
    # SI je souhaite récupérer le nbr de périodes en supériorité numérique de l'équipe jouant à domicile ==> j'utilise la fonction 'nbr_periodes_superiorite_domicile'
    
    if equipe in ["domicile" , "dom"] :
        
        
        return nbr_periodes_superiorite_domicile(data = data , journee = journee)
    
    
    
    
    
    
    # SI je souhaite récupérer le nbr de périodes en supériorité numérique de l'équipe jouant à l'extérieur ==> j'utilise la fonction 'nbr_periodes_superiorite_exterieur'
    
    elif equipe in ["extérieur" , "ext"] :
        
        
        return nbr_periodes_superiorite_exterieur(data = data , journee = journee)
    
    
    
    
    
    
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'equipe' : 'domicile' , 'dom' , 'extérieur' ou 'ext'.")
    
        
        
        


















## Fonction permettant de retourner la plus grosse série de buts encaissés successivement SANS INSCRIRE LE MOINDRE BUT, de l'équipe à domicile :
    
def plus_grosse_serie_buts_encaisses_domicile(data , journee = "J5") :
    
    """Retourne les dates de début / fin ainsi que la durée de la plus grosse période de disette offensive de l'équipe jouant 
       à domicile lors de la rencontre renseignée en argument."""
    
    
    
     # 0) On commence par filtrer les données : 
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à domicile : 
    
    equipe_domicile = dico_rencontres_USDH[journee][0]
    
    
    
    
    
    
    
    
     # 2) On récupère la liste des périodes de buts encaissés successivement sans scorer, de l'équipe à domicile :
    
    
    # CAS 1 : l'équipe à domicile est l'USDH ==> la fonction 'series_buts_encaisses' nous retourne les séries de buts consécutifs encaissés par l'USDH :
    
    if equipe_domicile == "USDH" : 
        
        periodes_encaissement = series_buts_encaisses(data = data , journee = journee)  # le dictionnaire des scores associés à chaque période de buts successifs inscrits par l'équipe adverse
    
    
    
    
    
    # CAS 2 : l'équipe à domicile est l'adversaire de l'USDH ==> la fonction 'series_buts_marques' nous retourne les séries de buts consécutifs marqués par l'USDH, donc encaissés par l'équipe :
    
    else : 
        
        periodes_encaissement = series_buts_marques(data = data , journee = journee)  # le dictionnaire des scores associés à chaque période de buts successifs inscrits par l'équipe adverse
        
        
        # On inverse la position des buts du tuple du score, car les buts marqués sont en 1ère position avec la fonction 'series_buts_marques' : 
    
        periodes_encaissement = dict([(cle , (valeur[1] , valeur[0])) for cle , valeur in periodes_encaissement.items()])
    
    
    
    
    
    # 3) Recherche de la plus grosse période, sachant que seul le 2ème chiffre du tuple nous intéresse (le 1er vaut toujours 0...) :
    
    # CAS 1 : il n'a a AUCUNE série de buts encaissés successvement dans scorer : 
    
    if periodes_encaissement == {} :
    
        return ((0 , 0) , (0 , 0))
    
    
    
    
    
    # CAS 2 : il n'a qu'UNE SEULE série de buts encaissés successivement sans scorer : 
    
    elif len(periodes_encaissement) == 1 :
        
        
        return periodes_encaissement[list(periodes_encaissement.keys())[0]] , list(periodes_encaissement.keys())[0] 
    
    
    
    
    
    # CAS 3 : il y a PLUSIEURS séries de buts encaissés successivement sans scorer : 
    
    elif len(periodes_encaissement) > 1 :
    
        k = 0


        # On initialise la plus grosse période à 0 :

        plus_grosse_periode = periodes_encaissement[list(periodes_encaissement.keys())[0]]



        # Pour chaque période : 

        for periode in list(periodes_encaissement.keys())[1:] :


            periode = periodes_encaissement[periode]    # la période considérée
            buts_successifs_encaisses_periode = periode[1]  # le nombre de buts successifs encaissés lors de la période considérée

            buts_successifs_encaisses_plus_grosse_periode = plus_grosse_periode[1]  # le nombre de buts successifs encaissés lors de la PLUS GROSSE période considérée à cet instant





            # SI le nombre de buts successifs encaissés lors de la période considérée surpasse celui de la plus grosse période actuelle :

            if buts_successifs_encaisses_periode >= buts_successifs_encaisses_plus_grosse_periode :

                plus_grosse_periode = periode  # la période considérée devient la plus grosse période

                k += 1




        # GESTION DU CAS OU LA 1ère PERIODE DU DICTIONNAIRE EST LA PLUS GROSSE ==> k ne peut pas rester à -1, il doit être incrémenté d'une unité :

        if k == -1 : 

            k += 1 # le rang de la plus grosse période est incrémenté d'1 unité







        # On retourne le tuple du score sur cette période AINSI QUE le tuple des dates de début et de fin de cette période :

        return plus_grosse_periode , list(periodes_encaissement.keys())[k]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  
    
    
    
## Fonction permettant de retourner la plus grosse série de buts encaissés successivement SANS INSCRIRE LE MOINDRE BUT, de l'équipe à l'extérieur :
    
def plus_grosse_serie_buts_encaisses_exterieur(data , journee = "J5") :
    
    """Retourne les dates de début / fin ainsi que la durée de la plus grosse période de disette offensive de l'équipe jouant 
       à l'extérieur lors de la rencontre renseignée en argument."""
    
    
    
    # 0) On commence par filtrer les données : 
    
    data_filtre = data[data["journée"] == journee]
    
    
    
    
    
    # 1) On récupère à présent le nom de l'équipe jouant à l'extérieur : 
    
    equipe_exterieur = dico_rencontres_USDH[journee][1]
    
    
    
    
    
    
    
    
     # 2) On récupère la liste des périodes de buts encaissés successivement sans scorer, de l'équipe à l'extérieur :
    
    
    # CAS 1 : l'équipe à l'extérieur est l'USDH ==> la fonction 'series_buts_encaisses' nous retourne les séries de buts consécutifs encaissés par l'USDH :
    
    if equipe_exterieur == "USDH" : 
        
        periodes_encaissement = series_buts_encaisses(data = data , journee = journee)  # le dictionnaire des scores associés à chaque période de buts successifs inscrits par l'équipe adverse
    
    
    
    
    
    # CAS 2 : l'équipe à l'extérieur est l'adversaire de l'USDH ==> la fonction 'series_buts_marques' nous retourne les séries de buts consécutifs marqués par l'USDH, donc encaissés par l'équipe :
    
    else : 
        
        periodes_encaissement = series_buts_marques(data = data , journee = journee)  # le dictionnaire des scores associés à chaque période de buts successifs inscrits par l'équipe adverse
    
    
        # On inverse la position des buts du tuple du score, car les buts marqués sont en 1ère position avec la fonction 'series_buts_marques' : 
    
        periodes_encaissement = dict([(cle , (valeur[1] , valeur[0])) for cle , valeur in periodes_encaissement.items()])
    
    
    
    
    
    
    
    # 3) Recherche de la plus grosse période, sachant que seul le 2ème chiffre du tuple nous intéresse (le 1er vaut toujours 0...) :
    
    # CAS 1 : il n'a a AUCUNE série de buts encaissés successvement dans scorer : 
    
    if periodes_encaissement == {} :
        
        return ((0 , 0) , (0 , 0))
    
    
    
    
    
    # CAS 2 : il n'a qu'UNE SEULE série de buts encaissés successivement sans scorer : 
    
    elif len(periodes_encaissement) == 1 :
        
        
        return periodes_encaissement[list(periodes_encaissement.keys())[0]] , list(periodes_encaissement.keys())[0] 
    
    
    
    
    
    # CAS 3 : il y a PLUSIEURS séries de buts encaissés successivement sans scorer : 
    
    elif len(periodes_encaissement) > 1 :
        
        k = 0


        # On initialise la plus grosse période à 0 :

        plus_grosse_periode = periodes_encaissement[list(periodes_encaissement.keys())[0]]



        # Pour chaque période : 

        for periode in list(periodes_encaissement.keys())[1:] :


            periode = periodes_encaissement[periode]    # la période considérée
            buts_successifs_encaisses_periode = periode[1]  # le nombre de buts successifs encaissés lors de la période considérée

            buts_successifs_encaisses_plus_grosse_periode = plus_grosse_periode[1]  # le nombre de buts successifs encaissés lors de la PLUS GROSSE période considérée à cet instant



            # SI le nombre de buts successifs encaissés lors de la période considérée surpasse celui de la plus grosse période actuelle :

            if buts_successifs_encaisses_periode >= buts_successifs_encaisses_plus_grosse_periode :

                plus_grosse_periode = periode  # la période considérée devient la plus grosse période


                k += 1   # le rang de la plus grosse période est incrémenté d'1 unité





        # GESTION DU CAS OU LA 1ère PERIODE DU DICTIONNAIRE EST LA PLUS GROSSE ==> k ne peut pas rester à -1, il doit être incrémenté d'une unité :

        if k == -1 : 

            k += 1 # le rang de la plus grosse période est incrémenté d'1 unité







        # On retourne le tuple du score sur cette période AINSI QUE le tuple des dates de début et de fin de cette période :

        return plus_grosse_periode , list(periodes_encaissement.keys())[k] 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
## Fonction récapitulative permettant de retourner la plus grosse série de buts encaissés successivement SANS INSCRIRE LE MOINDRE BUT, de l'équipe renseignée en argument (domicile ou extérieur) :
    
def plus_grosse_serie_buts_encaisses(data , journee = "J5" , equipe = "domicile") :
    
    """Retourne les dates de début / fin ainsi que la durée de la plus grosse période de disette offensive de l'équipe renseignée 
       en argument, lors de la rencontre renseignée en argument."""
    
    
    
    
     # SI je souhaite récupérer le nbr de périodes en supériorité numérique de l'équipe jouant à domicile ==> j'utilise la fonction 'nbr_periodes_superiorite_domicile'
    
    if equipe in ["domicile" , "dom"] :
        
        
        return plus_grosse_serie_buts_encaisses_domicile(data = data , journee = journee)
    
    
    
    
    
    
    # SI je souhaite récupérer le nbr de périodes en supériorité numérique de l'équipe jouant à l'extérieur ==> j'utilise la fonction 'nbr_periodes_superiorite_exterieur'
    
    elif equipe in ["extérieur" , "ext"] :
        
        
        return plus_grosse_serie_buts_encaisses_exterieur(data = data , journee = journee)
    
    
    
    
    
    
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'equipe' : 'domicile' , 'dom' , 'extérieur' ou 'ext'.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
     
        
        
        
        
## Fonction permettant de connaître la dynamique (= nbr de buts marqués / encaissés) de jeu de l'équipe à DOMICILE lors des x dernières minutes précédant la date t, lors de la journée précisée :
    
def dynamique_domicile(data , date = 29 , x_dernieres_minutes = 5  , journee = "J5") :
    
    """Retourne le différentiel des buts marqués / encaissés par l'équipe jouant à domicile sur les x_dernieres_minutes précédant 
       la date renseignée, lors de la journée de championnat voulue."""
    
    
    # On commence par récupérer le nom de l'équipe jouant à domicile / extérieur lors de cette rencontre : 
    
    equipe_domicile = list(data[data["journée"] == journee]["domicile"].unique())
    equipe_domicile = equipe_domicile[0]
    
    equipe_exterieur = list(data[data["journée"] == journee]["extérieur"].unique())
    equipe_exterieur = equipe_exterieur[0]
    
    
    
    # On commence par filtrer les données : 
    
    data_filtre = data[(data["journée"] == journee) & (data["temps"] <= date) & (data["temps"] >= date-x_dernieres_minutes)]
    
    
    
    
    
    # On compte à présent le nombre de buts marqués et encaissés par l'équipe à domicile lors de cette période du match : 
    
    buts_domicile = len(data_filtre[(data_filtre["équipe"] == equipe_domicile) & (data_filtre["action"].isin(["but" , "but 7m"]))])
    buts_exterieur = len(data_filtre[(data_filtre["équipe"] == equipe_exterieur) & (data_filtre["action"].isin(["but" , "but 7m"]))])
    
    
    differentiel = buts_domicile - buts_exterieur     # en faveur de l'équipe à domicile
        
    
    
    
    
    
    
    return differentiel
























## Fonction permettant de connaître la dynamique (= nbr de buts marqués / encaissés) de jeu de l'équipe à L'EXTERIEUR lors des x dernières minutes précédant la date t, lors de la journée précisée :
    
def dynamique_exterieur(data , date = 29 , x_dernieres_minutes = 5  , journee = "J5") :
    
    """Retourne le différentiel des buts marqués / encaissés par l'équipe jouant à l'extérieur sur les x_dernieres_minutes précédant 
       la date renseignée, lors de la journée de championnat voulue."""
    
    
    # On commence par récupérer le nom de l'équipe jouant à domicile / extérieur lors de cette rencontre : 
    
    equipe_domicile = list(data[data["journée"] == journee]["domicile"].unique())
    equipe_domicile = equipe_domicile[0]
    
    equipe_exterieur = list(data[data["journée"] == journee]["extérieur"].unique())
    equipe_exterieur = equipe_exterieur[0]
    
    
    
    # On commence par filtrer les données : 
    
    data_filtre = data[(data["journée"] == journee) & (data["temps"] <= date) & (data["temps"] >= date-x_dernieres_minutes)]
    
    
    
    
    
    # On compte à présent le nombre de buts marqués et encaissés par l'équipe à l'extérieur lors de cette période du match : 
    
    buts_domicile = len(data_filtre[(data_filtre["équipe"] == equipe_domicile) & (data_filtre["action"].isin(["but" , "but 7m"]))])
    buts_exterieur = len(data_filtre[(data_filtre["équipe"] == equipe_exterieur) & (data_filtre["action"].isin(["but" , "but 7m"]))])
    
    
    differentiel = buts_exterieur - buts_domicile     # en faveur de l'équipe à l'extérieur
        
    
    
    
    
    
    
    return differentiel






















## Fonction récapitulative permettant de connaître la dynamique (= nbr de buts marqués / encaissés) de jeu de l'équipe renseignée lors des x dernières minutes précédant la date t, lors de la journée précisée :
    
def dynamique(data , date = 29 , x_dernieres_minutes = 5  , journee = "J5" , equipe = "domicile") :
    
    """Retourne le différentiel des buts marqués / encaissés par l'équipe renseignée sur les x_dernieres_minutes précédant 
       la date renseignée, lors de la journée de championnat voulue."""
    
    
    
    # SI je souhaite calculer le différentiel pour l'équipe à domicile : 
    
    if equipe in ["domicile" , "dom"] : 
        
        return dynamique_domicile(data = data , date = date , x_dernieres_minutes = x_dernieres_minutes  , journee = journee)
    
    
    
    
     # SI je souhaite calculer le différentiel pour l'équipe à l'extérieur : 
        
    elif equipe in ["extérieur" , "ext"] : 
        
        return dynamique_exterieur(data = data , date = date , x_dernieres_minutes = x_dernieres_minutes  , journee = journee)
        
        
        
        
        
    else : 
        
        raise ValueError("paramètre attendu pour l'argument {equipe} : 'domicile' , 'dom' , 'extérieur' ou 'ext'.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
## Fonction permettant de retourner le nombre de buts marqué par l'équipe à DOMICILE lors des x dernières minutes précédant la date t, lors de la journée précisée :
    
def dynamique_buts_marques_domicile(data , date = 29 , x_dernieres_minutes = 5  , journee = "J5") :
    
    """Retourne le nbr de buts marqués par l'équipe jouant à domicile sur les x_dernieres_minutes précédant 
       la date renseignée, lors de la journée de championnat voulue."""
    
    
    # On commence par récupérer le nom de l'équipe jouant à domicile / extérieur lors de cette rencontre : 
    
    equipe_domicile = list(data[data["journée"] == journee]["domicile"].unique())
    equipe_domicile = equipe_domicile[0]
    
    equipe_exterieur = list(data[data["journée"] == journee]["extérieur"].unique())
    equipe_exterieur = equipe_exterieur[0]
    
    
    
    # On commence par filtrer les données : 
    
    data_filtre = data[(data["journée"] == journee) & (data["temps"] <= date) & (data["temps"] >= date-x_dernieres_minutes)]
    
    
    
    
    
    # On compte à présent le nombre de buts marqués et encaissés par l'équipe à domicile lors de cette période du match : 
    
    buts_domicile = len(data_filtre[(data_filtre["équipe"] == equipe_domicile) & (data_filtre["action"].isin(["but" , "but 7m"]))])

    
    
    
    
    return buts_domicile






















## Fonction permettant de retourner le nombre de buts marqué par l'équipe à L'EXTERIEUR lors des x dernières minutes précédant la date t, lors de la journée précisée :
    
def dynamique_buts_marques_exterieur(data , date = 29 , x_dernieres_minutes = 5  , journee = "J5") :
    
    """Retourne le nbr de buts marqués par l'équipe jouant à l'extérieur sur les x_dernieres_minutes précédant 
       la date renseignée, lors de la journée de championnat voulue."""
    
    
    # On commence par récupérer le nom de l'équipe jouant à domicile / extérieur lors de cette rencontre : 
    
    equipe_domicile = list(data[data["journée"] == journee]["domicile"].unique())
    equipe_domicile = equipe_domicile[0]
    
    equipe_exterieur = list(data[data["journée"] == journee]["extérieur"].unique())
    equipe_exterieur = equipe_exterieur[0]
    
    
    
    # On commence par filtrer les données : 
    
    data_filtre = data[(data["journée"] == journee) & (data["temps"] <= date) & (data["temps"] >= date-x_dernieres_minutes)]
    
    
    
    
    
    # On compte à présent le nombre de buts marqués et encaissés par l'équipe à domicile lors de cette période du match : 
    
    buts_exterieur = len(data_filtre[(data_filtre["équipe"] == equipe_exterieur) & (data_filtre["action"].isin(["but" , "but 7m"]))])
    
    
    
    
    
    return buts_exterieur























## Fonction récapitulative permettant de connaître le nbr de buts marqués par l'équipe renseignée lors des x dernières minutes précédant la date t, lors de la journée précisée :
    
def dynamique_buts_marques(data , date = 29 , x_dernieres_minutes = 5  , journee = "J5" , equipe = "domicile") :
    
    """Retourne le nbr de buts marqués par l'équipe renseignée sur les x_dernieres_minutes précédant 
       la date renseignée, lors de la journée de championnat voulue."""
    
    
    
    # SI je souhaite calculer le différentiel pour l'équipe à domicile : 
    
    if equipe in ["domicile" , "dom"] : 
        
        return dynamique_buts_marques_domicile(data = data , date = date , x_dernieres_minutes = x_dernieres_minutes  , journee = journee)
    
    
    
    
     # SI je souhaite calculer le différentiel pour l'équipe à l'extérieur : 
        
    elif equipe in ["extérieur" , "ext"] : 
        
        return dynamique_buts_marques_exterieur(data = data , date = date , x_dernieres_minutes = x_dernieres_minutes  , journee = journee)
        
        
        
        
        
    else : 
        
        raise ValueError("paramètre attendu pour l'argument {equipe} : 'domicile' , 'dom' , 'extérieur' ou 'ext'.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
  
        
## Fonction retournant un camembert PLOTLY du nombre de buts inscrits par joueur de l'équipe jouant à domicile, lors d'un match bien précis :
    
def camembert_domicile_plotly(data , journee = "J5" , show_title = True , type_action = ["but" , "but 7m"] , 
                              showlegend = False) : 

    """Retourne un diagramme circulaire du type d'actions voulu, par joueur de l'équipe jouant à domicile, lors de la rencontre 
       précisée."""
    
    
    
    # Filtrage des données qui nous intéressent :
    
    data_filtre = data[(data["journée"] == journee) & data["action"].isin(type_action)]
    
    
    
    
    # Récupération du nom de l'équipe jouant à domicile : 
    
    equipe_domicile = list(data_filtre["domicile"].unique()) 
    equipe_domicile = equipe_domicile[0]
    
    
    
    # Graphique : 
    
    fig = px.pie(values = data_filtre[data_filtre["équipe"] == equipe_domicile]["joueur"].value_counts() , 
                 names = data_filtre[data_filtre["équipe"] == equipe_domicile]["joueur"].value_counts(normalize = True).index , 
                 color_discrete_sequence = px.colors.sequential.RdBu , 
                 hole = 1/5)
    
    
    
    fig.update_traces(textposition = "inside" , 
                      textinfo = "percent+label")


    
    
    
    if show_title == True : 
        
        if len(type_action) == 2 : 
            
            if "but" in type_action : 
        
                fig.update_layout(title_text = f"Répartition des buts de {equipe_domicile} marqués par joueur, {journee}" , 
                                  showlegend = showlegend)
        
        
            else : 
                
                fig.update_layout(title_text = f"Répartition des avertissements + 2min de {equipe_domicile} par joueur, {journee}" , 
                                  showlegend = showlegend)
        
        
        else : 
            
            fig.update_layout(title_text = f"Répartition des {type_action[0]} de {equipe_domicile} marqués par joueur, {journee}" , 
                              showlegend = showlegend)
            
            
            
    
    else : 
        
        fig.update_layout(showlegend = showlegend)
        
        
    
    
    
    
    
    
    return fig





















## Fonction retournant un camembert PLOTLY du nombre de buts inscrits par joueur de l'équipe jouant à l'extérieur, lors d'un match bien précis :
    
def camembert_exterieur_plotly(data , journee = "J5" , show_title = True , type_action = ["but" , "but 7m"] , 
                               showlegend = False) : 

    """Retourne un diagramme circulaire du type d'actions voulu, par joueur de l'équipe jouant à l'extérieur, lors de la rencontre 
       précisée."""
    
    
    
    # Filtrage des données qui nous intéressent :
    
    data_filtre = data[(data["journée"] == journee) & data["action"].isin(type_action)]
    
    
    
    
    # Récupération du nom de l'équipe jouant à l'extérieur : 
    
    equipe_exterieur = list(data_filtre["extérieur"].unique()) 
    equipe_exterieur = equipe_exterieur[0]
    
    
    
    # Graphique : 
    
    fig = px.pie(values = data_filtre[data_filtre["équipe"] == equipe_exterieur]["joueur"].value_counts() , 
                 names = data_filtre[data_filtre["équipe"] == equipe_exterieur]["joueur"].value_counts(normalize = True).index , 
                 color_discrete_sequence = px.colors.sequential.RdBu , 
                 hole = 1/5)
    
    
    
    fig.update_traces(textposition = "inside" , 
                      textinfo = "percent+label")


    
    
    
    if show_title == True : 
        
        if len(type_action) == 2 : 
            
            if "but" in type_action : 
        
                fig.update_layout(title_text = f"Répartition des buts de {equipe_exterieur} marqués par joueur, {journee}" , 
                                  showlegend = showlegend)
        
        
            else : 
                
                fig.update_layout(title_text = f"Répartition des avertissements + 2min de {equipe_exterieur} par joueur, {journee}" , 
                                  showlegend = showlegend)
        
        
        else : 
            
            fig.update_layout(title_text = f"Répartition des {type_action[0]} de {equipe_exterieur} marqués par joueur, {journee}" , 
                              showlegend = showlegend)
            
            
            
            
    else : 
        
        fig.update_layout(showlegend = showlegend)
        
        
    
    
    
    
    
    
    return fig





















## Fonction récapitulative retournant un camembert PLOTLY du nombre de buts inscrits par joueur de l'équipe jouant à domicile OU à l'extérieur (au choix), lors d'un match bien précis :
    
def camembert_plotly(data , journee = "J5" , show_title = True , type_action = ["but" , "but 7m"] , 
                     equipe = "domicile" , showlegend = False) : 

    """Retourne un diagramme circulaire du type d'actions voulu, par joueur de l'équipe renseignée, lors de la rencontre 
       précisée."""
    
    
    
    # CAS 1 : si je souhaite regarder l'équipe jouant à domicile : 
    
    if equipe in ["domicile" , "dom"] : 
        
        return camembert_domicile_plotly(data = data , journee = journee , show_title = show_title , 
                                         type_action = type_action , showlegend = showlegend)
    
    
    
    
    
    # CAS 2 : si je souhaite regarder l'équipe jouant à l'extérieur : 
    
    if equipe in ["extérieur" , "ext"] : 
        
        return camembert_exterieur_plotly(data = data , journee = journee , show_title = show_title , 
                                          type_action = type_action , showlegend = showlegend)
    
    
    
    
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'equipe' : 'domicile' , 'dom' , 'extérieur' ou 'ext'.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


        
        
        
## Fonction permettant de tracer le diagramme en barres souhaité concernant les joueurs de l'équipe à domicile, lors d'un match précis :
    
def diagramme_en_barres_domicile_plotly(data , journee = "J1" , type_action = ["but" , "but 7m"]) :
    
    """Retourne le diagramme en barres demandé concernant les joueurs de l'équipe à domicile lors de la rencontre renseignée."""
    
    
    
    # On récupère le nom de l'équipe jouant à domicile : 
    
    equipe_domicile = data[data["journée"] == journee]["domicile"].unique()
    equipe_domicile = equipe_domicile[0]
    
    
    
    
    # On filtre les données : 
    
    data_filtre = data[(data["journée"] == journee) & (data["action"].isin(type_action)) & (data["équipe"] == equipe_domicile)]
    
    
    
    
    # On trace le diagramme en barre souhaité :
    
    fig = px.bar(x = data_filtre["joueur"].value_counts().index , 
                 y = data_filtre["joueur"].value_counts() , 
                 color = data_filtre["joueur"].value_counts() , 
                 text = data_filtre["joueur"].value_counts())


    
    
    if type_action == ["but" , "but 7m"] : 
        
        yaxis_title = "buts"
        
        
        
    elif type_action == ["tir" , "but" , "but 7m"] : 
        
        yaxis_title = "tirs"
        
       
    
    else : 
        
        yaxis_title = type_action[0]
        
        
        
        
        
        
    fig.update_layout(xaxis_title = "joueur" , 
                      yaxis_title = yaxis_title , 
                      template = "plotly_dark" , 
                      title_text = f"Répartition des {yaxis_title} de {equipe_domicile.upper()}, par joueur." , 
                      title_x = 0.5 ,
                      title_font = {"size" : 30 , 
                                    "family" : "serif"})


    fig.update_yaxes(range = [0 , data_filtre["joueur"].value_counts().max() + 1])


    
    fig.update_traces(textposition = "outside" , 
                      textfont = {"size" : 16 , 
                                  "color" : "red"})
    
    
    
    fig.update(layout_coloraxis_showscale = False)   # Pour masquer la barre de couleur
    
    
    
    
    
    return fig





















## Fonction permettant de tracer le diagramme en barres souhaité concernant les joueurs de l'équipe à l'extérieur, lors d'un match précis :
    
def diagramme_en_barres_exterieur_plotly(data , journee = "J1" , type_action = ["but" , "but 7m"]) :
    
    """Retourne le diagramme en barres demandé concernant les joueurs de l'équipe à l'extérieur lors de la rencontre renseignée."""
    
    
    
    # On récupère le nom de l'équipe jouant à l'extérieur : 
    
    equipe_exterieur = data[data["journée"] == journee]["extérieur"].unique()
    equipe_exterieur = equipe_exterieur[0]
    
    
    
    
    # On filtre les données : 
    
    data_filtre = data[(data["journée"] == journee) & (data["action"].isin(type_action)) & (data["équipe"] == equipe_exterieur)]
    
    
    
    
    # On trace le diagramme en barre souhaité :
    
    fig = px.bar(x = data_filtre["joueur"].value_counts().index , 
                 y = data_filtre["joueur"].value_counts() , 
                 color = data_filtre["joueur"].value_counts() , 
                 text = data_filtre["joueur"].value_counts())


    
    
    if type_action == ["but" , "but 7m"] : 
        
        yaxis_title = "buts"
        
        
        
    elif type_action == ["tir" , "but" , "but 7m"] : 
        
        yaxis_title = "tirs"
        
       
    
    else : 
        
        yaxis_title = type_action[0]
        
        
        
        
        
        
    fig.update_layout(xaxis_title = "joueur" , 
                      yaxis_title = yaxis_title , 
                      template = "plotly_dark" , 
                      title_text = f"Répartition des {yaxis_title} de {equipe_exterieur.upper()}, par joueur." , 
                      title_x = 0.5 ,
                      title_font = {"size" : 30 , 
                                    "family" : "serif"})


    fig.update_yaxes(range = [0 , data_filtre["joueur"].value_counts().max() + 1])


    
    fig.update_traces(textposition = "outside" , 
                      textfont = {"size" : 16 , 
                                  "color" : "red"})
    
    
    
    fig.update(layout_coloraxis_showscale = False)   # Pour masquer la barre de couleur
     
    
    
    
    
    return fig




















## Fonction récapitulative permettant de tracer le diagramme en barres souhaité concernant les joueurs de l'équipe renseignée (domicile OU extérieur, au choix), lors d'un match précis :
    
def diagramme_en_barres_plotly(data , journee = "J1" , type_action = ["but" , "but 7m"] , equipe = "domicile") :
    
    """Retourne le diagramme en barres demandé concernant les joueurs de l'équipe voulue (domicile ou extérieur, au choix) 
       lors de la rencontre renseignée."""
    
    
    
    if equipe in ["domicile" , "dom"] : 
        
        return diagramme_en_barres_domicile_plotly(data = data , journee = journee , type_action = type_action)
        
        
        
        
    elif equipe in ["extérieur" , "ext"] : 
        
        return diagramme_en_barres_exterieur_plotly(data = data , journee = journee , type_action = type_action)
    
        
        
        
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'equipe' : 'domicile' , 'dom' , 'extérieur' ou 'ext'.")  
        
        
        
        
        
        
#####################################################################################################################
#####################################################################################################################

###                                     FONCTIONS DE BILAN DE SAISON DE L'USDH :
    
#####################################################################################################################
#####################################################################################################################

## FONCTIONS D'ANALYSE :
    
#####################################################################################################################


## Fonction permettant de connaître le nombre d'actions du type renseigné réalisées par l'USDH OU par ses adversaires (au choix) depuis le début de la saison :
    
def nbr_type_action_saison(data , type_action = "buts marqués" , format_retour = "total" , equipe = "USDH" , periode = "match") :
    
    
    """Retourne au choix le nombre d'actions du type renseigné réalisées par l'USDH depuis le début de la saison."""
    
    
    
    if equipe == "USDH" : 
        
        
        if periode == "match" : 
            
    
            if type_action == "buts marqués" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "buts encaissés" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "tirs tentés" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["action"].isin(["tir" , "tirs 7m" , "but" , "but 7m"]))]




            elif type_action == "cartons jaunes" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["action"] == "avertissement")]  




            elif type_action == "exclusions" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["action"] == "2min")]




            elif type_action == "arrêts" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["action"].isin(["arrêt" , "arrêt 7m"]))]




            else : 

                raise ValueError("paramètre attendu pour l'argument 'type_action' : 'buts marqués' , 'buts encaissés' , 'tirs tentés' , 'cartons jaunes' , 'exclusions' ou 'arrêts'.")

        
        
        
        
        
        
        
        elif periode == "M1" : 
            
            
            if type_action == "buts marqués" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] <= 30) & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "buts encaissés" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] <= 30) & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "tirs tentés" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] <= 30) & (data["action"].isin(["tir" , "tirs 7m" , "but" , "but 7m"]))]




            elif type_action == "cartons jaunes" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] <= 30) & (data["action"] == "avertissement")]  




            elif type_action == "exclusions" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] <= 30) & (data["action"] == "2min")]




            elif type_action == "arrêts" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] <= 30) & (data["action"].isin(["arrêt" , "arrêt 7m"]))]




            else : 

                raise ValueError("paramètre attendu pour l'argument 'type_action' : 'buts marqués' , 'buts encaissés' , 'tirs tentés' , 'cartons jaunes' , 'exclusions' ou 'arrêts'.")
 
            
            
            
         
        
        elif periode == "M2" : 
            
            
            if type_action == "buts marqués" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] > 30) & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "buts encaissés" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] > 30) & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "tirs tentés" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] > 30) & (data["action"].isin(["tir" , "tirs 7m" , "but" , "but 7m"]))]




            elif type_action == "cartons jaunes" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] > 30) & (data["action"] == "avertissement")]  




            elif type_action == "exclusions" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] > 30) & (data["action"] == "2min")]




            elif type_action == "arrêts" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] > 30) & (data["action"].isin(["arrêt" , "arrêt 7m"]))]




            else : 

                raise ValueError("paramètre attendu pour l'argument 'type_action' : 'buts marqués' , 'buts encaissés' , 'tirs tentés' , 'cartons jaunes' , 'exclusions' ou 'arrêts'.")
 
            
            
            
            
            
            
            
            

        
    
    
    elif equipe == "adversaire" : 
        
    
        if periode == "match" : 
            
    
            if type_action == "buts marqués" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "buts encaissés" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "tirs tentés" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["action"].isin(["tir" , "tirs 7m" , "but" , "but 7m"]))]




            elif type_action == "cartons jaunes" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["action"] == "avertissement")]  




            elif type_action == "exclusions" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["action"] == "2min")]




            elif type_action == "arrêts" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["action"].isin(["arrêt" , "arrêt 7m"]))]




            else : 

                raise ValueError("paramètre attendu pour l'argument 'type_action' : 'buts marqués' , 'buts encaissés' , 'tirs tentés' , 'cartons jaunes' , 'exclusions' ou 'arrêts'.")

        
        
        
        
        
        
        
        elif periode == "M1" : 
            
            
            if type_action == "buts marqués" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] <= 30) & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "buts encaissés" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] <= 30) & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "tirs tentés" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] <= 30) & (data["action"].isin(["tir" , "tirs 7m" , "but" , "but 7m"]))]




            elif type_action == "cartons jaunes" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] <= 30) & (data["action"] == "avertissement")]  




            elif type_action == "exclusions" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] <= 30) & (data["action"] == "2min")]




            elif type_action == "arrêts" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] <= 30) & (data["action"].isin(["arrêt" , "arrêt 7m"]))]




            else : 

                raise ValueError("paramètre attendu pour l'argument 'type_action' : 'buts marqués' , 'buts encaissés' , 'tirs tentés' , 'cartons jaunes' , 'exclusions' ou 'arrêts'.")
 
            
            
            
         
        
        elif periode == "M2" : 
            
            
            if type_action == "buts marqués" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] > 30) & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "buts encaissés" : 

                data_filtre = data[(data["équipe"] == "USDH") & (data["temps"] > 30) & (data["action"].isin(["but" , "but 7m"]))]




            elif type_action == "tirs tentés" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] > 30) & (data["action"].isin(["tir" , "tirs 7m" , "but" , "but 7m"]))]




            elif type_action == "cartons jaunes" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] > 30) & (data["action"] == "avertissement")]  




            elif type_action == "exclusions" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] > 30) & (data["action"] == "2min")]




            elif type_action == "arrêts" : 

                data_filtre = data[(data["équipe"] != "USDH") & (data["temps"] > 30) & (data["action"].isin(["arrêt" , "arrêt 7m"]))]




            else : 

                raise ValueError("paramètre attendu pour l'argument 'type_action' : 'buts marqués' , 'buts encaissés' , 'tirs tentés' , 'cartons jaunes' , 'exclusions' ou 'arrêts'.")
 
            
        
        
    
    
    
    
    # SI un souhaite le TOTAL des buts : 
    
    if format_retour == "total" :
        
        nbr_total_buts = len(data_filtre)
        
        return nbr_total_buts
    
    
    
    
    elif format_retour == "par match" : 
        
        nbr_buts_par_match = len(data_filtre) / len(data["journée"].unique())
        
        return nbr_buts_par_match
    
    
    
    else : 
        
        raise ValueError("paramètre attendu pour l'argument 'format_retour' : 'total' ou 'par match'.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        




## Fonction permettant de retourner la SERIES du nombre d'actions du type renseigné effectuées par l'USDH OU par ses adversaires (au choix) lors de chaque match joué depuis le début de la saison :
    
def S_nbr_type_action_saison(data , type_action = "buts marqués" , equipe = "USDH" , periode = "match") :
    
    
    """Retourne la Series du nombre d'actions du type renseigné réalisées par l'équipe voulue lors de chacun des matchs qu'elle 
       a jouée depuis le début de la saison."""
    
    
    
        
        
    if periode == "match" : 

        filtre_periode = (data["temps"] >= 0) & (data["temps"] <= 60)



    elif periode == "M1" : 

        filtre_periode = data["temps"] <= 30




    elif periode == "M2" : 

        filtre_periode = data["temps"] > 30




    else : 

        raise ValueError("paramètre attendu pour l'argument 'periode' : 'match' , 'M1' ou 'M2'.")
        
        
        
        
        
        
    
    if equipe == "USDH" : 
            
            
    
        if type_action == "buts marqués" : 

            filtre_equipe = data["équipe"] == "USDH"
            filtre_action = data["action"].isin(["but" , "but 7m"])




        elif type_action == "buts encaissés" : 

            filtre_equipe = data["équipe"] != "USDH"
            filtre_action = data["action"].isin(["but" , "but 7m"])




        elif type_action == "tirs tentés" : 

            filtre_equipe = data["équipe"] == "USDH"
            filtre_action = data["action"].isin(["tir" , "tirs 7m" , "but" , "but 7m"])



        elif type_action == "cartons jaunes" : 


            filtre_equipe = data["équipe"] == "USDH"
            filtre_action = data["action"] == "avertissement"




        elif type_action == "exclusions" : 

            filtre_equipe = data["équipe"] == "USDH"
            filtre_action = data["action"] == "2min"

            


        elif type_action == "arrêts" : 

            filtre_equipe = data["équipe"] == "USDH"
            filtre_action = data["action"].isin(["arrêt" , "arrêt 7m"])


            

        else : 

            raise ValueError("paramètre attendu pour l'argument 'type_action' : 'buts marqués' , 'buts encaissés' , 'tirs tentés' , 'cartons jaunes' , 'exclusions' ou 'arrêts'.")




        L_nbr_actions = []


        # Pour chaque journée de championnat disputée par cette équipe :

        for journee in dico_rencontres_USDH.keys() :


            data_filtre = data[filtre_periode & (data["journée"] == journee) & (filtre_equipe) & (filtre_action)]

            nbr_actions_journee = len(data_filtre)

            L_nbr_actions.append(nbr_actions_journee)



        return pd.Series(L_nbr_actions)
        
        
        
        
        

        
        
    
    
    elif equipe == "adversaire" : 
        
    
        if type_action == "buts marqués" : 

            filtre_equipe = data["équipe"] != "USDH"
            filtre_action = data["action"].isin(["but" , "but 7m"])




        elif type_action == "buts encaissés" : 

            filtre_equipe = data["équipe"] == "USDH"
            filtre_action = data["action"].isin(["but" , "but 7m"])




        elif type_action == "tirs tentés" : 

            filtre_equipe = data["équipe"] != "USDH"
            filtre_action = data["action"].isin(["tir" , "tirs 7m" , "but" , "but 7m"])



        elif type_action == "cartons jaunes" : 


            filtre_equipe = data["équipe"] != "USDH"
            filtre_action = data["action"] == "avertissement"




        elif type_action == "exclusions" : 

            filtre_equipe = data["équipe"] != "USDH"
            filtre_action = data["action"] == "2min"

            


        elif type_action == "arrêts" : 

            filtre_equipe = data["équipe"] != "USDH"
            filtre_action = data["action"].isin(["arrêt" , "arrêt 7m"])


            

        else : 

            raise ValueError("paramètre attendu pour l'argument 'type_action' : 'buts marqués' , 'buts encaissés' , 'tirs tentés' , 'cartons jaunes' , 'exclusions' ou 'arrêts'.")




        L_nbr_actions = []


        # Pour chaque journée de championnat disputée par cette équipe :

        for journee in dico_rencontres_USDH.keys() :


            data_filtre = data[filtre_periode & (data["journée"] == journee) & (filtre_equipe) & (filtre_action)]

            nbr_actions_journee = len(data_filtre)

            L_nbr_actions.append(nbr_actions_journee)



        return pd.Series(L_nbr_actions)
    
    
    
    
    
    
    
    else : 
        
        
        raise ValueError("paramètre attendu pour l'argument 'equipe' : 'USDH' ou 'adversaire'.")
        
























## Fonction permettant de retourner la SERIES des temps passés en tête / derrière / à égalité (au choix) par l'équipe renseignée lors de chaque match joué depuis le début de la saison :

def S_durees_situation_score_saison(data , equipe = "USDH" , situation = "mène") :
    
    
    """Retourne la Series des temps passés dans la situation au score voulue par l'équipe renseignée, lors de chaque match de 
       championnat disputé depuis le début de la saison."""
    
    
    L_durees = []
    
    
    # Pour chaque journée de championnat disputée :
    
    for journee in dico_rencontres_USDH.keys() :
        
        
        # On récupère le dictionnaire des temps passés par l'USDH dans chaque situation au score lors de ce match :
        
        dico_durees_situations_journee = duree_situation_score(data = data , journee = journee)[2]  # le 3ème dictionnaire retourné par cette fonction contient les durées TOTALES pssées dans chacune des 3 situations au score
        
        
        
        if situation == "mène" : 
            
            
            if equipe == "USDH" : # ==> le temps passé par l'USDH à mener au score est accessible via la clé 'USDH mène' du dictionnaire ci-dessus
                

                duree_equipe_mene = dico_durees_situations_journee["USDH mène"]
                
                
                L_durees.append(duree_equipe_mene)

                
                
                
                
            elif equipe == "adversaire" : # ==> le temps passé par l'adversaire de l'USDH à mener au score est accessible via la clé 'adversaire mène' du dictionnaire ci-dessus

                
                duree_equipe_mene = dico_durees_situations_journee["adversaire mène"]

            
                L_durees.append(duree_equipe_mene)
                
                
                
                
            else : 
                
                raise ValueError("paramètre attendu pour l'argument 'equipe' : 'USDH' ou 'adversaire'.")
                
                
                
                
            
            
            
            
            
        elif situation == "est mené" : 
            
            
            if equipe == "USDH" : # ==> le temps passé par l'USDH à être mené au score est accessible via la clé 'adversaire mène' du dictionnaire ci-dessus
                

                duree_equipe_est_menee = dico_durees_situations_journee["adversaire mène"]
                
                
                L_durees.append(duree_equipe_est_menee)

                
                
                
                
            elif equipe == "adversaire" : # ==> le temps passé par l'adversaire de l'USDH à être mené au score est accessible via la clé 'adversaire mène' du dictionnaire ci-dessus

                
                duree_equipe_est_menee = dico_durees_situations_journee["USDH mène"]

            
                L_durees.append(duree_equipe_est_menee)
                
                
                
                
            else : 
                
                raise ValueError("paramètre attendu pour l'argument 'equipe' : 'USDH' ou 'adversaire'.")
                
                
                
                
                
            
        
        elif situation == "égalité" :
            
            
            duree_equipe_egalite = dico_durees_situations_journee["égalité"]

            
            L_durees.append(duree_equipe_egalite)
                
                
                
          
        
        
        else : 
            
            raise ValueError("paramètre attendu pour l'argument 'situation' : 'mène' , 'est mené' ou 'égalité'.")
    
    
   


    return pd.Series(L_durees)
























## Fonction permettant de retourner la SERIES des temps passés en supériorité / infériorité / à égalité numérique (au choix) par l'équipe renseignée lors de chaque match joué depuis le début de la saison :
    
def S_durees_situation_numerique_saison(data , equipe = "USDH" , situation = "infériorité numérique") :
    
    
    """Retourne la Series des temps passés dans la situation numérique voulue par l'équipe renseignée, lors de chaque match de 
       championnat disputé depuis le début de la saison."""
    
    
    L_durees = []
    
    
    # Pour chaque journée de championnat disputée :
    
    
    if equipe in ["USDH" , "adversaire"] :
    
        for journee in dico_rencontres_USDH.keys() :



            if equipe == "USDH" : 

                duree_equipe_en_sup_journee = duree_passee_situation_numerique_equipe(data = data , journee = journee , 
                                                                                      equipe = equipe , format_duree = 'float' , 
                                                                                      situation = situation)


                


                





            elif equipe == "adversaire" :

                # On récupère l'adversaire de l'USDH ce jour-là : 

                adv = [equipe for equipe in data[data["journée"] == journee]["équipe"].unique() if equipe not in [" " , "USDH"]]
                adv = adv[0]



                duree_equipe_en_sup_journee = duree_passee_situation_numerique_equipe(data = data , journee = journee , 
                                                                                      equipe = adv , format_duree = 'float' , 
                                                                                      situation = situation)




            L_durees.append(duree_equipe_en_sup_journee)


        
        
        return pd.Series(L_durees)

                
                
                
                
            
       
                
    else : 

        raise ValueError("paramètre attendu pour l'argument 'equipe' : 'USDH' ou 'adversaire'.")






















## Fonction permettant de retourner la SERIES des nbr de buts marqués / encaissés / différentiels (au choix) en supériorité / infériorité / à égalité numérique (au choix) par l'équipe renseignée lors de chaque match joué depuis le début de la saison :
    
def S_bilan_situation_numerique_saison(data , equipe = "USDH" , situation = "infériorité numérique" , type_bilan = "buts marqués") :
    
    
    """Retourne la Series des nbr de buts marqués / encaissés / différentiels (au choix) en supériorité / infériorité / à égalité 
       numérique (au choix) par l'équipe renseignée lors de chaque match joué depuis le début de la saison."""
    
    
    
    L_bilans_equipe = []
    
    
    if type_bilan in ["buts marqués" , "buts encaissés" , "différentiel de buts"] :
        
        
        if situation in ["infériorité numérique" , "supériorité numérique" , "égalité numérique"] : 
            
            
            if equipe in ["USDH" , "adversaire"] :
                
                
                
                # Pour chaque journée de championnat déjà jouée par cette équipe :
                
                for journee in dico_rencontres_USDH.keys() :
                
                
                    if equipe == "USDH" :


                        # On récupère le dictionnaire contenant, pour chaque période passée dans la situation numérique renseignée par l'USDH LORS DE CE MATCH, le bilan comptable de l'USDH :

                        dico_bilans_equipe_situation_journee = bilan_situation_numerique_equipe(data = data , journee = journee , 
                                                                                                equipe = "USDH" , 
                                                                                                situation = situation)
                        
                        
                        
                        
                        # On extrait de ce dictionnaire la liste des buts marqués / buts encaissés / différentiels de buts (au choix) pour chaque période que l'USDH a joué dans ce type de situation numérique LORS DE CE MATCH : 
                    
                        L_bilans_equipe_situation_journee = [dico_bilans_equipe_situation_journee[periode][f"{type_bilan} USDH"] for periode in dico_bilans_equipe_situation_journee.keys()]

        
        
                        




                    else :    # equipe == "adversaire" : 


                        # on récupère le nom de l'adversaire de l'USDH lors de cette rencontre :

                        adversaire = [equipe for equipe in data[data["journée"] == journee]["équipe"].unique() if equipe not in [" " , "USDH"]]
                        adversaire = adversaire[0]



                        # On récupère le dictionnaire contenant, pour chaque période passée dans la situation numérique renseignée par l'adversaire de l'USDH LORS DE CE MATCH, le bilan comptable de cet adversaire :

                        dico_bilans_equipe_situation_journee = bilan_situation_numerique_equipe(data = data , journee = journee , 
                                                                                                equipe = adversaire , 
                                                                                                situation = situation)

                        
                        
                    
                        # On extrait de ce dictionnaire la liste des buts marqués / buts encaissés / différentiels de buts (au choix) pour chaque période que l'adversaire de l'USDH a joué dans ce type de situation numérique LORS DE CE MATCH : 
                    
                        L_bilans_equipe_situation_journee = [dico_bilans_equipe_situation_journee[periode][f"{type_bilan} {adversaire}"] for periode in dico_bilans_equipe_situation_journee.keys()]

                
                
                
                
                
                    # On récupère le bilan (buts marqués / encaissés / différentiel de buts, au choix) TOTAL de l'équipe voulue dans ce type de situation numérique LORS DE CE MATCH, en sommant les éléments de la liste ci-dessus :
        
                    bilan_equipe_situation_journee = sum(L_bilans_equipe_situation_journee)




                    # On ajoute le bilan de l'équipe LORS DE CETTE JOURNEE à la liste des bilans de chaqu journée déjà disputée par l'équipe :

                    L_bilans_equipe.append(bilan_equipe_situation_journee)
                
                
                
                
                
                # On retourne la Series des bilans de cette équipe lors de chaque match déjà disputé :
                
                return pd.Series(L_bilans_equipe)
            
            
            
                
                
                
            else : 
                
                raise ValueError("paramètre attendu pour l'argument 'equipe' : 'USDH' ou 'adversaire'.")
                
              
            
            
            
            
            
                
        else : 
                
                raise ValueError("paramètre attendu pour l'argument 'situation' : 'infériorité numérique', 'supériorité numérique' ou 'égalité numérique'.")
                
      
    
    
    
    
    
    else : 
                
        raise ValueError("paramètre attendu pour l'argument 'type_bilan' : 'buts marqués', 'buts encaissés' ou 'différentiel de buts'.")
                
                








#####################################################################################################################

## FONCTIONS GRAPHIQUES : 

#####################################################################################################################


## Fonction permettant de retourner un double histogramme vertical du type d'action renseigné de l'USDH et de ses adversaires par tranche de 5 minutes, depuis le début de la saison :
    
def double_vertical_histogram_type_action_saison(fig , ax , data , type_action = ["but" , "but 7m"] , show_title = False , 
                                                 nbr_tranches = 12 , text_color = "black" , unite = "total") : 
    
    
    
    from itertools import permutations
    
    
    
    # SI l'utilisateur souhaite écrire les textes (graduations, noms des axes, titre, ...) en BLANC : 
    
    if text_color == "white" : 
        
        
        # Alors la couleur de fond du graphique st NOIRE :
        
        fig.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")
    
    
    
    
    
    
    # Filtrage des données concernées : 

    data_filtre = data[data["action"].isin(type_action)]
        
        
        

        
    if nbr_tranches in [3 , 4 , 5 , 6 , 10 , 12, 15, 20, 30, 60] :
        
        
        if nbr_tranches != 12 : 
            
            data_filtre["intervalle de temps"] = pd.cut(df["temps"] , bins = np.arange(0 , 61 , 60//nbr_tranches) , 
                                                        include_lowest = True)
            
            


        # diagramme en barres verticales de l'USDH (vers le haut ==> width >= 0) :
        
        # SI je souhaite le diagramme en barres du TOTAL des actions de ce type, depuis le début de saison : 
        
        if unite == "total" :
            
            S_height_USDH = data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index()
            S_height_adv = (-1)*data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().sort_index()
                
            
            
            
        elif unite == "moyenne / match" :
            
            S_height_USDH = data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index() / len(dico_rencontres_USDH)
            S_height_adv = (-1)*data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().sort_index() / len(dico_rencontres_USDH)
            
            
            
        else : 
            
            raise ValueError("paramètre attendu pour l'argument 'unite' : 'total' ou 'moyenne / match'.")
            
            
        
        
        
        
        # Choix du label à afficher : 
            

        if (tuple(type_action) in list(permutations(["but" , "but 7m"]))) or ((tuple(type_action) in list(permutations(["but" , "but 7m" , " "]))) or ((tuple(type_action) in list(permutations(["but" , "but 7m" , "tir" , "tir 7m"]))) or ((tuple(type_action) in list(permutations(["2min" , "avertissement"]))) or ((type_action == ["but"]) or ((type_action == ["but 7m"]) or ((type_action == ["tir"]) or ((type_action == ["avertissement"]) or ((type_action == ["2min"]))))))))) : 
            
            
            if tuple(type_action) in permutations(["but" , "but 7m"]) : 
                
                label_USDH = "buts marqués USDH"
                label_adv = "buts encaissés USDH"
                
                
            
            elif tuple(type_action) in permutations(["but" , "but 7m" , "tir" , "tir 7m"]) : 
                
                label_USDH = "tirs tentés USDH"
                label_adv = "tirs subbis USDH"
                
                
                
            elif tuple(type_action) in permutations(["2min" , "avertissement"]) : 
                
                label_USDH = "punitions reçues USDH"
                label_adv = "punitions reçues adversaires"
                
                
                
            elif type_action == ["but"] : 
                
                label_USDH = "buts marqués dans le jeu USDH"
                label_adv = "buts encaissés dans le jeu USDH"
                
                
                
            elif type_action == ["but 7m"] : 
                
                label_USDH = "buts marqués 7m USDH"
                label_adv = "buts encaissés 7m USDH"
                
                
                
            elif type_action == ["tir"] : 
                
                label_USDH = "tirs tentés 7m USDH"
                label_adv = "tirs subbis 7m USDH"
                
                
                
            elif type_action == ["avertissement"] : 
                
                label_USDH = "avertissements reçus USDH"
                label_adv = "avertissements reçus adversaires"
                
                
                
            elif type_action == ["2min"] : 
                
                label_USDH = "2min reçus USDH"
                label_adv = "2min reçus adversaires"
            
            
            
        

            

            ax.bar(x = range(1, nbr_tranches + 1) ,   # car si on découpe les 60 minutes en intervalle de 5 minutes, on trouve 12 intervalles (5 x 12 = 60).
                   height = S_height_USDH , 
                   align = 'center' , 
                   color = '#71E014' , 
                   label = label_USDH)
    
    
    
            # Idem pour son adversaire (vers le bas): 
    
            ax.bar(x = range(1, nbr_tranches + 1) , 
                   height = S_height_adv , 
                   align = 'center' , 
                   color = "#FF0000" , 
                   label = label_adv)
            
            
        
        
        
        else : 
            
            
            raise ValueError(f"Erreur : mauvais paramètre renseigné pour l'argument type_action' : {tuple(type_action)} mauvais !")







        # 3) Personnalisation : 

        ax.spines["top"].set_color(None)
        ax.spines["right"].set_color(None)
        ax.spines["bottom"].set_position(("data" , 0))
        ax.spines["left"].set_position(("data" , 0.5))
        
        ax.spines["left"].set_color(text_color)
        ax.spines["bottom"].set_color(text_color)
        

        ax.set_xlim([0.5 , nbr_tranches + 0.5])
        
        


        # ticks : 

        # yticks : 

        max_action_USDH = S_height_USDH.max()    # le plus grand nbr de 'type_action' effectués par l'USDH dans un intervalle de 5 minutes
        max_action_adv = (-1)*S_height_adv.min()  # le plus grand nbr de 'type_action' effectués par l'adversaire dans un intervalle de 5 minutes


        ytick_inf = (-1)*(max_action_adv + 1)      # borne inférieure des yticks
        ytick_sup = max_action_USDH + 1   # borne supérieure des yticks (+1 car un range s'arrête une unité avant la valeur spécifiée)



        ax.set_yticks(np.arange(int(ytick_inf) , int(ytick_sup) + 1 , 5))
        ax.tick_params(axis = 'y', colors = text_color)   # couleur des graduations
        ax.set_yticklabels([abs(tick) for tick in np.arange(int(ytick_inf) , int(ytick_sup) + 1 , 5)] , 
                            fontsize = 12 , 
                            color = text_color)
        
        
        
        





        # xticks :


        for tick in range(1 , nbr_tranches + 1) :

            ax.text(x = tick , 
                    y = ytick_inf + (9/10)*S_height_adv.mean() ,
                    s = f"{int(data_filtre['intervalle de temps'].value_counts().sort_index().index[tick-1].left)}ème - {int(data_filtre['intervalle de temps'].value_counts().sort_index().index[tick-1].right)}ème" ,
                    fontsize = 11 , 
                    rotation = 90 , 
                    color = text_color ,
                    verticalalignment = "center" , 
                    horizontalalignment = "center")



        ax.set_xticks(list(range(1 , nbr_tranches + 1)))
        ax.tick_params(axis = 'x', colors = text_color)   # couleur des graduations
        ax.set_xticklabels(nbr_tranches*[" "] , color = text_color)




        # titre du graphique : 

        # Si l'on regarde les tirs pris : ['tir' , 'but 7m' , 'but'] :

        if len(type_action) == 3 :


            titre = "Saison USDH : répartition des tirs par tranche de 5 minutes"


            ylabel = "nombre de tirs tentés"



        # Si l'on regarde les buts marqués : ['but 7m' , 'but'] :

        elif len(type_action) == 2 : 

            titre = "Saison USDH : répartition des buts par tranche de 5 minutes"


            ylabel = "nombre de buts inscrits"




        else : 

            titre = f"Saison USDH : répartition des {type_action[0]} par tranche de 5 minutes"


            ylabel = f"nombre de {type_action[0]}"






        if show_title == True : 

            ax.set_title(titre , fontsize = 30 , family = "serif" , color = text_color ,
                         pad = 75)





        ax.set_ylabel(ylabel , fontsize = 15 , family = "serif" , color = text_color)
        ax.set_xlabel(" ")







        # 4) Annotation des effectifs en face de chaque barre :

        # Pour chacune des 2 équipes : 

        for filtre in [data_filtre["équipe"] == "USDH" , data_filtre["équipe"] != "USDH"] :


            # Pour chaque intervalle de temps (12 au total) :

            for i , intervalle in zip(list(range(1,nbr_tranches + 1)) , data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index().index) :

                
                # CAS 1 : si le nombre de tranches souhaité vaut 3, 5 OU 15 --> la ligne de la mi-temps coupe la tranche du milieu et passe en plein sur le texte de l'effectif de cette tranche ==> décalage du texte sur un côté !
                
                if nbr_tranches in [3 , 5 , 15] : 
                    
                    if i == nbr_tranches//2 + 1 :  # S'il s'agit de la tranche du milieu :
                        
                        x = i + 0.075   # on décale le texte vers la droite
                        
                        
                    else : # SINON, s'il s'agit d'une autre tranche quelconque :
                        
                        x = i  # pas de soucis, on écrit le texte au milieu
                
                
                
                # CAS 2 : 
                
                else : 
                    
                    x = i
                    
                    
                    
                    
                # SI il s'agit des effectifs de l'USDH :

                if False not in (filtre == (data_filtre["équipe"] == "USDH")).unique() : 
                    
                    
                    # Texte et couleur du texte à afficher : 
                        
                    color = "#71E014"   # vert clair
                    txt = np.round(S_height_USDH.loc[intervalle] , 2)
                        


                    # Gestion de la taille de police : 
                        
                    # SI le nombre de tranches est élevé ET que l'on regarde les moyennes / match ==> texte long à afficher ==> réduire la taille de police :
                            
                    if (nbr_tranches in [30 , 60]) and (unite == "moyenne / match") :
                        
                        fontsize = 13
                        
                        
                        
                        # SI le nombre de tranches voulu est 60 ==> rotation des effectifs car sinon, chevauchement ==> illisible !
                        
                        if nbr_tranches == 60 : 
                            
                            rotation = 90
                            y = S_height_USDH.loc[intervalle] + (4.5/10)*S_height_USDH.mean()
                        
                            
                            
                        else : 
                            
                            rotation = 0
                            y = S_height_USDH.loc[intervalle] + (1.25/10)*S_height_USDH.mean()
                        
                        
                        
                        
                        
                        
    
                    # SINON, si le nombre de tranches est moyennement / peu élevé : 
                        
                    else :
                            
                        fontsize = 16
                        rotation = 0
                        y = S_height_USDH.loc[intervalle] + (1.25/10)*S_height_USDH.mean()
                    
                        
                    
                    
                    
                    
                        
                        
                        
                    
                    
                # SINON, s'il s'agit des effectifs de l'adversaire de l'USDH :
                    
                else : 
                    
                    
                    color = "#FF0000"
                    txt = (-1)*np.round(S_height_adv.loc[intervalle] , 2)
                    
                    
                    # Gestion de la taille de police : 
                        
                    # SI le nombre de tranches est élevé ET que l'on regarde les moyennes / match ==> texte long à afficher ==> réduire la taille de police :
                            
                    if (nbr_tranches in [30 , 60]) and (unite == "moyenne / match") :
                        
                        fontsize = 13
                        
                        
                        
                        # SI le nombre de tranches voulu est 60 ==> rotation des effectifs car sinon, chevauchement ==> illisible !
                        
                        if nbr_tranches == 60 : 
                            
                            rotation = 90
                            y = S_height_adv.loc[intervalle] + (4.5/10)*S_height_adv.mean()
                     
                        
                            
                            
                        else : 
                            
                            rotation = 0
                            y = S_height_adv.loc[intervalle] + (1.25/10)*S_height_adv.mean()
                     
                        
                        
                        
                        
                        
                        
    
                    # SINON, si le nombre de tranches est moyennement / peu élevé : 
                        
                    else :
                        
                        fontsize = 16
                        rotation = 0
                        y = S_height_adv.loc[intervalle] + (1.25/10)*S_height_adv.mean()
                     
                    
                    
                    
                       
 

                ax.text(x = x , 
                        y = y , 
                        s = txt , 
                        horizontalalignment = "center" , 
                        verticalalignment = "center" , 
                        color = color , 
                        fontsize = fontsize , 
                        rotation = rotation)








        # 5) Ligne symbolisant la mi-temps :


        ord_mi_temps_1 = ytick_inf - 0.5
        ord_mi_temps_2 = (ytick_sup-1) + (ytick_sup-1)/5 + (1.4/10)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().mean()

        abs_mi_temps = (nbr_tranches + 1)/2


        ax.plot(2*[abs_mi_temps] , [ord_mi_temps_1 , ord_mi_temps_2] , 
                color = "#00D1FF" , 
                ls = "--" , 
                lw = 2)


        ax.text(x = abs_mi_temps , 
                y = (51/50)*ord_mi_temps_2 , 
                color = "#00D1FF" , 
                fontsize = 12 , 
                s = "mi-temps" , 
                verticalalignment = "center" , 
                horizontalalignment = "center")




        ax.legend(loc = "upper left" , 
                  fontsize = 8)







        # 6) Inscription du score des 2 équipes lors de chaque période : 
        
        
        if type_action in [["but" , "but 7m"] , ["2min"] , ["avertissement"] , ["arrêt" , "arrêt 7m"] , ["tir" , "tir 7m" , "but" , "but 7m"]] :
        
        
            if type_action == ["but" , "but 7m"] :

                action = "buts marqués"


            elif type_action == ["2min"] : 

                action = "exclusions"


            elif type_action == ["avertissement"] : 

                action = "cartons jaunes"


            elif type_action == ["arrêt" , "arrêt 7m"] : 

                action = "arrêts"


            elif type_action == ["tir" , "tir 7m" , "but" , "but 7m"] : 

                action = "tirs tentés"
            
            
            
            
            
            if unite == "total" : 

                score_M1_USDH = S_nbr_type_action_saison(data = data , type_action = action , equipe = "USDH" , periode = "M1").sum()
                score_M2_USDH = S_nbr_type_action_saison(data = data , type_action = action , equipe = "USDH" , periode = "M2").sum()   # nbr de buts inscrits en 2ème période par l'USDH
    
                score_M1_adv = S_nbr_type_action_saison(data = data , type_action = action , equipe = "adversaire" , periode = "M1").sum()
                score_M2_adv = S_nbr_type_action_saison(data = data , type_action = action , equipe = "adversaire" , periode = "M2").sum()   # nbr de buts inscrits en 2ème période par les adversaires



                # Coordonnées du score de la M1 : 
                    
                x_M1_USDH = (1 + nbr_tranches/2)/2 - 2*nbr_tranches/50
                
                x_tiret_M1 = (1 + nbr_tranches/2)/2
                
                x_M1_adv = (1 + nbr_tranches/2)/2 + 2*nbr_tranches/50

                 
                
                

                
                # Coordonnées du score de la M2 : 
                    
                x_M2_USDH = (nbr_tranches + 0.25)/2 + (0.25 + nbr_tranches/2)/2 - 2*nbr_tranches/50
                
                x_tiret_M2 = (nbr_tranches + 0.25)/2 + (0.25 + nbr_tranches/2)/2

                x_M2_adv = (nbr_tranches + 0.25)/2 + (0.25 + nbr_tranches/2)/2 + 2*nbr_tranches/50
                
                
                
                # hauteur du texte : 
                    
                y_score = (ytick_sup-1) + (ytick_sup-1)/5 + (1.4/10)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().mean()
                
                




            elif unite == "moyenne / match" : 

                score_M1_USDH = S_nbr_type_action_saison(data = data , type_action = action , equipe = "USDH" , periode = "M1").sum() / len(dico_rencontres_USDH)
                score_M2_USDH = S_nbr_type_action_saison(data = data , type_action = action , equipe = "USDH" , periode = "M2").sum() / len(dico_rencontres_USDH)  # nbr de buts inscrits en 2ème période par l'USDH
    
                score_M1_adv = S_nbr_type_action_saison(data = data , type_action = action , equipe = "adversaire" , periode = "M1").sum() / len(dico_rencontres_USDH)
                score_M2_adv = S_nbr_type_action_saison(data = data , type_action = action , equipe = "adversaire" , periode = "M2").sum() / len(dico_rencontres_USDH)   # nbr de buts inscrits en 2ème période par les adversaires



                # Coordonnées du score de la M1 : 
                    
                x_M1_USDH = (1 + nbr_tranches/2)/2 - 4.5*nbr_tranches/50
                
                x_tiret_M1 = (1 + nbr_tranches/2)/2
                
                x_M1_adv = (1 + nbr_tranches/2)/2 + 1.75*nbr_tranches/50

                 
                
                

                
                # Coordonnées du score de la M2 : 
                    
                x_M2_USDH = (nbr_tranches + 0.25)/2 + (0.25 + nbr_tranches/2)/2 - 4.5*nbr_tranches/50
                
                x_tiret_M2 = (nbr_tranches + 0.25)/2 + (0.25 + nbr_tranches/2)/2

                x_M2_adv = (nbr_tranches + 0.25)/2 + (0.25 + nbr_tranches/2)/2 + 1.75*nbr_tranches/50
                
                
                
                # hauteur du texte : 
                    
                y_score = (ytick_sup-1) + (ytick_sup-1)/5 + (1.4/10)*data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().mean()
                






            # SCORE M1 : 

            # USDH : 

            ax.text(y = y_score , 
                    x = x_M1_USDH ,   # (nbr_tranches + 0.5)/4 , 
                    s = np.round(score_M1_USDH , 2) , 
                    color = "#71E014" , 
                    fontsize = 30 , 
                    verticalalignment = "center")


            # tiret : 

            ax.text(y = y_score , 
                    x = x_tiret_M1 ,  # (nbr_tranches + 0.5)/4 + nbr_tranches/30 , 
                    s = " -" , 
                    color = text_color , 
                    fontsize = 30 , 
                    verticalalignment = "center")



            # adv : 

            ax.text(y = y_score , 
                    x = x_M1_adv ,   # (nbr_tranches + 0.5)/4 + 2*nbr_tranches/30 , 
                    s = np.round(score_M1_adv , 2) , 
                    color = "#FF0000" , 
                    fontsize = 30 , 
                    verticalalignment = "center")







            # score M2 : 

            # USDH : 

            ax.text(y = y_score , 
                    x = x_M2_USDH , 
                    s = np.round(score_M2_USDH , 2) ,
                    color = "#71E014" , 
                    fontsize = 30 , 
                    verticalalignment = "center")


            # tiret : 

            ax.text(y = y_score , 
                    x = x_tiret_M2  ,     # 2.5*(nbr_tranches + 0.5)/4 + nbr_tranches/30 , 
                    s = " -" , 
                    color = text_color , 
                    fontsize = 30 , 
                    verticalalignment = "center")





            # adv : 

            ax.text(y = y_score , 
                    x = x_M2_adv , 
                    s = np.round(score_M2_adv , 2) ,
                    color = "#FF0000" , 
                    fontsize = 30 , 
                    verticalalignment = "center")
            
            
            


        

        return ax
    
    
    
    
    
    
    else : 
        
        
        raise ValueError("nombre de tranches attendu : 3, 4, 5, 6, 10, 12, 15, 20, 30 ou 60.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    



## Fonction permettant de retourner un double histogramme vertical du DIFFERENTIEL du type d'action renseigné de l'USDH et de ses adversaires par tranche de 5 minutes, depuis le début de la saison :
 
def histogram_differentiel_type_action_saison(fig , ax , data , type_action = ["but" , "but 7m"] , nbr_tranches = 12 , 
                                              text_color = "black" , unite = "total" , show_title = False) : 
    
    
    
    
    
    # SI l'utilisateur souhaite écrire les textes (graduations, noms des axes, titre, ...) en BLANC : 
    
    if text_color == "white" : 
        
        
        # Alors la couleur de fond du graphique st NOIRE :
        
        fig.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")
        
        
        
    
    
    
    # Filtrage des données concernées : 

    data_filtre = data[data["action"].isin(type_action)]
    
    
    
    
    
    if nbr_tranches in [3 , 4 , 5 , 6 , 10 , 12, 15, 20, 30, 60] :


        if nbr_tranches != 12 : 

            data_filtre["intervalle de temps"] = pd.cut(df["temps"] , bins = np.arange(0 , 61 , 60//nbr_tranches) , 
                                                        include_lowest = True)







        # diagramme en barres verticales des différentiels de buts :

        # On calcule la Series des différentiels, en faveur de l'USDH : 

        S_differentiel = data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index() - data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().sort_index()
        
        
        # On construit le DataFrame (à 1 seule colonne : 'intervalle de temps') des différentiels, en faveur de l'USDH : 

            
        # CAS 1 : SI l'on souhaite l'histogramme des différentiels TOTAUX par tranche, depuis le début de la saison :
           
        if unite == "total" : 
            
            
            data_differentiel = pd.DataFrame(data = S_differentiel)
            
            
            
        
        # CAS 2 : SI l'on souhaite l'histogramme des différentiels MOYENS / MATCH par tranche, depuis le début de la saison :
            
        elif unite == "moyenne / match" : 
            
            data_differentiel = pd.DataFrame(data = S_differentiel / len(dico_rencontres_USDH))
            
            
            
            
        else : 
            
            raise ValueError("paramètre attendu pour l'argument 'unite' : 'total' ou 'moyenne / match'.")
            
        
        
            
            
        # SI le nombre de tranches renseigné est le bon :

        if nbr_tranches in [3, 4, 5, 6, 10, 12, 15, 20, 30, 60] :



            # PARTIE 1 : histogramme des différentiels positifs (en VERT) :

            data_differentiel_pos = data_differentiel[data_differentiel["intervalle de temps"] > 0]
    

            ax.bar(x = np.arange(1, nbr_tranches + 1)[data_differentiel["intervalle de temps"] > 0] ,   # car si on découpe les 60 minutes en intervalle de 5 minutes, on trouve 12 intervalles (5 x 12 = 60).
                   height = data_differentiel_pos["intervalle de temps"] , 
                   align = 'center' , 
                   color = '#1FBF28')





            # PARTIE 2 : histogramme des différentiels negatifs (en ROUGE) :
                
            data_differentiel_neg = data_differentiel[data_differentiel["intervalle de temps"] < 0]


            ax.bar(x = np.arange(1, nbr_tranches + 1)[data_differentiel["intervalle de temps"] < 0] ,   # car si on découpe les 60 minutes en intervalle de 5 minutes, on trouve 12 intervalles (5 x 12 = 60).
                   height = data_differentiel_neg["intervalle de temps"] , 
                   align = 'center' , 
                   color = 'red')
            
            


    

            # 3) Personnalisation : 
    
            ax.spines["top"].set_color(None)
            ax.spines["right"].set_color(None)
            ax.spines["bottom"].set_position(("data" , 0))
            ax.spines["bottom"].set_color(text_color)
            ax.spines["left"].set_position(("data" , 0.5))
            ax.spines["left"].set_color(text_color)
            
            
            
            ax.set_xlim([0.15 , nbr_tranches + 1])
    
    
    
    
            # ticks : 
    
            # yticks : 
    
            min_diff = data_differentiel["intervalle de temps"].min()
            max_diff = data_differentiel["intervalle de temps"].max()
    
    
            ytick_inf = min_diff       # borne inférieure des yticks
            ytick_sup = max_diff       # borne supérieure des yticks (+1 car un range s'arrête une unité avant la valeur spécifiée)
    
    
    
            ax.set_yticks(list(np.arange(int(ytick_inf) , 0 , 1)) + list(np.arange(0 , int(ytick_sup) + 1 , 1)))
            ax.tick_params(axis = 'y', colors = text_color)   # couleur des graduations
            ax.set_yticklabels([abs(tick) for tick in list(np.arange(int(ytick_inf) , 0 , 1)) + list(np.arange(0 , int(ytick_sup) + 1 , 1))] , 
                                fontsize = 12  , color = text_color)
    
    
    
    
            # xticks :
    
    
            for tick in range(1, nbr_tranches + 1) :
                
                
                if nbr_tranches <= 6 : 
                    
                    rotation = 0
                    
                else : 
                    
                    rotation = 90
                    
                    
                   
    
                ax.text(x = tick , 
                        y = ytick_inf - 1 + (6/10)*data_differentiel_neg["intervalle de temps"].mean()  ,
                        s = f"{int(data_filtre['intervalle de temps'].value_counts().sort_index().index[tick-1].left)}ème - {int(data_filtre['intervalle de temps'].value_counts().sort_index().index[tick-1].right)}ème" ,
                        fontsize = 11 , 
                        rotation = rotation , 
                        color = text_color , 
                        verticalalignment = "center" , 
                        horizontalalignment = "center")
    
    
    
                
            ax.set_xticks(list(range(1, nbr_tranches + 1)))
            ax.tick_params(axis = 'x', colors = text_color)   # couleur des graduations
            ax.set_xticklabels(nbr_tranches*[" "] , color = text_color)
    
    
    
    
    
    
    
    
    
            # titre du graphique : 

            # Si l'on regarde les tirs pris : ['tir' , 'but 7m' , 'but'] :
    
            if len(type_action) == 3 :
    
    
                titre = "Saison USDH : différentiel des tirs par tranche de 5 minutes"
    
    
                ylabel = "différentiel de tirs tentés"
    
    
    
            # Si l'on regarde les buts marqués : ['but 7m' , 'but'] :
    
            elif len(type_action) == 2 : 
    
                titre = "Saison USDH : différentiel des buts par tranche de 5 minutes"
    
    
                ylabel = "différentiel de buts inscrits"
    
    
    
    
            else : 
    
                titre = f"Saison USDH : différentiel des {type_action[0]} par tranche de 5 minutes"
    
    
                ylabel = f"différentiel de {type_action[0]}"
    
    
    
    
    
    
            if show_title == True : 
    
                ax.set_title(titre , fontsize = 30 , family = "serif" , color = text_color ,
                             pad = 75)
    
    
    
    
    
            ax.set_ylabel(ylabel , fontsize = 15 , family = "serif" , color = text_color)
            ax.set_xlabel(" ")
    
    
    
    
    
    
    
            # 4) Annotation des effectifs en face de chaque barre :
    
    
    
            # Pour chaque intervalle de temps (12 au total) :
    
            for i , intervalle in zip(list(range(1, nbr_tranches + 1)) , data_differentiel.index) :
    
    
                
                # CAS 1 : si le nombre de tranches souhaité vaut 3 ou 5 --> la ligne de la mi-temps coupe la tranche du milieu et passe en plein sur le texte de l'effectif de cette tranche ==> décalage du texte sur un côté !
                
                if nbr_tranches in [3,5] : 
                    
                    if i == nbr_tranches//2 + 1 :  # S'il s'agit de la tranche du milieu :
                        
                        x = i + 0.075   # on décale le texte vers la droite
                        
                        
                    else : # SINON, s'il s'agit d'une autre tranche quelconque :
                        
                        x = i  # pas de soucis, on écrit le texte au milieu
                
                
                
                # CAS 2 : 
                
                else : 
                    
                    x = i
                
                
                
                
                
                if unite in ["total" , "moyenne / match"] :
                    
                    
                    # CAS 1 : si je souhaite le différentiel TOTAL par tranche, depuis le début de la saison :
                        
                    if unite == "total" : 
                        
    
                        differentiel_buts = data_differentiel["intervalle de temps"].loc[intervalle]    # data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index().loc[intervalle] - data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().sort_index().loc[intervalle]
    
                        
    
                        # Gestion de la police + de la couleur de l'affichage du différentiel de buts :
    
                        if differentiel_buts >= 0 :
                            
                            y = differentiel_buts + (2.75/10)*data_differentiel_pos["intervalle de temps"].mean()
                        
                        
                            if differentiel_buts > 0 :
        
                                couleur = "#71E014"
                                txt = "+ " + str(np.round(differentiel_buts , 2))
                                
                                
                            else :   # differentiel_buts == 0 : 
            
                                couleur = "orange"
                                txt = "0"
                            
                            
                            
                            
    
                        else :    # differentiel_buts < 0
                        
                        
                            y = differentiel_buts + (1.5/10)*data_differentiel_neg["intervalle de temps"].mean()
        
                            couleur = "#FF0000"
                            txt = "- " + str(abs(np.round(differentiel_buts , 2)))
    
    
    
    
    
    
    
                    # CAS 2 : si je souhaite le différentiel MOYEN / MATCH par tranche, depuis le début de la saison :
                        
                    else :    # unite == "moyenne / match" : 
                        
    
                        differentiel_buts = (data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts().sort_index().loc[intervalle])/len(dico_rencontres_USDH) - (data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts().sort_index().loc[intervalle])/len(dico_rencontres_USDH)
    
    
                        # Gestion de la police + de la couleur de l'affichage du différentiel de buts :
    
                        if differentiel_buts >= 0 :
                            

                        
                            if differentiel_buts > 0 :
        
                                couleur = "#71E014"
                                txt = "+ " + str(np.round(differentiel_buts , 2))
                                
                                
                            else :   # differentiel_buts == 0 : 
            
                                couleur = "orange"
                                txt = "0"
                            
                            
                            
                            
    
                        else :    # differentiel_buts < 0
                        
                        
                            couleur = "#FF0000"
                            txt = "- " + str(abs(np.round(differentiel_buts , 2)))
    
                    
    
                    
                        
                        
                        
                    
                    
                    
                    
                    
                    # Gestion de la taille + de l'orientation de l'affichage du différentiel de buts :
    
                    
                    # SI le nombre de tranches est élevé ET que l'on regarde les moyennes / match ==> texte long à afficher ==> réduire la taille de police :
                                
                    if nbr_tranches in [30 , 60] :
                        
                        if nbr_tranches == 60 :
                            
                            fontsize = 8.5
                            
                            
                            if differentiel_buts >= 0 :
                                
                                y = differentiel_buts + 3*(data_differentiel_pos["intervalle de temps"]/len(dico_rencontres_USDH)).mean()
                        
                        
                        
                        
                            else : 
                                
                                y = differentiel_buts + 2*(data_differentiel_neg["intervalle de temps"]/len(dico_rencontres_USDH)).mean()
                        
                                
                                
                            
                            
                            
                            
                            if unite == "total" :
                        
                                rotation = 0
                                
                                
                                
                            else : 
                                
                                rotation = 75
                                
                                
                                
                        else :   # nbr_tranches == 30
                        
                        
                            if differentiel_buts >= 0 :
                                
                                y = differentiel_buts + 2*(data_differentiel_pos["intervalle de temps"]/len(dico_rencontres_USDH)).mean()
                        
                        
                        
                        
                            else : 
                                
                                y = differentiel_buts + 2*(data_differentiel_neg["intervalle de temps"]/len(dico_rencontres_USDH)).mean()
                        
                        
                        
                            fontsize = 9.5
                            rotation = 0
                        
                        
                        
         
                        
                        
    
                    # SINON, si le nombre de tranches est moyennement / peu élevé : 
                        
                    else :
                        
                        rotation = 0
                        
                        
                        if unite == "moyenne / match" :
                            
                            fontsize = 13
                            
                            
                            if differentiel_buts >= 0 :
                                
                                y = differentiel_buts + 2*(data_differentiel_pos["intervalle de temps"]/len(dico_rencontres_USDH)).mean()
        
                            
                            else :
                                
                                y = differentiel_buts + 2*(data_differentiel_neg["intervalle de temps"]/len(dico_rencontres_USDH)).mean()
        
            
                            
                        else : 
                            
                            fontsize = 16
                            
                            
                       
                        
    
    
                    ax.text(x = x , 
                            y = y , 
                            s = txt , 
                            horizontalalignment = "center" , 
                            verticalalignment = "center" , 
                            color = couleur , 
                            fontsize = fontsize , 
                            rotation = rotation)
    
    
    
    
    
    
    
    
            # 5) Ligne symbolisant la mi-temps :
    
    
            ord_mi_temps_1 = ytick_inf - 0.5
            ord_mi_temps_2 = (ytick_sup-1) + (ytick_sup-1)/5 + (8/10)*abs(data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts() - data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts()).mean() + 0.55
    
            abs_mi_temps = (nbr_tranches + 1)/2
    
    
            ax.plot(2*[abs_mi_temps] , [ord_mi_temps_1 , ord_mi_temps_2] , 
                    color = "#00D1FF" , 
                    ls = "--" , 
                    lw = 2)
    
    
            ax.text(x = abs_mi_temps , 
                    y = (51/50)*ord_mi_temps_2 , 
                    color = "#00D1FF" , 
                    fontsize = 12 , 
                    s = "mi-temps" , 
                    verticalalignment = "center" , 
                    horizontalalignment = "center")
    
    
    
    
    
    
    
    
    
            # 6) Inscription du différentiel des 2 équipes lors de chaque période : 
    
    
            if type_action in [["but" , "but 7m"] , ["2min"] , ["avertissement"] , ["arrêt" , "arrêt 7m"] , ["tir" , "tir 7m" , "but" , "but 7m"]] :
    
    
                if type_action == ["but" , "but 7m"] :
    
                    action = "buts marqués"
    
    
                elif type_action == ["2min"] : 
    
                    action = "exclusions"
    
    
                elif type_action == ["avertissement"] : 
    
                    action = "cartons jaunes"
    
    
                elif type_action == ["arrêt" , "arrêt 7m"] : 
    
                    action = "arrêts"
    
    
                elif type_action == ["tir" , "tir 7m" , "but" , "but 7m"] : 
    
                    action = "tirs tentés"
    
    
    
    
    
    
                differentiel_M1_USDH = S_nbr_type_action_saison(data = data , type_action = action , equipe = "USDH" , periode = "M1").sum() - S_nbr_type_action_saison(data = data , type_action = action , equipe = "adversaire" , periode = "M1").sum()
                differentiel_M2_USDH = S_nbr_type_action_saison(data = data , type_action = action , equipe = "USDH" , periode = "M2").sum() - S_nbr_type_action_saison(data = data , type_action = action , equipe = "adversaire" , periode = "M2").sum()
    
    
    
                # différentiel M1 : 
    
                if differentiel_M1_USDH > 0 :
    
                    color = "lime"
    
                else : 
    
                    color = "red"
    
    
     
               
                    
                
                ax.text(y = (ytick_sup-1) + (ytick_sup-1)/5 + (8/10)*abs(data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts() - data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts()).mean() + 0.55, 
                        x = (1 + nbr_tranches/2)/3 ,  # (nbr_tranches + 0.5)/4 + nbr_tranches/30 , 
                        s = "M1 :" , 
                        color = text_color , 
                        fontsize = 30 , 
                        verticalalignment = "center")
                    
                    
                    
                ax.text(y = (ytick_sup-1) + (ytick_sup-1)/5 + (8/10)*abs(data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts() - data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts()).mean() + 0.55 , 
                        x = (1 + nbr_tranches/2)/2  ,  # (nbr_tranches + 0.5)/4 + nbr_tranches/30 , 
                        s = differentiel_M1_USDH , 
                        color = color , 
                        fontsize = 30 , 
                        verticalalignment = "center")
    
    
    
    
    
    
    
                # différentiel M2 : 
    
                if differentiel_M2_USDH > 0 :
    
                    color = "lime"
    
                else : 
    
                    color = "red"
    
                
                
                
                ax.text(y = (ytick_sup-1) + (ytick_sup-1)/5 + (8/10)*abs(data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts() - data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts()).mean() + 0.55 , 
                        x = 2*(1 + nbr_tranches)/3 ,  # (nbr_tranches + 0.5)/4 + nbr_tranches/30 , 
                        s = "M2 : " , 
                        color = text_color , 
                        fontsize = 30 , 
                        verticalalignment = "center")
                
    
    
                ax.text(y = (ytick_sup-1) + (ytick_sup-1)/5 + (8/10)*abs(data_filtre[data_filtre["équipe"] == "USDH"]["intervalle de temps"].value_counts() - data_filtre[data_filtre["équipe"] != "USDH"]["intervalle de temps"].value_counts()).mean() + 0.55 , 
                        x = 2*(1 + nbr_tranches)/2.65 ,  # (nbr_tranches + 0.5)/4 + nbr_tranches/30 , 
                        s = differentiel_M2_USDH , 
                        color = color , 
                        fontsize = 30 , 
                        verticalalignment = "center")
    
    
    
    
    
    
    
            return ax







        else : 
            
            
            raise ValueError("nombre de tranches attendu : 3, 4, 5, 6, 10, 12, 15, 20, 30 ou 60.")
        
        
        
        
        
################################ FIN DES FONCTIONS UTILES A L'ANALYSE ET A L'APPLICATION !! #########################        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################






###        IMPORTATION DE LA BASE DE DONNEES DES ACTIONS DE L'EQUIPE SM1 DE L'USDH 2022-2023 (fichier excel) : 

chemin_acces = "https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2FJulienLickel%2Fstreamlit-USDH-%2Frefs%2Fheads%2Fmain%2Ffaits_de_jeu.xlsx"

df = importation_et_nettoyage(link = chemin_acces) 






#####################################################################################################################
#####################################################################################################################
#####################################################################################################################

###                                          CREATION DE L'APPLICATION STREAMLIT.



#####################################################################################################################
#####################################################################################################################



##                                   Création d'un MENU LATERAL sur la gauche de l'écran :
    
    
    
st.sidebar.markdown("<h1 style='text-align: center; color: white;'>Menu :</h1>",
                    unsafe_allow_html = True)  
 
    
st.sidebar.write(" ")
st.sidebar.write(" ")









# Création d'un bouton DANS LE MENU LATERAL, pour renseigner le type d'analyse que l'on souhaite faire :
        
# Bouton pour le choix de l'activité :
    
    
bouton_activite = st.sidebar.selectbox("Que souhaitez-vous regarder ?" , 
                                      [" " , 
                                       "analyse de match" , 
                                       "BILAN saison USDH"])






        
        
for i in range(5) : 
    
    st.sidebar.write("")
    
    
    
    
# SI l'utilisateur N'a PAS renseigné ce qu'il souhaite faire :
    
if bouton_activite == " " :
    
    
    
    # Titre de l'application : 
                                     
    st.markdown(f"<h1 style='text-align: center; color: white;'>Application d'analyse de données pour l'Union Saumur Doué Handball.</h1>",
                unsafe_allow_html = True)
    
    
    
    for i in range(5) : 
        
        st.write("")
        
        
        
    st.header("- 1) Description de l'outil.")
    
    
    for i in range(3) : 
        
        st.write("")
        
        
        
     
    st.write("""--> Entièrement réalisée à partir des feuilles de match au format PDF disponibles sur le site de la FFHB, cette application web ne concernant à ce jour que l'équipe 
                    Sénior Masculine 1 du club de handball de l'USDH a pour vocation d'extraire de ces feuilles de matchs des statistiques et graphiques intéressants afin d'aider à 
                    une meilleure analyse et à la compréhension des matchs joués par cette équipe lors de la saison 2022-2023.""")  
    
    
    for i in range(2) : 
        
        st.write("")
        
        
            
                
    st.write("""--> A chaque nouvelle journée de championnat, la feuille de match devant être saisie manuellement pour mettre à jour la base de données utilisée pour cette application, 
                    il est possible que les données du dernier match ne soient pas immédiatement accessibles (quelques jours d'attente sont à prévoir). """)
    
    
    
    for i in range(5) : 
        
        st.write("")
        
     
    st.header("- 2) Temps de chargement.")
    
    
    
    for i in range(3) : 
        
        st.write("")
        
        
        
    st.write("""--> Certains graphiques et/ou statistiques nécessitent de réaliser des calculs longs et complexes, qui utilisent des ressources importantes en termes de mémoire de l'ordinateur : 
                    il faudra donc parfois attendre quelques dizaines de secondes avant de voir enfin s'afficher le résultat : tant que le bouton 'running' apparaît en haut à droite de votre écran, 
                    cela signifie que le calcul est en cours et que vous n'avez qu'à patienter.  
                    De la même manière, avec ce genre d'application, le fait de choisir une option via un bouton entraîne le rechargement de tout ce qui avait déjà été chargé pécédemment, d'ou 
                    un temps d'attente logique de quelques dizaines de secondes par moments dont je m'excuse par avance.""")
    
    
    
    
    for i in range(3) : 
        
        st.write("")
        
        
        
        
        
    st.header("- 3) Absence de chargement.")
    
    
    
    for i in range(3) : 
        
        st.write("")
        
        
        
    st.write("""--> Si la page ne charge plus malgré la fait que vous avez sélectionnez une option via un bouton, vous pouvez cliquer sur le bouton aux 3 bandes horizontales (en haut à droite de votre écran) 
                    et cliquer ensuite sur 'Rerun' afin de faire charger manuellement l'application.  
                    Vous pouvez également régler, si vous le souhaitez, quelques paramètres visuels grâce à ce même bouton aux 3 bandes (option 'Settings').""")
    
    
    
    
    for i in range(5) : 
        
        st.write("")
        
        
        
        
    st.header("- 4) Mise en veille de l'application.")
    
    
    
    for i in range(3) : 
        
        st.write("")
                     
                     
                     
    st.write("""--> Au bout d'un certain sans l'utiliser, l'application se met en veille : dans ce cas, il vous sera sûrement demandé de cliquer sur un bouton afin de 
                    'réveiller' l'application. Dans le cas contraire, me tenir informé afin de remédier au problème.""")
    
    
    
    for i in range(5) : 
        
        st.write("")
        
        
        
        
    st.header("- 5) Extension de l'application à un usage plus large.")
    
    
    
    for i in range(3) : 
        
        st.write("")
                     
     
                    
    st.write("""--> N'ayant eu que quelques semaines pour développer cette application, elle n'est aujourd'hui utile que pour l'équipe SM1 du club, mais son usage pourrait potentiellement 
                    être étendu aux autres équipes séniors du club (SF1, SF2, SM2, SM3). 
                    Cependant, pas mal de modifications devant être effectuer pour étendre cet outil aux autres équipes (adaptation du code informatique, saisie des feuilles de match) et mon emploi 
                    du temps étant amené à évoluer, une telle manoeuvre prendrait plus ou moins de temps.
                    N'hésitez pas à me signaler si une autre équipe du club souhaite disposer des mêmes analyses de match que les SM1 à l'heure actuelle.""")
    
    
    
    
    
    for i in range(7) : 
        
        st.write("")
        
        
        
        
    st.write("Bonne navigation !")
    
    
    
    
    for i in range(5) : 
        
        st.write("")
        
        
        
        
        
     # Ajout d'un lien clickable vers mes pages web : 
            
    st.write("Julien Lickel, Data Analyst et joueur de l'USDH.")

    lien_linkedin = "https://www.linkedin.com/in/julien-lickel-b45001211/"
    lien_instagram = "https://www.instagram.com/l_analyste_data/"


    st.write("[LinkedIn](%s)" % lien_linkedin)
    st.write("[Instagram](%s)" % lien_instagram)
    
    

        
        
        
       
    
    
    
    

    
    
# SI l'utilisateur a renseigné ce qu'il souhaite faire :
    
else :    # bouton_activite != " " :
        
        
    


#####################################################################################################################
#####################################################################################################################


### 2ème PAGE DE L'APPLICATION (analyse de match) :
    
    
     
        
    # CAS 1 : si l'utilisateur souhaite réaliser une analyse d'1 match particulier de cette saison 2022-23 : 
        
    if bouton_activite == "analyse de match" : 
        
        
        
        
        

        
        
        # Création d'un bouton DANS LE MENU LATERAL permettant de choisir la journée de championnat qui l'intéresse :
            
        bouton_journee = st.sidebar.selectbox("Choisissez le match de l'USDH à analyser :" , 
                                             [" "] + list(dico_rencontres_USDH.keys()))
        
        
        
        

        
        
        # SI l'utilisateur a renseigné une journée de championnat :
                
        if bouton_journee != " " : 
        
        
        
        
            # CAS A : le match de la journée saisie N'A PAS ENCORE ETE JOUE : 
                
            if bouton_journee not in dico_rencontres_USDH.keys() : 
                
                st.write(f"Le match de la {bouton_journee.split(sep = 'J')[1]}ème journée n'a pas encore été joué : veuillez sélectionner une journée antérieure.")
            
            
            
            
            
            
            
            
            # CAS B : le match de la journée saisie A BEL ET BIEN ETE JOUE :
                
            else :    
            
            
                # Titre de la page : 
                    
                    
                st.markdown(f"<h1 style='text-align: center; color: white;'>Journée {bouton_journee[-1]} :</h1>",
                            unsafe_allow_html = True)  
                
                
                
                
                
                
                for i in range(3) : 
                    
                    st.write("")









                # Filtrage de la base de données de l'USDH, en fonction de la journée sélectionnée : 
                        
                df_journee = df[df["journée"] == bouton_journee]    
                
                
                
                
                
                
                
                # Récupération du nom des 2 équipes opposées lors de cette journée : 
                    
        
                equipe_domicile = dico_rencontres_USDH[bouton_journee][0]   # nom de l'équipe jouant à domicile
                equipe_exterieur = dico_rencontres_USDH[bouton_journee][1]  # nom de l'équipe jouant à l'extérieur
                    
                    
                    
                
                    
                # Affichage des NOMS DES 2 EQUIPES OPPOSEES + DE LEUR LOGO (en face du nom) : 
                            
                # col1 , col2 , col3 , col4 , col5 = st.columns([2 , 2 , 2 , 2 , 2]) 
                
                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1]) 
                    
                
                col3.header(f"**{equipe_domicile.upper()}**")
                
                logo_equipe_1 = Image.open(dico_logos[equipe_domicile]) 
                col2.image(logo_equipe_1 , width = 115)
            
                
                col6.header(f"**{equipe_exterieur.upper()}**")
                
                logo_equipe_2 = Image.open(dico_logos[equipe_exterieur]) 
                col7.image(logo_equipe_2 , width = 115)
                
                    
                    
                st.write("")  
                st.write("")
                st.write("-------------------------------------------------------------------------------------")
                
                
                
                
                
                
                
                
                
                
                
                # PARTIE 1 : métriques / graphiques liés aux BUTS :
                    
                    
                st.markdown("<h1 style='text-align: center; color: white;'>Statistiques liées au score.</h1>",
                            unsafe_allow_html = True)  
                
                
                st.write("-------------------------------------------------------------------------------------")
                
                
                
                
                
                
                
                
                # Métrique n°1-2-3 : Affichage du SCORE FINAL / en M1 / en M2 DE CHAQUE EQUIPE : 
                        
                for type_score in ["final" , "M1" , "M2"] :
                    
                    
                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1]) 
                        
                    col4.write(f"score {type_score} :") 
                    
                    
                    # Récupération du score final de l'équipe à domicile et de l'équipe à l'extérieur :
                        
                    score_final_domicile = score(data = df , journee = bouton_journee , periode = type_score , equipe = "domicile")
                    score_final_exterieur = score(data = df , journee = bouton_journee , periode = type_score , equipe = "extérieur")
    
    

    
                    # Calcul de la différence de buts EN FAVEUR DE L'USDH : 
                        
                    # CAS 1 : l'USDH joue à domicile : 
                        
                    if equipe_domicile == "USDH" :
                    
                        difference_finale = score_final_domicile - score_final_exterieur   # différence de buts finale (en faveur de l'USDH)
                    
                    
                    
                    
                        # Ré-écriture de la différence de buts finale :
                         
                        if difference_finale > 0 : 
                                
                                difference_finale = "+ " + str(difference_finale) + " buts"
                            
                            
                            
                        elif difference_finale < 0 : 
                            
                            difference_finale = "- " + str(abs(difference_finale)) + " buts"
                            
                            
                            
                    
                    
                    
                        # On écrit le delta de buts en-dessous de l'équipe à domicile, car il s'agit de l'USDH :
                            
                        col3.metric(label = "" , 
                                    value = score_final_domicile , 
                                    delta = str(difference_finale))
                    
                    
                        col6.metric(label = "" , 
                                    value = score_final_exterieur , 
                                    delta = " ")
                    
                    
                    
                    
                    
                    
                    # CAS 2 : l'USDH joue à l'extérieur :
                        
                    else : 
                        
                        difference_finale = score_final_exterieur - score_final_domicile   # différence de buts finale (en faveur de l'USDH)
                    
                        
                        
                        # Ré-écriture de la différence de buts finale :
                         
                        if difference_finale > 0 : 
                                
                                difference_finale = "+ " + str(difference_finale) + " buts"
                            
                            
                            
                        elif difference_finale < 0 : 
                            
                            difference_finale = "- " + str(abs(difference_finale)) + " buts"
                            
                            
                            
                    
                    
                    
                        # On écrit le delta de buts en-dessous de l'équipe à l'extérieur, car il s'agit de l'USDH :
                            
                        col3.metric(label = "" , 
                                    value = score_final_domicile , 
                                    delta = " ")
                    
                    
                        col6.metric(label = "" , 
                                    value = score_final_exterieur , 
                                    delta = str(difference_finale))
                    
                    
                    
                    st.write("")
                    st.write("")
                    
                    
                    
                    
                    
                    
                    
                 
                    
                 
                    
                    
                    
                    
                # Métrique n°4 : Affichage du temps passé en tête PAR CHAQUE EQUIPE : 
                    
                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1.25,1.15,2.3,1]) 
                        
                col4.write("Temps passé en tête (en minutes) :") 
                
                
                # Récupération du temps passé en tête par l'équipe à domicile et par l'équipe à l'extérieur :
                        
                tps_en_tete_domicile = temps_en_tete(data = df , journee = bouton_journee , duree_en = "minutes" , equipe = "domicile")
                tps_en_tete_exterieur = temps_en_tete(data = df , journee = bouton_journee , duree_en = "minutes" , equipe = "extérieur")
 



                # Calcul de la différence de temps en tête EN FAVEUR DE L'USDH : 
                    
                # CAS 1 : l'USDH joue à domicile : 
                    
                if equipe_domicile == "USDH" :
                
                    difference_tps_en_tete = np.round(tps_en_tete_domicile - tps_en_tete_exterieur , 2)   # différence de temps passé en tête (en faveur de l'USDH)
                
                
                
                
                    # Ré-écriture de la différence de temps en tête :
                     
                    if difference_tps_en_tete > 0 : 
                            
                        difference_tps_en_tete = "+ " + str(np.round(difference_tps_en_tete , 2)) + " minutes"
                        
                        
                        
                    elif difference_tps_en_tete < 0 : 
                        
                        difference_tps_en_tete = "- " + str(abs(difference_tps_en_tete)) + " minutes"
                        
                        
                        
                
                
                
                    # On écrit le delta de temps passé en tête par l'équipe à domicile, car il s'agit de l'USDH :
                        
                    col3.metric(label = "" , 
                                value = np.round(tps_en_tete_domicile , 2) ,
                                delta = difference_tps_en_tete)
                
                
                    col6.metric(label = "" , 
                                value = np.round(tps_en_tete_exterieur , 2) , 
                                delta = " ")
                
                
                
                
                
                
                # CAS 2 : l'USDH joue à l'extérieur :
                    
                else : 
                    
                    difference_tps_en_tete = np.round(tps_en_tete_exterieur - tps_en_tete_domicile , 2)  # différence de temps passé en tête (en faveur de l'USDH)
                
                    
                    
                    # Ré-écriture de la différence de temps en tête :
                     
                    if difference_tps_en_tete > 0 : 
                            
                            difference_tps_en_tete = "+ " + str(difference_tps_en_tete) + " minutes"
                        
                        
                        
                    elif difference_tps_en_tete < 0 : 
                        
                        difference_tps_en_tete = "- " + str(abs(difference_tps_en_tete)) + " minutes"
                        
                        
                        
                
                
                
                    # On écrit le delta de temps passé en tête par l'équipe à l'extérieur, car il s'agit de l'USDH :
                        
                    col3.metric(label = "" , 
                                value = np.round(tps_en_tete_domicile , 2) , 
                                delta = " ")
                
                
                    col6.metric(label = "" , 
                                value = np.round(tps_en_tete_exterieur , 2) , 
                                delta = difference_tps_en_tete)
                
                
                
                st.write("")
                st.write("")
                
                
                
                
                
                
                
                
                
                
                
                # Métrique n°5 : Affichage de la plus grosse série de buts encaissés successivement sans scorer PAR LES 2 EQUIPES : 
                        
                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1.25,1.15,2.3,1]) 
                        
                col4.write("Plus grand nombre de buts encaissés successivement sans marquer :") 
                
                
                
                
                # Récupération de cette plus grosse série pour l'équipe à domicile et l'équipe à l'extérieur :
                        
                plus_grand_nbr_buts_encaisses_succ_domicile = plus_grosse_serie_buts_encaisses(data = df , journee = bouton_journee , equipe = "domicile")[0][1]
                plus_grand_nbr_buts_encaisses_succ_exterieur = plus_grosse_serie_buts_encaisses(data = df , journee = bouton_journee , equipe = "extérieur")[0][1]
                



                # Récupération des dates de début et de fin de la série de chacune des 2 équipes : 
                    
                date_debut_plus_grande_serie_domicile = plus_grosse_serie_buts_encaisses(data = df , journee = bouton_journee , equipe = 'domicile')[1][0]
                date_fin_plus_grande_serie_domicile = plus_grosse_serie_buts_encaisses(data = df , journee = bouton_journee , equipe = 'domicile')[1][1]
                duree_plus_grande_serie_domicile = date_fin_plus_grande_serie_domicile - date_debut_plus_grande_serie_domicile
                
                
                date_debut_plus_grande_serie_exterieur = plus_grosse_serie_buts_encaisses(data = df , journee = bouton_journee , equipe = 'extérieur')[1][0]
                date_fin_plus_grande_serie_exterieur = plus_grosse_serie_buts_encaisses(data = df , journee = bouton_journee , equipe = 'extérieur')[1][1]
                duree_plus_grande_serie_exterieur = date_fin_plus_grande_serie_exterieur - date_debut_plus_grande_serie_exterieur
                




                # Calcul de la différence de buts encaissés successivement sans scorer EN FAVEUR DE L'USDH : 
                    
                # CAS 1 : l'USDH joue à domicile : 
                    
                if equipe_domicile == "USDH" :
                
                    difference_plus_grand_nbr_buts_encaisses_succ = plus_grand_nbr_buts_encaisses_succ_domicile - plus_grand_nbr_buts_encaisses_succ_exterieur
                    
                
                
                    # Ré-écriture de la différence de temps en tête :
                     
                    if difference_plus_grand_nbr_buts_encaisses_succ > 0 : 
                            
                        difference_plus_grand_nbr_buts_encaisses_succ = "+ " + str(difference_plus_grand_nbr_buts_encaisses_succ) + " buts"
                        
                        
                        
                    elif difference_plus_grand_nbr_buts_encaisses_succ < 0 : 
                        
                        difference_plus_grand_nbr_buts_encaisses_succ = "- " + str(abs(difference_plus_grand_nbr_buts_encaisses_succ)) + " buts"
                        
                        
                        
                
                
                
                    # On écrit le delta de temps passé en tête par l'équipe à domicile, car il s'agit de l'USDH :
                        
                    col3.metric(label = f"de la {np.round(date_debut_plus_grande_serie_domicile , 2)}ème à la {np.round(date_fin_plus_grande_serie_domicile , 2)}ème ({np.round(duree_plus_grande_serie_domicile , 2)} min) :" , 
                                value = plus_grand_nbr_buts_encaisses_succ_domicile ,
                                delta = difference_plus_grand_nbr_buts_encaisses_succ , 
                                delta_color = "inverse")
                
                
                    col6.metric(label = f"de la {np.round(date_debut_plus_grande_serie_exterieur , 2)}ème à la {np.round(date_fin_plus_grande_serie_exterieur , 2)}ème ({np.round(duree_plus_grande_serie_exterieur , 2)} min) :" , 
                                value = plus_grand_nbr_buts_encaisses_succ_exterieur , 
                                delta = " ")
                
                
                
                
                
                
                # CAS 2 : l'USDH joue à l'extérieur :
                    
                else : 
                    
                    difference_plus_grand_nbr_buts_encaisses_succ = plus_grand_nbr_buts_encaisses_succ_exterieur - plus_grand_nbr_buts_encaisses_succ_domicile
                    
                    
                    
                    # Ré-écriture de la différence de temps en tête :
                     
                    if difference_plus_grand_nbr_buts_encaisses_succ > 0 : 
                            
                        difference_plus_grand_nbr_buts_encaisses_succ = "+ " + str(difference_plus_grand_nbr_buts_encaisses_succ) + " buts"
                        
                        
                        
                    elif difference_plus_grand_nbr_buts_encaisses_succ < 0 : 
                        
                        difference_plus_grand_nbr_buts_encaisses_succ = "- " + str(abs(difference_plus_grand_nbr_buts_encaisses_succ)) + " buts"
                        
                        
                        
                
                
                
                    # On écrit le delta de temps passé en tête par l'équipe à l'extérieur, car il s'agit de l'USDH :
                        
                    col3.metric(label = f"de la {np.round(date_debut_plus_grande_serie_domicile , 2)}ème à la {np.round(date_fin_plus_grande_serie_domicile , 2)}ème ({np.round(duree_plus_grande_serie_domicile , 2)} min) :" , 
                                value = plus_grand_nbr_buts_encaisses_succ_domicile , 
                                delta = " ")
                
                
                    col6.metric(label = f"de la {np.round(date_debut_plus_grande_serie_exterieur , 2)}ème à la {np.round(date_fin_plus_grande_serie_exterieur , 2)}ème ({np.round(duree_plus_grande_serie_exterieur , 2)} min) :" , 
                                value = plus_grand_nbr_buts_encaisses_succ_exterieur , 
                                delta = difference_plus_grand_nbr_buts_encaisses_succ  , 
                                delta_color = "inverse")
                
                
                
                
                for i in range(5) : 
                    
                    st.write("")
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                
                
                
                
                
                # Affichage du camembert / diagramme en barres des buts marqués par joueur de chaque équipe :
                    
                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1.75,1.15,2.3,1])
                
                
                st.write("")
                st.write("")
                
                bouton_graphique_buts = col4.selectbox("Répartition des buts marqués par joueur et par équipe :" , 
                                                       [" " , "camembert" , "bâtons"])
                
                
                


                
                if bouton_graphique_buts != " " :
                    
                    
                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2.5,1.15,2.3,1])
                    
                
                
                    if bouton_graphique_buts == "camembert" :
                    
                    
                        camembert_domicile = camembert_plotly(data = df , journee = bouton_journee , show_title = False , type_action = ["but" , "but 7m"] , equipe = "domicile" , showlegend = False)
                        camembert_exterieur = camembert_plotly(data = df , journee = bouton_journee , show_title = False , type_action = ["but" , "but 7m"] , equipe = "extérieur" , showlegend = False)
                        
                       
                        col1.write(camembert_domicile)
                        
                        col5.write(camembert_exterieur)
                    
                    
                    
                    
                    else : 
                        
                        
                        batons_domicile = diagramme_en_barres_plotly(data = df , journee = bouton_journee , type_action = ["but" , "but 7m"] , equipe = "domicile")
                        batons_exterieur = diagramme_en_barres_plotly(data = df , journee = bouton_journee , type_action = ["but" , "but 7m"] , equipe = "extérieur")
                        
                       
                        col1.write(batons_domicile)
                        
                        col5.write(batons_exterieur)
                        
                        
                        
                        
                        
                        
                        
                    for i in range(5) : 
                        
                        st.write("")
        
        
        
        
        
        
                    
        
        
        
        
        
                    # Affichage de GRAPHIQUES LIES AU SCORE :
                        
                        
                        
                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2.5,1.15,2.3,1])
                    
                        
                        
                    # Création d'un bouton multi-choix permettant d'afficher un graphique lié au score : 
                        
                    bouton_graphe_score = col4.selectbox("Choisissez un graphique à afficher :" , 
                                                         [" " , 
                                                          "évolution du score" , 
                                                          "évolution de l'écart au score" , 
                                                          "répartition des buts par période" , 
                                                          "différentiel de buts par période"])
                    
                    
                    
                    
                    for i in range(3) : 
                        
                        st.write("")
                    
                    
                    
                    
                    # SI un choix de graphique a été effectué :
                        
                    if bouton_graphe_score != " " :
                    
                        

                        
                        
                        # CAS 1 : SI l'on souhaite afficher le graphique de l'évolution du score des 2 équipes :
                            
                        if bouton_graphe_score == "évolution du score" :
                            
                            
                            # Création d'une figure vierge : 
                            
                            fig , ax = plt.subplots(figsize = (16,6.5))
                            
                            
                            
                            
                            evolution_score(fig = fig , ax = ax , data = df , 
                                            journee = bouton_journee , 
                                            show_title = True , afficher_points = False , 
                                            par_but_ou_par_minute = "par minute" , 
                                            colorer_gap = False , 
                                            text_color = "white");
                            
                            
                            st.write(fig)
 
                                
                            
                                                                                                                                 
                            
                            
   
                        
                        
                        
                        
                        # CAS 2 : SI l'on souhaite afficher le graphique de l'évolution du GAP au score :
                            
                        elif bouton_graphe_score == "évolution de l'écart au score" :
                            
                            # Création d'une figure vierge : 
                            
                            fig , ax = plt.subplots(figsize = (16,6.5))
                            
                            
                            evolution_gap_score(fig = fig , ax = ax , data = df , journee = bouton_journee , 
                                                show_title = True , afficher_points = False , 
                                                par_but_ou_par_minute = "par minute");
                            
                            
                            st.write(fig)
                            
                            
                            
                            
                            
                        # CAS 3 : SI l'on souhaite afficher l'histogramme des buts :
                            
                        elif bouton_graphe_score == "répartition des buts par période" :
                            
                            

                        
                            # Ajout d'un bouton pour le choix du nombre tranches des 60 minutes à découper :
                            
                            bouton_tranches = col6.selectbox("Découper les 60 minutes de match par périodes de ..... minutes :" , 
                                                             [" " , 1 , 2 , 4 , 5 , 6 , 10 , 12 , 15 , 20])
                            
                            
                            
                            for i in range(3) : 
                                
                                st.write("")
                                
                                
                                
                            
                            if bouton_tranches != " " :
                                
                                
                                # Création d'une figure vierge : 
                            
                                fig , ax = plt.subplots(figsize = (16,6.5))
                                
                                
                                double_vertical_histogram(fig = fig , ax = ax , data = df , 
                                                          journee = bouton_journee , 
                                                          type_action = ["but" , "but 7m"] , 
                                                          show_title = False , 
                                                          text_color = "white" , 
                                                          nbr_tranches = 60//bouton_tranches);
                                
                                
                                st.write(fig)
                            
                            
                            
                            
                            
                            
                        # CAS 4 : SI l'on souhaite afficher l'histogramme des différentiels de buts par tranches de 5 minutes :
                            
                        elif bouton_graphe_score == "différentiel de buts par période" :
                            
                            # Création d'une figure vierge : 
                            
                            fig , ax = plt.subplots(figsize = (16,6.5))
                            
                            
                            histogram_differentiel_buts(fig = fig , ax = ax , data = df , journee = bouton_journee , 
                                                        show_title = False);
                            
                            
                            
                            st.write(fig)
                            
                            
                    
                    
                    
                    
                    
                            
                        
                        
                    
                    
                    
                    
                        for i in range(10) : 
                            
                            st.write("")
                    
                    

                    
                        st.write("-------------------------------------------------------------------------------------")
                    
        
        
        
        
        
        
                    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                        # PARTIE 2 : métriques / graphiques liés à la SITUATION NUMERIQUE :
                        
                        
                        st.markdown("<h1 style='text-align: center; color: white;'>Statistiques liées à la situation numérique.</h1>",
                                    unsafe_allow_html = True)  
                        
                        
                        st.write("-------------------------------------------------------------------------------------")
                        
                    
                    
                    
                        for i in range(3) : 
                            
                            st.write("")
            
            



                        # Affichage de la DROITE GRAPHIQUE représentant les périodes de supériorité / égalité / infériorité numérique de l'USDH lors de CE MATCH : 
                            
                        col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,1,1,2,1,1,1])
                        
                        
                        col4.write("Découpage des 60 minutes de match selon la situation numérique de l'USDH :")
                        
                        
                        
                        for i in range(3) : 
                            
                            st.write("")
                        
                            
                        
                        fig , ax = plt.subplots(figsize = (16,6))



                        droite_sup_inf_numeriques_equipe(fig , ax , data = df , journee = bouton_journee , 
                                                         equipe = "USDH" , 
                                                         afficher_scores = True , 
                                                         afficher_differentiels = True ,
                                                         afficher_bilan = True , 
                                                         show_title = False , 
                                                         text_color = "white")

                        
                        
                        
                        
                        
                    
                        st.write(fig)
                        
                        
                        
                        
                        for i in range(12) : 
                                
                            st.write("")
                            
                            
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        # Métrique n°6-7 : Affichage du nombre d'AVERTISSEMENTS / 2MIN reçus PAR LES 2 EQUIPES : 
                            
                            
                        for punition in ["avertissement" , "2min"] :
                            
                            
                            col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1]) 
                              
                            
                            
                            if punition == "avertissement" :
                                
                                col4.write(f"nombre d'{punition}s reçus :") 
                                
                                
                            else:  
                                
                                col4.write(f"nombre de {punition} reçus :")
                                
                            
                            
                            # Récupération du nbr de punitions de ce type reçues par l'équipe à domicile et de l'équipe à l'extérieur :
                                    
                            nbr_punitions_recues_domicile = nbr_punitions(data = df , journee = bouton_journee , type_punition = punition , equipe = "domicile")
                            nbr_punitions_recues_exterieur = nbr_punitions(data = df , journee = bouton_journee , type_punition = punition , equipe = "extérieur")
            
            
    
            
                            # Calcul de la différence de punitions reçues EN FAVEUR DE L'USDH : 
                                
                            # CAS 1 : l'USDH joue à domicile : 
                                
                            if equipe_domicile == "USDH" :
                            
                                difference_nbr_punitions = nbr_punitions_recues_domicile - nbr_punitions_recues_exterieur
                                
                            
                            
                                # Ré-écriture de la différence de punitions :
                                 
                                if difference_nbr_punitions > 0 : 
                                        
                                    difference_nbr_punitions = "+ " + str(difference_nbr_punitions) + f" {punition}"
                                    
                                    
                                    
                                elif difference_nbr_punitions < 0 : 
                                    
                                    difference_nbr_punitions = "- " + str(abs(difference_nbr_punitions)) + f" {punition}"
                                    
                                    
                                    
                            
                            
                            
                                # On écrit le delta de cartons jaunes sous l'équipe à domicile, car il s'agit de l'USDH :
                                    
                                col3.metric(label = "" , 
                                            value = nbr_punitions_recues_domicile ,
                                            delta = difference_nbr_punitions , 
                                            delta_color = "inverse")
                            
                            
                                col6.metric(label = "" , 
                                            value = nbr_punitions_recues_exterieur , 
                                            delta = " ")
                            
                            
                            
                            
                            
                            
                            # CAS 2 : l'USDH joue à l'extérieur :
                                
                            else : 
                                
                                difference_nbr_punitions = nbr_punitions_recues_exterieur - nbr_punitions_recues_domicile
                                
                                
                                
                                # Ré-écriture de la différence de punitions :
                                 
                                if difference_nbr_punitions > 0 : 
                                        
                                    difference_nbr_punitions = "+ " + str(difference_nbr_punitions) + f" {punition}"
                                    
                                    
                                    
                                elif difference_nbr_punitions < 0 : 
                                    
                                    difference_nbr_punitions = "- " + str(abs(difference_nbr_punitions)) + f" {punition}"
                                    
                                    
                                    
                            
                            
                            
                                # On écrit le delta de punitions sous l'équipe à l'extérieur, car il s'agit de l'USDH :
                                    
                                col3.metric(label = "" , 
                                            value = nbr_punitions_recues_domicile , 
                                            delta = " ")
                            
                            
                                col6.metric(label = "" , 
                                            value = nbr_punitions_recues_exterieur , 
                                            delta = difference_nbr_punitions  , 
                                            delta_color = "inverse")
                            
                            
                            
                            
                            
                            for i in range(5) : 
                                
                                st.write("")
                                
                                
                                
                                
                            
                            
                            
                            
                            
                            
                        # Affichage de l'histogramme des 2min reçus par période :
                            
                        
                        col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1]) 
                        
                        
                        for i in range(3) : 
                            
                            st.write("")
                            
                            
                        
                    
                        col4.write("Répartition des 2min reçus par période :")
                        
                        
                        
                        
                        
                        
                        # Ajout d'un bouton pour le choix du nombre tranches des 60 minutes à découper :
                        
                        
                        bouton_tranches_bis = col6.selectbox("Découper les 60 minutes du match par périodes de ..... minutes :" , 
                                                             [" " , 1 , 2 , 4 , 5 , 6 , 10 , 12 , 15 , 20])
                        
                        
                        
                        for i in range(3) : 
                            
                            st.write("")
                            
                            
                            
                            
                        
                        if bouton_tranches_bis != " " :
                            
                            
                            fig , ax = plt.subplots(figsize = (16,8))
                        
                            
                            
                            double_vertical_histogram(fig = fig , ax = ax , data = df , 
                                                      journee = bouton_journee , 
                                                      type_action = ["2min"] , 
                                                      show_title = False , 
                                                      text_color = "white" , 
                                                      nbr_tranches = 60//bouton_tranches_bis);
                    
                    
                    
                        
                        
                            st.write(fig)
                        
                        
                        
                            for i in range(10) : 
                                
                                st.write("")
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                        
                            # Affichage du CAMEMBERT des EXCLUSIONS reçues par joueur de chaque équipe : 
                                
                            col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1]) 
                            
                            
                            col4.write("Répartition des 2min reçus par joueur :")
                            
                            
    
                            
                            # Récupération du nbr d'exclusions pour 2min reçues par l'équipe à domicile et par l'équipe à l'extérieur lors de match :
                                        
                            nbr_exclusions_recues_domicile = nbr_punitions(data = df , journee = bouton_journee , type_punition = "2min" , equipe = "domicile")
                            nbr_exclusions_recues_exterieur = nbr_punitions(data = df , journee = bouton_journee , type_punition = "2min" , equipe = "extérieur")
            
                            
                            
                            
                            # SI l'équipe jouant à domicile a reçu AU MOINS 1 exclusion durant ce match : 
                                
                            if nbr_exclusions_recues_domicile != 0 :
                                
                                
                                
                                # ALORS, dans ce cas, on dessine le camembert des exclusions de cette équipe :
                                
                                camembert_exclusions_domicile = camembert_plotly(data = df , journee = bouton_journee , 
                                                                                 show_title = False , 
                                                                                 type_action = ["2min"] , 
                                                                                 equipe = "domicile" , 
                                                                                 showlegend = False)
                                
                                
                            
                                col1.write(camembert_exclusions_domicile)
                                
                                
                                
                                
                                
                                
                            
                            # SI l'équipe jouant à l'extérieur a reçu AU MOINS 1 exclusion durant ce match :
                                
                            if nbr_exclusions_recues_exterieur != 0 :
                            
                                
                                # ALORS, dans ce cas, on dessine le camembert des exclusions de cette équipe :
                                
                                camembert_exclusions_exterieur = camembert_plotly(data = df , journee = bouton_journee , 
                                                                                  show_title = False , 
                                                                                  type_action = ["2min"] , 
                                                                                  equipe = "extérieur" , 
                                                                                  showlegend = False)
                                 
                                
                            
                                col5.write(camembert_exclusions_exterieur)
                                
                                
                            
                            
                            
                            for i in range(3) : 
                                
                                st.write("")
                                
                            
                            
                            
                            
                            
                            
                            
                            
                             
                            
                            
                            
                            
      
        
      
                            
                            
                            
                            
                            
                            
                            # Analyse des périodes de SUPERIORITE / INFERIORITE NUMERIQUE de chaque équipe :
                                    
                                
                            for situation_numerique in ["supériorité numérique" , "infériorité numérique"] :
                                
                                
                                
                                st.write("------------------------------------------------------------------------")
                                    
                                    
                                    
                                if situation_numerique == "supériorité numérique" : 
                                    
                                    st.markdown(f"<h1 style='text-align: center; color: white;'>Périodes de {situation_numerique} de l'USDH.</h1>",
                                                     unsafe_allow_html = True)   
                                    
                                    
                                    
                                else :    # situation_numerique == "infériorité numérique" : 
                                    
                                    st.markdown(f"<h1 style='text-align: center; color: white;'>Périodes d'{situation_numerique} de l'USDH.</h1>",
                                                     unsafe_allow_html = True)   
                                    
                                    
                                    
                                
                                
                                
                                for i in range(5) : 
                                    
                                    st.write("")
                                    
                                    
                                    
                                
                                
                                
                                
                                
                                # Métriques n°8 + 13 : Nombre de périodes jouées en 'situation_numerique' par les 2 équipes :
                                

                            
                                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                            
                            
                                col4.write(f"Nombre de fois où l'équipe s'est retrouvée en {situation_numerique} :")
                                
                                
                                
                                
                                    
                                # On récupère le nombre de périodes jouées en 'situation_numerique' par l'USDH et par ses adversaires lors de cette rencontre :
                                
                               
                                # CAS 1 : si l'équipe jouant à domicile est l'USDH = celle jouant à l'extérieur est son adversaire :
                                    
                                if equipe_domicile == "USDH" : 
                                    
                                    if situation_numerique == "supériorité numérique" : 
                                    
                                        nbr_periodes_situation_numerique_USDH_journee = nbr_periodes_superiorite(data = df , journee = bouton_journee , equipe = "domicile")
                                        nbr_periodes_situation_numerique_adv_journee = nbr_periodes_superiorite(data = df , journee = bouton_journee , equipe = "extérieur")
                                            
                                            
                                   
                                    else :   # situation_numerique == "infériorité numérique"
                                    
                                    
                                        nbr_periodes_situation_numerique_USDH_journee = nbr_periodes_superiorite(data = df , journee = bouton_journee , equipe = "extérieur")
                                        nbr_periodes_situation_numerique_adv_journee = nbr_periodes_superiorite(data = df , journee = bouton_journee , equipe = "domicile")
                                
                                
                                
                                
                                
                                
                                # CAS 2 : si l'équipe jouant à l'extérieur st l'USDH = celle jouant à domicile est son adversaire :
                                    
                                else :   # equipe_ext == "USDH" : 
                                    
                                    
                                    if situation_numerique == "supériorité numérique" : 
                                    
                                    
                                        nbr_periodes_situation_numerique_USDH_journee = nbr_periodes_superiorite(data = df , journee = bouton_journee , equipe = "extérieur")
                                        nbr_periodes_situation_numerique_adv_journee = nbr_periodes_superiorite(data = df , journee = bouton_journee , equipe = "domicile")
                                        
                                    
                                    else :   # situation_numerique == "infériorité numérique"
                                    
                                    
                                        nbr_periodes_situation_numerique_USDH_journee = nbr_periodes_superiorite(data = df , journee = bouton_journee , equipe = "domicile")
                                        nbr_periodes_situation_numerique_adv_journee = nbr_periodes_superiorite(data = df , journee = bouton_journee , equipe = "extérieur")
                                    
                                    
                                    
                                        

                                
                                # Calcul du différentiel de périodes jouées en 'situation_numerique' par les 2 équipes : 
                                    
                                differentiel_periodes_situation_numerique = nbr_periodes_situation_numerique_USDH_journee - nbr_periodes_situation_numerique_adv_journee
                                
                                
                                # Gestion de l'affichage du différentiel suivant son signe : 
                                    
                                if differentiel_periodes_situation_numerique > 0 :
                                    
                                    differentiel_periodes_situation_numerique = "+ " + str(np.round(differentiel_periodes_situation_numerique , 2)) + " périodes"
                                    
                                    
                                    
                                    
                                elif differentiel_periodes_situation_numerique == 0 : 
                                    
                                    differentiel_periodes_situation_numerique = str(differentiel_periodes_situation_numerique) + " périodes"
                                    
                                    
                                    
                                    
                                else : 
                                    
                                    differentiel_periodes_situation_numerique = "- " + str(abs(np.round(differentiel_periodes_situation_numerique , 2))) + " périodes"
                                    
                                
                                
                                
                                
                                    
                                col3.metric(label = "" , 
                                            value = np.round(nbr_periodes_situation_numerique_USDH_journee , 2) ,
                                            delta = differentiel_periodes_situation_numerique)
                            
                            
                                col6.metric(label = "" , 
                                            value = np.round(nbr_periodes_situation_numerique_adv_journee , 2))
                            
                            
                            
                            
                            
                                for i in range(3) : 
                            
                                    st.write("")
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                # Métrique n°9 + 14 : temps passé en 'situation_numerique' par les 2 équipes :
                                

                            
                                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                            
                            
                                col4.write(f"Temps durant lequel l'équipe a joué en {situation_numerique} (en minutes) :")
                                
                                
                                
                                
                                    
                                # On récupère le temps passé en 'situation_numerique' par l'USDH et par ses adversaires tout au long de la saison :
                                
                                temps_situation_numerique_USDH = S_durees_situation_numerique_saison(data = df , equipe = "USDH" , 
                                                                                                     situation = situation_numerique).loc[int(bouton_journee[-1])-1]
                                    
                                temps_situation_numerique_adv = S_durees_situation_numerique_saison(data = df , equipe = "adversaire" , 
                                                                                                    situation = situation_numerique).loc[int(bouton_journee[-1])-1]
                                    
                                    
                                    
                                    
                                
                                    
                                    
                                    
                                    
                                
                                # Calcul du différentiel de temps passé en 'situation_numerique' par les 2 équipes : 
                                    
                                differentiel_temps_situation_numerique = temps_situation_numerique_USDH - temps_situation_numerique_adv
                                
                                
                                
                                # Gestion de l'affichage du différentiel suivant son signe : 
                                    
                                if differentiel_temps_situation_numerique > 0 :
                                    
                                    differentiel_temps_situation_numerique = "+ " + str(np.round(differentiel_temps_situation_numerique , 2)) + " minutes"
                                    
                                    
                                    
                                    
                                elif differentiel_temps_situation_numerique == 0 : 
                                    
                                    differentiel_temps_situation_numerique = str(differentiel_temps_situation_numerique) + " minutes"
                                    
                                    
                                    
                                    
                                else : 
                                    
                                    differentiel_temps_situation_numerique = "- " + str(abs(np.round(differentiel_temps_situation_numerique , 2))) + " minutes"
                                    
                                
                                
                                
                                
                                    
                                col3.metric(label = "" , 
                                            value = np.round(temps_situation_numerique_USDH , 2) ,
                                            delta = differentiel_temps_situation_numerique)
                            
                            
                                col6.metric(label = "" , 
                                            value = np.round(temps_situation_numerique_adv , 2))
                            
                            
                            
                            
                            
                            
                            
                                for i in range(7) : 
                            
                                    st.write("")
                                    
                                    
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                # Métrique n°10-11-12 + 15-16-17 : Affichage du BILAN de l'USDH sur SES PROPRES PERIODES de 'situation_numerique' : 
                            
                                    
                                # SI l'USDH a joué AU MOINS 1 FOIS dans cette situation numérique lors de ce match : 
                                    
                                if nbr_periodes_situation_numerique_USDH_journee > 0 :
                                    
                                    
                                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,3.15,3.15,2.5,1.15,1,4])
                                            
                                    col4.write(f"COMPARATIF LORSQUE l'USDH JOUE EN {situation_numerique.upper()} :") 
                                    
                                    
                                    
                                    for i in range(3) : 
                                        
                                        st.write("")
                                        
                                        
                                        
                                        
                                        
                                        
                                    
                                    
                                    
                                    
                                    
                                    # Création d'un bouton pour le choix de l'unité des buts marqués / encaissés / différentiels sur les supériorités numériques lors de ce match : 
                                     
                                        
                                    bouton_unite_bilan_situation_numerique = col7.selectbox("Bilan exprimé en :" , 
                                                                                            [" " , 
                                                                                             "total" , 
                                                                                             f"/ minute jouée par l'USDH en {situation_numerique.split(sep = ' ')[0]}" , 
                                                                                             f"/ période jouée par l'USDH en {situation_numerique.split(sep = ' ')[0]}"])
                                    
                                    
                                    st.write("")
                                    st.write("")
                                    
                                    
                                    
                                    
                                    
                                    if bouton_unite_bilan_situation_numerique != " " :
                                        
                                        
                                        
                                        L_delta_colors = ["normal" , "inverse" , "normal"]
                                            
                                            
                                            
                                        
                                        for type_bilan , delta_color in zip(["buts marqués" , "buts encaissés" , "différentiel de buts"] , L_delta_colors) :
                                            
                                            
                                            col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                                
                                            
                                        
                                            
                                            
                                            # Récupération du bilan du type renseigné de l'équipe à domicile lorsqu'elle joue en 'situation_numerique', et idem pour l'équipe à l'extérieur :
                                             
                                            if bouton_unite_bilan_situation_numerique == "total" :
                                                
                                                
                                                
                                                # Bilan de l'USDH dans cette situation numérique : 
                                                    
                                                buts_type_situation_numerique_USDH = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                        equipe = "USDH" , 
                                                                                                                        situation = situation_numerique , 
                                                                                                                        type_bilan = type_bilan).loc[int(bouton_journee[-1])-1]
                                             
                                                
                                                
                                                
                                                # Bilan de ses adversaires dans cette même situation numérique : lorsque l'USDH joue en supériorité (resp. en infériorité) ==> son adversaire joue quant à lui en infériorité (resp. en supériorité) : 
                                                
                                                
                                                if situation_numerique == "supériorité numérique" :
                                                    
                                                
                                                    buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                           equipe = "adversaire" , 
                                                                                                                           situation = "infériorité numérique" , 
                                                                                                                           type_bilan = type_bilan).loc[int(bouton_journee[-1])-1]
                                                
                                                
                                                
                                                
                                                else :    # situation_numerique == "infériorité numérique"
                                                
                                                
                                                    buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                           equipe = "adversaire" , 
                                                                                                                           situation = "supériorité numérique" , 
                                                                                                                           type_bilan = type_bilan).loc[int(bouton_journee[-1])-1]
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                unite = f" {type_bilan}"
                                                
                                                
                                                
                                                
                                                col4.write(f"{type_bilan} (quand l'USDH joue en {situation_numerique}) :") 
                                                    
                                                    
                                               
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                            elif bouton_unite_bilan_situation_numerique == f"/ minute jouée par l'USDH en {situation_numerique.split(sep = ' ')[0]}" :
                                                
                                                
                                                
                                                # Calcul du temps passé en 'situation_numerique' par l'USDH lors de cette rencontre : 
                                                    
                                                temps_situation_numerique_USDH = S_durees_situation_numerique_saison(data = df , equipe = "USDH" , 
                                                                                                                     situation = situation_numerique).loc[int(bouton_journee[-1])-1]
                                                
    
                                                
                                                
                                                
                                                
                                                # SI l'USDH A PASSE DU TEMPS EN 'situation_numerique' (pour éviter une division par 0) : 
                                                
                                                if temps_situation_numerique_USDH > 0 :
                                                    
                                                    
                                                    # Bilan USDH :
                                                    
                                                    buts_type_situation_numerique_USDH = S_bilan_situation_numerique_saison(data = df , equipe = "USDH" ,  situation = situation_numerique , type_bilan = type_bilan).loc[int(bouton_journee[-1])-1] / temps_situation_numerique_USDH
                                                    
                                                    
                                                    
                                                    # Bilan adversaires : 
                                                        
                                                    if situation_numerique == "supériorité numérique" :
                                                        
                                                    
                                                        buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                               equipe = "adversaire" , 
                                                                                                                               situation = "infériorité numérique" , 
                                                                                                                               type_bilan = type_bilan).loc[int(bouton_journee[-1])-1] / temps_situation_numerique_USDH
                                                    
                                                    
                                                    
                                                    
                                                    else :    # situation_numerique == "infériorité numérique"
                                                    
                                                    
                                                        buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                               equipe = "adversaire" , 
                                                                                                                               situation = "supériorité numérique" , 
                                                                                                                               type_bilan = type_bilan).loc[int(bouton_journee[-1])-1] / temps_situation_numerique_USDH
                                                    
                                                        
                                                
                                                
                                                
                                                # SINON, si l'USDH a passé 0 seconde à jouer en supériorité cette saison :
                                                
                                                else : 
                                                    
                                                    
                                                    # Bilan USDH : 
                                                        
                                                    buts_type_situation_numerique_USDH = 0
                                                    
                                                    
                                                    
                                                    # Bilan adversaires : 
                                                    
                                                    buts_type_situation_numerique_adv = 0
                                                    
                                                    
                                                
                                                
    
                                                
                                                
                                                unite = f" {type_bilan} / min de {situation_numerique.split(sep = ' ')[0][0:4]}."
                                                
                                                
                                                col4.write(f"{type_bilan} (par minute que l'USDH a joué en {situation_numerique}) :") 
                                                    
                                                    
                                               
                                            
                                         
                                            
                                         
                                            
                                         
                                         
                                            elif bouton_unite_bilan_situation_numerique == f"/ période jouée par l'USDH en {situation_numerique.split(sep = ' ')[0]}" :
                                                
                                                
                                                
                                                
                                                # SI l'USDH A JOUE EN 'situation_numerique' (pour éviter une division par 0) : 
                                                
                                                if nbr_periodes_situation_numerique_USDH_journee > 0 :
                                                    
                                                    # Bilan USDH : 
                                                        
                                                    buts_type_situation_numerique_USDH = S_bilan_situation_numerique_saison(data = df , equipe = "USDH" ,  situation = situation_numerique , type_bilan = type_bilan).loc[int(bouton_journee[-1])-1] / nbr_periodes_situation_numerique_USDH_journee
                                                
                                                
                                                
                                                
                                                    # Bilan adversaires : 
                                                        
                                                    
                                                    if situation_numerique == "supériorité numérique" :
                                                        
                                                    
                                                        buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                               equipe = "adversaire" , 
                                                                                                                               situation = "infériorité numérique" , 
                                                                                                                               type_bilan = type_bilan).loc[int(bouton_journee[-1])-1] / nbr_periodes_situation_numerique_USDH_journee
                                                    
                                                    
                                                    
                                                    
                                                    else :    # situation_numerique == "infériorité numérique"
                                                    
                                                    
                                                        buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                               equipe = "adversaire" , 
                                                                                                                               situation = "supériorité numérique" , 
                                                                                                                               type_bilan = type_bilan).loc[int(bouton_journee[-1])-1] / nbr_periodes_situation_numerique_USDH_journee
                                                    
                                                        
                                                        
                                                        
                                                        
                                                        
                                                        
                                                
                                                # SINON, si l'USDH a passé 0 seconde à jouer en 'situation numerique' cette saison :
                                                
                                                else : 
                                                    
                                                    # Bilan USDH : 
                                                        
                                                    buts_type_situation_numerique_USDH = 0
                                                    
                                                    
                                                    
                                                    # Bilan adversaires :
                                                    
                                                    buts_type_situation_numerique_adv = 0
                                                    
                                                    
                                                
    
                                               
                                                
                                                
                                                
                                                unite = f" {type_bilan} / période jouée par l'USDH en {situation_numerique.split(sep = ' ')[0][0:4]}."
                                                
                                                
                                                if type_bilan in ["buts marqués" , "buts encaissés"] :
                                                
                                                    col4.write(f"{type_bilan} (par période que l'USDH a joué en {situation_numerique.split(sep = ' ')[0][0:4]}) :") 
                                                    
                                                    
                                                else : 
                                                    
                                                    col4.write("Différentiel de buts (par période que l'USDH a joué en {situation_numerique.split(sep = ' ')[0][0:4]}) :")
                                                
                                         
                                            
                                         
                                            
                                         
                                            
                                         
                                 
                                            # Calcul de la différence de bilan sur les 'situation_numerique' EN FAVEUR DE L'USDH : 
                                                    
                                                
                                            difference_type_buts_situation_numerique = np.round(buts_type_situation_numerique_USDH - buts_type_situation_numerique_adv , 2)
                                                
                                            
                                            
                                            
                                            # Ré-écriture de la différence bilan sur les 'situation_numerique' :
                                             
                                            if difference_type_buts_situation_numerique > 0 : 
                                                    
                                                difference_type_buts_situation_numerique = "+ " + str(difference_type_buts_situation_numerique) + unite
                                                
                                                
                                                
                                            elif difference_type_buts_situation_numerique < 0 : 
                                                
                                                difference_type_buts_situation_numerique = "- " + str(abs(difference_type_buts_situation_numerique)) + unite
                                                
                                                
                                                    
                                            
                                            
                                            
                                            # On écrit le delta de bilan en 'situation_numerique' sous l'USDH (à gauche) :
                                                
                                            col3.metric(label = "" , 
                                                        value = np.round(buts_type_situation_numerique_USDH , 2) ,
                                                        delta = str(difference_type_buts_situation_numerique) , 
                                                        delta_color = delta_color)
                                        
                                        
                                        
                                            col6.metric(label = "" , 
                                                        value = np.round(buts_type_situation_numerique_adv , 2) , 
                                                        delta = " ")
                                        
                                            
                                            
    
                                            
                                            
                                            for i in range(3) : 
                                                
                                                st.write("")
                                            
                                            
                                            
                                            
                                        
                                    
                                for i in range(5) : 
                                    
                                    st.write("")
                                    
                                    
                                    
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                            # Analyse des périodes d'EGALITE NUMERIQUE des 2 équipes : 
                                
                                
                            if bouton_unite_bilan_situation_numerique != " " :
                             
                            
                        
                                st.write("------------------------------------------------------------------------")
                                    
                                    
                                    
                                    
                                st.markdown("<h1 style='text-align: center; color: white;'>Périodes d'égalité numérique.</h1>",
                                                 unsafe_allow_html = True)   
                                    
                                
                                
                            
                            
                            
                                for i in range(5) : 
                                    
                                    st.write("")
                                    
                                    
                                    
                                

                                
                                
                                
                                
                                # Métrique n°18 : temps passé à égalité numérique par les 2 équipes :
                            

                        
                                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                            
                            
                                col4.write("Temps passé à égalité numérique (en minutes) :")
                                
                                
                                
                                
                                    
                                # On récupère le temps passé à égalité numérique par l'USDH et par ses adversaires tout au long de la saison :
                                
                                temps_egalite_num = S_durees_situation_numerique_saison(data = df , equipe = "USDH" , 
                                                                                        situation = "égalité numérique").loc[int(bouton_journee[-1]) -1]
                                    
                                   
                                    
                                    
                                    
                                
                                
                                
                                    
                                col3.metric(label = "" , 
                                            value = np.round(temps_egalite_num , 2))
                            
                            
                                col6.metric(label = "" , 
                                            value = np.round(temps_egalite_num , 2))
                            
                            
                            
                            
                            
                            
                            
                                for i in range(7) : 
                            
                                    st.write("")
                                    
                                    
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                # Métrique n°19-20-21 : Affichage du BILAN de chaque équipe sur LES PERIODES (communes) d'EGALITE NUMERIQUE DES 2 EQUIPES : 
                            

                                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                                        
                                col4.write("COMPARATIF DES 2 EQUIPES LORSQU'ELLES JOUENT A EGALITE NUMERIQUE :") 
                                
                                
                                
                                for i in range(3) : 
                                    
                                    st.write("")
                                
                                
                                
                                
                                
                                
                                # Création d'un bouton pour le choix de l'unité des buts marqués / encaissés / différentiels sur les égalités numériques : 
                                 
                               
                                bouton_unite_bilan_egalite = col6.selectbox("Chiffres exprimés en :" , 
                                                                            [" " , 
                                                                             "total" , 
                                                                             "/ minute jouée à égalité num"])

                                    
                                
                                

                                
                                st.write("")
                                st.write("")
                                
                                
                                
                                
                                
                                if bouton_unite_bilan_egalite != " " :
                                    
                                    
                                    for type_bilan , delta_color in zip(["buts marqués" , "buts encaissés" , "différentiel de buts"] , ["normal" , "inverse" , "normal"]) :
                                        
                                        
                                        col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                            
                                        
                                    
                                        
                                        
                                        # Récupération du bilan du type renseigné de l'équipe à domicile lorsqu'elle joue à égalité numérique, et idem pour l'équipe à l'extérieur :
                                         
                                        if bouton_unite_bilan_egalite == "total" :
                                            
                                            
                                            
                                            # Bilan de l'USDH : 
                                                
                                            buts_type_a_ega_USDH = S_bilan_situation_numerique_saison(data = df , 
                                                                                                      equipe = "USDH" , 
                                                                                                      situation = "égalité numérique" , 
                                                                                                      type_bilan = type_bilan).loc[int(bouton_journee[-1]) -1]
                                         
                                            
                                            
                                            
                                            # Bilan de ses adversaires : 
                                                
                                            buts_type_a_ega_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                     equipe = "adversaire" , 
                                                                                                     situation = "égalité numérique" , 
                                                                                                     type_bilan = type_bilan).loc[int(bouton_journee[-1]) -1]
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                            unite = f" {type_bilan}"
                                            
                                            
                                            
                                            
                                            col4.write(f"{type_bilan} sur les périodes d'égalité numérique :") 
                                                
                                                
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                        elif bouton_unite_bilan_egalite == "/ minute jouée à égalité num" :
                                            
                                            
                                            
                                            # Calcul du temps passé à égalité numérique par les 2 équipes depuis le début de la saison (temps total) : 
                                                
                                            temps_egalite_num = S_durees_situation_numerique_saison(data = df , equipe = "USDH" , 
                                                                                                    situation = "égalité numérique").loc[int(bouton_journee[-1]) -1]
                                            
                                            
                                            
                                            
                                            
                                            
                                            # SI les 2 équipes ONT JOUES A EGALITE NUMERIQUE cette saison (pour éviter une division par 0) : 
                                            
                                            if temps_egalite_num > 0 :
                                                
                                                buts_type_a_ega_USDH = S_bilan_situation_numerique_saison(data = df , equipe = "USDH" ,  situation = "égalité numérique" , type_bilan = type_bilan).loc[int(bouton_journee[-1]) -1] / temps_egalite_num
                                                buts_type_a_ega_adv = S_bilan_situation_numerique_saison(data = df , equipe = "adversaire" ,  situation = "égalité numérique" , type_bilan = type_bilan).loc[int(bouton_journee[-1]) -1] / temps_egalite_num
                                            
                                            
                                            
                                            
                                            # SINON, si l'USDH a passé 0 seconde à jouer en supériorité cette saison :
                                            
                                            else : 
                                                
                                                buts_type_a_ega_USDH = 0
                                                buts_type_a_ega_adv = 0
                                                
                                            
                                            
                                            
                                            

                                            
                                            
                                            unite = f" {type_bilan} / min à égalité num."
                                            
                                            
                                            if type_bilan in ["buts marqués" , "buts encaissés"] :
                                            
                                                col4.write(f"{type_bilan} / minute que l'équipe a joué à égalité numérique :") 
                                                
                                                
                                            else : 
                                                
                                                col4.write("Différentiel de buts / minute que l'équipe a joué à égalité numérique :")
                                            
                                            
                                     
                                        

                             
                                        # Calcul de la différence de bilan sur les égalités numériques EN FAVEUR DE L'USDH : 
                                                
                                            
                                        difference_type_buts_ega = np.round(buts_type_a_ega_USDH - buts_type_a_ega_adv , 2)
                                            
                                        
                                        
                                        # Ré-écriture de la différence bilan sur les égalités nums :
                                         
                                        if difference_type_buts_ega > 0 : 
                                                
                                            difference_type_buts_ega = "+ " + str(difference_type_buts_ega) + unite
                                            
                                            
                                            
                                        elif difference_type_buts_ega < 0 : 
                                            
                                            difference_type_buts_ega = "- " + str(abs(difference_type_buts_ega)) + unite
                                            
                                            
                                                
                                        
                                        
                                        
                                        # On écrit le delta de bilan en supériorité sous l'USDH (à gauche) :
                                            
                                        col3.metric(label = "" , 
                                                    value = np.round(buts_type_a_ega_USDH , 2) ,
                                                    delta = str(difference_type_buts_ega) , 
                                                    delta_color = delta_color)
                                    
                                    
                                    
                                        col6.metric(label = "" , 
                                                    value = np.round(buts_type_a_ega_adv , 2) , 
                                                    delta = " ")
                                    
                                        
                                        

                                        
                                        
                                        for i in range(3) : 
                                            
                                            st.write("")
                                            
                                            
                                            
                                            
                                        
                                    
                                    for i in range(5) : 
                                        
                                        st.write("")
                                        
                                        
                                     
                                        
                                     
                                    for i in range(7) : 
                                        
                                        st.write("")
                                        
                                        
                                        
                                    st.write("----------------------------------------------------------------------")
                                    
                                    
                                    
                                
                                
                                
                                
                                
                                
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
      
        
      
    
    
    
                                    # PARTIE 3 : métriques / graphiques liés à la DYNAMIQUE DE JEU :
                                
                                
                                    st.markdown("<h1 style='text-align: center; color: white;'>Statistiques liées à la dynamique de jeu.</h1>",
                                                unsafe_allow_html = True)  
                                    
                                    
                                    st.write("-------------------------------------------------------------------------------------")
                                    
                                
                                
                                
                                    for i in range(3) : 
                                        
                                        st.write("")
                                    
                                    
                                    
                                    
                                    
                                    st.markdown("<h1 style='text-align: center; color: white;'>A) Dans les moments cruciaux.</h1>",
                                                unsafe_allow_html = True)
                                    
                                    
                                    
                                    
                                    for i in range(2) : 
                                        
                                        st.write("")
                                        
                                        
                                        
                                    st.write("==> Pour évaluer la capacité des 2 équipes à être présente dans les moments cruciaux d'un match.")    
                                       
                                    
                                    
                                    
                                    for i in range(3) : 
                                        
                                        st.write("")
                                    
                                    
                                        
                                        
                                        
                                        
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    # Métrique n°11-12-13-14-15 : Affichage de la dynamique DES 2 EQUIPES dans les périodes cruciales du match (début de match, avant mi-temps, retour de mi-temps et money time) :
                        
                                    L_dates = [10 , 30 , 35 , 35 , 60]               # la liste des dates
                                    L_x_dernieres_minutes = [10 , 5 , 5 , 10 , 10]   # la liste des x dernières minutes à regarder précédant chaque date de la liste ci-dessus
                                    
                                    
                                    
                                    
                                    # Pour chaque période cruciale du match :
                                        
                                    for date , x_dernieres_minutes in zip(L_dates , L_x_dernieres_minutes) :
                                        
                                        
                                        col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1]) 
                                        
                                        
                                        
                                        # CAS 1 : SI l'on regarde la dynamique en DEBUT DE MATCH :
                                        
                                        if date == 10 :
                                                    
                                            col4.write("Dynamique début de match (0-10ème minute) :") 
                                            
                                        
                                        
                                        
                                        # CAS 2 : SI l'on regarde la dynamique d'AVANT MI-TEMPS :
                                        
                                        elif date == 30 : 
                                            
                                            col4.write("Dynamique avant mi-temps (25-30ème minute)")
                                            
                                            
                                        
                                        
                                        elif date == 35 : 
                                            
                                            
                                            # CAS 3 : SI l'on regarde la dynamique au RETOUR DE MATCH :
                                            
                                            if x_dernieres_minutes == 5 :
                                            
                                                col4.write("Dynamique retour de mi-temps (30-35ème minute) :")
                                                
                                             
                                                
                                             
                                            # CAS 4 : SI l'on regarde la dynamique AUTOUR DE LA MI-TEMPS (5 minutes avant + 5 minutes au retour) :
                                            
                                            else : 
                                            
                                                col4.write("Dynamique aux alentours de la mi-temps (25-35ème minute) :")    
                                            
                                            
                                            
                                           
                                            
                                        # CAS 5 : SI l'on regarde la dynamique dans le MONEY TIME :
                                            
                                        else : 
                                            
                                            col4.write("Dynamique money-time (50-60ème minute) :")
                                            
                                            
                                        
                                        
                                        # Récupération du nombre de buts inscrits par l'équipe à domicile et par l'équipe à l'extérieur dans cette période cruciale du match :
                                                
                                            
                                        nbr_buts_periode_cruciale_domicile = dynamique_buts_marques(data = df , 
                                                                                                    date = date , 
                                                                                                    x_dernieres_minutes = x_dernieres_minutes  , 
                                                                                                    journee = bouton_journee , 
                                                                                                    equipe = "domicile")
                                        
                                        
                                        nbr_buts_periode_cruciale_exterieur = dynamique_buts_marques(data = df , 
                                                                                                     date = date , 
                                                                                                     x_dernieres_minutes = x_dernieres_minutes  , 
                                                                                                     journee = bouton_journee , 
                                                                                                     equipe = "extérieur")
                                        
                                    
                                        
                             
                                
                                        # Calcul de la différence de buts marqués EN FAVEUR DE L'USDH dans cette période de jeu cruciale : 
                                                
                                            
                                        # CAS 1 : l'USDH joue à domicile : 
                                            
                                        if equipe_domicile == "USDH" :
                                        
                                            difference_nbr_buts_periode_cruciale = nbr_buts_periode_cruciale_domicile - nbr_buts_periode_cruciale_exterieur
                                            
                                        
                                        
                                            # Ré-écriture de la différence de buts marqués calculée ci-dessus :
                                             
                                            if difference_nbr_buts_periode_cruciale > 0 : 
                                                    
                                                difference_nbr_buts_periode_cruciale = "+ " + str(difference_nbr_buts_periode_cruciale) + " buts marqués"
                                                
                                                
                                                
                                                
                                            elif difference_nbr_buts_periode_cruciale < 0 : 
                                                
                                                difference_nbr_buts_periode_cruciale = "- " + str(abs(difference_nbr_buts_periode_cruciale)) + " buts marqués"
                                                
                                                
                                                
                                        
                                        
                                        
                                            # On écrit le delta de buts marqués sous l'équipe à domicile, car il s'agit de l'USDH :
                                                
                                            # SI on NE regarde PAS le début de match ==> on peut, en plus de la dynamique, afficher le score au début de la période :
                                            
                                            if date != 10 :
                                                
                                                score_USDH_debut_periode_cruciale = score_USDH(data = df , journee = bouton_journee , temps = date-x_dernieres_minutes)        # le score de l'USDH au début de cette période cruciale
                                                score_adv_debut_periode_cruciale = score_adversaire(data = df , journee = bouton_journee , temps = date-x_dernieres_minutes)   # le score de l'adversaire de l'USDH au début de cette période cruciale
                                                differentiel_debut_periode_cruciale = score_USDH_debut_periode_cruciale - score_adv_debut_periode_cruciale                     # le différentiel de buts en faveur de l'USDH a début de cette période cruciale
                                                
                                                
                                                # Ré-écriture du différentiel de buts suivant son signe : 
                                                    
                                                if differentiel_debut_periode_cruciale > 0 :
                                                    
                                                    differentiel_debut_periode_cruciale = "+ " + str(differentiel_debut_periode_cruciale)
                                                    
                                                    
                                                    
                                                    
                                                elif differentiel_debut_periode_cruciale < 0 :
                                                    
                                                    differentiel_debut_periode_cruciale = "- " + str(abs(differentiel_debut_periode_cruciale))
                                                    
                                                    
                                                    
                                                    
                                               
                                                    
                                                    
                                                
                                                label_USDH = f"score à la {date-x_dernieres_minutes}ème minute : {score_USDH_debut_periode_cruciale} - {score_adv_debut_periode_cruciale} ({differentiel_debut_periode_cruciale})"
                                                label_adv = " "
                                            
                                              
                                            # SINON, si on regarde le début de match ==> pas besoin d'afficher le score, car il est de 0-0 :
                                        
                                            else : 
                                                
                                                label_USDH = " "
                                                label_adv = " "
                                                
                                              
                                                
                                              
                                              
                                            col3.metric(label = label_USDH , 
                                                        value = nbr_buts_periode_cruciale_domicile ,
                                                        delta = difference_nbr_buts_periode_cruciale)
                                            
                                                
                                                
                                            col6.metric(label = label_adv , 
                                                        value = nbr_buts_periode_cruciale_exterieur , 
                                                        delta = " ")
                                        
                                        
                                        
                                        
                                        
                                        
                                        # CAS 2 : l'USDH joue à l'extérieur :
                                            
                                        else : 
                                            
                                            difference_nbr_buts_periode_cruciale = nbr_buts_periode_cruciale_exterieur - nbr_buts_periode_cruciale_domicile
                                            
                                            
                                            
                                            
                                            # Ré-écriture de la différence de buts marqués calculée ci-dessus :
                                             
                                            if difference_nbr_buts_periode_cruciale > 0 : 
                                                    
                                                difference_nbr_buts_periode_cruciale = "+ " + str(difference_nbr_buts_periode_cruciale) + " buts marqués"
                                                
                                                
                                                
                                            elif difference_nbr_buts_periode_cruciale < 0 : 
                                                
                                                difference_nbr_buts_periode_cruciale = "- " + str(abs(difference_nbr_buts_periode_cruciale)) + " buts marqués"
                                                
                                                
                                        
                                        
                                        
                                            # On écrit le delta de buts marqués sous l'équipe à l'extérieur, car il s'agit de l'USDH :
                                             
                                            # SI on NE regarde PAS le début de match ==> on peut, en plus de la dynamique, afficher le score au début de la période :
                                            
                                            if date != 10 :
                                                
                                                label_USDH = f"score à la {date-x_dernieres_minutes}ème minute : {score_USDH(data = df , journee = bouton_journee , temps = date-x_dernieres_minutes)} - {score_adversaire(data = df , journee = bouton_journee , temps = date-x_dernieres_minutes)}"
                                                label_adv = " "
                                            
                                              
                                            
                                            # SINON, si on regarde le début de match ==> pas besoin d'afficher le score, car il est de 0-0 :
                                        
                                            else : 
                                                
                                                label_USDH = " "
                                                label_adv = " "
                                                
                                                
                                              
                                            col3.metric(label = label_adv , 
                                                        value = nbr_buts_periode_cruciale_domicile , 
                                                        delta = " ")
                                        
                                        
                                            col6.metric(label = label_USDH , 
                                                        value = nbr_buts_periode_cruciale_exterieur , 
                                                        delta = difference_nbr_buts_periode_cruciale)
                                        
                                        
                                        
                                        
                                        
                                        for i in range(6) : 
                                            
                                            st.write("")
                                            
                                            
                                            
                                    
                                    
                                    
                                    
                                    
                                    for i in range(3) : 
                                        
                                        st.write("")
                                        
                                        
                                    
                                    st.markdown("<h1 style='text-align: center; color: white;'>B) Au sortir des temps morts.</h1>",
                                                unsafe_allow_html = True)
                                    
                                    
                                    
                                    
                                    for i in range(2) : 
                                        
                                        st.write("")
                                        
                                        
                                        
                                    st.write("==> Pour évaluer la capacité des 2 équipes à réagir ou à maintenir le même niveau de jeu au sortir d'un temps mort.")    
                                       
                                    
                                    
                                    for i in range(3) : 
                                        
                                        st.write("")
                                        
                                        
                                        
                                        
                                    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                                        
                                        
                                    # Métrique n°15-16 : Affichage de la DYNAMIQUE DES 2 EQUIPES au SORTIR DES TEMPS MORTS posés par chaque equipe : 
                            
                                    # Pour chacune des 2 équipes opposées ce jour-là :
                                        
                                    for TM_de , num_equipe in zip([equipe_domicile , equipe_exterieur] , [1 , 2]) :
                                        
                                        
                                        st.markdown(f"<h1 style='text-align: center; color: white;'>B-{num_equipe}) Temps morts {TM_de}.</h1>",
                                                    unsafe_allow_html = True)
                                        
                                        
                                       
                                        
                                        for i in range(5) : 
                                            
                                            st.write("")
                                            
                                            
                                        # On récupère le dictionnaire des dynamiques des 2 équipes opposées AVANT et APRES le TM, POUR CHAQUE TM posé par cette équipe :
                                            
                                        dico_dynamiques_avant_TM_domicile = dynamique_autour_TM(data = df , 
                                                                                                avant_ou_apres = "avant" ,
                                                                                                x_minutes_avant_apres = 5 , 
                                                                                                journee = bouton_journee , 
                                                                                                equipe = equipe_domicile , 
                                                                                                TM_de = TM_de)
                                        
                                        
                                        
                                        dico_dynamiques_apres_TM_domicile = dynamique_autour_TM(data = df , 
                                                                                                avant_ou_apres = "après" ,
                                                                                                x_minutes_avant_apres = 5 , 
                                                                                                journee = bouton_journee , 
                                                                                                equipe = equipe_domicile , 
                                                                                                TM_de = TM_de)
                                        
                                        
                                        
                                        
                                        dico_dynamiques_avant_TM_exterieur = dynamique_autour_TM(data = df , 
                                                                                                 avant_ou_apres = "avant" ,
                                                                                                 x_minutes_avant_apres = 5 , 
                                                                                                 journee = bouton_journee , 
                                                                                                 equipe = equipe_exterieur , 
                                                                                                 TM_de = TM_de)
                                        
                                        
                                        
                                        dico_dynamiques_apres_TM_exterieur = dynamique_autour_TM(data = df , 
                                                                                                 avant_ou_apres = "après" ,
                                                                                                 x_minutes_avant_apres = 5 , 
                                                                                                 journee = bouton_journee , 
                                                                                                 equipe = equipe_exterieur , 
                                                                                                 TM_de = TM_de)
                                            
                                            
                                            
                                                
                                        
        
                                        # CAS 1 : si AU MOINS 1 temps mort a été posé par l'équipe :
                                            
                                        if len(dico_dynamiques_avant_TM_domicile) > 0 :
                                            
                                            
                                            
                                            
                                            # On extrait de n'importe lequel des 4 dictionaires la (les) date(s) des temps morts posés :
                                        
                                            L_dates_TM = list(dico_dynamiques_avant_TM_domicile.keys())
                                            
                                            
                                            
                                            # Pour chaque date de temps mort posé :
                                            
                                            k = 1
                                            
                                            for date_TM in L_dates_TM :
                                                
                                                
                                                st.write("------------------------------------------------------------")
                                                
                                                
                                                for i in range(2) : 
                                                    
                                                    st.write("")
                                                    
                                                
                                                
                                                
                                                
                                                # On récupère le score des 2 équipes à la date lors de laquelle a été pris le TM :
                                                        
                                                            
                                                score_dom_a_date_TM = score_USDH(data = df , journee = bouton_journee , temps = date_TM[0])        # le score de l'USDH au moment ou le TM est posé
                                                score_ext_a_date_TM = score_adversaire(data = df , journee = bouton_journee , temps = date_TM[0])        # le score de l'adversaire de l'USDH au moment ou le TM est posé
                                                difference_score_a_date_TM = score_dom_a_date_TM - score_ext_a_date_TM  # écart au score en faveur de l'USDH au moment du TM
                                                
                                                
                                                
                                    
                                                # Ré-écriture de la différence de buts marqués calculée ci-dessus :
                                                 
                                                if difference_score_a_date_TM > 0 : 
                                                        
                                                    difference_score_a_date_TM = "+ " + str(difference_score_a_date_TM)
                                                    
                                                    
                                                    
                                                    
                                                elif difference_score_a_date_TM < 0 : 
                                                    
                                                    difference_score_a_date_TM = "- " + str(abs(difference_score_a_date_TM))
                                                    
                                                      
                                                    
                                                    
                                                    
                                                    
                                                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([4,1,1,1,1,1,1]) 
                                            
                                                col1.write(f"Temps mort °{k} {TM_de} : {np.round(date_TM[0] , 2)}ème minute (score : {score_dom_a_date_TM} - {score_ext_a_date_TM} , {difference_score_a_date_TM}) :")
                                                    
                                                    
                                                for i in range(3) : 
                                                    
                                                    st.write("")
                                                    
                                                    
                                                
                                                
                                                # Pour les x minutes AVANT / APRES la date du temps mort :
                                                    
                                                for anteriorite in ["avant" , "après"] :
                                                
                                                
                                                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1]) 
                                            
                                                    
                                                    
                                                    if k == 1 : 
                                                        
                                                        col4.write(f"Dynamique lors des 5 minutes {anteriorite.upper()} ce temps mort :")
                                                
                                                    
                                                    else : 
                                                        
                                                        col4.write(f"Dynamique lors des 5 minutes {anteriorite.upper()} ce temps mort :")
                                                
                                                
                                                
                                                
                                                    
                                                    # On récupère le score de chaque équipe dans les 5 minutes autour de ce TM posé + le différentiel de buts :
                                                        
                                                    if anteriorite == "avant" : 
                                                        
                                                        buts_marques_domicile_autour_TM = dico_dynamiques_avant_TM_domicile[date_TM][f"buts marqués {equipe_domicile}"]
                                                        buts_marques_exterieur_autour_TM = dico_dynamiques_avant_TM_domicile[date_TM][f"buts encaissés {equipe_domicile}"]
                                                        
                                                        
                                                    else : 
                                                        
                                                        buts_marques_domicile_autour_TM = dico_dynamiques_apres_TM_domicile[date_TM][f"buts marqués {equipe_domicile}"]
                                                        buts_marques_exterieur_autour_TM = dico_dynamiques_apres_TM_domicile[date_TM][f"buts encaissés {equipe_domicile}"]
                                                        
                                                        
                                                        
                                                        
                                                    
                                                    # On calcule le différentiel de buts (en faveur de l'USDH) :
                                                    
                                                        
                                                    # SI l'USDH joue à domicile : 
                                                        
                                                    if equipe_domicile == "USDH" :
                                                        
                                                        differentiel_buts_autour_TM = buts_marques_domicile_autour_TM - buts_marques_exterieur_autour_TM
                                                        
                                                        
                                                        
                                                        
                                                        # Ré-écriture du différentiel de buts suivant son signe : 
                                                    
                                                        if differentiel_buts_autour_TM > 0 :
                                                            
                                                            differentiel_buts_autour_TM = "+ " + str(differentiel_buts_autour_TM)
                                                            
                                                            
                                                            
                                                            
                                                        elif differentiel_buts_autour_TM < 0 :
                                                            
                                                            differentiel_buts_autour_TM = "- " + str(abs(differentiel_buts_autour_TM))
                                                            
                                                            
        
                                                        
            
                                                        # On écrit le différentiel de buts sous l'équipe à domicile, car il s'agit de l'USDH :
                                                             
                                                        col3.metric(label = "" , 
                                                                    value = buts_marques_domicile_autour_TM ,
                                                                    delta = differentiel_buts_autour_TM)
                                                        
                                                            
                                                            
                                                        col6.metric(label = "" , 
                                                                    value = buts_marques_exterieur_autour_TM , 
                                                                    delta = " ")
                                                        
                                                        
                                                        
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    # SINON, SI l'USDH joue à l'extérieur : 
                                                        
                                                    else :   # equipe_exterieur == "USDH" :
                                                        
                                                        differentiel_buts_autour_TM = buts_marques_exterieur_autour_TM - buts_marques_domicile_autour_TM
                                                        
                                                        
                                                        
                                                        
                                                        # Ré-écriture du différentiel de buts suivant son signe : 
                                                    
                                                        if differentiel_buts_autour_TM > 0 :
                                                            
                                                            differentiel_buts_autour_TM = "+ " + str(differentiel_buts_autour_TM)
                                                            
                                                            
                                                            
                                                            
                                                        elif differentiel_buts_autour_TM < 0 :
                                                            
                                                            differentiel_buts_autour_TM = "- " + str(abs(differentiel_buts_autour_TM))
                                                            
                                                            
            
                                                        
                                                        # On récupère également le score des 2 équipes à la date lors de laquelle a été pris le TM :
                                                        
                                                            
                                                        score_dom_a_date_TM = score_adversaire(data = df , journee = bouton_journee , temps = date_TM[0])        # le score de l'adversaire de l'USDH au moment ou le TM est posé
                                                        score_ext_a_date_TM = score_USDH(data = df , journee = bouton_journee , temps = date_TM[0])        # le score de l'USDH au moment ou le TM est posé
                                                        difference_score_a_date_TM = score_ext_a_date_TM - score_dom_a_date_TM  # écart au score en faveur de l'USDH au moment du TM
                                                        
                                                        
                                                        
                                            
                                                        # Ré-écriture de la différence de buts marqués calculée ci-dessus :
                                                         
                                                        if difference_score_a_date_TM > 0 : 
                                                                
                                                            difference_score_a_date_TM = "+ " + str(difference_score_a_date_TM)
                                                            
                                                            
                                                            
                                                            
                                                        elif difference_score_a_date_TM < 0 : 
                                                            
                                                            difference_score_a_date_TM = "- " + str(abs(difference_score_a_date_TM))
                                                        
                                                        
                                                        
            
                                                        # On écrit le différentiel de buts sous l'équipe à l'extérieur, car il s'agit de l'USDH :
                                                             
                                                        
                                                        col3.metric(label = "" , 
                                                                    value = buts_marques_domicile_autour_TM ,
                                                                    delta = " ")
                                                        
                                                            
                                                            
                                                        col6.metric(label = "" , 
                                                                    value = buts_marques_exterieur_autour_TM , 
                                                                    delta = differentiel_buts_autour_TM)
                                                        
                                                        
                                                        
                                                        
                                                    for i in range(3) : 
                                                        
                                                        st.write("")
                                        
                                        
                                                        
                                                    
                                                    
                                                    
                                                k += 1
                                                
                                                for i in range(3) : 
                                                    
                                                    st.write("")
                                                    
                                                
                            
                                                    
                                                    
                                                    
                                                    
                                           
                                        
                                        
                                        
          
        
          
                                            
                                                
                                        # CAS 2 : SINON, si AUCUN temps mort N'a été posé par cette équipe :
                                            
                                        else :   # len(dico_dynamiques_TM_domicile) == 0 :     
                                            
                                            st.write(f"--> {TM_de} n'a posé aucun temps mort lors de ce match !")
                                            
                                            
                                            
                                            for i in range(8) : 
                                                
                                                st.write("")
                                                
                                                
                                                
                                        st.write("--------------------------------------------------------------------")
                                 
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                     
                                            
                                     

                                





















    # CAS 2 : si l'utilisateur souhaite réaliser une analyse GLOBALE DE L'USDH lors de cette saison 2022-23 : 
        
    else :    # bouton_activite == "BILAN saison USDH" : 
        
      
    
        st.markdown(f"<h1 style='text-align: center; color: white;'>BILAN saison USDH ({list(dico_rencontres_USDH.keys())[0]} - {list(dico_rencontres_USDH.keys())[-1]}) :</h1>",
                                    unsafe_allow_html = True)  
        
        
        
        
        for i in range(5) : 
            
            st.write("")
            
            
            
            
            
            
            
        # Affichage des équipes (USDH et adversaire) et du logo de l'USDH : 
                            
                        
                            
        # Affichage des NOMS DES 2 EQUIPES OPPOSEES + DE LEUR LOGO (en face du nom) : 
                    
        # col1 , col2 , col3 , col4 , col5 = st.columns([2 , 2 , 2 , 2 , 2]) 
        
        col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1]) 
            
        
        col3.header("**USDH**")
        
        logo_equipe_1 = Image.open(dico_logos["USDH"]) 
        col2.image(logo_equipe_1 , width = 115)
    
        
        col6.header("**ADVERSAIRES**")
        
      
        
            
            
        for i in range(3) : 
            
            st.write("")
            
            
        
        
    
        
        
        # Création DANS LE MENU LATERAL d'un bouton pour le choix de l'unité des métriques à venir (TOTAL ou PAR MATCH) :
                            
        
                
        bouton_unite = st.sidebar.radio("Dans quelle unité souhaitez-vous afficher les statistiques et graphiques ?" , 
                                        [" " , "total" , "moyenne / match"])
             
             
             

        
        
        
            
        # SI un choix a été fait pour l'unité des indicateurs : 
                            
        if bouton_unite != " " :
            
            
            
            

            
            
            
            
                # PARTIE 1 : métriques / graphiques liés aux BUTS :
                    
                    
                    
                st.write("-------------------------------------------------------------------------------------")
                
                    
                    
                st.markdown("<h1 style='text-align: center; color: white;'>Statistiques liées au score.</h1>",
                            unsafe_allow_html = True)  
                
                
                st.write("-------------------------------------------------------------------------------------")
                
        
        
            
                for i in range(3) : 
                    
                    st.write("")
        
        
        
        
        
            
                # Métrique 1-2-3 : Nombre de BUTS MARQUES par les 2 équipes depuis le début de la saison (match entier, M1 et M2) : 
                
                for periode in ["match" , "M1" , "M2"] :
                    
                    
                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1]) 
                        
                        
                        
                    # On récupère la série des buts de l'USDH et de ses adversaires depuis le début de saison :
                
                    S_buts_USDH = S_nbr_type_action_saison(data = df , type_action = "buts marqués" , 
                                                           equipe = "USDH" , periode = periode)
                    
                    
                    L_buts_USDH = list(S_buts_USDH)
                    
                    L_buts_USDH.append(24)  # on ajoute manuellement les buts marqués par l'USDH lors de la J11, dont les faits de jeu n'ont pas été enregistrés.
                    
                    S_buts_USDH = pd.Series(L_buts_USDH)   
                    
                    
                    
                    
                    
                    S_buts_adv = S_nbr_type_action_saison(data = df , type_action = "buts marqués" , 
                                                          equipe = "adversaire" , periode = periode)
                    
                    
                    L_buts_adv = list(S_buts_adv)
                    
                    L_buts_adv.append(29)  # on ajoute manuellement les buts marqués par le RACC de Nantes lors de la J11, dont les faits de jeu n'ont pas été enregistrés.
                    
                    
                    S_buts_adv = pd.Series(L_buts_adv)   
                    
                    
                    
                    if periode == "match" :
                    
                        col4.write("Nombre de buts marqués (sur le match entier) :")
                        
                        
                        
                    else :
                    
                        col4.write(f"Nombre de buts marqués en {periode} :")
                    
                    
                    
                    
                    
                    # CAS 1 : si je souhaite avoir les TOTAUX de buts ==> je n'ai qu'à SOMMER les buts de la série.
                        
                    if bouton_unite == "total" : 
                        
                        
                        nbr_buts_USDH = S_buts_USDH.sum()  
                        nbr_buts_adv = S_buts_adv.sum()    
                        
                        differentiel_nbr_buts = nbr_buts_USDH - nbr_buts_adv
                        
                        
                        
                        
                    # CAS 2 : si je souhaite avoir les MOYENNES de buts / MATCH ==> je n'ai qu'à MOYENNER les buts de la série.
                        
                    elif bouton_unite == "moyenne / match" : 
                        
                        
                        nbr_buts_USDH = S_buts_USDH.mean()
                        nbr_buts_adv = S_buts_adv.mean()
                        
                        differentiel_nbr_buts = nbr_buts_USDH - nbr_buts_adv
                        
                        
                        
                    
                    # CAS 3 : si je souhaite avoir les MEDIANES de buts / MATCH ==> je n'ai qu'à calculer la MEDIANE des buts de la série.
                        
                    else :   # bouton_unite == "mediane" : 
                        
                        
                        nbr_buts_USDH = S_buts_USDH.median()
                        nbr_buts_adv = S_buts_adv.median()
                        
                        differentiel_nbr_buts = nbr_buts_USDH - nbr_buts_adv
                        
                        
                        
                        
                        
                    
                    
                    
                    # Ré-écriture de la différence de buts marqués :
                     
                    if differentiel_nbr_buts > 0 : 
                            
                        differentiel_nbr_buts = "+ " + str(np.round(differentiel_nbr_buts , 2)) + " buts marqués"
                        
                        
                        
                    elif differentiel_nbr_buts < 0 : 
                        
                        differentiel_nbr_buts = "- " + str(abs(np.round(differentiel_nbr_buts , 2))) + " buts marqués"
                        
                        
            


                        
                        
                    col3.metric(label = "" , 
                                value = np.round(nbr_buts_USDH , 2) ,
                                delta = differentiel_nbr_buts)
                
                
                    col6.metric(label = "" , 
                                value = np.round(nbr_buts_adv , 2))
                
                
                
                
                
                    for i in range(3) : 
                
                        st.write("")
                        
                        
                        
                        
                        
                
                
                
                
                
                
                
                
                
                # HISTOGRAMME de la répartition des buts inscrits par les 2 équipes par tranche de x minutes : 
                                
                # Création d'un bouton pour le choix du nombre de tranches des 60 minutes à créer : 
                    
                    
                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1])
                
                col4.write("Répartition des buts par tranches de x minutes :")
                
                
                bouton_choix_graphe = col6.selectbox("Type de graphique :" , 
                                                      [" " , 
                                                       "répartition des buts par période" , 
                                                       "différentiel de buts par période"])
                
                
                
                
                for i in range(3) : 
                    
                    st.write("")
                    
                    
                    
                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1]) 
                
                

                
                
                # SI un choix de graphique a été fait : 
                
                if bouton_choix_graphe != " " :
                    
                    

                    
                    # Ajout d'un bouton pour le choix du nombre tranches des 60 minutes à découper :
                    
                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1])
                    
                    
                    bouton_tranches = col6.selectbox("Découper les 60 minutes de match par périodes de ..... minutes :" , 
                                                     [" " , 1 , 2 , 4 , 5 , 6 , 10 , 12 , 15 , 20])
                    
                    
                    
                    for i in range(5) : 
                        
                        st.write("")
                        
                        
                        
                        
                        
                    if bouton_tranches != " " :
                        
                        
                        
                        fig , ax = plt.subplots(figsize = (16,6.5))
                        
                        
                        
                        # SI l'utilisateur souhaite regarder la répartition des buts par tranches :
                            
                        if bouton_choix_graphe == "répartition des buts par période" :
                                
                                

                                
                            double_vertical_histogram_type_action_saison(fig = fig , 
                                                                         ax = ax , 
                                                                         data = df , 
                                                                         type_action = ["but" , "but 7m"] , 
                                                                         nbr_tranches = 60//bouton_tranches ,
                                                                         text_color = "white" , 
                                                                         unite = bouton_unite)
                            
                            
                            
                            
                            
                        else :   # bouton_choix_graphe == "différentiel de buts par période"
                        
                        
                            histogram_differentiel_type_action_saison(fig = fig , 
                                                                      ax = ax , 
                                                                      data = df , 
                                                                      type_action = ["but" , "but 7m"] , 
                                                                      nbr_tranches = 60//bouton_tranches , 
                                                                      text_color = "white" , 
                                                                      unite = bouton_unite)
                            
                        
                        
                        
                        
                        
                        
                        
                        st.write(fig)
                        
                        
                        
                        
                
                
                
                        for i in range(10) : 
                            
                            st.write("")
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                        # Graphique en CAMEMBERT du temps passé devant / derrière au score par l'USDH depuis le début de la saison (match entier, M1 et M2) : 
                                    
                                    
                        col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1])
                        
                        
                        col4.write("Temps passé par l'USDH dans chaque situation au score possible :")
                        
                                    
                                
                        # On récupère le temps passé par l'USDH à mener / être mené / égalité depuis le début de saison :
                            
                            
                        # CAS 1 : si je souhaite avoir le temps TOTAL :
                            
                        if bouton_unite == "total" : 
                    
                            temps_USDH_devant = S_durees_situation_score_saison(data = df , equipe = "USDH" , situation = "mène").sum()
                            temps_USDH_derriere = S_durees_situation_score_saison(data = df , equipe = "USDH" , situation = "est mené").sum()
                            temps_USDH_egalite = S_durees_situation_score_saison(data = df , equipe = "USDH" , situation = "égalité").sum()
                            
                            
                        
                        # CAS 2 : si je souhaite avoir le temps MOYEN / MATCH :
                            
                        elif bouton_unite == "moyenne / match" : 
                    
                            temps_USDH_devant = S_durees_situation_score_saison(data = df , equipe = "USDH" , situation = "mène").mean()
                            temps_USDH_derriere = S_durees_situation_score_saison(data = df , equipe = "USDH" , situation = "est mené").mean()
                            temps_USDH_egalite = S_durees_situation_score_saison(data = df , equipe = "USDH" , situation = "égalité").mean()
                            
                            
                            
                            
                        
                        
                        
                        
                        # Construction du camembert PLOTLY associé : 
                            
                            
                        fig = px.pie(values = [temps_USDH_devant , temps_USDH_derriere , temps_USDH_egalite] , 
                                     names = ["USDH devant" , "USDH derrière" , "égalité"] , 
                                     color_discrete_sequence = px.colors.sequential.RdBu , 
                                     hole = 1/5)  
                        
                        
                        
                        fig.update_layout(width = 1250 , 
                                          height = 600)
                        
                        
                        
                        
                        
                        col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([0.25,0.25,2,1,1,1,1])
                        
                        col3.write(fig)
                        
                        
                        
                        
                        
                        for i in range(3) : 
                            
                            st.write("")
                            
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        # Diagramme en barres du nombre de buts inscrits par joueur de l'USDH depuis le début de la saison :
                           
                            
                        col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1])
                        
                        col4.write("Nombre de buts inscrits par joueur de l'USDH :")
                        
                        
                        for i in range(2) : 
                            
                            st.write("")
                        
                        
                            
                        # On commence par récupérer la série du nombre de buts inscrits par joueur de l'USDH cette saison :
                        
                        # CAS 1 : on souhaite regarder le nombre de buts TOTAL de chaque joueur :
                        
                        if bouton_unite == "total" :
                            
                            S_buts_par_joueur_USDH_saison = df[(df["équipe"] == "USDH") & (df["action"].isin(["but" , "but 7m"]))]["joueur"].value_counts()
                        
                        
                        
                            # On créer un diagramme en barres plotly à partir de cette Series : 
                            
                            
                            fig = px.bar(x = S_buts_par_joueur_USDH_saison.index , 
                                         y = S_buts_par_joueur_USDH_saison , 
                                         color = S_buts_par_joueur_USDH_saison , 
                                         text = S_buts_par_joueur_USDH_saison)
        
        
            
            
                            
                                
                                
                                
                            # Personnalisation de la figure : 
                                
                            fig.update_layout(xaxis_title = "joueur USDH" , 
                                              yaxis_title = "buts marqués" , 
                                              template = "plotly_dark" , 
                                              width = 1350 , 
                                              height = 700)
                        
                        
                            fig.update_yaxes(range = [0 , S_buts_par_joueur_USDH_saison.max() + 1])
                        
                        
                            
                            fig.update_traces(textposition = "outside" , 
                                              textfont = {"size" : 16 , 
                                                          "color" : "red"})
                            
                            
                            
                            fig.update(layout_coloraxis_showscale = False)   # Pour masquer la barre de couleur
                            
                            
                            
                            
                              
                            st.write(fig)
                        
                        
                        
                        
                        
                        
                        # CAS 2 : on souhaite regarder le nombre de buts MOYEN / MATCH de chaque joueur :
                        
                        else :   # bouton_unite == "moyenne / match"
                        
                            L_buts_par_joueur_USDH_saison = []
                            
                            L_matchs_par_joueur_USDH_saison = []
                            
                            L_joueurs_USDH_scoreurs = list(df[(df["équipe"] == "USDH") & (df["action"].isin(["but" , "but 7m"]))]["joueur"].unique())  # la liste des joueurs de l'USDH 
                        
                            
                            # Pour chaque scoreur de l'USDH :
                                
                            for joueur in L_joueurs_USDH_scoreurs :
                                
                                nbr_matchs_joues = 0
                                nbr_buts_marques = 0
                                
                                
                                # Pour chaque journée de championnat déjà jouée par l'USDH :
                                    
                                for journee in dico_rencontres_USDH.keys() : 
                                    
                                    
                                    # SI le scoreur de l'USDH a joué lors de cette journée :
                                        
                                    if joueur in df[(df["journée"] == journee) & (df["équipe"] == "USDH")]["joueur"].unique() :
                                        
                                        
                                        nbr_matchs_joues += 1
                                        
                                        nbr_buts_inscrits_journee = len(df[(df["journée"] == journee) & (df["joueur"] == joueur) & (df["action"].isin(["but" , "but 7m"]))])
                        
                                        nbr_buts_marques += nbr_buts_inscrits_journee
                                        
                                        
                                
                                # SI le joueur a joué AU MOINS 1 MATCH cette saison :
                                    
                                if nbr_matchs_joues > 0 :
                                    
                                    L_buts_par_joueur_USDH_saison.append(np.round(nbr_buts_marques / nbr_matchs_joues , 2))
                                    
                                    L_matchs_par_joueur_USDH_saison.append(nbr_matchs_joues)
                                    
                                
                                
                                    
                                    
                                    
                                    
                                    
                               
                                    
                                    
                                
                                
                                
                            S_buts_par_joueur_USDH_saison = pd.Series(L_buts_par_joueur_USDH_saison , 
                                                                      index = L_joueurs_USDH_scoreurs)
                            
                        
                        
             
                        
                            df_stats_joueurs_USDH = pd.DataFrame(data = list(S_buts_par_joueur_USDH_saison.index) ,
                                                                 columns = ["joueur"])
                            
                            
                            
                            df_stats_joueurs_USDH["buts marqués"] = list(S_buts_par_joueur_USDH_saison)
                            
                            
                            df_stats_joueurs_USDH["matchs joués"] = L_matchs_par_joueur_USDH_saison
                            
                            
                            df_stats_joueurs_USDH = df_stats_joueurs_USDH.sort_values(by = "buts marqués" , 
                                                                                      ascending = False)
                            
                            
                            
                            
                            
                            
                        
                        
                        
                        
                            # On créer un diagramme en barres plotly à partir de cette Series : 
                                
                                
                            fig = px.bar(x = df_stats_joueurs_USDH["joueur"] , 
                                         y = df_stats_joueurs_USDH["buts marqués"] , 
                                         color = df_stats_joueurs_USDH["buts marqués"] , 
                                         text = df_stats_joueurs_USDH["buts marqués"])
        
        
            
            
                            
                                
                                
                                
                            # Personnalisation de la figure : 
                                
                            fig.update_layout(xaxis_title = "joueur USDH" , 
                                              yaxis_title = "buts marqués" , 
                                              template = "plotly_dark" , 
                                              width = 1450 , 
                                              height = 700)
                        
                        
                            fig.update_yaxes(range = [0 , df_stats_joueurs_USDH["buts marqués"].max() + 1])
                        
                        
                            
                            fig.update_traces(textposition = "outside" , 
                                              textfont = {"size" : 16 , 
                                                          "color" : "red"})
                            
                            
                            
                            fig.update(layout_coloraxis_showscale = False)   # Pour masquer la barre de couleur
                            
                            
                            
         
        
                            st.write(fig)
                            
                            
                            
                            
                            

                            
                        for i in range(10) : 
                            
                            st.write("")
                            
                            
                            
                        st.write("-------------------------------------------------------------------------------------")
                    
        
        
        
        
        
        
                    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                        # PARTIE 2 : métriques / graphiques de bilan de saison liés à la SITUATION NUMERIQUE :
                        
                        
                        st.markdown("<h1 style='text-align: center; color: white;'>Statistiques liées à la situation numérique.</h1>",
                                    unsafe_allow_html = True)  
                        
                        
                        st.write("-------------------------------------------------------------------------------------")
                        
                    
                    
                    
                    
                        for i in range(3) : 
                            
                            st.write("")
            
            









                        # Affichage de la DROITE GRAPHIQUE représentant les périodes de supériorité / égalité / infériorité numérique de l'USDH LORS DU MATCH VOULU : 
                            
                        col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                            
                        
                        col4.write("Découpage des 60 minutes de match selon la situation numérique de l'USDH :")
                        
                        
                        
                        # Création d'un bouton pour le choix du (des) match(s) dont on souhaite voir la droite des périodes d'infériorité / supériorité / égalité numérique :
                            
                        bouton_journee = col6.selectbox("Choisissez le(s) match(s) qui vous intéresse(nt) :" , 
                                                       [" "] + list(dico_rencontres_USDH.keys()) + ["tous"])
                        
                        
                        
                        for i in range(5) : 
                            
                            st.write("")
                            
                            
                            
                        if bouton_journee != " " :
                            
                            
                            if bouton_journee != "tous" :
                        
                            
                                fig , ax = plt.subplots(figsize = (16,6))
        
        
                                droite_sup_inf_numeriques_equipe(fig , ax , data = df , journee = bouton_journee , 
                                                                 equipe = "USDH" , 
                                                                 afficher_scores = True , 
                                                                 afficher_differentiels = True ,
                                                                 afficher_bilan = True , 
                                                                 show_title = True , 
                                                                 text_color = "white")
                                
                                
                                
                                st.write(fig)
                                
                                
                                
                                
                                for i in range(8) : 
                                    
                                    st.write("")
                                
                                
                                
                                
                                
                                
                            else : 
                                
                                
                                for journee in dico_rencontres_USDH.keys() : 
                                    
                                    
                                    fig , ax = plt.subplots(figsize = (16,6))
        
        
                                    droite_sup_inf_numeriques_equipe(fig , ax , data = df , 
                                                                     journee = journee , 
                                                                     equipe = "USDH" , 
                                                                     afficher_scores = True , 
                                                                     afficher_differentiels = True ,
                                                                     afficher_bilan = True , 
                                                                     show_title = True , 
                                                                     text_color = "white")
                                    
                                    


                                    st.write(fig)
                        
                        
                                    for i in range(10) : 
                                        
                                        st.write("")
                        
                        
                        
                        
                        
                        
                            for i in range(5) : 
                                
                                st.write("")
                                
                                
                                
                                
                                
                                
                                
                            
                            
                            
                            
                            
                            
                            
                            
                            
                                    

                                
                                
                                
                                
                            # Métriques n°1-2 : nombre de cartons JAUNES + nombre de 2MINS reçus par l'USDH et par ses adversaires : 
                            
                                
                            for punition in ["cartons jaunes" , "exclusions"] :    
                                
                        
                                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                            
                            
                            
                                if punition == "cartons jaunes" : 
                                
                                    col4.write(f"Nombre de {punition} reçus ({bouton_unite}) :")
                                    
                                else : 
                                    
                                    col4.write(f"Nombre d'{punition} reçues ({bouton_unite}) :")
                                
                                
                                
                                
                                for i in range(2) : 
                            
                                    st.write("")
                                    
                                    
                                    
                                    
                                # On récupère le nombre de punitions de ce type reçues par l'USDH et par ses adversaires tout au long de la saison :
                                
                                # CAS 1 : on souhaite afficher le nombre TOTAL de punitions des 2 équipes :
                                
                                if bouton_unite == "total" :
                                
                                    nbr_punitions_USDH = S_nbr_type_action_saison(data = df , type_action = punition , 
                                                                                  equipe = "USDH" , periode = "match").sum()
                                    
                                    nbr_punitions_adv = S_nbr_type_action_saison(data = df , type_action = punition , 
                                                                                 equipe = "adversaire" , periode = "match").sum()
                                    
                                    
                                    
                                    
                                else :  # bouton_unite == "moyenne / match"
                                            
                                    nbr_punitions_USDH = S_nbr_type_action_saison(data = df , type_action = punition , 
                                                                                  equipe = "USDH" , periode = "match").mean()
                                    
                                    nbr_punitions_adv = S_nbr_type_action_saison(data = df , type_action = punition , 
                                                                                 equipe = "adversaire" , periode = "match").mean()
                                    
                                    
                                    
                                    
                                
                                # Calcul du différentiel entre les punitions reçues par l'USDH, et celles reçues par ses adversaires : 
                                    
                                differentiel_punitions = nbr_punitions_USDH - nbr_punitions_adv
                                
                                
                                # Gestion de l'affichage du différentiel suivant son signe : 
                                    
                                if differentiel_punitions > 0 :
                                    
                                    differentiel_punitions = "+ " + str(np.round(differentiel_punitions , 2))
                                    
                                    
                                    
                                elif differentiel_punitions == 0 : 
                                    
                                    differentiel_punitions = str(differentiel_punitions)
                                    
                                    
                                    
                                else : 
                                    
                                    differentiel_punitions = "- " + str(abs(np.round(differentiel_punitions , 2)))
                                    
                                
                                
                                
                                
                                    
                                col3.metric(label = "" , 
                                            value = np.round(nbr_punitions_USDH , 2) ,
                                            delta = differentiel_punitions , 
                                            delta_color = "inverse")
                            
                            
                                col6.metric(label = "" , 
                                            value = np.round(nbr_punitions_adv , 2))
                            
                            
                            
                            
                            
                                for i in range(3) : 
                            
                                    st.write("")
                                            
                                                
                                
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            # Double histogramme de la répartition des 2mins reçus par tranches de x minutes : 
                            
                            
                            # Ajout d'un bouton pour le choix du nombre tranches des 60 minutes à découper :
                                
                    
                            col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1.5,1.15,2.3,1])
                            
                            col4.write("Répartition des 2mins reçus par période :")
                            
                            
                            bouton_tranches_bis = col6.selectbox("Découper les 60 minutes du match par périodes de ..... minutes :" , 
                                                                 [" " , 4 , 5 , 6 , 10 , 12 , 15 , 20])
                            
                            
                            
                            for i in range(5) : 
                                
                                st.write("")
                                
                                
                                
                                
                                
                            if bouton_tranches_bis != " " :
                                
                                
                                
                                fig , ax = plt.subplots(figsize = (16,6.5))
                                

                                double_vertical_histogram_type_action_saison(fig = fig , 
                                                                             ax = ax , 
                                                                             data = df , 
                                                                             type_action = ["2min"] , 
                                                                             nbr_tranches = 60//bouton_tranches_bis ,
                                                                             text_color = "white" , 
                                                                             unite = bouton_unite)
                                
                                
                                
                                st.write(fig)
                                
                                
                                
                                
                                
                                for i in range(6) : 
                                    
                                    st.write("")
                                
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                                # Affichage du diagramme en barres des 2mins reçus par joueur de l'USDH :
                            
                                col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                            
                                
                                col4.write("Répartition des 2mins reçus par joueur de l'USDH :")
                                
                                
                                for i in range(2) : 
                            
                                    st.write("")
                                
                                
                                    
                                # On commence par récupérer la série du nombre de 2mins reçus par joueur de l'USDH cette saison :
                                
                                # CAS 1 : on souhaite regarder le nombre de 2mins TOTAL de chaque joueur :
                                
                                if bouton_unite == "total" :
                                    
                                    S_2mins_par_joueur_USDH_saison = df[(df["équipe"] == "USDH") & (df["action"] == "2min")]["joueur"].value_counts()
                                
                                
                                
                                    # On créer un diagramme en barres plotly à partir de cette Series : 
                                    
                                    
                                    fig = px.bar(x = S_2mins_par_joueur_USDH_saison.index , 
                                                 y = S_2mins_par_joueur_USDH_saison , 
                                                 color = S_2mins_par_joueur_USDH_saison , 
                                                 text = S_2mins_par_joueur_USDH_saison)
                
                
                    
                    
                                    
                                        
                                        
                                        
                                    # Personnalisation de la figure : 
                                        
                                    fig.update_layout(xaxis_title = "joueur USDH" , 
                                                      yaxis_title = "2mins reçus" , 
                                                      template = "plotly_dark" , 
                                                      width = 1450 , 
                                                      height = 700)
                                
                                
                                    fig.update_yaxes(range = [0 , S_2mins_par_joueur_USDH_saison.max() + 1])
                                
                                
                                    
                                    fig.update_traces(textposition = "outside" , 
                                                      textfont = {"size" : 16 , 
                                                                  "color" : "red"})
                                    
                                    
                                    
                                    fig.update(layout_coloraxis_showscale = False)   # Pour masquer la barre de couleur
                                    
                                    
                                    
                                    
                                    
                                    st.write(fig)
                                    
                                    
                                    
                                    for i in range(3) : 
                                        
                                        st.write("")
                            
                            
                            
                            
                            
                            
                                # CAS 2 : on souhaite regarder le nombre de 2mins reçus MOYEN / MATCH de chaque joueur :
                                
                                else :   # bouton_unite == "moyenne / match"
                                
                                    L_2mins_par_joueur_USDH_saison = []
                                    
                                    L_matchs_par_joueur_USDH_saison = []
                                    
                                    L_joueurs_USDH_expulses = list(df[(df["équipe"] == "USDH") & (df["action"] == "2min")]["joueur"].unique())  # la liste des joueurs de l'USDH ayant été expulsés au moins 1 fois
                                
                                    
                                    # Pour chaque scoreur de l'USDH :
                                        
                                    for joueur in L_joueurs_USDH_expulses :
                                        
                                        nbr_matchs_joues = 0
                                        nbr_2min_recus = 0
                                        
                                        
                                        # Pour chaque journée de championnat déjà jouée par l'USDH :
                                            
                                        for journee in dico_rencontres_USDH.keys() : 
                                            
                                            
                                            # SI le joueur expulsé de l'USDH a joué lors de cette journée :
                                                
                                            if joueur in df[(df["journée"] == journee) & (df["équipe"] == "USDH")]["joueur"].unique() :
                                                
                                                
                                                nbr_matchs_joues += 1
                                                
                                                nbr_2min_recus_journee = len(df[(df["journée"] == journee) & (df["joueur"] == joueur) & (df["action"] == "2min")])
                                
                                                nbr_2min_recus += nbr_2min_recus_journee
                                                
                                                
                                        
                                        # SI le joueur a joué AU MOINS 1 MATCH cette saison :
                                            
                                        if nbr_matchs_joues > 0 :
                                            
                                            L_2mins_par_joueur_USDH_saison.append(np.round(nbr_2min_recus / nbr_matchs_joues , 2))
                                            
                                            L_matchs_par_joueur_USDH_saison.append(nbr_matchs_joues)
                                            
                                        
                                        
                                            
                                            
                                           
                                            
                                            
                                       
                                            
                                            
                                        
                                        
                                        
                                    S_2min_par_joueur_USDH_saison = pd.Series(L_2mins_par_joueur_USDH_saison , 
                                                                              index = L_joueurs_USDH_expulses)
                                    
                                
                                
                     
                                
                                    df_stats_joueurs_USDH = pd.DataFrame(data = list(S_2min_par_joueur_USDH_saison.index) ,
                                                                         columns = ["joueur"])
                                    
                                    
                                    
                                    df_stats_joueurs_USDH["2mins reçus"] = list(S_2min_par_joueur_USDH_saison)
                                    
                                    
                                    df_stats_joueurs_USDH["matchs joués"] = L_matchs_par_joueur_USDH_saison
                                    
                                    
                                    df_stats_joueurs_USDH = df_stats_joueurs_USDH.sort_values(by = "2mins reçus" , 
                                                                                              ascending = False)
                                    
                                    
                                    
                                    
                                    
                                    
                                
                                
                                
                                
                                    # On créer un diagramme en barres plotly à partir de cette Series : 
                                        
                                        
                                    fig = px.bar(x = df_stats_joueurs_USDH["joueur"] , 
                                                 y = df_stats_joueurs_USDH["2mins reçus"] , 
                                                 color = df_stats_joueurs_USDH["2mins reçus"] , 
                                                 text = df_stats_joueurs_USDH["2mins reçus"])
                
                
                    
                    
                                    
                                        
                                        
                                        
                                    # Personnalisation de la figure : 
                                        
                                    fig.update_layout(xaxis_title = "joueur USDH" , 
                                                      yaxis_title = "2mins reçus" , 
                                                      template = "plotly_dark" , 
                                                      width = 1450 , 
                                                      height = 700)
                                
                                
                                    fig.update_yaxes(range = [0 , df_stats_joueurs_USDH["2mins reçus"].max() + 1])
                                
                                
                                    
                                    fig.update_traces(textposition = "outside" , 
                                                      textfont = {"size" : 16 , 
                                                                  "color" : "red"})
                                    
                                    
                                    
                                    fig.update(layout_coloraxis_showscale = False)   # Pour masquer la barre de couleur
                                    
                                    


                                    
                                    
                                    st.write(fig)
                                    
                                    
                                    
                                    
                                    
                                    for i in range(3) : 
                                        
                                        st.write("")
                                        
                                        
                                        
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                # Analyse des périodes de SUPERIORITE / INFERIORITE NUMERIQUE de chaque équipe :
                                    
                                
                                for situation_numerique in ["supériorité numérique" , "infériorité numérique"] :
                                    
                                    
                                    
                                    st.write("------------------------------------------------------------------------")
                                        
                                        
                                        
                                    if situation_numerique == "supériorité numérique" : 
                                        
                                        st.markdown(f"<h1 style='text-align: center; color: white;'>Périodes de {situation_numerique} de l'USDH.</h1>",
                                                         unsafe_allow_html = True)   
                                        
                                        
                                        
                                    else :    # situation_numerique == "infériorité numérique" : 
                                        
                                        st.markdown(f"<h1 style='text-align: center; color: white;'>Pérodes d'{situation_numerique} de l'USDH.</h1>",
                                                         unsafe_allow_html = True)   
                                        
                                        
                                        
                                    
                                    
                                    
                                    for i in range(5) : 
                                        
                                        st.write("")
                                        
                                        
                                        
                                    
                                    
                                    
                                    
                                    
                                    # Métriques n°3 + 9 : Nombre de périodes jouées en 'situation_numerique' par les 2 équipes :
                                    
    
                                
                                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                                
                                
                                    col4.write(f"Nombre de fois où l'équipe s'est retrouvée en {situation_numerique} ({bouton_unite}) :")
                                    
                                    
                                    
                                    
                                        
                                    # On récupère le nombre de périodes jouées en 'situation_numerique' par l'USDH et par ses adversaires tout au long de la saison :
                                    
                                    L_nbr_periodes_situation_numerique_USDH = []  # la liste du nbr de périodes que l'USDH a joué en situation_numerique lors de chaque match disputé
                                    L_nbr_periodes_situation_numerique_adv = []   # la liste du nbr de périodes que l'adversaire de l'USDH a joué en situation_numerique lors de chaque match disputé
                                        
                                    
                                    # Pour chaque journée de championnat disputée :
                                        
                                    for journee in dico_rencontres_USDH.keys() : 
                                        
                                        if journee != 'J11' :
                                        
                                            equipe_dom = df[df["journée"] == journee]["domicile"].unique()
                                            equipe_dom = equipe_dom[0]  # nom de l'équipe jouant à domicile

                                            equipe_ext = df[df["journée"] == journee]["extérieur"].unique()
                                            equipe_ext = equipe_ext[0]  # nom de l'équipe jouant à l'extérieur



                                            # CAS 1 : si l'équipe jouant à domicile est l'USDH = celle jouant à l'extérieur est son adversaire :

                                            if equipe_dom == "USDH" : 

                                                if situation_numerique == "supériorité numérique" : 

                                                    nbr_periodes_situation_numerique_USDH_journee = nbr_periodes_superiorite(data = df , journee = journee , equipe = "domicile")
                                                    nbr_periodes_situation_numerique_adv_journee = nbr_periodes_superiorite(data = df , journee = journee , equipe = "extérieur")



                                                else :   # situation_numerique == "infériorité numérique"


                                                    nbr_periodes_situation_numerique_USDH_journee = nbr_periodes_superiorite(data = df , journee = journee , equipe = "extérieur")
                                                    nbr_periodes_situation_numerique_adv_journee = nbr_periodes_superiorite(data = df , journee = journee , equipe = "domicile")






                                            # CAS 2 : si l'équipe jouant à l'extérieur st l'USDH = celle jouant à domicile est son adversaire :

                                            else :   # equipe_ext == "USDH" : 


                                                if situation_numerique == "supériorité numérique" : 


                                                    nbr_periodes_situation_numerique_USDH_journee = nbr_periodes_superiorite(data = df , journee = journee , equipe = "extérieur")
                                                    nbr_periodes_situation_numerique_adv_journee = nbr_periodes_superiorite(data = df , journee = journee , equipe = "domicile")


                                                else :   # situation_numerique == "infériorité numérique"


                                                    nbr_periodes_situation_numerique_USDH_journee = nbr_periodes_superiorite(data = df , journee = journee , equipe = "domicile")
                                                    nbr_periodes_situation_numerique_adv_journee = nbr_periodes_superiorite(data = df , journee = journee , equipe = "extérieur")

                                            
                                            
                                            
                                            
                                            
                                            
                                        
                                        # On ajoute le nombre de périodes des équipes respectives à la liste qui leur est dédiée : 
                                            
                                        L_nbr_periodes_situation_numerique_USDH.append(nbr_periodes_situation_numerique_USDH_journee)
                                        L_nbr_periodes_situation_numerique_adv.append(nbr_periodes_situation_numerique_adv_journee)
                                        
                                        
                                        
                                        
                                    # On utilise ces 2 listes pour créer 2 Series : 
                                        
                                    S_nbr_periodes_situation_numerique_USDH = pd.Series(L_nbr_periodes_situation_numerique_USDH)
                                    S_nbr_periodes_situation_numerique_adv = pd.Series(L_nbr_periodes_situation_numerique_adv)      
                                        
                                        
                                    
                                    
                                    
                                    # CAS 1 : on souhaite afficher le nombre TOTAL de périodes jouées en 'situation_numerique' des 2 équipes :
                                    
                                    if bouton_unite == "total" :
                                    
                                        nbr_periodes_situation_numerique_USDH = S_nbr_periodes_situation_numerique_USDH.sum()
                                        
                                        nbr_periodes_situation_numerique_adv = S_nbr_periodes_situation_numerique_adv.sum()
                                        
                                        
                                        
                                        
                                    else :  # bouton_unite == "moyenne / match"
                                                
                                        nbr_periodes_situation_numerique_USDH = S_nbr_periodes_situation_numerique_USDH.mean()
                                        
                                        nbr_periodes_situation_numerique_adv = S_nbr_periodes_situation_numerique_adv.mean()
                                        
                                        
                                        
                                        
                                    
                                    # Calcul du différentiel de périodes jouées en 'situation_numerique' par les 2 équipes : 
                                        
                                    differentiel_periodes_situation_numerique = nbr_periodes_situation_numerique_USDH - nbr_periodes_situation_numerique_adv
                                    
                                    
                                    # Gestion de l'affichage du différentiel suivant son signe : 
                                        
                                    if differentiel_periodes_situation_numerique > 0 :
                                        
                                        differentiel_periodes_situation_numerique = "+ " + str(np.round(differentiel_periodes_situation_numerique , 2)) + " périodes"
                                        
                                        
                                        
                                    elif differentiel_periodes_situation_numerique == 0 : 
                                        
                                        differentiel_periodes_situation_numerique = str(differentiel_periodes_situation_numerique) + " périodes"
                                        
                                        
                                        
                                    else : 
                                        
                                        differentiel_periodes_situation_numerique = "- " + str(abs(np.round(differentiel_periodes_situation_numerique , 2))) + " périodes"
                                        
                                    
                                    
                                    
                                    
                                        
                                    col3.metric(label = "" , 
                                                value = np.round(nbr_periodes_situation_numerique_USDH , 2) ,
                                                delta = differentiel_periodes_situation_numerique)
                                
                                
                                    col6.metric(label = "" , 
                                                value = np.round(nbr_periodes_situation_numerique_adv , 2))
                                
                                
                                
                                
                                
                                    for i in range(3) : 
                                
                                        st.write("")
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    # Métrique n°4 + 10 : temps passé en 'situation_numerique' par les 2 équipes :
                                    
    
                                
                                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                                
                                
                                    col4.write(f"Temps durant lequel l'équipe a joué en {situation_numerique} ({bouton_unite}, en minutes) :")
                                    
                                    
                                    
                                    
                                        
                                    # On récupère le temps passé en 'situation_numerique' par l'USDH et par ses adversaires tout au long de la saison :
                                    
                                    # CAS 1 : on souhaite afficher le temps TOTAL en 'situation_numerique' des 2 équipes :
                                    
                                    if bouton_unite == "total" :
                                    
                                        temps_situation_numerique_USDH = S_durees_situation_numerique_saison(data = df , equipe = "USDH" , 
                                                                                                             situation = situation_numerique).sum()
                                        
                                        temps_situation_numerique_adv = S_durees_situation_numerique_saison(data = df , equipe = "adversaire" , 
                                                                                                            situation = situation_numerique).sum()
                                        
                                        
                                        
                                        
                                    else :  # bouton_unite == "moyenne / match"
                                                
                                        temps_situation_numerique_USDH = S_durees_situation_numerique_saison(data = df , equipe = "USDH" , 
                                                                                                             situation = situation_numerique).mean()
                                        
                                        temps_situation_numerique_adv = S_durees_situation_numerique_saison(data = df , equipe = "adversaire" , 
                                                                                                            situation = situation_numerique).mean()
                                        
                                        
                                        
                                        
                                    
                                    # Calcul du différentiel de temps passé en 'situation_numerique' par les 2 équipes : 
                                        
                                    differentiel_temps_situation_numerique = temps_situation_numerique_USDH - temps_situation_numerique_adv
                                    
                                    
                                    # Gestion de l'affichage du différentiel suivant son signe : 
                                        
                                    if differentiel_temps_situation_numerique > 0 :
                                        
                                        differentiel_temps_situation_numerique = "+ " + str(np.round(differentiel_temps_situation_numerique , 2)) + " minutes"
                                        
                                        
                                        
                                    elif differentiel_temps_situation_numerique == 0 : 
                                        
                                        differentiel_temps_situation_numerique = str(differentiel_temps_situation_numerique) + " minutes"
                                        
                                        
                                        
                                    else : 
                                        
                                        differentiel_temps_situation_numerique = "- " + str(abs(np.round(differentiel_temps_situation_numerique , 2))) + " minutes"
                                        
                                    
                                    
                                    
                                    
                                        
                                    col3.metric(label = "" , 
                                                value = np.round(temps_situation_numerique_USDH , 2) ,
                                                delta = differentiel_temps_situation_numerique)
                                
                                
                                    col6.metric(label = "" , 
                                                value = np.round(temps_situation_numerique_adv , 2))
                                
                                
                                
                                
                                
                                
                                
                                    for i in range(7) : 
                                
                                        st.write("")
                                        
                                        
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    # Métrique n°5-6-7 + 11-12-13 : Affichage du BILAN de l'USDH sur SES PROPRES PERIODES de 'situation_numerique' : 
                                
                                
                                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,3.15,3.15,2.5,1.15,1,4])
                                            
                                    col4.write(f"BILAN DE l'USDH LORSQU'IL JOUE EN {situation_numerique.upper()} :") 
                                    
                                    
                                    
                                    for i in range(3) : 
                                        
                                        st.write("")
                                    
                                    
                                    
                                    
                                    
                                    
                                    # Création d'un bouton pour le choix de l'unité des buts marqués / encaissés / différentiels sur les supériorités numériques : 
                                     
                                        
                                    bouton_unite_bilan_situation_numerique = col7.selectbox("Bilan exprimé en :" , 
                                                                                            [" " , 
                                                                                             "total" , 
                                                                                             f"/ minute jouée par l'USDH en {situation_numerique.split(sep = ' ')[0]}" , 
                                                                                             f"/ période jouée par l'USDH en {situation_numerique.split(sep = ' ')[0]}"])
                                    
                                    
                                    st.write("")
                                    st.write("")
                                    
                                    
                                    
                                    
                                    
                                    if bouton_unite_bilan_situation_numerique != " " :
                                        
                                        
                                        
                                        L_delta_colors = ["normal" , "inverse" , "normal"]
                                            
                                            
                                            
                                        
                                        for type_bilan , delta_color in zip(["buts marqués" , "buts encaissés" , "différentiel de buts"] , L_delta_colors) :
                                            
                                            
                                            col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                                
                                            
                                        
                                            
                                            
                                            # Récupération du bilan du type renseigné de l'équipe à domicile lorsqu'elle joue en 'situation_numerique', et idem pour l'équipe à l'extérieur :
                                             
                                            if bouton_unite_bilan_situation_numerique == "total" :
                                                
                                                
                                                
                                                # Bilan de l'USDH dans cette situation numérique : 
                                                    
                                                buts_type_situation_numerique_USDH = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                        equipe = "USDH" , 
                                                                                                                        situation = situation_numerique , 
                                                                                                                        type_bilan = type_bilan).sum()
                                             
                                                
                                                
                                                
                                                # Bilan de ses adversaires dans cette même situation numérique : lorsque l'USDH joue en supériorité (resp. en infériorité) ==> son adversaire joue quant à lui en infériorité (resp. en supériorité) : 
                                                
                                                
                                                if situation_numerique == "supériorité numérique" :
                                                    
                                                
                                                    buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                           equipe = "adversaire" , 
                                                                                                                           situation = "infériorité numérique" , 
                                                                                                                           type_bilan = type_bilan).sum()
                                                
                                                
                                                
                                                
                                                else :    # situation_numerique == "infériorité numérique"
                                                
                                                
                                                    buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                           equipe = "adversaire" , 
                                                                                                                           situation = "supériorité numérique" , 
                                                                                                                           type_bilan = type_bilan).sum()
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                unite = f" {type_bilan}"
                                                
                                                
                                                
                                                
                                                col4.write(f"{type_bilan} lorsque l'USDH joue en {situation_numerique} :") 
                                                    
                                                    
                                               
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                            elif bouton_unite_bilan_situation_numerique == f"/ minute jouée par l'USDH en {situation_numerique.split(sep = ' ')[0]}" :
                                                
                                                
                                                
                                                # Calcul du temps passé en 'situation_numerique' par l'USDH depuis le début de la saison (temps total) : 
                                                    
                                                temps_situation_numerique_USDH = S_durees_situation_numerique_saison(data = df , equipe = "USDH" , 
                                                                                                                     situation = situation_numerique).sum()
                                                

                                                
                                                
                                                
                                                
                                                # SI l'USDH A PASSE DU TEMPS EN 'situation_numerique' (pour éviter une division par 0) : 
                                                
                                                if temps_situation_numerique_USDH > 0 :
                                                    
                                                    
                                                    # Bilan USDH :
                                                    
                                                    buts_type_situation_numerique_USDH = S_bilan_situation_numerique_saison(data = df , equipe = "USDH" ,  situation = situation_numerique , type_bilan = type_bilan).sum() / temps_situation_numerique_USDH
                                                    
                                                    
                                                    
                                                    # Bilan adversaires : 
                                                        
                                                    if situation_numerique == "supériorité numérique" :
                                                        
                                                    
                                                        buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                               equipe = "adversaire" , 
                                                                                                                               situation = "infériorité numérique" , 
                                                                                                                               type_bilan = type_bilan).sum() / temps_situation_numerique_USDH
                                                    
                                                    
                                                    
                                                    
                                                    else :    # situation_numerique == "infériorité numérique"
                                                    
                                                    
                                                        buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                               equipe = "adversaire" , 
                                                                                                                               situation = "supériorité numérique" , 
                                                                                                                               type_bilan = type_bilan).sum() / temps_situation_numerique_USDH
                                                    
                                                        
                                                
                                                
                                                
                                                # SINON, si l'USDH a passé 0 seconde à jouer en supériorité cette saison :
                                                
                                                else : 
                                                    
                                                    
                                                    # Bilan USDH : 
                                                        
                                                    buts_type_situation_numerique_USDH = 0
                                                    
                                                    
                                                    
                                                    # Bilan adversaires : 
                                                    
                                                    buts_type_situation_numerique_adv = 0
                                                    
                                                    
                                                
                                                

                                                
                                                
                                                unite = f" {type_bilan} / min de l'USDH en {situation_numerique.split(sep = ' ')[0][0:4]}."
                                                
                                                
                                                col4.write(f"{type_bilan} / minute que l'USDH a joué en {situation_numerique} :") 
                                                    
                                                    
                                               
                                            
                                         
                                            
                                         
                                            
                                         
                                         
                                            elif bouton_unite_bilan_situation_numerique == f"/ période jouée par l'USDH en {situation_numerique.split(sep = ' ')[0]}" :
                                                
                                                
                                                
                                                # Calcul du nombre de périodes jouées en 'situation_numerique' par l'USDH depuis le début de la saison (temps total) : 
                                                    
                                                    
                                                nbr_periodes_situation_numerique_USDH = S_nbr_periodes_situation_numerique_USDH.sum()
                                        
                                                
                                                
                                                
                                                
                                                
                                                # SI l'USDH A JOUE EN 'situation_numerique' (pour éviter une division par 0) : 
                                                
                                                if nbr_periodes_situation_numerique_USDH > 0 :
                                                    
                                                    # Bilan USDH : 
                                                        
                                                    buts_type_situation_numerique_USDH = S_bilan_situation_numerique_saison(data = df , equipe = "USDH" ,  situation = situation_numerique , type_bilan = type_bilan).sum() / nbr_periodes_situation_numerique_USDH
                                                
                                                
                                                
                                                
                                                    # Bilan adversaires : 
                                                        
                                                    
                                                    if situation_numerique == "supériorité numérique" :
                                                        
                                                    
                                                        buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                               equipe = "adversaire" , 
                                                                                                                               situation = "infériorité numérique" , 
                                                                                                                               type_bilan = type_bilan).sum() / nbr_periodes_situation_numerique_USDH
                                                    
                                                    
                                                    
                                                    
                                                    else :    # situation_numerique == "infériorité numérique"
                                                    
                                                    
                                                        buts_type_situation_numerique_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                                               equipe = "adversaire" , 
                                                                                                                               situation = "supériorité numérique" , 
                                                                                                                               type_bilan = type_bilan).sum() / nbr_periodes_situation_numerique_USDH
                                                    
                                                        
                                                        
                                                        
                                                        
                                                        
                                                        
                                                
                                                # SINON, si l'USDH a passé 0 seconde à jouer en 'situation numerique' cette saison :
                                                
                                                else : 
                                                    
                                                    # Bilan USDH : 
                                                        
                                                    buts_type_situation_numerique_USDH = 0
                                                    
                                                    
                                                    
                                                    # Bilan adversaires :
                                                    
                                                    buts_type_situation_numerique_adv = 0
                                                    
                                                    
                                                

                                               
                                                
                                                
                                                
                                                unite = f" {type_bilan} / période jouée par l'USDH en {situation_numerique.split(sep = ' ')[0][0:4]}."
                                                
                                                
                                                if type_bilan in ["buts marqués" , "buts encaissés"] :
                                                
                                                    col4.write(f"{type_bilan} / période que l'USDH a joué en {situation_numerique.split(sep = ' ')[0][0:4]} :") 
                                                    
                                                    
                                                else : 
                                                    
                                                    col4.write("Différentiel de buts / période que l'USDH a joué en {situation_numerique.split(sep = ' ')[0][0:4]} :")
                                                
                                         
                                            
                                         
                                            
                                         
                                            
                                         
                                 
                                            # Calcul de la différence de bilan sur les 'situation_numerique' EN FAVEUR DE L'USDH : 
                                                    
                                                
                                            difference_type_buts_situation_numerique = np.round(buts_type_situation_numerique_USDH - buts_type_situation_numerique_adv , 2)
                                                
                                            
                                            
                                            
                                            # Ré-écriture de la différence bilan sur les 'situation_numerique' :
                                             
                                            if difference_type_buts_situation_numerique > 0 : 
                                                    
                                                difference_type_buts_situation_numerique = "+ " + str(difference_type_buts_situation_numerique) + unite
                                                
                                                
                                                
                                            elif difference_type_buts_situation_numerique < 0 : 
                                                
                                                difference_type_buts_situation_numerique = "- " + str(abs(difference_type_buts_situation_numerique)) + unite
                                                
                                                
                                                    
                                            
                                            
                                            
                                            # On écrit le delta de bilan en 'situation_numerique' sous l'USDH (à gauche) :
                                                
                                            col3.metric(label = "" , 
                                                        value = np.round(buts_type_situation_numerique_USDH , 2) ,
                                                        delta = str(difference_type_buts_situation_numerique) , 
                                                        delta_color = delta_color)
                                        
                                        
                                        
                                            col6.metric(label = "" , 
                                                        value = np.round(buts_type_situation_numerique_adv , 2) , 
                                                        delta = " ")
                                        
                                            
                                            
    
                                            
                                            
                                            for i in range(3) : 
                                                
                                                st.write("")
                                                
                                                
                                                
                                                
                                            
                                        
                                        for i in range(5) : 
                                            
                                            st.write("")
                                        
                                        
                                    
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                # Analyse des périodes d'EGALITE NUMERIQUE des 2 équipes : 
                                    
                                    
                                if bouton_unite_bilan_situation_numerique != " " :
                                 
                                
                            
                                    st.write("------------------------------------------------------------------------")
                                        
                                        
                                        
                                        
                                    st.markdown("<h1 style='text-align: center; color: white;'>Gestion des périodes d'égalité numérique.</h1>",
                                                     unsafe_allow_html = True)   
                                        
                                    
                                    
                                
                                
                                
                                    for i in range(5) : 
                                        
                                        st.write("")
                                        
                                        
                                        
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    # Métrique n°8 : temps passé à égalité numérique par les 2 équipes :
                                
    
                            
                                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                                
                                
                                    col4.write(f"Temps passé à égalité numérique ({bouton_unite}, en minutes) :")
                                    
                                    
                                    
                                    
                                        
                                    # On récupère le temps passé à égalité numérique par l'USDH et par ses adversaires tout au long de la saison :
                                    
                                    # CAS 1 : on souhaite afficher le temps TOTAL à égalité des 2 équipes :
                                    
                                    if bouton_unite == "total" :
                                    
                                        temps_egalite_num = S_durees_situation_numerique_saison(data = df , equipe = "USDH" , 
                                                                                                situation = "égalité numérique").sum()
                                        
                                       
                                        
                                        
                                        
                                    else :  # bouton_unite == "moyenne / match"
                                                
                                        temps_egalite_num = S_durees_situation_numerique_saison(data = df , equipe = "USDH" , 
                                                                                                situation = "égalité numérique").mean()
                                        
                                        
                                        
                                        
                                        
                                    
                                    
                                    
                                        
                                    col3.metric(label = "" , 
                                                value = np.round(temps_egalite_num , 2))
                                
                                
                                    col6.metric(label = "" , 
                                                value = np.round(temps_egalite_num , 2))
                                
                                
                                
                                
                                
                                
                                
                                    for i in range(7) : 
                                
                                        st.write("")
                                        
                                        
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    # Métrique n°9-10-11 : Affichage du BILAN de chaque équipe sur LES PERIODES (communes) d'EGALITE NUMERIQUE DES 2 EQUIPES : 
                                
    
                                    col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                                            
                                    col4.write("BILAN de l'équipe lorsqu'elle joue à égalité numérique :") 
                                    
                                    
                                    
                                    for i in range(3) : 
                                        
                                        st.write("")
                                    
                                    
                                    
                                    
                                    
                                    
                                    # Création d'un bouton pour le choix de l'unité des buts marqués / encaissés / différentiels sur les égalités numériques : 
                                     
                                   
                                    bouton_unite_bilan_ega = col6.selectbox("Bilan exprimé en :" , 
                                                                            [" " , 
                                                                             "total" , 
                                                                             "/ minute jouée à égalité num"])
    
                                        
                                    
                                    

                                    
                                    st.write("")
                                    st.write("")
                                    
                                    
                                    
                                    
                                    
                                    if bouton_unite_bilan_ega != " " :
                                        
                                        
                                        for type_bilan , delta_color in zip(["buts marqués" , "buts encaissés" , "différentiel de buts"] , ["normal" , "inverse" , "normal"]) :
                                            
                                            
                                            col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,2,1.15,2.3,1])
                                
                                            
                                        
                                            
                                            
                                            # Récupération du bilan du type renseigné de l'équipe à domicile lorsqu'elle joue à égalité numérique, et idem pour l'équipe à l'extérieur :
                                             
                                            if bouton_unite_bilan_ega == "total" :
                                                
                                                
                                                
                                                # Bilan de l'USDH : 
                                                    
                                                buts_type_a_ega_USDH = S_bilan_situation_numerique_saison(data = df , 
                                                                                                          equipe = "USDH" , 
                                                                                                          situation = "égalité numérique" , 
                                                                                                          type_bilan = type_bilan).sum()
                                             
                                                
                                                
                                                
                                                # Bilan de ses adversaires : 
                                                    
                                                buts_type_a_ega_adv = S_bilan_situation_numerique_saison(data = df , 
                                                                                                         equipe = "adversaire" , 
                                                                                                         situation = "égalité numérique" , 
                                                                                                         type_bilan = type_bilan).sum()
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                unite = f" {type_bilan}"
                                                
                                                
                                                
                                                
                                                col4.write(f"{type_bilan} sur les périodes d'égalité numérique :") 
                                                    
                                                    
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                            elif bouton_unite_bilan_ega == "/ minute jouée à égalité num" :
                                                
                                                
                                                
                                                # Calcul du temps passé à égalité numérique par les 2 équipes depuis le début de la saison (temps total) : 
                                                    
                                                temps_egalite_num = S_durees_situation_numerique_saison(data = df , equipe = "USDH" , 
                                                                                                        situation = "égalité numérique").sum()
                                                
                                                
                                                
                                                
                                                
                                                
                                                # SI les 2 équipes ONT JOUES A EGALITE NUMERIQUE cette saison (pour éviter une division par 0) : 
                                                
                                                if temps_egalite_num > 0 :
                                                    
                                                    buts_type_a_ega_USDH = S_bilan_situation_numerique_saison(data = df , equipe = "USDH" ,  situation = "égalité numérique" , type_bilan = type_bilan).sum() / temps_egalite_num
                                                    buts_type_a_ega_adv = S_bilan_situation_numerique_saison(data = df , equipe = "adversaire" ,  situation = "égalité numérique" , type_bilan = type_bilan).sum() / temps_egalite_num
                                                
                                                
                                                
                                                
                                                # SINON, si l'USDH a passé 0 seconde à jouer en supériorité cette saison :
                                                
                                                else : 
                                                    
                                                    buts_type_a_ega_USDH = 0
                                                    buts_type_a_ega_adv = 0
                                                    
                                                
                                                
                                                
                                                
    
                                                
                                                
                                                unite = f" {type_bilan} / min à égalité num."
                                                
                                                
                                                if type_bilan in ["buts marqués" , "buts encaissés"] :
                                                
                                                    col4.write(f"{type_bilan} / minute que l'équipe a joué à égalité numérique :") 
                                                    
                                                    
                                                else : 
                                                    
                                                    col4.write("Différentiel de buts / minute que l'équipe a joué à égalité numérique :")
                                                
                                                
                                         
                                            
    
                                 
                                            # Calcul de la différence de bilan sur les égalités numériques EN FAVEUR DE L'USDH : 
                                                    
                                                
                                            difference_type_buts_ega = np.round(buts_type_a_ega_USDH - buts_type_a_ega_adv , 2)
                                                
                                            
                                            
                                            # Ré-écriture de la différence bilan sur les égalités nums :
                                             
                                            if difference_type_buts_ega > 0 : 
                                                    
                                                difference_type_buts_ega = "+ " + str(difference_type_buts_ega) + unite
                                                
                                                
                                                
                                            elif difference_type_buts_ega < 0 : 
                                                
                                                difference_type_buts_ega = "- " + str(abs(difference_type_buts_ega)) + unite
                                                
                                                
                                                    
                                            
                                            
                                            
                                            # On écrit le delta de bilan en supériorité sous l'USDH (à gauche) :
                                                
                                            col3.metric(label = "" , 
                                                        value = np.round(buts_type_a_ega_USDH , 2) ,
                                                        delta = str(difference_type_buts_ega) , 
                                                        delta_color = delta_color)
                                        
                                        
                                        
                                            col6.metric(label = "" , 
                                                        value = np.round(buts_type_a_ega_adv , 2) , 
                                                        delta = " ")
                                        
                                            
                                            
    
                                            
                                            
                                            for i in range(3) : 
                                                
                                                st.write("")
                                                
                                                
                                                
                                                
                                            
                                        
                                        for i in range(5) : 
                                            
                                            st.write("")
                                        
                                        
                                    
                                    
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
    
                                
                                
                                        for i in range(10) : 
                            
                                            st.write("")
                                            
                                            
                                            
                                        st.write("-------------------------------------------------------------------------------------")
                                    
                        
                        
                        
                        
                        
                        
                                    
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                                        # PARTIE 3 : métriques / graphiques de bilan de saison liés à la DYNAMIQUE DE JEU :
                                        
                                        
                                        st.markdown("<h1 style='text-align: center; color: white;'>Statistiques liées à la dynamique de jeu dans les moments cruciaux.</h1>",
                                                    unsafe_allow_html = True)  
                                        
                                        
                                        st.write("-------------------------------------------------------------------------------------")
                                        
                                    
                                    
                                    
                                    
                                        for i in range(3) : 
                                            
                                            st.write("")
                                            
                                            

                                    
                                    
                                    
                                    
                                        # Métrique n°13-14-15-16-17 : Affichage de la dynamique DES 2 EQUIPES dans les périodes cruciales du match (début de match, avant mi-temps, retour de mi-temps et money time) :
                            
                                        L_dates = [10 , 30 , 35 , 35 , 60]               # la liste des dates
                                        L_x_dernieres_minutes = [10 , 5 , 5 , 10 , 10]   # la liste des x dernières minutes à regarder précédant chaque date de la liste ci-dessus
                                        
                                        
                                        
                                        
                                        # Pour chaque période cruciale du match :
                                            
                                        for date , x_dernieres_minutes in zip(L_dates , L_x_dernieres_minutes) :
                                            
                                            
                                            L_buts_marques_periode_cruciale_USDH = []  # la liste des buts marqués par l'USDH dans cette période cruciale, par match
                                            L_buts_encaisses_periode_cruciale_USDH = []   # la liste des buts encaissés par l'adversaire de l'USDH dans cette période cruciale, par match
                                            L_differentiels_buts_periode_cruciale_USDH = []  # la liste des différentiels de buts en faveur de l'USDH dans cette période cruciale, par match
                                            
                                            
                                            col1 , col2 , col3 , col4 , col5 , col6 , col7 = st.columns([1,2,2.3,1,1.15,2.3,1]) 
                                            
                                            
                                            
                                            # CAS 1 : SI l'on regarde la dynamique en DEBUT DE MATCH :
                                            
                                            if date == 10 :
                                                        
                                                col4.write("Dynamique début de match (0-10ème minute) :") 
                                                
                                            
                                            
                                            
                                            # CAS 2 : SI l'on regarde la dynamique d'AVANT MI-TEMPS :
                                            
                                            elif date == 30 : 
                                                
                                                col4.write("Dynamique avant mi-temps (25-30ème minute)")
                                                
                                                
                                            
                                            
                                            elif date == 35 : 
                                                
                                                
                                                # CAS 3 : SI l'on regarde la dynamique au RETOUR DE MATCH :
                                                
                                                if x_dernieres_minutes == 5 :
                                                
                                                    col4.write("Dynamique retour de mi-temps (30-35ème minute) :")
                                                    
                                                 
                                                    
                                                 
                                                # CAS 4 : SI l'on regarde la dynamique AUTOUR DE LA MI-TEMPS (5 minutes avant + 5 minutes au retour) :
                                                
                                                else : 
                                                
                                                    col4.write("Dynamique aux alentours de la mi-temps (25-35ème minute) :")    
                                                
                                                
                                                
                                               
                                                
                                            # CAS 5 : SI l'on regarde la dynamique dans le MONEY TIME :
                                                
                                            else : 
                                                
                                                col4.write("Dynamique money-time (50-60ème minute) :")
                                                
                                                
                                            
                                            
                                            # Pour chaque match disputé par l'USDH cette saison : 
                                                
                                            for journee in dico_rencontres_USDH.keys() :
                                                
                                                
                                                # Récupération de l'équipe jouant à domicile et à l'extérieur lors de match :
                                                
                                                equipe_dom_match = df[df["journée"] == journee]["domicile"].unique()
                                                equipe_dom_match = equipe_dom_match[0]    # équipe jouant à domicile
                                                
                                                
                                                equipe_ext_match = df[df["journée"] == journee]["extérieur"].unique()
                                                equipe_ext_match = equipe_ext_match[0]    # équipe jouant à l'extérieur
                                                
                                                
                                            
                                                # Récupération du nombre de buts inscrits par l'USDH et par son adversaire dans CETTE période cruciale, lors de CE match :
                                                        
                                                if equipe_dom_match == "USDH" :
                                                    
                                                    nbr_buts_periode_cruciale_USDH = dynamique_buts_marques(data = df , 
                                                                                                            date = date , 
                                                                                                            x_dernieres_minutes = x_dernieres_minutes  , 
                                                                                                            journee = journee , 
                                                                                                            equipe = "domicile")
                                                    
                                                    
                                                    nbr_buts_periode_cruciale_adv = dynamique_buts_marques(data = df , 
                                                                                                           date = date , 
                                                                                                           x_dernieres_minutes = x_dernieres_minutes  , 
                                                                                                           journee = journee , 
                                                                                                           equipe = "extérieur")
                                                    
                                                    
                                                    
                                                    
                                                    
                                                else :   # equipe_ext_match == "USDH" :
                                                    
                                                    nbr_buts_periode_cruciale_USDH = dynamique_buts_marques(data = df , 
                                                                                                            date = date , 
                                                                                                            x_dernieres_minutes = x_dernieres_minutes  , 
                                                                                                            journee = journee , 
                                                                                                            equipe = "extérieur")
                                                    
                                                    
                                                    nbr_buts_periode_cruciale_adv = dynamique_buts_marques(data = df , 
                                                                                                           date = date , 
                                                                                                           x_dernieres_minutes = x_dernieres_minutes  , 
                                                                                                           journee = journee , 
                                                                                                           equipe = "domicile")
                                                
                                        
                                            
                                 
                                    
                                                # Calcul de la différence de buts marqués EN FAVEUR DE L'USDH dans cette période de jeu cruciale : 
                                                        
                                                    
                                                difference_nbr_buts_periode_cruciale = nbr_buts_periode_cruciale_USDH - nbr_buts_periode_cruciale_adv
                                                    
                                                
                                                
                                                # On ajoute le nombre de buts marqués / encaissés + le différentiel de buts à leur liste dédiée : 
                                                    
                                                L_buts_marques_periode_cruciale_USDH.append(nbr_buts_periode_cruciale_USDH)
                                                L_buts_encaisses_periode_cruciale_USDH.append(nbr_buts_periode_cruciale_adv)
                                                L_differentiels_buts_periode_cruciale_USDH.append(difference_nbr_buts_periode_cruciale)
                                            
                                            
                                            
                                            
                                            # On récupère le nombre de buts marqués / encaissés + le différentiel de buts TOTAL ou MOYEN / MATCH en sommant ou en moyennant les 3 listes créées :
                                                
                                            if bouton_unite == "total" : 
                                                
                                                nbr_buts_marques_USDH_periode_cruciale = pd.Series(L_buts_marques_periode_cruciale_USDH).sum()
                                                nbr_buts_encaisses_USDH_periode_cruciale = pd.Series(L_buts_encaisses_periode_cruciale_USDH).sum()
                                                differentiel_buts_USDH_periode_cruciale = np.round(pd.Series(L_differentiels_buts_periode_cruciale_USDH).sum() , 2)
                                            
                                            
                                            
                                            
                                            else :    # bouton_unite == "moyenne / match" : 
                                                
                                                nbr_buts_marques_USDH_periode_cruciale = pd.Series(L_buts_marques_periode_cruciale_USDH).mean()
                                                nbr_buts_encaisses_USDH_periode_cruciale = pd.Series(L_buts_encaisses_periode_cruciale_USDH).mean()
                                                differentiel_buts_USDH_periode_cruciale = np.round(pd.Series(L_differentiels_buts_periode_cruciale_USDH).mean() , 2)
                                            
                                            
                                            
                                            
                                            
                                            
                                    
                                            # Ré-écriture du différentiel de buts suivant son signe : 
                                                
                                            if differentiel_buts_USDH_periode_cruciale > 0 :
                                                
                                                differentiel_buts_USDH_periode_cruciale = "+ " + str(differentiel_buts_USDH_periode_cruciale) + " buts marqués"
                                                
                                                
                                                
                                                
                                            elif differentiel_buts_USDH_periode_cruciale < 0 :
                                                
                                                differentiel_buts_USDH_periode_cruciale = "- " + str(abs(differentiel_buts_USDH_periode_cruciale)) + " buts marqués"
                                                
                                                        
                                                        
                                                        
       
                                                  
                                                  
                                            col3.metric(label = "" , 
                                                        value = np.round(nbr_buts_marques_USDH_periode_cruciale , 2) ,
                                                        delta = differentiel_buts_USDH_periode_cruciale)
                                            
                                                
                                                
                                            col6.metric(label = "" , 
                                                        value = np.round(nbr_buts_encaisses_USDH_periode_cruciale , 2) ,
                                                        delta = " ")
                                            
                                            
                                            
                                            
                                            
    
                                            
                                            for i in range(6) : 
                                                
                                                st.write("")
                                            
                                            
                                            
                                    
                                    
                                    
                                
                                    













