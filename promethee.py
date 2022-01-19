import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import *
from bs4 import BeautifulSoup
import urllib3
from xlwt import Workbook, Formula
import pickle
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Initialization of Selenium
CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
CHROMEDRIVER_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH


# Liste GP 1A
# liste_all_gp = ["Composantes de l'Entreprise", "Concepts et Outils de l’Electronique",
#                 "Concepts et Outils de l'Informatique", "Découverte de l'entreprise", "Langues S5",
#                 "Outils Mathématiques de l'Ingénieur", "Projet Robot S5", " Découverte des Enjeux Technologiques",
#                 "Informatique", "Intelligence Collective",
#                 "Langues S6", "Métiers de l'Ingénieur", "Projet Robot S6", "Sciences des Matériaux et du Vivant",
#                 "Systèmes Electroniques"]

# Liste GP 2A
liste_all_gp = ["Langues S7", "Management de l'activité de l'entreprise", "Projet Industriel - Avant Projet",
                "Projet Robot S7", "Systèmes Electroniques S7", "Systèmes Informatiques",
                "Transmission Capteurs Energie",
                "Gestion de Projets", "Langues S8", "Simulation, Expérimentation, Prototypage",
                "Visa Entrepreunariat"]


class Eleve:
    def __init__(self, name, id):
        self.name = name
        self.ID = id
        self.notes = {}
        self.average = 0
        self.average_GPs = {}
        self.GPA = 0
        self.grades = []

class Promethee:
    def __init__(self):
        self.username = "Arthur.driant"
        self.password = "3c6b593c796bb"

        self.listenumero1a = []
        self.listenom1a = []
        self.liste1a = []

        self.listenoteeleve = {}

    def getCookies(self):
        """Returns cookies needed to get marks"""
        driver = webdriver.Chrome("D:\Programmes\webdrivers\chromedriver.exe")
        driver.implicitly_wait(10)  # seconds
        driver.get("https://promethee.emse.fr/OpDotNet/Noyau/Login.aspx?")

        driver.find_element_by_xpath("//button[@class=\"provider\"]").click()
        driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(self.username)
                                                                    # Remplir la case identifiants
        sleep(0.5)
        driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(self.password)
                                                                    # Remplir la case mot de passe
        sleep(1)
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        sleep(2)

        return driver.get_cookies()

    @staticmethod
    def _getHtmlList():
        """Returns the html code with all the informations about users (IDs)"""
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
            'session_IdUser': '5749',
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
        return response


    def _ScrapeList(self, response):
        """Scrapes the html page of the calendar to get IDs and Names of the students, takes in argument the response
        from '_getHtmlList' """
        # scraping
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find('body')
        text = body.find('script').get_text()

        liste = BeautifulSoup(text[15:len(text)-3], 'html.parser')

        eleves = liste.findAll('a')

        for eleve in eleves[1:len(eleves)-1]:            # We avoid the junk at the end
            try:
                nom = eleve.get_text().split("<")[0].replace("\xa0", ' ')
                numero = eleve.get('onclick')[8:12]
                self.listenumero1a.append(numero)
                self.listenom1a.append(nom)
            except:
                break


    def getList(self):
        """Fills the \"liste1A\" with with \"Eleve\" type elements """
        response = self._getHtmlList()
        self._ScrapeList(response)

        for i in range(len(self.listenom1a)-6):
            eleve = Eleve(self.listenom1a[i], self.listenumero1a[i])
            self.liste1a.append(eleve)


    def getListFromFile(self):
        with open('Listeelevesbatoche', 'rb') as fichier:
            mon_depickler = pickle.Unpickler(fichier)
            Listeeleve = mon_depickler.load()
            fichier.close()

        for i in range(len(Listeeleve["listenumero2a"])):
            eleve = Eleve(Listeeleve["listenom2a"][i], Listeeleve["listenumero2a"][i])
            self.liste1a.append(eleve)


    def getID(self, name):
        """ Takes last + first name of a student and returns its ID """
        for elt in self.liste1a:
            if name in elt.name:
                print(f"ID de {elt.name} : {elt.ID}")



    def getNote(self):
        cookies = self.getCookies()

        requestsliste = requests.Session()
        c = [requestsliste.cookies.set(c['name'], c['value']) for c in cookies]

        idProcess = 40933
        idIns = 218320

        # student_promethee_number = 5749
        s = 0
        nb = 0
        classeur = Workbook()
        for eleve in self.liste1a:
            # On récup chaque page de données
            student_promethee_number = eleve.ID
            name = eleve.name
            headers = {
                'Referer': 'https://promethee.emse.fr/OpDotNet/Eplug/FPC/Process/Annuaire/Parcours/Parcours.aspx?IdObjet=4379&typeRef=process',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
                'Host': 'promethee.emse.fr',
            }

            params = (
                ('idProcess', idProcess),
                ('idUser', student_promethee_number),
                ('idIns', idIns),
                ('idProcessUC', '35468'),
                ('typeRef', 'process'),
            )

            response = requestsliste.get(
                'https://promethee.emse.fr/OpDotNet/Eplug/FPC/Process/Annuaire/Parcours/pDetailParcours.aspx',
                headers=headers, params=params, verify=False, allow_redirects=False)

            # scraping
            soup = BeautifulSoup(response.content, 'html.parser')

            listeclass = soup.findAll('tr', {'class': 'DataGridItem'})
            listematieretemp = []   #Matières que l'on a scrape sans les avoir renommées
            listematiere = []       #Matières sans doublon
            listenote = []  # Contiendra les notes de l'élève
            listecoef = []  # Contiendra les coefs des notes de l'élève


            for notes in listeclass:
                if notes.find('td', {'class': 'DataGridColumn EncadrementPaveRL'}) is not None:
                    if notes.find('td', {'class': 'largeurIE DataGridColumn'}).find('a') is None:
                        matiere = notes.find('td', {'class': 'largeurIE DataGridColumn'}).get_text()[2:]
                        pasnote = 1
                    else:
                        matiere = notes.find('td', {'class': 'largeurIE DataGridColumn'}).find('a').get_text()
                        pasnote = 0
                    listematieretemp.append(matiere)

                    if pasnote:
                        note = ""
                        # coef = notes.find_all('td', {'align': 'center'})[0].get_text()
                        coef = '0'
                    else:
                        coef = notes.find_all('td', {'align': 'center'})[0].get_text()
                        note = notes.find_all('td', {'align': 'center'})[1].get_text()

                    listenote.append(note)
                    listecoef.append(coef)

            self.listenoteeleve.clear()

            for i in range(len(listematieretemp)):  #Renomme les matières en double

                if listematieretemp[i] not in listematiere:
                    listematiere.append(listematieretemp[i])
                else:  # Si 2 matieres avec le meme nom
                    listematiere.append(str(listematieretemp[i]) + "_2")

                elt = {}
                elt.clear()
                elt["note"] = listenote[i]
                elt["coef"] = listecoef[i]
                self.listenoteeleve[listematiere[i]] = elt

            print("Notes de ", name, " :")
            print(self.listenoteeleve)

            # We write everything in an xls file
            last_name = name.split(" ")[0]
            feuille = classeur.add_sheet("Notes de {}".format(last_name))

            for i in range(len(self.listenoteeleve)):

                feuille.write(i+1, 1, listematiere[i])
                coef = float(self.listenoteeleve[listematiere[i]]["coef"].replace(",", "."))
                # print(coef)
                if coef == 0:
                    note = ""
                else:
                    try:
                        note = float(self.listenoteeleve[listematiere[i]]["note"])

                    except:
                        note = ""
                        coef = 0
                feuille.write(i+1, 2, note)
                feuille.write(i + 1, 3, coef)

            feuille.write(len(self.listenoteeleve)+1, 2, "Moyenne")
            feuille.write(len(self.listenoteeleve) + 1, 3, Formula('(C2*D2+C3*D3+C4*D4+C5*D5+C6*D6+C7*D7+C8*D8+C9*D9+C10*D10+'
                                                              'C11*D11+C12*D12+C13*D13+C14*D14+C15*D15+C16*D16)/('
                                                              'D2+D3+D4+D5+D6+D7+D8+D9+D10+D11+D12+D13+D14+D15+D16)'))
        classeur.save("fichier_excel2A.xls")


    def getGrades(self):
        """ Fills the \"GPA\" attribute of every student in the \"liste1a\" list and writes everything in
        \"liste_grades.xls\" """
        cookies = self.getCookies()

        requestsliste = requests.Session()

        c = [requestsliste.cookies.set(c['name'], c['value']) for c in cookies]

        # idProcess = 35469 1A Arthur
        # idIns = 178458
        # idProcessUC = 35468

        # idProcess = 40933   # 2A Arthur
        # idIns = 218320
        # idProcessUC = 35468

        # idProcess = 29867   # 1A Baptiste
        # idIns = 130235
        # idProcessUC = 29866

        idProcess = 34751   # 2A Baptiste
        idIns = 167715
        idProcessUC = 29866

        classeur = Workbook()
        j = 0
        for eleve in self.liste1a:

            # On récup chaque page de données
            student_promethee_number = eleve.ID
            name = eleve.name
            headers = {
                'Referer': 'https://promethee.emse.fr/OpDotNet/Eplug/FPC/Process/Annuaire/Parcours/Parcours.aspx?IdObjet=4379&typeRef=process',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
                'Host': 'promethee.emse.fr',
            }

            params = (
                ('idProcess', idProcess),
                ('idUser', student_promethee_number),
                ('idIns', idIns),
                ('idProcessUC', idProcessUC),
                ('typeRef', 'process'),
            )

            response = requestsliste.get(
                'https://promethee.emse.fr/OpDotNet/Eplug/FPC/Process/Annuaire/Parcours/pDetailParcours.aspx',
                headers=headers, params=params, verify=False, allow_redirects=False)

            # scraping

            soup = BeautifulSoup(response.content, 'html.parser')
            gps = soup.findAll('tr', {'class': 'DataGridItem'})

            for gp in gps:
                potentiel_gp = gp.findAll('td', {'class': 'DataGridColumn EncadrementPaveRL FondtresClair'})
                if potentiel_gp:
                    grade = potentiel_gp[2].text  # Pareil que de faire .find('b').text

                    if grade in ["A+", 'A', 'B', 'C', 'D', 'E']:
                        eleve.grades.append(grade)

                    elif grade == "Fx":     # This is not how the GPA is calculated --> If Fx, then it doesn't count
                        eleve.grades.append('C')

            # last_name = name.split(" ")[0]    # Pour Arthur
            if len(name) > 15:
                last_name = name[0:15]
            else:
                last_name = name
            last_name.replace('/', '').replace("'", "")


            try:
                feuille = classeur.add_sheet("Grades de {}".format(last_name))
            except:
                feuille = classeur.add_sheet(f"Grades de inconnu {j}")
                j += 1

            feuille.write(1, 1, "GPs")
            feuille.write(1, 2, "Grade")

            print("Grades de ", last_name, ": ", eleve.grades)

            i = 0
            for lettre in eleve.grades:
                feuille.write(i+2, 1, liste_all_gp[i])
                feuille.write(i+2, 2, lettre)
                i += 1

        classeur.save("Batoche/liste_grades_Batoche.xls")
