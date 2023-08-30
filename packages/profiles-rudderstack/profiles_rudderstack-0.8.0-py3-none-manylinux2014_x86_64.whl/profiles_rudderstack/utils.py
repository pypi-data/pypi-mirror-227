class RefManager:
    def __init__(self):
        self.refsDict = {}
        self.refId = 1

    def createRef(self, obj):
        refId = self.refId
        self.refsDict[refId] = obj
        self.refId += 1
        return refId
    
    def createRefWithKey(self, key, obj):
        self.refsDict[key] = obj
        return key
    
    def getRef(self, refId):
        return self.refsDict.get(refId, None)
    