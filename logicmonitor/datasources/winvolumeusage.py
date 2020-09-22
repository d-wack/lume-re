from models.datasources.winvolumeusage import WinVolumeUsage
from datetime import datetime

def processWinVolumeUsage(db_controller, dataPoints, instance_id):
    #print(list(dataPoints))
    winvolumeusage_list = []
    for datapoint in dataPoints:
        winvolumeusage = WinVolumeUsage()
        if 'No Data' in datapoint[1]:
            continue
        winvolumeusage.instance_id = instance_id
        winvolumeusage.ds_timestamp = datapoint[0]
        winvolumeusage.ds_datetime = datetime.utcfromtimestamp(datapoint[0]/1000)
        winvolumeusage.Capacity = datapoint[1][0]
        winvolumeusage.FreeSpace = datapoint[1][1]
        winvolumeusage.PercentUsed = datapoint[1][2]
        winvolumeusage_list.append(winvolumeusage)
    if len(winvolumeusage_list) > 0:
        db_controller.add_many(winvolumeusage_list)