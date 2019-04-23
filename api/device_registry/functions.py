def get_people_count(graph):
        cypher = graph.cypher
        query = "MATCH (:Person) RETURN count(*)"
        result = cypher.execute(query)

        return result[0][0]


def get_disease_count(graph):
        cypher = graph.cypher
        query = "MATCH (:Disease) RETURN count(*)"
        result = cypher.execute(query)

        return result[0][0]
