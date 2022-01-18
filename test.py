class Test():
    def __init__(self, acc):
        self.acc = acc

test = Test(acc=23)

setattr(test,'cc',25) 
print(test.cc)