import pandas as pd

def average_days(start, end):
    #create dataframe
    dates = pd.DataFrame({'start':start,'end':end})
    dates['start'] = pd.to_datetime(dates['start'])
    dates['end'] = pd.to_datetime(dates['end'])

    #calculate difference of start/end dates
    dates['diff'] = dates['end'].dt.date - dates['start'].dt.date
    diff = dates['diff']

    #calculate sum of dates
    sum=0
    for d in diff:
        d = d.days
        d = int(d)
        sum = sum + d

    #calculate average
    average_days = int(sum / len(diff))

    return average_days
