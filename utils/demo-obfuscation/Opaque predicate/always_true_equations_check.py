__author__ = 'Alexey'

def modulo():
    '''Check combinations (x, n) for equation (x^n-x) modn == 0. size(x^n) <= 32 bits'''
    couples_x_n = dict()
    for n in range(2, 32):
        x = 1
        while 1:
            x += 1
            if x ** n > 2**32-1:
                couples_x_n[n] = x-1
                #print("%s**%s = %s < 4294967296" % (x-1, n, (x-1)**n))
                break
    #print(couples_x_n)

    false = 0
    true = 0
    for n in couples_x_n.keys():
        for x in range(couples_x_n[n]+1):
            if (x**n - x) % n == 0:
                true += 1
                #print("(%s**%s - %s) mod %s == 0" % (x, n, x, n))
            else:
                false += 1
                #print("(%s**%s - %s) mod %s != 0" % (x, n, x, n))
                #break
    print("Total combinations - %s, True - %s (%s%%), False - %s (%s%%)" % (false+true, true, true*100/float(false+true), false, false*100/float(false+true)))

if __name__ == '__main__':
    modulo()