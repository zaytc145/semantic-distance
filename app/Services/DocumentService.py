from numpy import dot
from numpy.linalg import norm
from app.Services.OntologyService import OntologyService

from app.models import Document, KeyWord, SimilarityValue, db


class DocumentService:
    def compare(_self_, document1, document2):
        vec1 = [keyword.name for keyword in document1.keyWords]
        vec2 = [keyword.name for keyword in document2.keyWords]
        conceptsKeysList = vec1 + \
            list(set(vec2) - set(vec1))
        v1 = [1 if key in vec1 else 0 for key in conceptsKeysList]
        v2 = [1 if key in vec2 else 0 for key in conceptsKeysList]

        return dot(v1, v2)/(norm(v1)*norm(v2))

    def handleDoc(_self_, docId):
        document = Document.query.options(
            db.joinedload(Document.keyWords)).get(docId)
        documents = Document.query.options().all()
        
        ontologySV = OntologyService()
        extraKeyWords = ontologySV.searchKeywords(document.keyWords)
        for word in extraKeyWords:
            document.keyWords.append(
                KeyWord(name=word.lower(), fromOntology=True))

        for doc in documents:
            if doc.id != document.id:
                sim = _self_.compare(doc, document)
                if sim > 0:
                    simVal = SimilarityValue(
                        firstDocId=doc.id, secondDocId=document.id, value=sim)
                    db.session.add(simVal)
            document.status = 'complete'
            db.session.add(document)
            db.session.commit()
        return document
