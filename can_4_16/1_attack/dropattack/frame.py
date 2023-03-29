class Frame():
    def __init__(self, arb_id, data=[], data_len=0x08, frameType="Standard", frameReq="Data"):
        self.id = arb_id
        self.data = data
        self.data_len = data_len
        self.frameType = frameType
        self.frameReq = frameReq
        self._ErrorNum = 0
        
    def WriteErrorNum(self,ErrorNum):
        self._ErrorNum = ErrorNum
        
    def ReadErrorNum(self):
        return self._ErrorNum