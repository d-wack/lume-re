from models.datasources.winmemory import WinMemory
from datetime import datetime

def processWinMemory(db_controller, dataPoints, instance_id):
    #print(list(dataPoints))
    winmemory_list = []
    for datapoint in dataPoints:
        winmemory = WinMemory()
        if 'No Data' in datapoint[1]:
            continue
        winmemory.instance_id = instance_id
        winmemory.ds_timestamp = datapoint[0]
        winmemory.ds_datetime = datetime.utcfromtimestamp(datapoint[0]/1000)
        winmemory.FreePhysicalMemory = datapoint[1][0]
        winmemory.FreeSpaceInPagingFiles = datapoint[1][1]
        winmemory.NumberOfProcesses = datapoint[1][2]
        winmemory.SizeStoredInPagingFiles = datapoint[1][3]
        winmemory.TotalVisibleMemorySize = datapoint[1][4]
        winmemory.MemoryUtilizationPercent = datapoint[1][5]
        winmemory.PercentVirtualMemoryInUse = datapoint[1][6]
        winmemory.FreeVirtualMemory = datapoint[1][7]
        winmemory.TotalVirtualMemorySize = datapoint[1][8]
        winmemory_list.append(winmemory)
    if len(winmemory_list) > 0:
        db_controller.add_many(winmemory_list)