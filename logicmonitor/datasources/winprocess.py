from models.datasources.winprocess import WinProcess
from datetime import datetime

def processWinProcess(db_controller, dataPoints, instance_id):
    #print(list(dataPoints))
    winprocess_list = []
    for datapoint in dataPoints:
        winprocess = WinProcess()
        if 'No Data' in datapoint[1]:
            continue
        winprocess.instance_id = instance_id
        winprocess.ds_timestamp = datapoint[0]
        winprocess.ds_datetime = datetime.utcfromtimestamp(datapoint[0]/1000)
        winprocess.HandleCount = datapoint[1][0]
        winprocess.ProcessesCount = datapoint[1][1]
        winprocess.ThreadCount = datapoint[1][2]
        winprocess.WorkingSet = datapoint[1][3]
        winprocess_list.append(winprocess)
    if len(winprocess_list) > 0:
        db_controller.add_many(winprocess_list)