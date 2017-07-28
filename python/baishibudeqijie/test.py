a=1
def aa():
    global a
    a+=1
    print a
if __name__ == '__main__':
    for i in range(1,10):
        aa()