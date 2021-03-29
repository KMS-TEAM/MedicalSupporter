from neo4j import GraphDatabase
class neo4jGraph:


    def __init__(self, username, pwd):
        self.driver = GraphDatabase.driver(uri="neo4j:neo4j://localhost:7687", auth=(username, pwd))

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
    def MATCH(self, key):
        with self.driver.session() as session:
            result = session.write_transaction(
                self.m_match, key
           )
            return result
    @staticmethod
    def m_match(tx, key):
        for property in key:
               cmd = (
               "MATCH (w:Word) "
               "where w.name = $key "
               "return *;"
               )
               temp = tx.run(cmd, key = key[property])
               record= temp.single()
               value = record.value()
               return  value
    def UPDATE(self, new_properties):
        with self.driver.session() as session:
            result = session.write_transaction(
                self.m_update, new_properties
            )
    @staticmethod
    def m_update(tx, new_properties):
        cmd = (
            "match (w:Word {name: $name}) "
            "set w = $new_prop")
        temp = tx.run(cmd, new_prop = new_properties, name = new_properties['name'])
    def DELETE(self, delete):
        with self.driver.session() as session:
            result = session.write_transaction(
                self.m_delete,delete)
    @staticmethod
    def m_delete(tx, delete):
         if (delete['cmd'] == 'delete_nodes'):
            for node in delete['node']:
             cmd = (
                "match (w:Word {name: $name})"
                "detach delete w"
             )
             tx.run(cmd, name=node)
         elif (delete['cmd'] =='delete_all'):
             cmd = (
                "match (n)"
                "detach delete n"
              )
             tx.run(cmd)
         elif (delete['cmd'] == 'greater'):
             cmd = (
                 "match (w:Word) "
                 "where w.count > $count "
                 "detach delete w"
             )
             tx.run(cmd,count=delete['count'])
         elif (delete['cmd'] == "equal"):
             cmd = (
                 "match (w:Word) "
                 "where w.count = $count "
                 "detach delete w"
             )
             tx.run(cmd,count=delete['count'])
         elif (delete['cmd'] == "lesser"):
             cmd = (
                 "match (w:Word) "
                 "where w.count < $count "
                 "detach delete w"
             )
             tx.run(cmd,count=delete['count'])

