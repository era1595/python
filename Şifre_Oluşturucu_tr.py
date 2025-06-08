import random

a=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0","!","?",":","@","*","<",">","#"]
b=[]
p= ""
op = False
while True:
    try:
        print("################\nŞifre Oluşturucu\n################\n1-Kolay\n2-Orta\n3-Zor\n4-İmkansız\n5-Çıkış")
        x=int(input("Lütfen birini seçiniz:"))
        if x==1 or x==2 or x==3:
            pass
        elif x==5:
            print("Çıkış yapıldı.")
            break
        elif x==4:
            print("İmkansız modun ana prensibi şifrenin tamamıyla beraber her 3 karakteri kontrol etmektir. Büyük sayılarda bu işlem çok uzun sürebilir bu yüzden karakter sayısı 21'i geçecek şifrelerde optimize bir versiyon kullanılır. Optimize versiyon her 3 karakteri değil karakterleri üçer üçer kontrol eder.")
        else:
            print("Hatalı giriş yapıldı. Tekrar deneyin.")
            continue
        y=int(input("Şifre uzunluğunu giriniz:"))
        if y==1 and x==2 or y<3 and x==3 or y<3 and x==4:
            print("Kodun şifre güvenliği mekanizmasının doğru çalışması için lütfen daha büyük bir sayı girin.")
            continue
        elif y<1:
            print("Hatalı giriş yapıldı. Tekrar deneyin.")
            continue
        elif x==4 and y>21:
            print("Optimize Mod Açık")
            op = True
        else:
            pass
        c=input("Büyük ve küçük karakterler kullanılsın mı(e/h):")
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
            elif c=="H":
                for i in range(y):
                    v=random.randint(0,25)
                    b.append(a[v])
            else:
                print("Hatalı giriş yapıldı. Tekrar deneyin.")
                continue
            print("".join(b))
            b.clear()    
        elif x==2:
            if c=="E":
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
            elif c=="H":
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
                print("Hatalı giriş yapıldı. Tekrar deneyin.")
                continue
            print("".join(b))
            b.clear()
        elif x==3:
            if c=="E":
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
            elif c=="H":
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
                print("Hatalı giriş yapıldı. Tekrar deneyin.")
                continue
            print("".join(b))
            b.clear()
        elif x==4:
            if op==True:
                if c=="E":
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
                elif c=="H":
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
                if c=="E":
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
                elif c=="H":
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
                print("Hatalı giriş yapıldı. Tekrar deneyin.")
                continue
            print("".join(b))
            b.clear()
        elif x==5:
            print("Çıkış yapıldı.")
            break
        else:
            print("Hatalı giriş yapıldı. Tekrar deneyin.")
            continue
    except ValueError:
        print("Hatalı giriş yapıldı. Tekrar deneyin.")
        continue
