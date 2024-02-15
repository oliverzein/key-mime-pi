from zero_hid import Keyboard, Mouse

k = Keyboard()
k.set_layout(language='DE_ASCII')
#k.type("Hello world! zzz #+\\")

""" with Mouse() as m:
    for i in range(5):
        m.move(5,5) """
        
with Mouse() as m:
    m.move(5,0)
    m.move(0,-5)
    m.move(-5,0)
    m.move(0,5)