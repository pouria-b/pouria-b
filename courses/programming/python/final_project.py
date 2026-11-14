import math

selector = ""
error = False
class Final:

    def menu(self):
        return """
****************************
>>>>>>>>>>>>>end<<<<<<<<<<<*
>>>>>>>>>>>>back<<<<<<<<<<<*
****************************
1.adad ha nesbat be ham    *
****************************
2. histogram               *
****************************
3.factorial                *
****************************
4.fibonatchy               *
****************************
5.rectangle /square /circle*
****************************
6.horof sedadar            *
****************************
7.ghabz khone              *
****************************
8.encode / decode          *
****************************
9.search string            *
****************************
10. sms                    *
------------------------"""

    def p1(self):
        global error
        x = input("enter a number for x: ").lower()
        if x == "end":
            exit(0)
        if x == 'back':
            return self.menu()
        x = int(x)
        y = input("enter a number for y: ").lower()
        if y == "end":
            exit(0)
        if  y== 'back':
            return self.menu()
        y = int(y)

        if 10 < y < 20:
            raise TypeError("you enter y between 10 and 20")

        if x < y:
            print("%5s less of %5s" % (x, y))
        elif x > y:
            print("%5s great of %5s" % (x, y))
        else:
            print("%5s equal %5s" % (x, y))

    def p2(self):
        global error
        x = input("enter a number :").lower()
        if x == 'end':
            exit(0)
        if x == 'back':
            return self.menu()
        x = int(x)
        for i in range(1, x+1):
            print(i, ':', end='')
            for j in range(1, i+1):
                if i == 4:
                    print('4', end='')
                else:
                    print("*", end='')
            print()

    def p3(self):
         global error
         x = input("enter a number :").lower()
         if x == 'end':
             exit(0)
         if x == 'back':
             return self.menu()
         x = int(x)
         if x < 0:
             raise ValueError("Factorial requires a nonnegative integer")
         if x == 5:
             raise ValueError ("its value error")
         else:
             e = 1
             for i in range(1, x + 1):
                 e = i * e
             print(e)

    def p4(self):
        global error
        class NumberERROR(Exception):
            pass
        x = input("enter a number for x: ").lower()
        if x == "end":
            exit(0)
        if x == 'back':
            return self.menu()
        x = int(x)
        if x < 0:
            raise ValueError("Fibonacci count must be nonnegative")
        if x == 8 :
            raise NumberERROR("moshkel dary kolan")
        a, b = 1, 1
        for _ in range(x):
            print(a, end=';')
            a, b = b, a + b
        print()

    def p5(self):
        global error
        a = input('enter name:').lower()
        if a == 'end':
            exit(0)
        if a == 'back':
            return self.menu()
        if a == 'circle':
            b = input('enter area or perimeter').lower()
            if b == 'end':
                exit(0)
            if b == 'back':
                return self.menu()
            if b == 'area':
                c = (input('radius')).lower()
                if c == 'end':
                    exit(0)
                if c == 'back':
                    return self.menu()
                c = int(c)
                if c <= 0:
                    raise ValueError("Dimensions must be positive")
                print(c * c * math.pi)
            elif b == 'perimeter':
                c =(input('radius')).lower()
                if c == 'end':
                    exit(0)
                if c == 'back':
                    return self.menu()
                c = int(c)
                if c <= 0:
                    raise ValueError("Dimensions must be positive")
                print(c * 2 * math.pi)

        elif a == 'square':
            b = input('enter area or perimeter').lower()
            if b == 'end':
                exit(0)
            if b == 'back':
                return self.menu()
            if b == 'area':
                c = (input('enter length :')).lower()
                if c == 'end':
                    exit(0)
                if c == 'back':
                    return self.menu()
                c = int(c)
                if c <= 0:
                    raise ValueError("Dimensions must be positive")
                print(c * c)
            elif b == 'perimeter':
                c = (input('enter length :')).lower()
                if c == 'end':
                    exit(0)
                if c == 'back':
                    return self.menu()
                c = int(c)
                if c <= 0:
                    raise ValueError("Dimensions must be positive")
                print(c * 4)

        elif a == 'rectangle':
            b = input('enter area or perimeter').lower()
            if b == 'end':
                exit(0)
            if b == 'back':
                return self.menu()
            if b == 'area':
                c = (input('enter length :')).lower()
                if c == 'end':
                    exit(0)
                if c == 'back':
                    return self.menu()
                c = int(c)
                if c <= 0:
                    raise ValueError("Dimensions must be positive")
                d = (input('enter width :')).lower()
                if d == 'end':
                    exit(0)
                if d == 'back':
                    return self.menu()
                d = int(d)
                if d <= 0:
                    raise ValueError("Dimensions must be positive")
                print(c * d)
            elif b == 'perimeter':
                c = (input('enter length :')).lower()
                if c == 'end':
                    exit(0)
                if c == 'back':
                    return self.menu()
                c = int(c)
                if c <= 0:
                    raise ValueError("Dimensions must be positive")
                d = (input('enter width :')).lower()
                if d == 'end':
                    exit(0)
                if d == 'back':
                    return self.menu()
                d = int(d)
                if d <= 0:
                    raise ValueError("Dimensions must be positive")
                print((c + d) * 2)

    def p6(self):
        global error
        x = input("enter a string :").lower()
        if x == 'end':
            exit(0)
        if x == 'back':
            return self.menu()
        a = e = i = o = u = 0
        for y in x:
            if y =='a':
                a = a + 1
            elif y == 'e':
                e = e + 1
            elif y == 'i':
                i = i + 1
            elif y == 'o':
                o = o + 1
            elif y == 'u':
                u = u + 1
        print('a :   %g' % (a))
        print('e :   %g' % (e))
        print('i :   %g' % (i))
        print('o :   %g' % (o))
        print('u :   %g' % (u))

    def p7(self):
        global error
        sakhtemon = {1: 2, 2: 4, 3: 5, 4: 6, 5: 2, 6: 1, 7: 3, 8: 2}
        ghabz = input('mablagh ra vared konid :')
        if ghabz == 'end':
            exit(0)
        if ghabz == 'back':
            return self.menu()
        ghabz = int(ghabz)
        if ghabz < 0:
            raise ValueError("Bill must be nonnegative")
        tedad_kol = 0
        for x in sakhtemon:
            tedad_kol = tedad_kol + sakhtemon[x]
        harnafar = ghabz/tedad_kol
        for x in sakhtemon:
            print(x, ': $', (sakhtemon[x]*harnafar))

    def p8(self):
        global error
        x = input("enter text or comma-separated code points: ")
        if x == "end":
            exit(0)
        if x == 'back':
            return self.menu()
        y = input("encode or decode: ").lower()
        if y == "end":
            exit(0)
        if y == 'back':
            return self.menu()

        if y == 'encode':
            print(str([ord(char) for char in list(x)]).replace(']', '').replace('[', ''))
        elif y == 'decode':
            decoded_string = ''
            decoded_chars = [chr(int(x)) for x in x.split(',')]
            for x in decoded_chars:
                decoded_string += x
            print(decoded_string)

    def p9(self):
        global error
        x = 0
        x = input("enter a string :").lower()
        if x == 'end':
            exit(0)
        if x == 'back':
            return self.menu()
        s = 'python language tutorials by freezeman'
        char = 'freezeman'
        index = 0
        if 10 <= len(x):
            char = char[0]
            for ch in x:
                if ch in x:
                    index += 1
                if ch == char:
                    print(index)
        else:
            char = char[0]
            for ch in s:
                if ch in s:
                    index += 1
                if ch == char:
                    print(index)

    def p10(self):
        global error
        keyboard = {
            0: [' '],
            1: ['.', ',', '_', ';'],
            2: ['a', 'b', 'c'],
            3: ['d', 'e', 'f'],
            4: ['g', 'h', 'i'],
            5: ['j', 'k', 'l'],
            6: ['m', 'n', 'o'],
            7: ['p', 'q', 'r', 's'],
            8: ['t', 'u', 'v'],
            9: ['w', 'x', 'y', 'z'],
        }

        string = input("enter a text: ").lower()
        if string == "end":
            exit(0)
        if string == 'back':
            return self.menu()
        else:
            key_print = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
            for x in list(string):
                for key, chars in keyboard.items():
                    if x in chars:
                        key_print[key] += chars.index(x) + 1
                        break
                else:
                    raise ValueError(f"Unsupported SMS character: {x!r}")
            print(key_print)

def main():
    global error, selector
    f = Final()
    while True:
        try:
            if not error:
                print(f.menu())
                selector = input("Enter a number for choose program: ").lower()
                if selector == "end":
                    exit(0)
    
            if selector == "1":
                error = False
                f.p1()
    
            elif selector == "2":
                error = False
                f.p2()
    
            elif selector == "3":
                error = False
                f.p3()
    
            elif selector == "4":
                error = False
                f.p4()
    
            elif selector == "5":
                error = False
                f.p5()
    
            elif selector == "6":
                error = False
                f.p6()
    
            elif selector == "7":
                error = False
                f.p7()
    
            elif selector == "8":
                error = False
                f.p8()
    
            elif selector == "9":
                error = False
                f.p9()
    
            elif selector == "10":
                error = False
                f.p10()
    
        except (EOFError, KeyboardInterrupt):
            return
        except Exception as e:
            error = True
            print(e)


if __name__ == "__main__":
    main()
