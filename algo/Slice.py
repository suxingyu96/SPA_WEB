class Slice:
    XUpper = None
    XLower = None
    YUpper = None
    YLower = None
    Area = None

    def __init__(self, XUpper, XLower, YUpper, YLower):
        self.XUpper = XUpper
        self.XLower = XLower
        self.YUpper = YUpper
        self.YLower = YLower
        self.Area = self.getArea()

    def getArea(self):
        return (self.XUpper - self.XLower) * (self.YUpper - self.YLower)