#İstediğiniz şeyi istediğiniz defa otomatik olarak yazmanızı sağlayan bir kod. (fare imlecini ekranın solüstüne götürürseniz program durur)
import pyautogui
import time

pyautogui.FAILSAFE = True

x=input("Yazdırmak İstediğiniz Veriyi Giriniz:")
c=int(input("Kaç Kere Yazdırcağınızı Giriniz:"))
z=float(input("Yazma Hızını Giriniz:"))
y=input("Yazdıktan Sonra Enter Butonuna Basılsın mı (Y/N):")

start_delay = float(input("Yazmaya başlamadan önce kaç saniye beklensin?: "))

print("\nUYARI: Script klavye kontrolünü devralacaktır.")
confirmation = input("Yazma işlemini başlatmak istediğinizden emin misiniz? (E/H): ").strip().upper()

if confirmation == "E":
    if y.upper() == "Y":
        print(f"{start_delay} Saniye Sonra Yazmaya Başlayacak. Durdurmak için fareyi sol üst köşeye çekin.")
        time.sleep(start_delay)
        try:
            for i in range(0,c):
                pyautogui.typewrite(x, interval=0.01)
                pyautogui.press("enter")
                time.sleep(z)
            print("Yazma İşlemi Bitirildi")
        except pyautogui.FailSafeException:
            print("Fare ekranın sol üstüne götürüldü. İşlem durduruldu.")
    elif y.upper() == "N":
        print(f"{start_delay} Saniye Sonra Yazmaya Başlayacak. Durdurmak için fareyi sol üst köşeye çekin.")
        time.sleep(start_delay)
        try:
            for i in range(0,c):
                pyautogui.typewrite(x, interval=0.01)
                time.sleep(z)
            print("Yazma İşlemi Bitirildi")
        except pyautogui.FailSafeException:
            print("Fare ekranın sol üstüne götürüldü. İşlem durduruldu.")
    else:
        print("Geçersiz 'Enter' seçimi. İşlem iptal edildi.")
else:
    print("Yazma işlemi kullanıcı tarafından iptal edildi.")
