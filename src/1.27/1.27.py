from datetime import datetime

class Meta(type):
    def __new__(cls, name, base, attrs):
        attrs['created_at'] = datetime.now() 
        return super().__new__(cls, name, base, attrs)
    

class Example(metaclass=Meta):
    pass

a = Example()

print(a.created_at)
