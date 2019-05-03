FROM neo4j:3.4

WORKDIR /var/lib/neo4j

COPY neo4j-elasticsearch-3.4.5.jar ./plugins/.
COPY neo4j.conf ./conf/neo4j.conf


EXPOSE 7474 7687

CMD ["neo4j"]


