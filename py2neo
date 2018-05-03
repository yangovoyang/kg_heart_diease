import py2neo
import time


class HandleNeo4j:
    def __init__(self):
        self.graph = py2neo.Graph('bolt://localhost:7687', user='neo4j', password='140030')

    def merge_or_create(self):
        try:
            # 方法一时间上较慢
            with self.graph.begin() as tx:
                for i in range(10):
                    tx.run('merge (a:a{name:"owen"})')

            # 方法二时间上快，但是空间消耗大
            tx = self.graph.begin()
            for i in range(10):
                tx.run('merge (a:a{name:"owen"})')
            tx.commit()
        except py2neo.database.status.CypherSyntaxError as e: # 如果有cypher语法错误
            print(e)
        except Exception as e:
            print(e)

    def read(self):
        try:
            tx = self.graph.begin()
            cursor = tx.run('match (a) return a.name as name')
            while cursor.forward():
                record = cursor.current()
                yield record['name']
        except py2neo.database.status.CypherSyntaxError as e:
            print(e)
        except Exception as e:
            print(e)

    def test(self):
        transaction = self.graph.begin()
        a = py2neo.Node(name='owen')
        transaction.create(a)
        transaction.create(a)


if __name__ == '__main__':
    hn = HandleNeo4j()
    hn.test()




