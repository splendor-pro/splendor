import os
import json
import pymysql

class DB_SCHEMA:
    '''
    There are two ways to create the database schema.
    The first step is using the automatic method to build.
    And the second step is using the manual way.
    '''
    def __init__(self):
        self.is_manual = False
        # database information
        #self.host_name = "192.168.120.90" # the path of MySQL
        self.host_name = "127.0.0.1"
        self.user_name = "root"
        self.password = "root"
        self.db_name = "xxx"
        # 
        self.target_directory  = ""
        self.target_sql_files = []
        self.has_tables = False
        self.cursor = ""
        # database schema
        self.tables = []
        self.fields = {}
        self.taintable_fields = {}
        self.taint_sites =[]

    def connect(self):
        return pymysql.connect(host=self.host_name, user=self.user_name, password=self.password, database=self.db_name)

    def create_db_schema(self, target_directory=""):
        if self.is_manual:
            print("[!] create database manual")
            return 

        self.target_directory = target_directory
        # create a database name
        self.target_sql_files = self.get_target_sql_files()
        print("[+] Start: "+ self.target_directory + ".....")
        #
        if len(self.target_sql_files) != 0:
            with open("./count", "r") as fh:
                count =  json.load(fh)
            #count = int(count)
            with open("./count", "w") as fh:
                json.dump(count, fh)
            sql_contents = ""
            for f in self.target_sql_files:
                with open(f, 'r') as fh:
                    sql_contents += fh.read()                
            self.init_db(self.get_create_info(sql_contents))
        else:
            print("no sql info...............")
        return self.has_tables

    def db_analysis(self, taintable_check=True):
        # connect the database
        self.cursor = self.connect().cursor()
        #
        _sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='{}';".format(self.db_name)
        self.cursor.execute(_sql)
        res = self.cursor.fetchall()
        self.tables = res
        #
        for i in res:
            table_name = str(i[0])
            col = self.get_column_info(str(i[0]))
            self.fields[table_name] = col
        #
        # check the taintable_fields
        if taintable_check:
            self.get_taintable_fields()

    def get_column_info(self, table_name):
        col_list = []
        col_info = {}
        _sql = "SELECT * FROM information_schema.columns WHERE table_schema='{database}' and table_name='{table}';".format(database=self.db_name, table=table_name)
        self.cursor.execute(_sql)
        res = self.cursor.fetchall()
        for i in res:
            col_info['name'] = i[3]
            col_info['length'] = i[8]
            col_info['type'] = i[7]
            if col_info:
                col_list.append(col_info)
            col_info = {}
        return col_list
    
    def get_taintable_fields(self):
        for k, v in self.fields.items():
            taintable_fields = []
            for i in v:
                _type = str(i['type']).lower()
                _len = i['length']
                if (_type == 'text') or ((_type == 'varchar' or _type == 'char') and _len>=9):
                    taintable_fields.append(i)
            self.taintable_fields[k] = taintable_fields


    def get_create_info(self, sql_contents):
        '''
            collect the create table info into code
        '''
        query_list = []
        #
        for i in sql_contents.split(';'):
            if str(i).strip().upper().find('CREATE') == 0:
               #print(i) 
               #print("-----------")
               query_list.append(i)
        #
        return query_list


    def get_target_sql_files(self):
        '''
            search all of the sql files into the target directoies
        '''
        target_sql_files = []

        if not os.path.isdir(self.target_directory):
            print("[!] the target directory is file")
            exit()

        for r, d, f in os.walk(self.target_directory):
            for file in f:
                if file.endswith(".sql"):
                    target_sql_files.append(os.path.join(r, file))
        return target_sql_files


    def init_db(self, query_info):
        
        #1 clear the datbase(drop and create the db to clear the table)
        db = pymysql.connect(host=self.host_name, user=self.user_name, password=self.password, database=self.db_name)
        cursor = db.cursor()
        drop_ql = "DROP database "+self.db_name
        create_ql = "CREATE database "+self.db_name
        cursor.execute(drop_ql)
        cursor.execute(create_ql)
        cursor.close()
        #
        print("~~~~~~~~~~~~~")
        #2 execute the sql contents
        db = pymysql.connect(host=self.host_name, user=self.user_name, password=self.password, database=self.db_name)
        cursor = db.cursor()
        #
        for i in query_info:
            try:
                #print(i+";")
                cursor.execute(i)
                #print("database init ok")
                self.has_tables = True
            except Exception as e:
                #print(e)
                pass
        #
        cursor.close()


def main():
    target_dir = ""
    if DB_SCHEMA().create_db_schema(target_dir):
        print("ok")
    else:
        print("no")
    


if __name__ == '__main__':
    print("[!] Start to parse the sql file:")
    main()