from neo4j import GraphDatabase

class neo4jGraph:

    def __init__(self, username, pwd):
        self.driver = GraphDatabase.driver(uri="neo4j:neo4j://localhost:7687", auth=(username, pwd))

    def CLEAR(self):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.m_clear)

    @staticmethod
    def m_clear(tx):
        cmd = (
              "match (n)"
              "detach delete n"
        )
        tx.run(cmd)
    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def CREATE(self, sentence):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self.m_create, sentence)

    @staticmethod
    def m_create (tx, sentence):
        temp = sentence.lower()
        texts = temp.split()
        for i in range(0, len(texts)-1):
            cmd = (
                    "merge (w1:Word{name:$tx}) "
                    "on create set w1.count = 1 on match set w1.count = w1.count +1 "     
                    "merge (w2:Word{name:$tx2}) "
                    "on create set w2.count = 1 on match set w2.count = w2.count +1 "
                    "merge (w1)-[r:NEXT]->(w2) "
                    "on create set r.count =1 "
                    "on match set r.count = r.count +1;"
            )
            #print(cmd)
            tx.run(cmd, sz=len(texts) - 2, tx=texts[i], tx2=texts[i+1])