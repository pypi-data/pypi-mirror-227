istek = input("İşlem giriniz: ")
istek = istek.lower().strip()

if "yazdır" in istek:
    yazi = istek.replace("yazdır","")
    print(yazi)

elif "liste" in istek:
    print("list1 = []")

elif "fonksiyon" in istek:
    ad = input("adı ne olsun: ")

elif "input" in istek:
    type1 = input("inputunuz string mi yoksa integer mı: ")
    if "string" in type1 or "str" in type1:
        print("input1 = input("")")
    elif "integer" in type1 or "int" in type1:
        print("input1 = int(input(""))")

