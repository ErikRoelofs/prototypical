class ComplexType:
    def __init__(self, name, size, shape, bgColor, backside, type, uniqueBack):
        self.name = name
        self.size = size
        self.shape = shape
        self.bgColor = bgColor
        self.backside = backside
        self.type = type
        self.uniqueBack = uniqueBack

    def required_content(self):
        keys = list(self.shape.areas.keys())
        for extra_key in self.bgColor.get_content_keys():
            keys.append(extra_key)
        return keys

    def decide_bg_color(self, object):
        return self.bgColor.get_color(object)

    def decide_back_color(self, object):
        return self.backside.get_color(object)