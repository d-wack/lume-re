from logicmonitor.lm_request import lm_request

def getDataSources(db_controller):
    #TODO : Create Logic for Datasources - May need this in other applications
    lm_resourcePath = '/setting/datasources'
    lm_fields = '?fields=id,name' #LM Filter
    data = lm_request(lm_resourcePath=lm_resourcePath,lm_fields=lm_fields)  # Calls LM API Request
    print(data['items'][0])