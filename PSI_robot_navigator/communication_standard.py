from enums import *

codes = [["23019", "32037"], ["32037", "29295"], ["18789", "13603"], ["16443", "29533"], ["18189", "21952"]]

def check_data(data, check_ending=False):

    data_state = Response_status.SUCCESS
    data_len = len(data)
    if(data_len <= 2): 
        data_state = Response_status.WRONG_LEN
        print("Wrong len")
    
    
    if(check_ending and data[data_len-2:data_len] != "\a\b"): # endswith
        data_state = Response_status.WRONG_ENDING
        print(data)
        print(data[data_len-2:data_len])
        print("Wrong endinggg")
    
    return data_state


def extract_data_from_string(s, x, y):
    words = s.split()

    if len(words) == 3:
        if words[0] == "OK":
            try:
                number1 = int(words[1])
                number2 = int(words[2])
                return 0, number1, number2
            except ValueError:
                raise ValueError("Invalid number format")
        elif words[0] == "RECHARGING":
            return 1, x, y
        elif words[0] == "FULL" and words[1] == "POWER":
            return 2, x, y
    raise ValueError("Invalid string format")