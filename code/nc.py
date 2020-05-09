import time

a = 3

def unicometodo():
    global a
    while True:
        a += 1
        print (a)
        devuelveA()
        time.sleep(1)


def devuelveA():
    global a
    archivo = open("a.txt","w")
    archivo.write(str(a))
    archivo.close()

def main():

    unicometodo()


if __name__ == '__main__':
    main()

