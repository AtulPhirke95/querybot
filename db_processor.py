import pyodbc
def db_processor(query):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\atul.narayan.phirke\Desktop\chatbot_training\archieve_querybot\db1.accdb;')
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            #print (row)
            result.append(row)
        return result
    except TypeError:
        print("queryBot : Please try entering different queries in db")

#db_processor('select top 1 count(*) from faileddata')  
#db_processor('select top 1 team,failurecategory, count(*) from faileddata where team = \'kranken\'  group by team,failurecategory order by count(*)')

##select AA.ACount,BB.BCount from (select count(*) as ACount from failedData where 1=1 AND team = \'motor\' AND failureCategory = \'data issue\') AA,(select count(*) as BCount from failedData where 1=1 AND team = \'claims\' AND failureCategory = \'functional defect\') BB;

##select AA.ACount,BB.BCount,CC.CCount,DD.DCount
##from 
##(select count(*) as ACount from Customers where 1=1 AND City = 'México D.F.' AND Country = 'Mexico') AA 
##,(select count(*) as BCount from Customers where 1=1 AND City = 'México D.F.' AND Country = 'Mexico') BB 
##,(select count(*) as CCount from Customers where 1=1 AND City = 'México D.F.' AND Country = 'Mexico') CC 
##,(select count(*) as DCount from Customers where 1=1 AND City = 'México D.F.' AND Country = 'Mexico') DD 
##;
