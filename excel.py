from promethee import *
import requests
from bs4 import BeautifulSoup
import xlrd
from xlwt import Workbook

liste1A = []  # Liste des élèves de classe "Eleve"

liste_coefs_gpa = [  # 3/30, 4/30, 5/30, 6/30, 4/30, 5/30, 3/30,
    0, 8 / 29, 4 / 29, 4 / 29, 1 / 29, 4 / 29, 5 / 29, 3 / 29]
l_coefs_tot = []  # Not used anymore

liste_GP_1A_S1 = {"Composantes de l'Entreprise": ["Culture de l'Entreprise et Modes Managériaux",
                                                  "Visions et Stratégie d’Entreprise"],
                  "Concepts et Outils de l’Electronique": ["Electronique Analogique ", "Electronique Numérique "],
                  "Concepts et Outils de l'Informatique": ["Algorithmique et Programmation",
                                                           "Systèmes à Microcontrôleurs"],
                  "Découverte de l'entreprise": ["Développement Relationnel", "Stage Connaissance de l'Entreprise "],
                  "Langues S5": ["Anglais", "LV2"],
                  "Outils Mathématiques de l'Ingénieur": ["Projet Matlab - application à la robotique",
                                                          "Mathématiques et Traitement du Signal", "Probabilités"],
                  "Projet Robot S5": ["Projet Robot", "Automatique linéaire"]}

liste_GP_1A = {
    "Composantes de l'Entreprise": ["Culture de l'Entreprise et Modes Managériaux",
                                    "Visions et Stratégie d’Entreprise"],
    "Concepts et Outils de l’Electronique": ["Electronique Analogique ", "Electronique Numérique "],
    "Concepts et Outils de l'Informatique": ["Algorithmique et Programmation", "Systèmes à Microcontrôleurs"],
    "Découverte de l'entreprise": ["Développement Relationnel", "Stage Connaissance de l'Entreprise "],
    "Langues S5": ["Anglais", "LV2"],
    "Outils Mathématiques de l'Ingénieur": ["Projet Matlab - application à la robotique",
                                            "Mathématiques et Traitement du Signal", "Probabilités"],
    "Projet Robot S5": ["Projet Robot", "Automatique linéaire"],
    "Découverte des Enjeux Technologiques": ["Découverte des Enjeux Technologiques"],
    "Informatique": ["Algorithmique et Programmation", "Graphes et Optimisation", "Programmation Système",
                     "Challenge Optimisation", "Réseaux TCP/IP"],
    "Intelligence Collective": ["Projet ISA", "Retour d'expérience"],
    "Langues S6": ["Anglais_2", "LV2_2"],
    "Métiers de l'Ingénieur": ["International", "Métiers", "Secteurs"],
    "Projet Robot S6": ["Interface Design", "System Design"],
    "Sciences des Matériaux et du Vivant": ["Expérimentations en Labo", "Physique Appliquée",
                                            "Propriétés des Matériaux", "Sciences du Vivant"],
    "Systèmes Electroniques": ["Electronique Analogique", "Electronique Fondamentale"]}

#### Liste GP 1A
# liste_all_gp = ["Composantes de l'Entreprise", "Concepts et Outils de l’Electronique",
#                 "Concepts et Outils de l'Informatique", "Découverte de l'entreprise", "Langues S5",
#                 "Outils Mathématiques de l'Ingénieur", "Projet Robot S5", " Découverte des Enjeux Technologiques",
#                 "Informatique", "Intelligence Collective",
#                 "Langues S6", "Métiers de l'Ingénieur", "Projet Robot S6", "Sciences des Matériaux et du Vivant",
#                 "Systèmes Electroniques"]
# coef_all_gp = [3, 4, 5, 6, 4, 5, 3, 0, 8, 3, 4, 2, 4, 5, 3]


#### Liste GP 2A
liste_all_gp = ["Langues S7", "Management de l'activité de l'entreprise", "Projet Industriel - Avant Projet",
                "Projet Robot S7", "Systèmes Electroniques S7", "Systèmes Informatiques",
                "Transmission Capteurs Energie"] # ,
                # "Gestion de Projets", "Langues S8", "Simulation, Expérimentation, Prototypage",
                # "Visa Entrepreunariat"]
coef_all_gp = [3, 4, 2, 4, 5, 7, 5]

liste_Sub_2A = {"Langues S7": ["Anglais", "LV2"]}

classement_des_gp = {}


def saveID():
    """Ecrit dans un Liste_IDs.xls la liste des élèves et leur ID"""

    liste_nom_1a = []
    liste_numero_1a = []

    requestsliste = requests.Session()

    # We first load the calendar page
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer': 'https://promethee.emse.fr/OpDotnet/commun/Login/aspxtoasp.aspx?url=/Eplug/Agenda/\
                    Agenda.asp?IdApplication=190&TypeAcces=Utilisateur&groupe=31',
        'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': 'promethee.emse.fr',
    }
    data = {
        'url': '/Eplug/Agenda/Agenda.asp?IdApplication=190',
        'TypeAcces': 'Utilisateur',
        'groupe': '31',
        'session_IdCommunaute': '2',
        'session_IdUser': '4379',
        'session_IdGroupe': '31',
        'session_IdLangue': '1',
    }
    response = requestsliste.post('https://promethee.emse.fr/commun/aspxtoasp.asp', headers=headers,
                                  verify=False, data=data)

    # Then we get the calendar page with all the names in it
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer': 'https://promethee.emse.fr/EPlug/Agenda/Agenda.asp',
        'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': 'promethee.emse.fr',
    }
    params = (
        ('NumEve', '62766'),
        ('DatSrc', '20200520'),
        ('NomCal', 'USR5749'),
    )
    response = requestsliste.get('https://promethee.emse.fr/Eplug/Agenda/Eve-Det.asp',
                                 headers=headers, params=params, verify=False)

    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('body')
    text = body.find('script').get_text()

    liste = BeautifulSoup(text[15:len(text) - 3], 'html.parser')

    eleves = liste.findAll('a')

    for eleve in eleves[1:len(eleves) - 7]:  # on evite la merde a la fin
        try:
            nom = eleve.get_text().split("<")[0].replace("\xa0", ' ')
            numero = eleve.get('onclick')[8:12]
            liste_numero_1a.append(numero)
            liste_nom_1a.append(nom)
        except:
            break

    print(liste_nom_1a, liste_numero_1a)

    classeur = Workbook()
    feuille = classeur.add_sheet("Student IDs")

    for i in range(len(liste_nom_1a)):
        feuille.write(i + 1, 1, liste_nom_1a[i])
        feuille.write(i + 1, 2, int(liste_numero_1a[i]))

    classeur.save("Liste_IDs.xls")


def getSubjects():
    """Dresse la liste des matières et la renvoie à partir de fichier_excel.xls"""
    wb = xlrd.open_workbook("fichier_excel.xls")

    liste_up_1a = []

    sh = wb.sheet_by_name(wb.sheet_names()[0])

    for rownum in range(1, sh.nrows):
        row = sh.row_values(rownum)[1::]

        if row[0] in ["Chinois", "Allemand", "Espagnol", "Portugais", "Japonais"]:
            liste_up_1a.append("LV2")

        elif row[0] in ["Chinois_2", "Allemand_2", "Espagnol_2", "Portugais_2", "Japonais_2"]:
            liste_up_1a.append("LV2_2")
        else:
            liste_up_1a.append(row[0])

    # print(liste_up_1a)
    return liste_up_1a


def getID():
    """Récupère la liste des IDs depuis le xls et la renvoie, dlf [[Nom1, ID1], [Nom2, ID2]...]"""
    wb = xlrd.open_workbook("Liste_IDs.xls")
    sh_name = wb.sheet_names()[0]
    liste_num_1a = []

    sh = wb.sheet_by_name(sh_name)

    for rownum in range(1, sh.nrows):
        row = sh.row_values(rownum)[1::]

        liste_num_1a.append([row[0], int(row[1])])

    # print(liste_num_1a)
    return liste_num_1a


def getData():
    """ Remplit la liste 'liste1A' d'élèves avec leurs moyennes depuis le fichier excel et calcule leur GPA"""
    # wb = xlrd.open_workbook("fichier_excel.xls")  # On ouvre le fichier Excel 1A Arthur
    wb = xlrd.open_workbook("fichier_excel2A.xls")  # On ouvre le fichier Excel 2A Arthur

    liste_num_1a = getID()
    for student in liste_num_1a:
        student_name = student[0]
        student_last_name = student_name.split(" ")[0]
        student_id = student[1]
        sh = wb.sheet_by_name(f"Notes de {student_last_name}")

        new_student = Eleve(student_name, student_id)

        for rownum in range(1, sh.nrows):
            row = sh.row_values(rownum)[1::]
            # print(row)

            if row[0] in ["Chinois", "Allemand", "Espagnol", "Portugais", "Japonais"]:  # On renomme les LV2
                # print("Renommage LV2_1")
                if row[1] == '':  # S'il n'y a pas encore de note
                    new_student.notes["LV2"] = -1

                else:
                    new_student.notes["LV2"] = row[1]

            elif row[0] in ["Chinois_2", "Allemand_2", "Espagnol_2", "Portugais_2", "Japonais_2"]:  # On renomme les LV2
                # print("Renommage LV2_2")
                if row[1] == '':  # S'il n'y a pas encore de note
                    new_student.notes["LV2_2"] = -1

                else:
                    new_student.notes["LV2_2"] = row[1]

            else:
                if row[1] == 'Moyenne':  # On enlève la moyenne
                    pass

                elif row[1] == '':  # S'il n'y a pas encore de note
                    new_student.notes[row[0]] = -1

                else:
                    new_student.notes[row[0]] = row[1]

        # print(new_student.notes)
        liste1A.append(new_student)

    # liste1A.pop()

    # Partie qui gère le GPA
    wb = xlrd.open_workbook("liste_grades.xls")
    liste_sans_1b = []

    for eleve in liste1A:
        student_last_name = eleve.name.split(" ")[0]
        sh = wb.sheet_by_name(f"Grades de {student_last_name}")

        for rownum in range(2, sh.nrows):
            row = sh.row_values(rownum)[1::]  # row contient une rangée
            eleve.grades.append(row[1])

        # print(eleve.grades)

    for student in liste1A:
        if not (student.ID in [4433, 4391, 4415, 4399, 4423, 4357]):
            liste_sans_1b.append(student)

    for student in liste_sans_1b:
        i = 0
        for lettre in student.grades:
            if lettre == "A+":
                note = 4.33

            elif lettre == "A":
                note = 4

            elif lettre == "B":
                note = 3.33

            else:
                note = 2.66

            summ = sum(coef_all_gp)
            student.GPA += note * (coef_all_gp[i] / summ)
            i += 1
        student.GPA = round(student.GPA, 2)


def printStudent(id):
    """Prend en argument l'ID de l'élève et affiche ses notes """
    # getData()
    for student in liste1A:
        if student.ID == id:
            print(student.notes)


def findStudent(student_id):
    """Renvoie l'élève avec l'id student_id"""
    c = 0
    student = liste1A[0]

    while student.ID != student_id:
        c += 1
        student = liste1A[c]

        if c > len(liste1A):
            print("Erreur, ID non trouvée.")
            break

    return student


def getSubAverage():
    "Calcule les moyennes de toutes les matières pour calculer les moyennes des GPs"

    j = 0  # Compteur de matières pour récup le coef
    for gp in liste_GP_1A.items():  # On récup chaque GP
        print("\nGP : ", gp)
        moy = 0
        for sub in gp[1]:  # gp est un tuple de deux elts, on récup donc que la liste des mat
            # print("Matière : ", sub)
            a = 0
            i = 0  # Compteur d'eleves par matière
            # print("Matière : ", sub)
            for student in liste1A:  # Calcul de la moyenne générale
                if not (student.ID in [4433, 4391, 4415, 4399, 4423, 4357]):
                    # print("Eleve : ", student.name)
                    a += student.notes[sub]
                    i += 1

            moy += a / i * l_coefs_tot[j]
            j += 1

        print("Moyenne du GP ", gp[0], " : ", moy)


def getStudentAverage(student_id, listesub=[], infunction=False):
    """Calcule la moyenne générale d'un élève, option pour savoir si on doit calculer la listeSub dans cette fonction"""

    if not (infunction):
        getData()
        listesub = getSubjects()

    student = findStudent(student_id)
    if student.notes == {}:
        pass
    else:
        s = 0
        i = 0
        for gp in liste_Sub_2A.items():  # On parcourt tous les GPs
            moy_gp = 0
            for sub in gp[1]:  # Pour chaque matière à l'intérieur du gp
                # Contiendra la S des moy des GPs
                moy_gp += student.notes[sub] * l_coefs_tot[i]
                i += 1

            s += moy_gp
            student.average_GPs[gp[0]] = moy_gp

        # print("Moyenne de ", student.name, " : ", s/7)
        return (s / 1)
    return (-1)


def printStudentAverages(student_id):
    """ Calcule et renvoie la moyenne de l'élève"""
    student = findStudent(student_id)
    getStudentAverage(student_id)

    print("Moyennes des GPs de ", student.name, " : ", student.average_GPs)


def getGlobalRanking():
    """ Pas ouf, calcule le classement en fonction de la moyenne générale (qui est mal calculée)"""
    # getData()
    listeSub = getSubjects()
    liste_sans_1b = []  # Liste sans les 1B

    for student in liste1A:
        if not (student.ID in [4433, 4391, 4415, 4399, 4423, 4357]):
            liste_sans_1b.append(student)

    for student in liste_sans_1b:  # On calcule les moyennes de tout le monde
        student.average = getStudentAverage(student.ID, listeSub, True)

    rankList = [liste_sans_1b[0]]

    for k in range(1, len(liste_sans_1b)):
        stud = liste_sans_1b[k]
        i = 0
        while i < len(rankList) and stud.average < rankList[i].average:
            i += 1

        rankList.insert(i, stud)

    rank_list_propre = []
    i = 1
    for student in rankList:
        rank_list_propre.append([i, student.name, student.average])
        i += 1

    print(rank_list_propre)

    classeur = Workbook()
    feuille = classeur.add_sheet("Ranking")

    for i in range(len(rank_list_propre)):
        feuille.write(i + 1, 1, rank_list_propre[i][0])
        feuille.write(i + 1, 2, rank_list_propre[i][1])
        feuille.write(i + 1, 3, rank_list_propre[i][2])

    classeur.save("Rank_List.xls")


def getRankingByGP():
    """Écrit dans \"Rank_List_Of_GP.xls\" les classements par GP. Fonctionne bien. """
    # listeSub = getListGP()
    listeSub = liste_GP_1A
    liste_sans_1b = []  # Liste sans les 1B

    for student in liste1A:
        if not (student.ID in [4433, 4391, 4415, 4399, 4423, 4357]):
            liste_sans_1b.append(student)

    for student in liste_sans_1b:  # On calcule les moyennes de tout le monde
        student.average = getStudentAverage(student.ID, listeSub, True)

    classeur = Workbook()

    for gp in liste_Sub_2A.items():  # gp est un tuple contenant le nom du GP et la liste des matières

        if len(gp[0]) > 31:  # Si le nom du GP est trop long pour la feuille
            name = gp[0][0:31]

        else:
            name = gp[0]

        feuille = classeur.add_sheet(f"{name}")

        rankList = [liste_sans_1b[0]]

        print(rankList[0].average_GPs)

        for k in range(1, len(liste_sans_1b)):  # On effectue ensuite le classement des élèves
            stud = liste_sans_1b[k]
            i = 0
            if stud.average_GPs == {}:
                pass
            else:
                while i < len(rankList) and stud.average_GPs[gp[0]] < rankList[i].average_GPs[gp[0]]:
                    i += 1

                rankList.insert(i, stud)

        rank_list_propre = []
        i = 1
        for student in rankList:
            rank_list_propre.append([i, student.name, student.average_GPs[gp[0]]])
            i += 1

        classement_des_gp[gp[0]] = rank_list_propre
        print("Classement pour le GP ", gp[0], " : ", rank_list_propre)

        for i in range(len(rank_list_propre)):
            feuille.write(i + 1, 1, rank_list_propre[i][0])
            feuille.write(i + 1, 2, rank_list_propre[i][1])
            feuille.write(i + 1, 3, rank_list_propre[i][2])

    classeur.save("Rank_List_Of_GPs_2A.xls")


def getListGP():
    """"Renvoie la liste des noms des GPs"""
    l = []
    for gp in liste_GP_1A.items():
        l.append(gp[0])
    # print(l)
    return (l)


def printGPA(student_id):
    """" Astucieux, attribue les grades en fonction du classement de chacun dans chaque GP puis calcule le GPA"""
    student = findStudent(student_id)

    wb = xlrd.open_workbook("Rank_List_Of_GP.xls")  # On ouvre le fichier Excel
    i = 0
    GPNames = getListGP()
    # print(GPNames)
    for sh_name in wb.sheet_names():  # On dresse les classements des GPs stockés dans un dict classement_des_gp
        sh = wb.sheet_by_name(sh_name)
        rankList = []
        for rownum in range(1, sh.nrows):
            row = sh.row_values(rownum)[1::]
            row[0] = int(row[0])

            rankList.append(row)

        classement_des_gp[GPNames[i]] = rankList
        i += 1
    # print(classement_des_gp)

    # GPA = 0
    # i = 0
    # for gp_ranking in classement_des_gp.values():  # ranking contient le classement
    #     for rank in gp_ranking:    # On parcourt tout le classement du GP
    #         if student.name == rank[1]:
    #             if rank[0] < 9:
    #                 GPA += 4.33*liste_coefs_gpa[i]
    #
    #             elif rank[0] < 31:
    #                 GPA += 4*liste_coefs_gpa[i]
    #
    #             elif rank[0] < 58:
    #                 GPA += 3.33*liste_coefs_gpa[i]
    #
    #             else:
    #                 GPA += 2.33*liste_coefs_gpa[i]
    #             print("Classement de ", student.name, " au GP ", GPNames[i], " : ", rank[0])
    #     i += 1

    print("GPA de ", student.name, " : ", student.GPA)
    print("Grades de ", student.name, " :", student.grades)
    # student.GPA = GPA


def getRankGPA():
    """Écrit le classement dans \"Rank_List_GPA.xls\" """
    liste_sans_1b = []

    for student in liste1A:
        if not (student.ID in [4433, 4391, 4415, 4399, 4423, 4357]):
            liste_sans_1b.append(student)

    liste_classee = [liste_sans_1b[0]]
    for student in liste_sans_1b[1::]:
        i = 0
        while i < len(liste_classee) and student.GPA < liste_classee[i].GPA:
            i += 1

        liste_classee.insert(i, student)

    l_GPA_classee = []
    l_GPA_non_classee = []
    i = 1

    for student in liste_classee:
        l_GPA_classee.append([i, student.name, student.GPA])
        i += 1

    for student in liste_sans_1b:
        l_GPA_non_classee.append([student.name, student.GPA])

    classeur = Workbook()
    feuille = classeur.add_sheet("GPAs")
    feuille.write(1, 1, "Nom")
    feuille.write(1, 2, "GPA")

    for i in range(len(l_GPA_non_classee)):
        feuille.write(i + 2, 1, l_GPA_non_classee[i][0])
        feuille.write(i + 2, 2, l_GPA_non_classee[i][1])

    feuille = classeur.add_sheet("GPA Ranking")
    feuille.write(1, 1, "Classement")
    feuille.write(1, 2, "Nom")
    feuille.write(1, 3, "GPA")

    for i in range(len(l_GPA_classee)):
        feuille.write(i + 2, 1, l_GPA_classee[i][0])
        feuille.write(i + 2, 2, l_GPA_classee[i][1])
        feuille.write(i + 2, 3, l_GPA_classee[i][2])

    classeur.save("Batoche/Rank_List_GPA.xls")


def classementUP(nom_up):
    """ Prend en argument un nom d'UP et renvoie le classement des élèves dans cet UP et la moyenne générale"""
    print(f"Classement de l'UP {nom_up} :")
    classement = []
    moy = 0
    nb_rat = 0

    for eleve in liste1A:
        try:
            # print(f"Note de {eleve.name} en {nom_up} : {eleve.notes[nom_up]}")
            classement.append((eleve.name, eleve.notes[nom_up]))
        except:
            None
    classement = sorted(classement, key=lambda eleve: eleve[1], reverse=True)

    for i in range(len(classement)):
        moy += classement[i][1] / len(classement)
        if classement[i][1] < 10:
            nb_rat += 1
        # print(f"{classement[i][0]}")
        print(f"#{i + 1}: {classement[i][0]}  -  {classement[i][1]}")

    print(f"\nMoyenne de la classe : {moy}.")
    print(f"Nombre de personnes au rattrapage : {nb_rat}")


def listeUP():
    """ Affiche la liste des UPs et indique s'il y a déjà la note"""

    ups = liste1A[0].notes
    for key in ups.keys():
        if ups[key] == -1:
            print(key, " (X)")

        else:
            print(key)


def lecture_groupes():
    """Lit le fichier "liste_groupes.txt pour créer les groupes, renvoie une liste de listes de groupes
    (uniquement les noms de famille"""
    fic = open("liste_groupes.txt")
    mega_l = fic.readlines()
    print(mega_l)
    p = mega_l[0]
    fic.close()


def get_GPA_ranking_Batoche():
    with open('Listeelevesbatoche', 'rb') as fichier:
        mon_depickler = pickle.Unpickler(fichier)
        Listeeleve = mon_depickler.load()
        fichier.close()

    liste_eleves = []
    wb = xlrd.open_workbook("Batoche/liste_grades_Batoche.xls")
    for i in range(len(Listeeleve["listenom2a"])):
        sh = wb.sheet_by_index(i)

        eleve = Eleve(Listeeleve["listenom2a"][i], Listeeleve["listenumero2a"][i])
        for rownum in range(2, sh.nrows):
            row = sh.row_values(rownum)[1::]  # row contient une rangée
            eleve.grades.append(row[1])
        liste_eleves.append(eleve)

    for student in liste_eleves:
        if student.grades:
            i = 0
            for lettre in student.grades[:7]:
                if lettre == "A+":
                    note = 4.33

                elif lettre == "A":
                    note = 4

                elif lettre == "B":
                    note = 3.33

                else:
                    note = 2.66

                summ = sum(coef_all_gp)
                student.GPA += note * (coef_all_gp[i] / summ)
                i += 1
            student.GPA = round(student.GPA, 2)

    liste_eleves_n = []
    for eleve in liste_eleves:
        if eleve.GPA != 0:
            liste_eleves_n.append(eleve)

    liste_eleves = liste_eleves_n

    liste_classee = [liste_eleves[0]]
    for student in liste_eleves[1::]:
        i = 0
        while i < len(liste_classee) and student.GPA < liste_classee[i].GPA:
            i += 1

        liste_classee.insert(i, student)

    l_GPA_classee = []
    l_GPA_non_classee = []
    i = 1

    for student in liste_classee:
        l_GPA_classee.append([i, student.name, student.GPA])
        i += 1

    for student in liste_eleves:
        l_GPA_non_classee.append([student.name, student.GPA])

    classeur = Workbook()
    feuille = classeur.add_sheet("GPAs")
    feuille.write(1, 1, "Nom")
    feuille.write(1, 2, "GPA")

    for i in range(len(l_GPA_non_classee)):
        feuille.write(i + 2, 1, l_GPA_non_classee[i][0])
        feuille.write(i + 2, 2, l_GPA_non_classee[i][1])

    feuille = classeur.add_sheet("GPA Ranking")
    feuille.write(1, 1, "Classement")
    feuille.write(1, 2, "Nom")
    feuille.write(1, 3, "GPA")

    for i in range(len(l_GPA_classee)):
        feuille.write(i + 2, 1, l_GPA_classee[i][0])
        feuille.write(i + 2, 2, l_GPA_classee[i][1])
        feuille.write(i + 2, 3, l_GPA_classee[i][2])

    classeur.save("Batoche/Rank_List_GPA.xls")


getData()
# listeUP()
# classementUP("Conception d'un Système Numérique")
# getRankGPA()
get_GPA_ranking_Batoche()

# lecture_groupes()

# printStudent(5749)
# getSubAverage()
# getRankingByGP()


# printGPA(5773)
# getRankGPA()
# getRankingByGP()
# print("Notes de Léo : ", liste1A[1].notes)
# print("Nom : ", liste1A[len(liste1A)-4].name, "\nMoyenne : ", liste1A[len(liste1A)-4].average)
