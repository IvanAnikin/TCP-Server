from enums import *

codes = [["23019", "32037"], ["32037", "29295"], ["18789", "13603"], ["16443", "29533"], ["18189", "21952"]]

def check_data(data, check_ending=False):

    data_state = Response_status.SUCCESS
    data_len = len(data)
    if(data_len <= 0): # 2
        data_state = Response_status.WRONG_LEN
        print("Wrong len")
    
    
    if(check_ending and data[data_len-2:data_len] != "\a\b"): # endswith
        data_state = Response_status.WRONG_ENDING
        print(data)
        print(data[data_len-2:data_len])
        print("Wrong endinggg")
    
    return data_state


def extract_data_from_string(s):
    words = s.split()

    if len(words) == 3:
        if words[0] == "OK":
            state = 0
            try:
                number1 = int(words[1])
                number2 = int(words[2])
                return state, number1, number2
            except ValueError:
                raise ValueError("Invalid number format")
        elif words[0] == "RECHARGING":
            state = 1
            return state, None, None
        elif words[0] == "FULL" and words[1] == "POWER":
            state = 2
            return state, None, None
    raise ValueError("Invalid string format")
    
'''
def extract_numbers_from_string(s):
    # split the string into words
    words = s.split()
    
    # check if the string is in the right format
    if len(words) != 3 or words[0] != "OK":
        raise ValueError("Invalid string format")
    
    # extract the numbers
    try:
        number1 = int(words[1])
        number2 = int(words[2])
        return number1, number2, state
    except ValueError:
        raise ValueError("Invalid number format")
        '''