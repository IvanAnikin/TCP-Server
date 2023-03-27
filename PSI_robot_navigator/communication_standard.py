from enums import *

codes = [["23019", "32037"], ["32037", "29295"], ["18789", "13603"], ["16443", "29533"], ["18189", "21952"]]

def check_data(data):

    data_state = Response_status.SUCCESS
    data_len = len(data)
    if(data_len <= 2):
        data_state = Response_status.WRONG_LEN
        print("Wrong len")
    if(data[data_len-2:data_len] != "\a\b"):
        data_state = Response_status.WRONG_ENDING
        print("Wrong endinggg")

    return data_state