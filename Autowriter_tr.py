#İstediğiniz şeyi istediğiniz defa otomatik olarak yazmanızı sağlayan bir kod. (fare imlecini ekranın solüstüne götürürseniz program durur)
import pyautogui
import time

pyautogui.FAILSAFE = True

x=input("Yazdırmak İstediğiniz Veriyi Giriniz:")
c=int(input("Kaç Kere Yazdırcağınızı Giriniz:"))
z=float(input("Yazma Hızıni Giriniz:"))
y=input("Yazdıktan Sonra Enter Butonuna Basılsın mı (Y/N):")

print("\nUYARI: Script klavye kontrolünü devralacaktır.")
confirmation = input("Yazma işlemini başlatmak istediğinizden emin misiniz? (E/H): ").strip().upper()

if confirmation == "E":
    if y.upper() == "Y":
        print("5 Saniye Sonra Yazmaya Başlayacak. Durdurmak için fareyi sol üst köşeye çekin.")
        time.sleep(5)
        for i in range(0,c):
            pyautogui.typewrite(x)
            pyautogui.press("enter")
            time.sleep(z)
        print("Yazma İşlemi Bitirildi")
    elif y.upper() == "N":
        print("5 Saniye Sonra Yazmaya Başlayacak. Durdurmak için fareyi sol üst köşeye çekin.")
        time.sleep(5)
        for i in range(0,c):
            pyautogui.typewrite(x)
            time.sleep(z)
        print("Yazma İşlemi Bitirildi")
    else:
        print("Geçersiz 'Enter' seçimi. İşlem iptal edildi.")
else:
    print("Yazma işlemi kullanıcı tarafından iptal edildi.")
