import requests
from bs4 import BeautifulSoup

input1 = input("Ne aramak istiyorsunuz: ")
url = "https://www.uludagsozluk.com/k/balina/"
# Web sayfasına GET isteği gönderelim
list1 = []
i = 255
response = requests.get(url)

# İsteğin başarılı olup olmadığını kontrol edelim
if response.status_code == 200:
        # BeautifulSoup ile web sayfasının içeriğini çıkaralım
        soup = BeautifulSoup(response.content, "html.parser")

        # Başlıkları çekmek için uygun HTML etiketlerini kullanalım (örn. <h1>, <h2>, <h3>)
        # Burada örnek olarak sadece h2 başlıklarını alalım
        headers = soup.find_all("div")

        # Başlıkları ekrana yazdıralım
        for header in headers:
            list1.append(header.text)
        for i in range(1):
            print(list1[76])