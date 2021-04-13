
class test():
    data0 = 0
    data1 = 1
    data2 = []
    def __init__(self,value=3):
        self.instance = value
a = test()
b = test()
print(a.__dict__)
a.data0 = "data0"
print(a.__dict__)
a.data2.append(1)
print(a.__dict__)
print(test.__dict__)
