import numpy as np
import requests
from numpy import dot
from numpy.linalg import norm
import math
import re


class OntologyService:
    ontologyURL = 'http://lobachevskii-dml.ru:8890/sparql'
    params = {
        'format': "application/sparql-results+json",
        'timeout': 0,
        'debug': 'on',
    }

    def getConcept(_self_, label):
        params = dict(_self_.params)
        query = """
            SELECT DISTINCT ?class ?label ?parent ?parentLabel
            WHERE {{
                ?class rdfs:label ?label
                OPTIONAL{{?class rdfs:subClassOf ?parent }}.
                OPTIONAL{{?parent rdfs:label ?parentLabel}}.
                FILTER (lcase(?label) = "{}"@ru)
            }}""".format(label)
        
        params['query'] = query
        response = requests.get(url=_self_.ontologyURL, params=params)
        return _self_.getFirst(response.json())

    def getOntologyGraph(_self_):
        params = dict(_self_.params)
        query = """    
        SELECT DISTINCT ?subject ?parent
        WHERE {
            { ?subject a owl:Class . } UNION { ?individual a ?subject . } .
            OPTIONAL { ?subject rdfs:subClassOf ?parent } .
            OPTIONAL { ?subject rdfs:label ?label }
            } ORDER BY ?subject
        """
        params['query'] = query
        response = requests.get(url=_self_.ontologyURL, params=params)
        concepts = response.json()['results']['bindings']

        graph = {}
        for concept in concepts:
            parent = _self_.getValue(concept, 'parent')
            conceptClass = _self_.getValue(concept, 'subject')
            if parent:
                if parent not in graph:
                    graph[parent] = [conceptClass]
                else:
                    graph[parent].append(conceptClass)
            if conceptClass not in graph:
                graph[conceptClass] = []
        return graph

    def dijkstra(_self_, concept1, concept2):
        if concept1['class'] == concept2['class']:
            return 1

        graph = _self_.getOntologyGraph()
        dist = {}
        queue = []
        for vertex in graph:
            dist[vertex] = math.inf
            queue.append(vertex)

        dist[concept1['class']] = 0
        while(len(queue)):
            min = None
            vertex = None
            for el in queue:
                if min is None:
                    min = dist[el]
                    vertex = el
                elif dist[el] < min:
                    min = dist[el]
                    vertex = el

            if math.isinf(dist[vertex]):
                dist[vertex] = 0

            queue = [v for v in queue if v != vertex]

            for neighbor in graph[vertex]:
                alt = dist[vertex] + 1
                if alt < dist[neighbor]:
                    dist[neighbor] = alt

        return dist[concept2['class']]

    def getGeneralConcept(_self_, firstConceptNodes, secondConceptNodes):
        for node in firstConceptNodes:
            if(node in secondConceptNodes):
                return firstConceptNodes[node]
        return 0

    def getConceptPath(_self_, concept):

        parent = concept
        nodes = {}

        nodes[concept['class']] = concept

        while(parent['parent_label']):
            parent = _self_.getConcept(re.search('"([^"]*)"', parent['parent_label']))
            nodes[parent['class']] = parent

        return nodes

    def mapBindigs(_self_, response):
        return list(map(lambda el: {
            'class': _self_.getValue(el, 'class'),
            'parent_class': _self_.getValue(el, 'parent'),
            'label': _self_.getValue(el, 'label'),
            'parent_label': _self_.getValue(el, 'parentLabel'),
        }, response['results']['bindings']))

    def getValue(_self_, dict, key):
        if(key in dict):
            if(key == "label" or key == 'parentLabel'):
                return "'{}'@{}".format(dict[key]['value'], dict[key]['xml:lang'])
            return dict[key]['value']
        return ''

    def getFirst(_self_, response):
        bindings = _self_.mapBindigs(response)
        if len(bindings) > 0:
            return bindings[0]
        return 0

    def getParent(_self_, className):
        params = dict(_self_.params)
        query = 'SELECT DISTINCT ?class WHERE {{ <{}> rdfs:subClassOf ?class }}'.format(
            className)
        params['query'] = query
        response = requests.get(url=_self_.ontologyURL, params=params)
        return response.json()

    def getAllChildren(_self_, concept):
        params = dict(_self_.params)
        query = """
            SELECT DISTINCT ?label
            WHERE {{
                ?class rdfs:subClassOf <{}>.
                ?class rdfs:label ?label.
                FILTER (lang($label) = 'ru')
            }}
        """.format(concept)
        params['query'] = query
        response = requests.get(url=_self_.ontologyURL, params=params).json()
        return _self_.getLabels(response)

    def getAllParent(_self_, concept):
        params = dict(_self_.params)
        query = """
            SELECT DISTINCT ?label
            WHERE {{
                <{}> rdfs:subClassOf ?parent.
                ?parent rdfs:label ?label.
                FILTER (lang($label) = 'ru')
            }}
        """.format(concept)
        params['query'] = query
        response = requests.get(url=_self_.ontologyURL, params=params).json()
        return _self_.getLabels(response)

    def getLabels(_self_,arr):
        return [label['label']['value'] for label in arr['results']['bindings']]