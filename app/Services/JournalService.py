from bs4 import BeautifulSoup
import requests
from app.Services.OntologyService import OntologyService

from app.models import Document, KeyWord, SimilarityValue, db

class JournalService:
    def __init__(self):
        self.url = 'https://lobachevskii-dml.ru/journal/ivm'
        page = requests.get(self.url)
        self.journalSoup = BeautifulSoup(page.text, "html.parser")

    def parseJournal(self):
        pageTable = self.journalSoup.find('table', class_='table')
        volumeLinks = pageTable.find_all('a', href=True)
        for volumeLink in volumeLinks:
            self.parseVolume(volumeLink['href'])

    def parseVolume(self, volumeLink):
        page = requests.get('https:' + volumeLink)
        soup = BeautifulSoup(page.text, "html.parser")
        pageTable = soup.find('table', class_='table')
        articleLinks = pageTable.find_all('a', href=True)
        for articleLink in articleLinks:
            self.parseArticle(articleLink['href'])

    def parseArticle(self, articleLink):
        ontologyService = OntologyService()
        page = requests.get('https:' + articleLink)
        soup = BeautifulSoup(page.text, "html.parser")
        wrapper = soup.find('ol', class_='breadcrumb')
        if wrapper:
            headings = wrapper.parent.find_all('h4')
            for heading in headings:
                if(heading.text.lower() == 'ключевые слова'):
                    title = soup.find('h3', id="title")
                    keyWordSpans = heading.parent.find_all('span')
                    keyWords = []
                    document = Document(name=title.text)
                    for keyWordSpan in keyWordSpans:
                        word = keyWordSpan.text.replace(
                            ';', '').replace('.', '').strip().lower()
                        if word:
                            keyWords.append(
                                KeyWord(name=word)
                            )

                    extraKeyWords = []
                    for concept in [ontologyService.getConcept(word.name) for word in keyWords]:
                        if concept:
                            children = ontologyService.getAllChildren(concept['class'])
                            parent = ontologyService.getAllParent(concept['class'])
                            extraKeyWords = extraKeyWords + children + parent

                    extraKeyWords = set(extraKeyWords)
                    for word in extraKeyWords:
                        keyWords.append(
                            KeyWord(name=word.lower(), fromOntology=True))

                    document.keyWords = keyWords
                    db.session.add(document)
                    db.session.commit()
                    
                    
