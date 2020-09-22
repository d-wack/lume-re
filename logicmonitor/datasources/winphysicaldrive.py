from models.datasources.winphysicaldrive import WinPhysicalDrive
from datetime import datetime

def processWinPhysicalDrive(db_controller, dataPoints, instance_id):
    #print(list(dataPoints))
    winphyscialdrive_list = []
    for datapoint in dataPoints:
        winphyscialdrive = WinPhysicalDrive()
        if 'No Data' in datapoint[1]:
            continue
        winphyscialdrive.instance_id = instance_id
        winphyscialdrive.ds_timestamp = datapoint[0]
        winphyscialdrive.ds_datetime = datetime.utcfromtimestamp(datapoint[0]/1000)
        winphyscialdrive.AvgDiskSecPerRead = datapoint[1][0]
        winphyscialdrive.AvgDiskSecPerWrite = datapoint[1][1]
        winphyscialdrive.CurrentDiskQueueLength = datapoint[1][2]
        winphyscialdrive.DiskReadBytesPerSec = datapoint[1][3]
        winphyscialdrive.DiskReadsPerSec = datapoint[1][4]
        winphyscialdrive.DiskWriteBytesPerSec = datapoint[1][5]
        winphyscialdrive.DiskWritesPerSec = datapoint[1][6]
        winphyscialdrive.Frequency_PerfTime = datapoint[1][7]
        winphyscialdrive.PercentDiskReadTime = datapoint[1][8]
        winphyscialdrive.PercentDiskWriteTime = datapoint[1][9]
        winphyscialdrive.PercentIdleTime = datapoint[1][10]
        winphyscialdrive.SplitIOPercent = datapoint[1][11]
        winphyscialdrive.SplitIOPerSec = datapoint[1][12]
        winphyscialdrive_list.append(winphyscialdrive)
    if len(winphyscialdrive_list) > 0:
        db_controller.add_many(winphyscialdrive_list)