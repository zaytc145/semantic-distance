from numpy import dot
from numpy.linalg import norm

class DocumentService:
    def compare(_self_, document1, document2):
        concept1Path = [keyword.name for keyword in document1.keyWords]
        concept2Path = [keyword.name for keyword in document2.keyWords]
        conceptsKeysList = concept1Path + \
            list(set(concept2Path) - set(concept1Path))
        v1 = [1 if key in concept1Path else 0 for key in conceptsKeysList]
        v2 = [1 if key in concept2Path else 0 for key in conceptsKeysList]

        return dot(v1, v2)/(norm(v1)*norm(v2))
