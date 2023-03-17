import enum


class Response_status(enum.Enum):
    SUCCESS = 1
    WRONG_LEN = 2
    WRONG_ENDING = 3
    WRONG_CODE = 4
    
    def show(self):
        if self == self.SUCCESS:
            print("SUCCESS")
        if self == self.WRONG_LEN:
            print("WRONG_LEN")
        if self == self.WRONG_ENDING:
            print("WRONG_ENDING")
        if self == self.WRONG_CODE:
            print("WRONG_CODE")

class Connection_status(enum.Enum):
    BEFORE_USERNAME = 1
    KEY_REQUEST_SENT = 2
    KEY_SHARED = 3
    KEY_SHARED_2 = 4
    POSITION_KNOWN = 5
    
    def show(self):
        if self == self.BEFORE_USERNAME:
            print("BEFORE_USERNAME")
        if self == self.KEY_REQUEST_SENT:
            print("KEY_REQUEST_SENT")
        if self == self.KEY_SHARED:
            print("KEY_SHARED")
        if self == self.KEY_SHARED_2:
            print("KEY_SHARED_2")
        if self == self.POSITION_KNOWN:
            print("POSITION_KNOWN")

class Client_status(enum.Enum):
    BEFORE_USERNAME = 1
    USERNAME_SENT = 2
    KEY_SENT = 3
    KEY_APPROVED = 4
    
    def show(self):
        if self == self.BEFORE_USERNAME:
            print("BEFORE_USERNAME")
        if self == self.USERNAME_SENT:
            print("USERNAME_SENT")
        if self == self.KEY_SENT:
            print("KEY_SENT")
        if self == self.KEY_APPROVED:
            print("KEY_APPROVED")

