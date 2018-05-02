import openpyxl
import re
import neo4j
from neo4j.v1 import GraphDatabase

def correct(str, label):
    target = '-（）()、“”'
    for ch in target:
        str = str.replace(ch, '')

    return label + str


def readExcel(path):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.get_sheet_by_name('Sheet1')
    with open('cypher.txt', 'w', encoding='utf-8') as f:
        for row in sheet.rows[1:]:
            for index, cell in enumerate(row):
                if index == 0:
                    name = cell.value
                if index == 2:
                    if cell.value is None:
                        alias_list = None
                    else:
                        alias_list = (cell.value).split('，')
                if index == 3:
                    if cell.value is None:
                        typical_symptom = 'null'
                    else:
                        result = re.findall('_x000D_[\s]+([^\s]+)', cell.value)
                        typical_symptom = result[0]
                if index == 4:
                    if cell.value is None:
                        early_symptom = 'null'
                    else:
                        early_symptom = re.findall('_x000D_[\s]+([^\s]+)', cell.value)[0]
                if index == 5:
                    if cell.value is None:
                        late_symptom = 'null'
                    else:
                        late_symptom = re.findall('_x000D_[\s]+([^\s]+)', cell.value)[0]
                if index == 6:
                    if cell.value is None:
                        relative_symtom = None
                    else:
                        result = re.findall('相关症状：([^\s]+)', cell.value)[0]
                        relative_symtom = result.split('，')

            f.write('merge (' + correct(name,'d') + ':Diease{name:\'' + name +'\', typical_symptom:\'' + typical_symptom + '\', early_symptom:\''  \
                    + early_symptom + '\', late_symptom:\'' + late_symptom + '\'}) ')

            # 写别名
            if alias_list is None:
                pass
            else:
                for item in alias_list:
                    f.write('merge (' + correct(item, 'd') + ':Diease{name:\'' + item + '\'}) ')
                    f.write('merge (' + correct(name, 'd') + ')-[:别名]->(' + correct(item, 'd') + ') ')

            # 写相关症状
            if relative_symtom is None:
                pass
            else:
                for item in relative_symtom:
                    f.write('merge (' + correct(item, 's') + ':Symptom{name:\'' + item + '\'}) merge (' + correct(name, 'd') + ')-[:症状]->(' + correct(item, 's') + ') ')

            f.write('\n')
            f.flush()

def create_graph():

    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "140030"))
    with driver.session() as session:
        with open('cypher.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines):
                try:
                    with session.begin_transaction() as t:
                        print('执行', line[:50])
                        t.run(line)
                    print(line_num, '行/', len(lines), '行完成')
                except neo4j.exceptions.ConstraintError:
                    with open('errorr.txt', 'a', encoding='utf-8') as f:
                        f.write('ConstraintError: ' + line[:50] + '\n')
                        f.flush()
                except Exception as e:
                    with open('errorr.txt', 'a', encoding='utf-8') as f:
                        f.write(e + ': ' + line[:50])


# readExcel("G:/result.xlsx")
create_graph()