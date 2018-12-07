class rectangle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def getperi(self):
        return (self.x+self.y)*2
    def getArea(self):
        return self.x*self.y
class CapStr(str):
    def __new__(cls,  string):#实例化处理？
        string = string.upper()
        return str.__new__(cls, string)
# print (CapStr('pipixia'))
# 输出： PIPIXIA
class C:
    def __init__(self):
        print ("niubia,big brother")
    def __del__(self):#python垃圾回收机制时调用
        print('shabi,sB')
