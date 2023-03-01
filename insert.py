from properties import *
import csv
import os
import pymysql

BASE_DIR = os.path.dirname(__file__)
categoryId = {"기획": 1, "마케팅": 2, "개발": 3, "디자인": 4, "비즈니스": 5, "IT": 6}

def saveTerms():
    arr = []
    with open(BASE_DIR + '/terms.tsv') as file:
        rdr = csv.reader(file, delimiter='\t')
        for row in rdr:
            arr.append(row)
    return arr


def printTermInfo(terms_arr, n):
    name = terms_arr[n][0]
    categories = terms_arr[n][1].split(',')
    categories = changeCategoryToId(list(map(trim, categories)))
    description = terms_arr[n][2]
    source = terms_arr[n][3]
    
    print('단어명 : ' + name)
    print('카테고리 : ', categories)
    print('뜻 : ' + description)
    print('출처 : ' + source)

    
def trim(word):
    return word.strip()


def changeCategoryToId(arr):
    for i in range(len(arr)):
        if arr[i] == 'All':
            return [1, 2, 3, 4, 5, 6]
        else:
            arr[i] = categoryId[arr[i]]
    
    return arr


def connect_RDS():
    conn = pymysql.connect(database=DATABASE,
                        host=HOST,
                        port=PORT,
                        user=USER,
                        password=PASSWORD)
    return conn, conn.cursor()


def disconnect_RDS(conn):
    conn.close()
    
    
def commit_RDS(conn):
    conn.commit()
        

def insertTerm(terms_arr, cur):
    for n in range(len(terms_arr)):
        name = terms_arr[n][0]
        categories = terms_arr[n][1].split(',')
        categories = changeCategoryToId(list(map(trim, categories)))
        description = terms_arr[n][2]
        source = terms_arr[n][3]
        
        cur.execute("INSERT INTO term (name, description, source) VALUES (%s, %s, %s);", (name, description, source))
        
        id = cur.lastrowid
        for categoryId in categories:
            cur.execute("INSERT INTO term_category (term_id, category_id) VALUES (%s, %s)", (id, categoryId))


def main():
    terms_arr = saveTerms() 
    
    conn, cur = connect_RDS()
    insertTerm(terms_arr, cur)
    
    commit_RDS(conn)
    disconnect_RDS(conn)
    
    
if __name__ == "__main__":
    main()
