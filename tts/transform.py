class Transform():
    def __init__(self, posX, posY, posZ, rotX, rotY, rotZ, scaleX, scaleY, scaleZ):
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.scaleZ = scaleZ

    def as_dict(self):
        return {
            'posX': self.posX,
            'posY': self.posY,
            'posZ': self.posZ,
            'rotX': self.rotX,
            'rotY': self.rotY,
            'rotZ': self.rotZ,
            'scaleX': self.scaleX,
            'scaleY': self.scaleY,
            'scaleZ': self.scaleZ,
        }
