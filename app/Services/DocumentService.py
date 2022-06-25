from numpy import dot
from numpy.linalg import norm

class DocumentService:
    def compare(_self_, document1, document2):
        vec1 = [keyword.name for keyword in document1.keyWords]
        vec2 = [keyword.name for keyword in document2.keyWords]
        conceptsKeysList = vec1 + \
            list(set(vec2) - set(vec1))
        v1 = [1 if key in vec1 else 0 for key in conceptsKeysList]
        v2 = [1 if key in vec2 else 0 for key in conceptsKeysList]

        return dot(v1, v2)/(norm(v1)*norm(v2))
