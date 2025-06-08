import random

a=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0","!","?",":","@","*","<",">","#"]
b=[]
p= ""
op = False
while True:
    try:
        print("################\nPassword Generator\n################\n1-Easy\n2-Medium\n3-Hard\n4-Impossible\n5-Exit")
        x=int(input("Please select an option:"))
        if x==1 or x==2 or x==3:
            pass
        elif x==5:
            print("Exited.")
            break
        elif x==4:
            print("The main principle of impossible mode is to check every 3 characters along with the entire password. This process can take a very long time for large numbers, so an optimized version is used for passwords that will exceed 21 characters. The optimized version checks characters in groups of three, not every three characters.")
        else:
            print("Invalid input. Please try again.")
            continue
        y=int(input("Enter password length:"))
        if y==1 and x==2 or y<3 and x==3 or y<3 and x==4:
            print("Please enter a larger number for the code's password security mechanism to work correctly.")
            continue
        elif y<1:
            print("Invalid input. Please try again.")
            continue
        elif x==4 and y>21:
            print("Optimized Mode On")
            op = True
        else:
            pass
        c=input("Use upper and lower case characters (y/n):")
        c=c.upper()
        if x==1:
            if c=="E":
                for i in range(y):
                    v=random.randint(0,25)
                    b.append(a[v])
                for i in range(y):
                    v=random.randint(0,1)
                    if v==1:
                        if b[i].isalpha()==True:
                            b[i]=b[i].upper()
                        else:
                            pass
                    else:
                        pass
            elif c=="N":
                for i in range(y):
                    v=random.randint(0,25)
                    b.append(a[v])
            else:
                print("Invalid input. Please try again.")
                continue
            print("".join(b))
            b.clear()
        elif x==2:
            if c=="Y":
                while True:
                    b.clear()
                    for i in range(y):
                        v=random.randint(0,35)
                        b.append(a[v])
                    p=("".join(b))
                    if p.isalpha() or p.isdigit()==True:
                        b.clear()
                        continue
                    else:
                        pass
                    for i in range(y):
                        v=random.randint(0,1)
                        if v==1:
                            if b[i].isalpha()==True:
                                b[i]=b[i].upper()
                            else:
                                pass
                        else:
                            pass
                    break
            elif c=="N":
                while True:
                    b.clear()
                    for i in range(y):
                        v=random.randint(0,35)
                        b.append(a[v])
                    p=("".join(b))
                    if p.isalpha() or p.isdigit()==True:
                        b.clear()
                        continue
                    else:
                        break
            else:
                print("Invalid input. Please try again.")
                continue
            print("".join(b))
            b.clear()
        elif x==3:
            if c=="Y":
                while True:
                    b.clear()
                    for i in range(y):
                        v=random.randint(0,43)
                        b.append(a[v])
                    p=("".join(b))
                    if p.isalnum() or p.isdigit() or p.isalpha()==True:
                        b.clear()
                        continue
                    else:
                        pass
                    for i in range(y):
                        v=random.randint(0,1)
                        if v==1:
                            if b[i].isalpha()==True:
                                b[i]=b[i].upper()
                            else:
                                pass
                        else:
                            pass
                    break
            elif c=="N":
                while True:
                    b.clear()
                    for i in range(y):
                        v=random.randint(0,43)
                        b.append(a[v])
                    p=("".join(b))
                    if p.isalnum() or p.isdigit() or p.isalpha()==True:
                        b.clear()
                        continue
                    else:
                        break
            else:
                print("Invalid input. Please try again.")
                continue
            print("".join(b))
            b.clear()
        elif x==4:
            if op==True:
                if c=="Y":
                    while True:
                        k=-3
                        b.clear()
                        for i in range(y):
                            v=random.randint(0,43)
                            b.append(a[v])
                        for l in range(y//3*2):
                            k=k+3
                            n=b[k]
                            m=b[k+1]
                            j=b[k+2]
                            k2=k
                            if m.isalpha()==True and n.isalpha()==True and j.isalpha() or m.isdigit()==True and n.isdigit()==True and j.isdigit() or m.isalnum()==True and n.isalnum()==True and j.isalnum()==True:
                                for i in range(3):
                                    v=random.randint(0,43)
                                    b[k2]=a[v]
                                    k2=k2+1
                                break
                            else:
                                pass
                            pass
                        for i in range(y):
                            v=random.randint(0,1)
                            if v==1:
                                if b[i].isalpha()==True:
                                    b[i]=b[i].upper()
                                else:
                                    pass
                            else:
                                pass
                        break
                elif c=="N":
                        b.clear()
                        for i in range(y):
                            v=random.randint(0,43)
                            b.append(a[v])
                        while True:
                            k=-3
                            for l in range(y//3*2):
                                k=k+3
                                n=b[k]
                                m=b[k+1]
                                j=b[k+2]
                                k2=k
                                if m.isalpha()==True and n.isalpha()==True and j.isalpha() or m.isdigit()==True and n.isdigit()==True and j.isdigit() or m.isalnum()==True and n.isalnum()==True and j.isalnum()==True:
                                    for i in range(3):
                                        v=random.randint(0,43)
                                        b[k2]=a[v]
                                        k2=k2+1
                                    break
                                else:
                                    pass
                            break
            elif op==False:
                if c=="Y":
                    while True:
                        k=-1
                        b.clear()
                        for i in range(y):
                            v=random.randint(0,43)
                            b.append(a[v])
                        for l in range(y//3*2):
                            k=k+1
                            n=b[k]
                            m=b[k+1]
                            j=b[k+2]
                            k2=k
                            if m.isalpha()==True and n.isalpha()==True and j.isalpha() or m.isdigit()==True and n.isdigit()==True and j.isdigit() or m.isalnum()==True and n.isalnum()==True and j.isalnum()==True:
                                for i in range(3):
                                    v=random.randint(0,43)
                                    b[k2]=a[v]
                                    k2=k2+1
                                break
                            else:
                                pass
                            pass
                        for i in range(y):
                            v=random.randint(0,1)
                            if v==1:
                                if b[i].isalpha()==True:
                                    b[i]=b[i].upper()
                                else:
                                    pass
                            else:
                                pass
                        break
                elif c=="N":
                        b.clear()
                        for i in range(y):
                            v=random.randint(0,43)
                            b.append(a[v])
                        while True:
                            k=-1
                            for l in range(y//3*2):
                                k=k+1
                                n=b[k]
                                m=b[k+1]
                                j=b[k+2]
                                k2=k
                                if m.isalpha()==True and n.isalpha()==True and j.isalpha() or m.isdigit()==True and n.isdigit()==True and j.isdigit() or m.isalnum()==True and n.isalnum()==True and j.isalnum()==True:
                                    for i in range(3):
                                        v=random.randint(0,43)
                                        b[k2]=a[v]
                                        k2=k2+1
                                    break
                                else:
                                    pass
                            break
            else:
                print("Invalid input. Please try again.")
                continue
            print("".join(b))
            b.clear()
        elif x==5:
            print("Exited.")
            break
        else:
            print("Invalid input. Please try again.")
            continue
    except ValueError:
        print("Invalid input. Please try again.")
        continue
