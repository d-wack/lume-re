from models.datasources.wincpu import WinCPU
from datetime import datetime

def processWinCPU(db_controller, dataPoints,instance_id):
    wincpu_list = []
    for datapoint in dataPoints:
        wincpu = WinCPU()
        if 'No Data' in datapoint[1]:
            continue
        wincpu.instance_id = instance_id
        wincpu.ds_timestamp = datapoint[0]
        wincpu.ds_datetime = datetime.utcfromtimestamp(datapoint[0]/1000)
        wincpu.ProcessorQueueLength = datapoint[1][0]
        wincpu.Frequency_Sys100NS = datapoint[1][1]
        wincpu.CPUBusyPercent = datapoint[1][2]
        wincpu.PercentProcessorTime = datapoint[1][3]
        wincpu_list.append(wincpu)
    if len(wincpu_list) > 0:
        db_controller.add_many(wincpu_list)