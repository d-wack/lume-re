from models.datasources.wininterface import WinInterface
from datetime import datetime

def processWinInterface(db_controller, dataPoints, instance_id):
    #print(list(dataPoints))
    wininterface_list = []
    for datapoint in dataPoints:
        wininterface = WinInterface()
        if 'No Data' in datapoint[1]:
            continue
        wininterface.instance_id = instance_id
        wininterface.ds_timestamp = datapoint[0]
        wininterface.ds_datetime = datetime.utcfromtimestamp(datapoint[0]/1000)
        wininterface.BytesSentPerSec = datapoint[1][0]
        wininterface.PacketsOutboundDiscarded = datapoint[1][1]
        wininterface.PacketsReceivedDiscarded = datapoint[1][2]
        wininterface.PacketsReceivedNonUnicastPerSec = datapoint[1][3]
        wininterface.PacketsReceivedUnicastPerSec = datapoint[1][4]
        wininterface.PacketsSentNonUnicastPerSec = datapoint[1][5]
        wininterface.PacketsSentUnicastPerSec = datapoint[1][6]
        wininterface.ReceivedBitsPerSec = datapoint[1][7]
        wininterface.OutboundBitsPerSec = datapoint[1][8]
        wininterface.BytesReceivedPerSec = datapoint[1][9]
        wininterface_list.append(wininterface)
    if len(wininterface_list) > 0:
        db_controller.add_many(wininterface_list)