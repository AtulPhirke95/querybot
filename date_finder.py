from date_extractor import extract_dates
def date_picker(user_query):
    dates = extract_dates(u'{}'.format(user_query))
    if(len(dates)==1):
        dates = str(dates[0])
        dates = dates.split(" ")
        return dates[0]
    elif len(dates)==1 :
        return dates
