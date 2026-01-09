import datetime

def Date2Stamp(dateIn):
    if dateIn == None:
        return 0
    else:
        dt = datetime.strptime(dateIn, "%Y-%m-%dT%H:%M:%SZ")
        timestamp = dt.timestamp()
        return timestamp
    
def dateFromAfas(AfasDate, astimestamp = False):
    T = 'T' if 'T' in AfasDate else ' '
    if 'Z' in AfasDate:
        dt = datetime.strptime(AfasDate, f"%Y-%m-%d{T}%H:%M:%SZ")
    else:
        temp = AfasDate.split(':')
        if len(temp) == 3:
            dt = datetime.strptime(AfasDate, f"%Y-%m-%d{T}%H:%M:%S")
        elif len(temp) == 2:
            dt = datetime.strptime(AfasDate, f"%Y-%m-%d{T}%H:%M")
        elif len(temp) == 1:
            dt = datetime.strptime(AfasDate, "%Y-%m-%d")
    if astimestamp: dt = dt.timestamp()
    return dt