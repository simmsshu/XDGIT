class test():
    data0 = 0
    def change(self,data):
        self.data0 = data

s = test()
print(s.data0)
s.data0 = 10
s.data1 = "data1"
print(s.data0)
print(s.data1)
print(test.data0)
test.data0 = 20
print(s.data0)
print(test.data0)