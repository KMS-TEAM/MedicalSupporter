from neo4j import GraphDatabase
import simpleNLP as xxx

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "1"))

def add_friend(tx , title ):
    tx.run("CREATE (source:entitiy_1{title: $title})", title=title)
    return None
def print_friends(tx, name):
    result = tx.run("MATCH (a:Person {name: $name})", name=name)
    return result.single()
def update_friends(tx, live, name):
    tx.run ("MATCH (a:Person {name: $name})"
            "SET a.live = $live", live=live, name = name)
    return None

#    session.write_transaction(update_friends, "HongKong", "Arthur")
#    session.read_transaction(print_friends, "Arthur")
driver.close()
if __name__ == "__main__":
    test = xxx.SimpleNLP(u"data/input/test.txt")
    doc = test.read_txt()

    with driver.session() as session:
        for title in test.source():
            session.write_transaction(add_friend, title)
        for titles in test.target():
            session.write_transaction(add_friend, titles)