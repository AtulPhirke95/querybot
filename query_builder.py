import db_processor as db
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import simpledialog

def select_clause(user_query,intent_name,entities_extraction_results,table_name,date_entity):
    """
        This function is used to create select caluse template and returns select column_name from table where 1=1
    """
    
    select_count_query = "SELECT "
    team_list = []
    category_list = []

    for i,j in entities_extraction_results :
        """
            This for loop is used to add column names which in turn used with aggregate function so that the same columns are used with group by syntax.
        """
        if i == 'TEAM' and 'TEAM' not in team_list:
            select_count_query =  select_count_query + "{}".format("TEAM, ")
            team_list.append('TEAM')
        elif i == 'FAILURECATEGORY' and 'FAILURECATEGORY' not in category_list:
            select_count_query =  select_count_query + "{}".format("FAILURECATEGORY, ")
            category_list.append('FAILURECATEGORY')
            
    select_count_query = select_count_query + "{}(*) from {} where 1=1".format(intent_name,table_name)

    return select_count_query

def where_clause(select_count_query,user_query,intent_name,entities_extraction_results,table_name,date_entity):
    """
        This function is used to create where clause
    """
    teams=[]
    category=[]
    executiondates=[]
    failedlogs = []

    """
        Checking if any entities are there in user query and seperate them by saving in respective list
    """
    for i,j in entities_extraction_results :
        if i == 'TEAM':
            teams.append(j)
        elif i == 'FAILURECATEGORY':
            category.append(j)
        elif i == 'EXECUTIONDATE':
            executiondates.append(j)
        elif i == 'FAILURELOGS':
            failedlogs.append(j)
            
    count=0   #used for adjusting the syntax used for IN()
    s1="TEAM IN("
    
    for i in teams:
        if i in ["cnd","collections and disbursement","inex"]:
            i = "Collections and Disbursement"
        elif i in ["commission","provision"]:
            i = "Provision"
        elif i in ["motor","kraft"]:
            i = "Motor"
        elif i in ["claims","schaden"]:
            i = "Claims"
        elif i in ["leben","life"]:
            i = "Life"
        if count == 0:
            s1=s1+"\'{}\'".format(i)
        else:
            s1 = s1 + ",\'{}\'".format(i)
        count=count+1
        
    s1=s1 +")"
    
    count=0
    s2="FAILURECATEGORY IN("
    
    for i in category:
        if count==0:
            s2=s2+"\'{}\'".format(i)
        else:
            s2 =s2 +",\'{}\'".format(i)
        count=count+1
    s2 = s2+")"
    
    flag = 0
    count_1 = 0
    for i,j in entities_extraction_results :
        if(i=='TEAM' or i=="FAILURECATEGORY"):
            continue
        elif i == 'FAILURELOGS':
            if len(failedlogs)>1:
                if count_1==len(failedlogs)-1:
                    select_count_query = select_count_query + "{} LIKE \'%{}%\'".format(i,j)
                else:
                    select_count_query = select_count_query + " and {} LIKE \'%{}%\' or ".format(i,j)
                count_1 = count_1 + 1
            else:
                select_count_query = select_count_query + " and {} LIKE \'%{}%\'".format(i,j)
        else:
            select_count_query = select_count_query + " and {} = \'{}\'".format(i,j)
            
    if count_1 == 0:
        """
            Group by syntax can not be used if user query contains multiple failure category so count_1 is used. if count_1 is 0 then do not append team or category in where clause else append it.
            If there is only one failure category then team in() or category in() can be append to where clause
        """
        if(len(teams)>0):
            select_count_query = select_count_query + " and {} ".format(s1)
        
        if(len(category)>0):
            select_count_query = select_count_query + " and {} ".format(s2)
      
    return teams,category,select_count_query

def group_by_clause(select_count_query,teams,category):
    
    if len(teams)>0 and len(category)==0:
        select_count_query = select_count_query +" group by "
        select_count_query =  select_count_query + "{}".format("TEAM")
        
    elif len(teams)>0 and len(category)>0:
        select_count_query = select_count_query +" group by "
        select_count_query =  select_count_query + "{}".format("TEAM,FAILURECATEGORY")
        
    elif len(teams)==0 and len(category)>0:
        select_count_query = select_count_query +" group by "
        select_count_query =  select_count_query + "{}".format("FAILURECATEGORY")

    return select_count_query


def analysed_query_builder(select_count_query,user_query,intent_name,entities_extraction_results,table_name,date_entity,null_string):
    select_count_query = select_clause(user_query,intent_name,entities_extraction_results,table_name,date_entity)
    
    teams=[]
    executiondates=[]
    failedlogs = []
    
    for i,j in entities_extraction_results :
        if i == 'TEAM':
            teams.append(j)
        elif i == 'EXECUTIONDATE':
            executiondates.append(j)
            
    count=0
    s1="TEAM IN("
    
    for i in teams:
        if i in ["cnd","collections and disbursement","inex"]:
            i = "Collections and Disbursement"
        elif i in ["commission","provision"]:
            i = "Provision"
        elif i in ["motor","kraft"]:
            i = "Motor"
        elif i in ["claims","schaden"]:
            i = "Claims"
        elif i in ["leben","life"]:
            i = "Life"
            
        if count == 0:
            s1=s1+"\'{}\'".format(i)
        else:
            s1 = s1 + ",\'{}\'".format(i)
        count=count+1
        
    s1=s1 +")"
    
    for i,j in entities_extraction_results :
        if(i=='TEAM'):
           continue
        elif i == 'EXECUTIONDATE':
            select_count_query = select_count_query + " and {} = \'{}\'".format(i,j)
            
    if len(teams)>0:
        select_count_query = select_count_query + " and " + s1 + " and {} IS {}".format("FAILURECATEGORY",null_string)
        select_count_query = select_count_query + " group by {}".format("TEAM")
    else:
        select_count_query = select_count_query + " and {} IS {}".format("FAILURECATEGORY",null_string)
        
    return select_count_query


def query_builder(user_query,intent_name,entities_extraction_results,table_name,date_entity):
    if intent_name == 'count':
        if (len(entities_extraction_results)==0):
            if 'not analysed' in user_query or 'not filled' in user_query or 'empty' in user_query or 'not analyzed' in user_query:
                select_count_query = "SELECT {}(*) FROM {} WHERE FAILURECATEGORY IS NULL".format(intent_name,table_name)
                return select_count_query
            
            elif 'analysed' in user_query or 'filled' in user_query or 'not empty' in user_query or 'analyzed' in user_query:
                select_count_query = "SELECT {}(*) FROM {} WHERE FAILURECATEGORY IS NOT NULL".format(intent_name,table_name)
                return select_count_query
            
            else:
                root = Tk()
                root.withdraw()
                x = simpledialog.askstring("Suggestions:Yes/No","Sorry we can not identify your request but you can try out asking some different things.do you want to try?", parent=root)
                root.destroy()
                if(x!=None):
                    if('yes'in x or "yeah" in x or "yup" in x or "sure" in x):
                        root = Tk()
                        root.withdraw()
                        #decision_count = input("queryBot : Press 1 for team or module wise, 2 for failure category wise and 3 for both").lower()
                        decision_count = simpledialog.askstring("Suggestions:1/2/3","Press 1 for team or module wise, 2 for failure category wise and 3 for both", parent=root)
                        root.destroy()
                        if(decision_count == '1'):
                             select_count_query = "SELECT {},{}(*) FROM {} GROUP BY {}".format('TEAM',intent_name,table_name,'TEAM')
                             return select_count_query
                        elif (decision_count == '2'):
                            select_count_query = "SELECT {}, {}(*)  FROM {} GROUP BY {}".format('FAILURECATEGORY',intent_name,table_name,'FAILURECATEGORY')
                            return select_count_query
                        elif (decision_count == '3'):
                            select_count_query = "SELECT {},{},{}(*) FROM {} GROUP BY {}, {}".format('TEAM','FAILURECATEGORY',intent_name,table_name,'TEAM','FAILURECATEGORY')
                            return select_count_query
                        else:
                            return "queryBot : You have not choosed the specified option. Please try entering your query again. "
                        
                    elif('no' in x or 'nope' in x or 'not' in x or "not interested"):
                        return "queryBot : try some other queries."
                    
                    else:
                        return "queryBot : try asking something different"
                else:
                    return "queryBot : try asking something different"
                
        elif (len(entities_extraction_results)>0):
            
            if 'not analysed' in user_query or 'not filled' in user_query or 'empty' in user_query or 'not analyzed' in user_query:
                select_count_query = select_clause(user_query,intent_name,entities_extraction_results,table_name,date_entity)
                null_string = 'NULL'
                select_count_query = analysed_query_builder(select_count_query,user_query,intent_name,entities_extraction_results,table_name,date_entity,null_string)        
                return select_count_query
            
            elif 'analysed' in user_query or 'filled' in user_query or 'not empty' in user_query or 'analyzed' in user_query:
                select_count_query = select_clause(user_query,intent_name,entities_extraction_results,table_name,date_entity)
                null_string = 'NOT NULL'
                select_count_query = analysed_query_builder(select_count_query,user_query,intent_name,entities_extraction_results,table_name,date_entity,null_string)
                return select_count_query
            
            else :
                select_count_query = select_clause(user_query,intent_name,entities_extraction_results,table_name,date_entity)
                teams,category,select_count_query = where_clause(select_count_query,user_query,intent_name,entities_extraction_results,table_name,date_entity)
                select_count_query = group_by_clause(select_count_query,teams,category)
                return select_count_query

    elif intent_name == 'min':
        #x = input("Ohh so you are looking for minimum count. We provides below options. Please select one of them to proceed. Do you want to proceed?").lower()
        root = Tk()
        root.withdraw()
        x = simpledialog.askstring("Suggestions:Yes/No","Ohh so you are looking for minimum count. We provides below options. Please select one of them to proceed. Do you want to proceed?", parent=root)
        root.destroy()
        if x!=None:
            if('yes'in x or "yeah" in x or "yup" in x or "sure" in x):
                root = Tk()
                root.withdraw()
                decision_count = simpledialog.askstring("Suggestions:1/2/3","1 for minimum team wise. 2 for minimum failurecategorywise. 3 for minimum number of test cases failed for particular team and category.", parent=root)
                root.destroy()
                #decision_count = input("queryBot : 1 for maximum team wise. 2 for minimum failurecategorywise. 3 for minimum number of test cases failed for particular team and category.").lower()
                if(decision_count == '1'):
                    select_count_query = "SELECT TOP 1 {},{}(*) FROM {} GROUP BY {} ORDER BY COUNT(*)".format('TEAM','count',table_name,'TEAM')
                    return select_count_query
                elif (decision_count == '2'):
                    select_count_query = "SELECT TOP 1 {},{}(*) FROM {} where failurecategory is not null GROUP BY {} ORDER BY COUNT(*)".format('FAILURECATEGORY','count',table_name,'FAILURECATEGORY')
                    return select_count_query
                elif (decision_count == '3'):
                    teams_min=[]
                    query_display=[]
                    for i,j in entities_extraction_results :
                        if i == 'TEAM':
                            teams_min.append(j)
                        
                    if len(teams_min)>0:
                        for i in teams_min:
                            select_count_query = ""
                            if i in ["cnd","collections and disbursement","inex"]:
                                i = "Collections and Disbursement"
                            elif i in ["commission","provision"]:
                                i = "Provision"
                            elif i in ["motor","kraft"]:
                                i = "Motor"
                            elif i in ["claims","schaden"]:
                                i = "Claims"
                            elif i in ["leben","life"]:
                                i = "Life"
                            select_count_query = "select top 1 team,failurecategory, count(*) from faileddata where team =\'{}\' and failurecategory is not null group by team,failurecategory order by count(*)".format(i)
                            query_display.append(db.db_processor(select_count_query))
                        return query_display
                    else:
                        return "queryBot : No records found"

                else:
                    return "queryBot : try asking something different"
            elif('no'in x or 'nope' in x or 'not' in x or "not interested"):
                return "queryBot : try asking something different"
        else:
            return "queryBot : try asking something different"
        
    elif intent_name == 'max':
        #x = input("Ohh so you are looking for maximum count. We provides below options. Please select one of them to proceed. Do you want to proceed?").lower()
        root = Tk()
        root.withdraw()
        x = simpledialog.askstring("Suggestions:Yes/No","Ohh so you are looking for maximum count. We provides below options. Please select one of them to proceed. Do you want to proceed?", parent=root)
        root.destroy()
        if x != None:
            if('yes'in x or "yeah" in x or "yup" in x or "sure" in x):
                #decision_count = input("queryBot : 1 for maximum team wise. 2 for maximum failurecategorywise. 3 for maximum number of test cases failed for particular team and category.").lower()
                root = Tk()
                root.withdraw()
                decision_count = simpledialog.askstring("Suggestions:1/2/3","1 for maximum team wise. 2 for maximum failurecategorywise. 3 for maximum number of test cases failed for particular team and category.", parent=root)
                root.destroy()
                if(decision_count == '1'):
                    select_count_query = "SELECT TOP 1 {},{}(*) FROM {} GROUP BY {} ORDER BY COUNT(*) DESC".format('TEAM','count',table_name,'TEAM')
                    return select_count_query
                elif (decision_count == '2'):
                    select_count_query = "SELECT TOP 1 {},{}(*) FROM {} WHERE failurecategory is not null GROUP BY {} ORDER BY COUNT(*) DESC".format('FAILURECATEGORY','count',table_name,'FAILURECATEGORY')
                    return select_count_query
                elif (decision_count == '3'):
                    teams_max=[]
                    query_display=[]
                    for i,j in entities_extraction_results :
                        if i == 'TEAM':
                            teams_max.append(j)
                        
                    if len(teams_max)>0:
                        for i in teams_max:
                            select_count_query = ""
                            if i in ["cnd","collections and disbursement","inex"]:
                                i = "Collections and Disbursement"
                            elif i in ["commission","provision"]:
                                i = "Provision"
                            elif i in ["motor","kraft"]:
                                i = "Motor"
                            elif i in ["claims","schaden"]:
                                i = "Claims"
                            elif i in ["leben","life"]:
                                i = "Life"
                            select_count_query = "select top 1 team,failurecategory, count(*) from faileddata where team =\'{}\' and failurecategory is not null group by team,failurecategory order by count(*) desc".format(i)
                            query_display.append(db.db_processor(select_count_query))
                            #return query_display
                            #show_results.show_query_result(query_display)
                        return query_display
                    else:
                        return "queryBot : No records found"

                else:
                    return "queryBot : try asking something different"
            elif('no'in x or 'nope' in x or 'not' in x or "not interested"):
                return "queryBot : try asking something different"
        else:
            return "queryBot : try asking something different"
            
        
