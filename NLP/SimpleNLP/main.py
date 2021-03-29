from testgraph import neo4jGraph

if __name__ == "__main__":
    connect = neo4jGraph("neo4j", "1")
    #connect.CLEAR()
    #connect.CREATE("His dog eats turkey on tuesday My cat eats fish on Saturday")
    doc = {
        'properties_1': 'on',
        'properties_2' : 'his'
    }
    #result = connect.MATCH(doc)
    new_properties = {
        "name" : 'on',
        "count" : "30",
        "lam" : "ngao vl"
     }
    connect.UPDATE(new_properties)
    delete = {
        "cmd" : "elete_all"
    }
    delete_1 = {
        "cmd" : "delete_nodes",
        "nodes" : ["on", "his"]
    }
    delete_2 = {
        "cmd" : "greater",
        "count" : 4
    }

    delete_3 = {
        "cmd" : "equal",
        "count" : 4
    }

    delete_4 = {
        "cmd" : "lesser",
        "count" : 4
    }

    connect.DELETE(delete_4)