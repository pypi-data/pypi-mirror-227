#prepared by Aras Tokdemir

def wix():
    import random
    import webbrowser
    import time
    import getpass
    import wikipedia
    import json
    from getpass import getpass
    import socket
    import string
    import os

    # Modelin yanıtlarını içeren bir sözlük
    responses = {
        "merhaba": "Merhaba, nasıl yardımcı olabilirim?",
        "sa": "as",
        "nasılsınız": "Ben bir algoritma olduğum için hissetmiyorum, ama teşekkür ederim, iyiyim!",
        "naber": "Ben bir algoritma olduğum için hissetmiyorum, ama teşekkür ederim, iyiyim!",
        "güle güle": "Hoşça kalın!",
        "teşekkür ederim": "Rica ederim, yardımcı olabildiysem ne mutlu bana!",
        "diğerleri": "Üzgünüm, bu konuda henüz bilgim yok. Başka bir soru sormak ister misiniz?",
        "python öğrenmek istiyorum": "Python öğrenmek harika bir seçim! Başlamak için online kaynaklara göz atabilirsiniz, Python öğrenmeye başlamak için birçok ücretsiz kaynak bulunmaktadır. İyi bir başlangıç noktası olarak Python belgelerine bakabilirsiniz.",
        "programlama dilleri": "Programlama dilleri, yazılım geliştirme için kullanılan araçlardır. Bazı popüler programlama dilleri Python, Java, C++, JavaScript, Ruby vb. şeklinde sıralanabilir. Programlama dilleri, bilgisayarlara talimatlar vermek ve yazılım oluşturmak için kullanılan yapılardır. Her dilin kendine özgü özellikleri ve kullanım alanları vardır.",
        "yapay zeka nedir": "Yapay zeka, bilgisayar sistemlerinin insan benzeri zekaya sahip olmasını amaçlayan bir alanı ifade eder. Makine öğrenmesi, derin öğrenme, doğal dil işleme gibi teknikler kullanarak bilgisayarların öğrenme, anlama ve karar verme yetenekleri geliştirilmeye çalışılır. Yapay zeka, bilgisayar sistemlerine insan benzeri zeka ve öğrenme yetenekleri kazandırmayı hedefleyen bir alandır. Bu alanda pek çok yöntem ve teknik bulunur ve çeşitli uygulamalarda kullanılır."
    }

    sakalar = [
        "İki balık yüzmüş, biri düşmüş. Diğeri ne demiş? Hadi çık, balık tutalım!",
        "Temel, doktora gitmiş. Doktor: Sigarayı bırakmazsan ömrünü yarı yarıya kaybedersin. demiş. Temel: Doktor bey, ben zaten paketin yarısını içiyorum!",
        "Bir bankaya giren hırsız, kasada ne olduğunu sormuş. Banka görevlisi: Sevgi var. demiş. Hırsız: E peki, bana biraz sevgi verin o zaman!",
        "Bir matematikçi kahveye gitmiş, garsona demiş ki: Bana bir kahve getir, lütfen, sonsuzluğa kadar şekersiz. Garson: Sonsuzluğa kadar şekersiz mi? demiş. Matematikçi gülümseyerek cevaplamış: Evet, çünkü sonsuz artı bir değişmez!",
        "Nasrettin Hoca'ya sormuşlar: Hocam, dünya dönüyor mu? Hoca yanıtlamış: Dönüyor tabii ki, bir gün bir yöne, bir gün başka bir yöne.",
        "Bir tavuk yolda yürürken şöyle demiş: Eğer yolun karşısına geçebilirsem, neden yürüyorum ki?"
    ]


    def welcome():
        print("""


*     *  ****  *     ****   *****    *     *  ****       *    *****     *    *****
*     *  *     *    *      *     *   **   **  *         * *   *    *   * *  *
*  *  *  ****  *   *      *       *  * * * *  ****     *   *  *****   *   *  *****
* * * *  *     *    *      *     *   *  *  *  *       ******* *   *  *******      *
**   **  ****  ****  ****   *****    *     *  ****   *       **    **       ******


    """)

    def uludag():
        import requests
        from bs4 import BeautifulSoup

        input1 = input("Ne aramak istiyorsunuz: ")
        url = "https://www.uludagsozluk.com/k/" + input1 + "/"
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
                    print(i)

    def bekle(n):
        time.sleep(n)

    def help_aras():
        print("""

        Kullanıcının girişine göre önceden tanımlanmış bazı sorulara yanıt verir.

        Ör: merhaba, naber, yapay zeka nedir?...
        ***********************************************************************************************************

        Kullanıcının "araştır" kelimesini kullanarak Google'da arama yapmasına olanak sağlar.
        ***********************************************************************************************************

        Kullanıcının "wikipedia" kelimesini kullanarak Wikipedia'da arama yapmasına olanak sağlar.
        ***********************************************************************************************************

        Kullanıcının "kimdir" kelimesini kullanarak Google'da bir kişi hakkında arama yapmasına olanak sağlar.
        ***********************************************************************************************************

        Kullanıcının IP adresini öğrenmesini sağlar.
        ***********************************************************************************************************

        Kullanıcının kayıt oluşturmasını sağlar.
        ***********************************************************************************************************

        Kullanıcının kaydolmasını sağlar.
        ***********************************************************************************************************

        Kullanıcının giriş yapmasını sağlar.
        ***********************************************************************************************************

        Kullanıcının admin girişi yapmasını sağlar.
        ***********************************************************************************************************

        Belirli bir anahtar kelimenin Wikipedia'da özetini alır.
        ***********************************************************************************************************

        Sayı tahmin oyunu oynamak için kullanıcının sayı girmesini sağlar.
        ***********************************************************************************************************
        8 haneli şifre oluşturur ve ekrana yazar.
        ***********************************************************************************************************

        Kullanıcının belirli bir URL'yi açmasını sağlar.
        ***********************************************************************************************************

        Kullanıcının metni Google Translate aracılığıyla çevirmesine olanak sağlar.
        ***********************************************************************************************************

        lstm yazarak ileriye dönük veri tahmini yaptırılabilir.
        ***********************************************************************************************************

        text generated veya metin oluştur yazarak rastgele bir konuda metin yazabilir.
        ***********************************************************************************************************

        fake info generate özelliği ile gerçek olmayan bilgiler üretebilir
        ***********************************************************************************************************

        text generate yazarak rastgele matin yazdırabilir.
        ***********************************************************************************************************

        kendi içinde tanımlı bir yapılacaklar listesi vardır görev ekleyebilir görüntüleyebilir ve silebilir.
        ***********************************************************************************************************


        """)

    def help_default():
        print("""

        Kullanıcının girişine göre önceden tanımlanmış bazı sorulara yanıt verir.

        Ör: merhaba, naber, yapay zeka nedir?...
        ***********************************************************************************************************


        """)

    def help_developer():
        print("""

        Kullanıcının girişine göre önceden tanımlanmış bazı sorulara yanıt verir.

        Ör: merhaba, naber, yapay zeka nedir?...
        
        Geleceğe yönelik veri tahmini yapabilir.
        ***********************************************************************************************************


        """)

    def encode_url(url):
        return url.encode('ascii', 'ignore').decode('ascii')

    def account_generate():
        from faker import Faker

        fake = Faker()
        profile = fake.profile()
        print(profile)


    def to_do_list():
        to_do_list = []

        def bekle(n):
            time.sleep(n)

        def ekle(to_do_list):
            gorev = input("Girilecek görevi yazınız: ")
            to_do_list.append(gorev)
            with open('gorevler.json', 'a') as dosya:
                dosya.write(json.dumps(to_do_list) + '\n')
            bekle(1)
            print("Görev başarıyla eklendi.")

        def goster(to_do_list):
            print("")
            print("Görevler yazdırılıyor")
            print("")
            bekle(1)
            if os.path.exists('gorevler.json'):
                with open('gorevler.json', 'r') as dosya:
                    for i in dosya:
                        print(i)
            else:
                print("Görevler dosyası bulunamadı.")

        def sil(to_do_list):
            print("Görevler yazdırılıyor")
            print("")
            bekle(1)
            for i in to_do_list:
                print(i)
            gorev_sil = input("Silmek istediğiniz görevi yazınız: ")

            if gorev_sil in to_do_list:
                to_do_list.remove(gorev_sil)
                with open('gorevler.json', 'w') as dosya:
                    dosya.write(json.dumps(to_do_list))
                bekle(1)
                print("Görev başarıyla silindi")
            else:
                print("Görev bulunamadı.")

        while True:
            print("""
    ************************************************************

    1.Görev Ekle
    2.Göverleri Göster
    3.Görev Sil
    4.Çıkış

    ************************************************************

            """)

            secim = input("Yapmak istediğiniz işlemi seçiniz: ")
            bekle(1)

            if secim == "1":
                ekle(to_do_list)
            elif secim == "2":
                goster(to_do_list)
            elif secim == "3":
                sil(to_do_list)
            elif secim == "4":
                break

    def sifrele():
        chars = string.ascii_letters + string.digits + string.punctuation

        rand_kucuk = random.randint(0,25)
        rand_buyuk = random.randint(26,31)
        rand_rakam = random.randint(32,41)
        rand_isaret = random.randint(42,73)
        rand_all = random.randint(26,31)
        rand_all2 = random.randint(0,73)
        rand_all3 = random.randint(42,73)
        rand_all4 = random.randint(0,73)

        sifre = chars[rand_buyuk] + chars[rand_rakam] + chars[rand_kucuk] + chars[rand_isaret] + chars[rand_all] + chars[rand_all2] + chars[rand_all3] + chars[rand_all4]
        print("Wix: 8 haneli şifreniz oluşturuluyor, lütfen bekleyiniz.")
        bekle(1)
        print(sifre)

    def ip():
        import requests
        from bs4 import BeautifulSoup

        host = socket.gethostname()
        ip = socket.gethostbyname(host)
        print("Wix: Local IP'niz: {}\n".format(ip))

        try:
            url = "https://www.ipsorgu.com/"
            list1 = []
            i = 0
            response = requests.get(url)
            if response.status_code == 200:
            # BeautifulSoup ile web sayfasının içeriğini çıkaralım
                soup = BeautifulSoup(response.content, "html.parser")

                    # Başlıkları çekmek için uygun HTML etiketlerini kullanalım (örn. <h1>, <h2>, <h3>)
                    # Burada örnek olarak sadece h2 başlıklarını alalım
                headers = soup.find_all("span")
                for header in headers:
                    list1.append(header.text)
                for i in range(3):
                    print(list1[i])
                    i+=1
        except:
            print("Bir sorun oluştu daha sonra tekrar deneyiniz...")

    def kayit_olustur():
        ad = input("Adınızı girin: ")
        soyad = input("Soyadınızı girin: ")
        kullanici_adi = input("Kullanıcı adınızı girin: ")
        sifre = getpass("Şifrenizi girin: ")

        kullanici = {
            'ad': ad,
            'soyad': soyad,
            'kullanici_adi': kullanici_adi,
            'sifre': sifre
        }

        return kullanici

    def kullanici_kaydet(kullanici):
        with open('kullanicilar.json', 'a') as dosya:
            dosya.write(json.dumps(kullanici) + '\n')

    def kullanici_giris():
        kullanici_adi = input("Kullanıcı adınızı girin: ")
        sifre = getpass("Şifrenizi girin: ")
        print("")

        if kullanici_adi == "Aras" and sifre == "Aras.123!":
            print("")
            bekle(1)
            print("Giriş başarılı!")
            print("")
            bekle(1)
            aras()
        elif kullanici_adi == "admin" and sifre == "DPiQBKXq":
            print("")
            bekle(1)
            print("Admin girişi başarılı!")
            print("")
            bekle(1)
            admin()
        elif kullanici_adi == "developer" and sifre == "DMn8BD3H":
            print("")
            bekle(1)
            print("Developer girişi başarılı!")
            print("")
            bekle(1)
            developer()
        else:
            with open('kullanicilar.json', 'r') as dosya:
                for satir in dosya:
                    kullanici = json.loads(satir)
                    if kullanici['kullanici_adi'] == kullanici_adi and kullanici['sifre'] == sifre:
                        print("Giriş başarılı!, merhaba " + kullanici_adi)
                        print("")
                        bekle(1)
                        default()
                        return

        print("Kullanıcı adı veya şifre hatalı.")
        bekle(1)

    def admin_giris():
        admin_adi = input("Admin kullanıcı adını girin: ")
        admin_sifre = getpass("Admin şifresini girin: ")

        if admin_adi == "admin" and admin_sifre == "DPiQBKXq":
            print("")
            print("Admin girişi başarılı!")
            print("")
            bekle(1)
            admin()
        else:
            print("")
            print("Admin kullanıcı adı veya şifre hatalı.")
            bekle(1)
            return False

    def get_wikipedia_summary(keyword):
        try:
            summary = wikipedia.summary(keyword)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            # Eğer birden fazla anlamı varsa, ilk anlamı döndürebilirsiniz
            summary = wikipedia.summary(e.options[0])
            return summary
        except wikipedia.exceptions.PageError:
            # Sayfa bulunamadı hatası
            return "Aradığınız konu Wikipedia'da bulunamadı."
        
    def lstm():
            lstmsayi=0
            while lstmsayi<3:
                print("""\n********************************************************

1.Veri setim var
2.Veri setim yok

********************************************************""")
                secim1 = input("Lütfen size uygun olan seçeneğin sayı numarasını giriniz: ")
                if secim1 == "1":
                    import numpy as np
                    import pandas as pd
                    import matplotlib.pyplot as plt
                    import tensorflow as tf
                    from sklearn.preprocessing import MinMaxScaler
                    from sklearn.metrics import mean_squared_error
                    from tensorflow.keras.models import Sequential
                    from tensorflow.keras.layers import LSTM, Dropout, Dense
                    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

                    inputdf = input("Veri setinin giriniz: ")
                    # Veri setini yükle
                    df = pd.read_csv(inputdf)

                    # Veri setini incele
                    def check_df(dataframe, head=5):
                        print("******************** SHAPE ********************")
                        print(dataframe.shape)
                        print("******************** TYPES ********************")
                        print(dataframe.dtypes)
                        print("******************** HEAD ********************")
                        print(dataframe.head(head))
                        print("******************** TAIL ********************")
                        print(dataframe.tail(head))
                        print("******************** NA ********************")
                        print(dataframe.isnull().sum())

                    check_df(df)

                    # Tarih sütununu datetime formatına dönüştür
                    df['Date'] = pd.to_datetime(df['Date'])

                    # Kapanış fiyatını içeren sütunu seç
                    tesla_df = df[['Date', 'Close']]

                    # Veri setinin başlangıç ve bitiş tarihlerini kontrol et
                    print("Maximum Tarih: ", tesla_df['Date'].max())
                    print("Minimum Tarih: ", tesla_df['Date'].min())
                    print("Maximum Kapanış: ", tesla_df['Close'].max())
                    print("Minimum Kapanış: ", tesla_df['Close'].min())

                    # Tarih sütununu indeks olarak ayarla
                    tesla_df.set_index('Date', inplace=True)

                    # Veri setini görselleştir
                    #plt.figure(figsize=(12, 6))
                    #plt.plot(tesla_df['Close'], color='blue')
                    #plt.ylabel('Stock Price')
                    #plt.title('Bitcoin Stock Price')
                    #plt.xlabel('Time')
                    #plt.show()

                    # Veri setini ölçeklendir
                    scaler = MinMaxScaler(feature_range=(0, 1))
                    scaled_data = scaler.fit_transform(tesla_df)

                    # Eğitim ve test veri setlerini oluştur
                    train_size = int(len(scaled_data) * 0.8)
                    train_data = scaled_data[:train_size]
                    test_data = scaled_data[train_size:]

                    # Veri setini özelliklere ve hedef değişkene ayır
                    def create_features(data, lookback):
                        X, y = [], []
                        for i in range(lookback, len(data)):
                            X.append(data[i-lookback:i, 0])
                            y.append(data[i, 0])
                        return np.array(X), np.array(y)

                    lookback = 4
                    X_train, y_train = create_features(train_data, lookback)
                    X_test, y_test = create_features(test_data, lookback)

                    # Veri setinin şekillerini yeniden düzenle
                    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
                    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

                    # Modeli oluştur
                    #model = Sequential()
                    #model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], 1)))
                    #model.add(Dropout(0.2))
                    #model.add(Dense(1))

                    model = Sequential()
                    model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], 1), return_sequences=True))
                    model.add(LSTM(units=50, activation='relu', return_sequences=True))
                    model.add(LSTM(units=50, activation='relu'))
                    model.add(Dropout(0.2))
                    model.add(Dense(1))
                    model.summary()
                    # Modeli derle
                    model.compile(loss='mean_squared_error', optimizer='adam')

                    filep = "lstm_model_1"
                    # Modeli eğitim sürecini tanımla
                    callbacks = [EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='min'),
                                ModelCheckpoint(filepath=filep, monitor='val_loss', mode='min',
                                                save_best_only=True, save_weights_only=False, verbose=1)]

                    # Modeli eğit
                    history = model.fit(X_train, y_train, epochs=123, batch_size=37,
                                        validation_data=(X_test, y_test), callbacks=callbacks, shuffle=False)

                    # Modelin performansını değerlendir
                    train_predict = model.predict(X_train)
                    test_predict = model.predict(X_test)

                    # Ölçeklemeyi tersine çevirerek tahminleri gerçek değerlere dönüştür
                    train_predict = scaler.inverse_transform(train_predict)
                    test_predict = scaler.inverse_transform(test_predict)

                    # RMSE değerlerini hesapla
                    train_rmse = np.sqrt(mean_squared_error(tesla_df[lookback:train_size], train_predict))
                    test_rmse = np.sqrt(mean_squared_error(tesla_df[train_size + lookback:], test_predict))

                    # Tahminleri içeren veri setlerini oluştur
                    train_prediction_df = tesla_df.copy()
                    train_prediction_df.iloc[lookback:train_size, 0] = train_predict[:, 0]

                    test_prediction_df = tesla_df.copy()
                    test_prediction_df.iloc[train_size + lookback:, 0] = test_predict[:, 0]

                    # Tahminleri görselleştir
                    #plt.figure(figsize=(14, 5))
                    #plt.plot(tesla_df, label='Real Values')
                    #plt.plot(train_prediction_df, color='blue', label='Train Predicted')
                    #plt.plot(test_prediction_df, color='red', label='Test Predicted')
                    #plt.ylabel('Stock Values')
                    #plt.xlabel('Time')
                    #plt.legend()
                    #plt.show()

                    import pandas as pd
                    import numpy as np
                    from sklearn.preprocessing import MinMaxScaler
                    from tensorflow.keras.models import load_model
                    import os

                    # Eğittiğiniz modelin kaydedildiği h5 dosyasının adı
                    model_filename = filep

                    # Önceki verileri içeren dönem uzunluğu (lookback) ve tahmin edilecek dönem uzunluğu
                    # Önceki verileri içeren dönem uzunluğu (lookback) ve tahmin edilecek dönem uzunluğu
                    lookback = 4
                    prediction_period = 4

                    # Veri setini yükle
                    df = pd.read_csv(inputdf)

                    # Veri setini datetime formatına dönüştür
                    df['Date'] = pd.to_datetime(df['Date'])

                    # Kapanış fiyatlarını içeren sütunu seç
                    bitcoin_df = df[['Date', 'Close']]

                    # Tarih sütununu indeks olarak ayarla
                    bitcoin_df.set_index('Date', inplace=True)

                    # Veri setini ölçeklendir
                    scaler = MinMaxScaler(feature_range=(0, 1))
                    scaled_data = scaler.fit_transform(bitcoin_df)

                    # Modeli yükle
                    model = load_model(model_filename)

                    # En son veri setinin dönem uzunluğu kadarını al
                    recent_data = scaled_data[-lookback:]

                    # Veriyi yeniden şekillendir
                    recent_data = np.reshape(recent_data, (1, lookback, 1))

                    # Tahmin yap
                    predicted_price = model.predict(recent_data)

                    # Tahmini tersine çevirerek gerçek değere dönüştür
                    predicted_price = scaler.inverse_transform(predicted_price)[0][0]

                    print(f"Train RMSE: {train_rmse}")
                    print(f"Test RMSE: {test_rmse}")
                    model_success = (1 - train_rmse / 67549.14) * 100 , (1 - test_rmse / 67549.14) * 100
                    print(model_success)
                    loss = model.evaluate(X_test, y_test, batch_size=20)
                    print("\nTest loss: %.1f%%" % (100.0 * loss))
                    print("\n4 gün sonrasının tahmini fiyat:", predicted_price)
                    bekle(1)
                    os.remove(inputdf)
                    print(f"\n Sevgili kullanıcı, veri karışıklığını önlemek amacıyla oluşturduğunuz '{inputdf}' dosyası silinmiştir lstm data yazarak tekrar oluşturabilirsiniz...")
                    lstmsayi+=1
                elif secim1 == "2":
                    import csv
                    import datetime
                    import cryptocompare
                    import numpy as np
                    import pandas as pd
                    import matplotlib.pyplot as plt
                    import tensorflow as tf
                    from sklearn.preprocessing import MinMaxScaler
                    from sklearn.metrics import mean_squared_error
                    from tensorflow.keras.models import Sequential
                    from tensorflow.keras.layers import LSTM, Dropout, Dense
                    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

                    input1 = input("\nGeçimiş değerlerini çekmek istediğiniz kripto paranın sembolik adını yazınız örneğin 'BTC': ")
                    date_input = input("\nVeri setinde olmasını istediğiniz son tarihi sayıların arasına "+"'.' "+"yerine "+"'-' "+"koyarak tarih,ay,gün sırasıyla yazınız yazınız. örneğin 2023-10-01: " )
                    def get_historical_btc_price(start_date, end_date):
                        historical_data = cryptocompare.get_historical_price_day(input1, currency='USD', toTs=datetime.datetime.strptime(end_date, '%Y-%m-%d'))
                        prices = []
                        for data in historical_data:
                            date = datetime.datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d')
                            price = data['close']
                            prices.append((date, price))
                            if date == start_date:
                                break
                        return prices

                    # Örnek kullanım
                    start_date = date_input
                    end_date = date_input
                    historical_prices = get_historical_btc_price(start_date, end_date)

                    # CSV dosyasına yazma
                    filename1 = input1+'_prices.csv'
                    with open(filename1, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Date', 'Close'])
                        writer.writerows(historical_prices)

                    print(input1+f" değerleri '{filename1}' dosyasına kaydedildi.")
                    bekle(1)
                    inputdf = filename1
                    # Veri setini yükle
                    df = pd.read_csv(inputdf)

                    # Veri setini incele
                    def check_df(dataframe, head=5):
                        print("******************** SHAPE ********************")
                        print(dataframe.shape)
                        print("******************** TYPES ********************")
                        print(dataframe.dtypes)
                        print("******************** HEAD ********************")
                        print(dataframe.head(head))
                        print("******************** TAIL ********************")
                        print(dataframe.tail(head))
                        print("******************** NA ********************")
                        print(dataframe.isnull().sum())

                    check_df(df)

                    # Tarih sütununu datetime formatına dönüştür
                    df['Date'] = pd.to_datetime(df['Date'])

                    # Kapanış fiyatını içeren sütunu seç
                    tesla_df = df[['Date', 'Close']]

                    # Veri setinin başlangıç ve bitiş tarihlerini kontrol et
                    print("Maximum Tarih: ", tesla_df['Date'].max())
                    print("Minimum Tarih: ", tesla_df['Date'].min())
                    print("Maximum Kapanış: ", tesla_df['Close'].max())
                    print("Minimum Kapanış: ", tesla_df['Close'].min())

                    # Tarih sütununu indeks olarak ayarla
                    tesla_df.set_index('Date', inplace=True)

                    # Veri setini görselleştir
                    #plt.figure(figsize=(12, 6))
                    #plt.plot(tesla_df['Close'], color='blue')
                    #plt.ylabel('Stock Price')
                    #plt.title('Bitcoin Stock Price')
                    #plt.xlabel('Time')
                    #plt.show()

                    # Veri setini ölçeklendir
                    scaler = MinMaxScaler(feature_range=(0, 1))
                    scaled_data = scaler.fit_transform(tesla_df)

                    # Eğitim ve test veri setlerini oluştur
                    train_size = int(len(scaled_data) * 0.8)
                    train_data = scaled_data[:train_size]
                    test_data = scaled_data[train_size:]

                    # Veri setini özelliklere ve hedef değişkene ayır
                    def create_features(data, lookback):
                        X, y = [], []
                        for i in range(lookback, len(data)):
                            X.append(data[i-lookback:i, 0])
                            y.append(data[i, 0])
                        return np.array(X), np.array(y)

                    lookback = 4
                    X_train, y_train = create_features(train_data, lookback)
                    X_test, y_test = create_features(test_data, lookback)

                    # Veri setinin şekillerini yeniden düzenle
                    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
                    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

                    # Modeli oluştur
                    #model = Sequential()
                    #model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], 1)))
                    #model.add(Dropout(0.2))
                    #model.add(Dense(1))

                    model = Sequential()
                    model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], 1), return_sequences=True))
                    model.add(LSTM(units=50, activation='relu', return_sequences=True))
                    model.add(LSTM(units=50, activation='relu'))
                    model.add(Dropout(0.2))
                    model.add(Dense(1))
                    model.summary()
                    # Modeli derle
                    model.compile(loss='mean_squared_error', optimizer='adam')

                    filep = "lstm_model_1"
                    # Modeli eğitim sürecini tanımla
                    callbacks = [EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='min'),
                                ModelCheckpoint(filepath=filep, monitor='val_loss', mode='min',
                                                save_best_only=True, save_weights_only=False, verbose=1)]

                    # Modeli eğit
                    history = model.fit(X_train, y_train, epochs=123, batch_size=37,
                                        validation_data=(X_test, y_test), callbacks=callbacks, shuffle=False)

                    # Modelin performansını değerlendir
                    train_predict = model.predict(X_train)
                    test_predict = model.predict(X_test)

                    # Ölçeklemeyi tersine çevirerek tahminleri gerçek değerlere dönüştür
                    train_predict = scaler.inverse_transform(train_predict)
                    test_predict = scaler.inverse_transform(test_predict)

                    # RMSE değerlerini hesapla
                    train_rmse = np.sqrt(mean_squared_error(tesla_df[lookback:train_size], train_predict))
                    test_rmse = np.sqrt(mean_squared_error(tesla_df[train_size + lookback:], test_predict))

                    # Tahminleri içeren veri setlerini oluştur
                    train_prediction_df = tesla_df.copy()
                    train_prediction_df.iloc[lookback:train_size, 0] = train_predict[:, 0]

                    test_prediction_df = tesla_df.copy()
                    test_prediction_df.iloc[train_size + lookback:, 0] = test_predict[:, 0]

                    # Tahminleri görselleştir
                    #plt.figure(figsize=(14, 5))
                    #plt.plot(tesla_df, label='Real Values')
                    #plt.plot(train_prediction_df, color='blue', label='Train Predicted')
                    #plt.plot(test_prediction_df, color='red', label='Test Predicted')
                    #plt.ylabel('Stock Values')
                    #plt.xlabel('Time')
                    #plt.legend()
                    #plt.show()

                    import pandas as pd
                    import numpy as np
                    from sklearn.preprocessing import MinMaxScaler
                    from tensorflow.keras.models import load_model
                    import os

                    # Eğittiğiniz modelin kaydedildiği h5 dosyasının adı
                    model_filename = filep

                    # Önceki verileri içeren dönem uzunluğu (lookback) ve tahmin edilecek dönem uzunluğu
                    # Önceki verileri içeren dönem uzunluğu (lookback) ve tahmin edilecek dönem uzunluğu
                    lookback = 4
                    prediction_period = 4

                    # Veri setini yükle
                    df = pd.read_csv(inputdf)

                    # Veri setini datetime formatına dönüştür
                    df['Date'] = pd.to_datetime(df['Date'])

                    # Kapanış fiyatlarını içeren sütunu seç
                    bitcoin_df = df[['Date', 'Close']]

                    # Tarih sütununu indeks olarak ayarla
                    bitcoin_df.set_index('Date', inplace=True)

                    # Veri setini ölçeklendir
                    scaler = MinMaxScaler(feature_range=(0, 1))
                    scaled_data = scaler.fit_transform(bitcoin_df)

                    # Modeli yükle
                    model = load_model(model_filename)

                    # En son veri setinin dönem uzunluğu kadarını al
                    recent_data = scaled_data[-lookback:]

                    # Veriyi yeniden şekillendir
                    recent_data = np.reshape(recent_data, (1, lookback, 1))

                    # Tahmin yap
                    predicted_price = model.predict(recent_data)

                    # Tahmini tersine çevirerek gerçek değere dönüştür
                    predicted_price = scaler.inverse_transform(predicted_price)[0][0]

                    print(f"Train RMSE: {train_rmse}")
                    print(f"Test RMSE: {test_rmse}")
                    model_success = (1 - train_rmse / 67549.14) * 100 , (1 - test_rmse / 67549.14) * 100
                    print(model_success)
                    loss = model.evaluate(X_test, y_test, batch_size=20)
                    print("\nTest loss: %.1f%%" % (100.0 * loss))
                    print("\n4 gün sonrasının tahmini fiyat:", predicted_price)
                    bekle(1)
                    os.remove(inputdf)
                    print(f"\n Sevgili kullanıcı, veri karışıklığını önlemek amacıyla oluşturduğunuz '{inputdf}' dosyası silinmiştir lstm data yazarak tekrar oluşturabilirsiniz...")
                    lstmsayi+=1

    def aras():
        welcome()
        bekle(1)
        print("\nUygulamada yeniyseniz help() yazarak neler yapabildiğimi görebilirsiniz...")
        while True:
            user_input = input("Aras: ")

            cleaned_input = ''.join(c for c in user_input if c.isalnum() or c.isspace())

            # Küçük harflere dönüştürme ve özel karakterleri temizleme
            user_input = cleaned_input.lower().strip()

            # Kullanıcının girişine en uygun yanıtı bulma
            if user_input in responses:
                print("Wix: " + responses[user_input])

            elif "teşekkür ederim" in user_input or "teşekkürler" in user_input or "eyw" in user_input or "eyv" in user_input or "saolasın" in user_input or "saol" in user_input or "sağol" in user_input or "sağolasın" in user_input:
                print("Wix: " + responses["teşekkür ederim"])

            elif "help" in user_input or "help()" in user_input:
                help_aras()

            elif "araştır" in user_input:
                arastir = "araştır"
                new_sentence = user_input.replace(arastir, "")
                webbrowser.open_new_tab("https://www.google.com/search?q=+" + encode_url(new_sentence))

                if "wikipedia" in user_input:
                    sentence1 = new_sentence.replace("wikipedia","")
                    get_wikipedia_summary(sentence1)
                    summary = get_wikipedia_summary(sentence1)
                    print(summary)
                else:
                    print("Araştırılacak içerik bulunamadı, lüften tekrar deneyiniz...")


            elif "wikipedia" in user_input or "wiki" in user_input:
                    wikipedia = "wikipedia"
                    sentence2 = user_input.replace(wikipedia, "")
                    get_wikipedia_summary(sentence2)
                    summary = get_wikipedia_summary(sentence2)
                    print(summary)

            elif "kimdir" in user_input or "kim" in user_input:
                kim = "kim"
                kimdir = "kimdir"

                if "kim" in user_input:
                    new_sentence_kim = user_input.replace(kim, "")
                    webbrowser.open_new_tab("https://www.google.com/search?q=+" + new_sentence_kim)

                elif "kimdir" in user_input:
                    new_sentence_kimdir = user_input.replace(kimdir, "")
                    webbrowser.open_new_tab("https://www.google.com/search?q=+" + new_sentence_kimdir)

                else:
                    print("Wix bu kişiyle alakalı google'da bir şey bulamadı")

            elif "ip" in user_input or "ipconfig" in user_input or "ifconfig" in user_input or "ip sorgusu" in user_input:
                ip()

            elif "çıkış" in user_input or "çıkış yap" in user_input or "exit" in user_input or "stop" in user_input or "bitir" in user_input or "durdur" in user_input:
                bekle(1)
                print("")
                print("Çıkış yapılıyor iyi günler dilerim Aras")
                print("")
                bekle(1)
                break

            elif "sayı tahmin" in user_input or "sayı tahmin oyunu" in user_input or "tahmin oyunu" in user_input or "oyun oyna" in user_input or "sayı oyunu" in user_input:
                random_sayi = random.randint(0,5)
                sayi = int(input("Wix: 0 ile 5 arasında bir sayı giriniz: "))

                if sayi != random_sayi:
                    print("Wix: tahmin yanlış tekrar deneyin")
                    bekle(1)
                else:
                    print("Wix: doğru tahmin")

            elif "şifre oluştur" in user_input or "sifrele" in user_input or "şifre yaz" in user_input or "şifre" in user_input:
                sifrele()

            elif "fake generator" in user_input or "info generator" in user_input or "fake info generator" in user_input or "fake info" in user_input or "fake infos" in user_input:
                account_generate()

            elif "yardımcı" in user_input or "helper" in user_input:
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
            
            elif "open" in user_input:
                word_list = user_input.split(" ")
                index_open = word_list.index("open")

                if("chatopenaicom" in word_list[index_open + 1]):
                    url = "https://" + word_list[index_open + 1]
                    url = url.replace("chatopenai", "chat.openai")
                    url = url.replace("com", ".com")
                    webbrowser.open_new_tab(url)

                elif ("com" in word_list[index_open + 1]):
                    com = ".com"
                    url = "https://" + word_list[index_open + 1]
                    url_new = url.replace("com", com)
                    webbrowser.open_new_tab(url_new)
                elif("net" in word_list[index_open + 1]):
                    url = "https://" + word_list[index_open + 1]
                    url = url.replace("https", "http")  # HTTPS'i HTTP ile değiştiriyoruz
                    url = url.replace(".com", "")
                    url = url.replace("net", "")
                    url = url + ".net"
                    webbrowser.open_new_tab(url)
                else:
                    url = "https://" + word_list[index_open + 1] + ".com"
                    webbrowser.open_new_tab(url)

            elif "çeviri" in user_input or "çevir" in user_input or "translate" in user_input:
                if "çeviri" in user_input:
                    ceviri = user_input.replace("çeviri" ,"")
                    webbrowser.open_new_tab("https://translate.google.com.tr/?sl=en&tl=tr&text=" + ceviri + "&op=translate")
                elif "çevir" in user_input:
                    ceviri2 = user_input.replace("çevir", "")
                    webbrowser.open_new_tab("https://translate.google.com.tr/?sl=en&tl=tr&text=" + ceviri2 + "&op=translate")
                elif "translate" in user_input:
                    ceviri3 = user_input.replace("translate", "")
                    webbrowser.open_new_tab("https://translate.google.com.tr/?sl=en&tl=tr&text=" + ceviri3 + "&op=translate")

            elif "şaka yap" in user_input or "şaka yaz" in user_input or "şaka" in user_input or "beni biraz güldür" in user_input or "bizi güldür" in user_input:
                rando = random.randint(0,5)
                saka = sakalar[rando]
                print("")
                print(saka)
                print("")

            elif "yapılacaklar listesi" in user_input or "yapılacaklar" in user_input or "to do list" in user_input:
                to_do_list()

            elif "lstm data" in user_input:
                import csv
                import datetime
                import cryptocompare

                input1 = input("Geçimiş değerlerini çekmek istediğiniz kripto paranın sembolik adını yazınız örneğin 'BTC': ")
                date_input = input("\nVeri setinde olmasını istediğiniz son tarihi sayıların arasına "+"'.' "+"yerine "+"'-' "+"koyarak tarih,ay,gün sırasıyla yazınız yazınız. örneğin 2023-10-01: " )
                def get_historical_btc_price(start_date, end_date):
                    historical_data = cryptocompare.get_historical_price_day(input1, currency='USD', toTs=datetime.datetime.strptime(end_date, '%Y-%m-%d'))
                    prices = []
                    for data in historical_data:
                        date = datetime.datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d')
                        price = data['close']
                        prices.append((date, price))
                        if date == start_date:
                            break
                    return prices

                # Örnek kullanım
                start_date = date_input
                end_date = date_input
                historical_prices = get_historical_btc_price(start_date, end_date)

                # CSV dosyasına yazma
                filename1 = input1+'_prices.csv'
                with open(filename1, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Date', 'Close'])
                    writer.writerows(historical_prices)

                print(input1+f" değerleri '{filename1}' dosyasına kaydedildi.")

            elif "lstm" in user_input:
                print("""\n********************************************************

1.Veri setim var
2.Veri setim yok

********************************************************""")
                secim1 = input("Lütfen size uygun olan seçeneğin sayı numarasını giriniz: ")
                if secim1 == "1":
                    import numpy as np
                    import pandas as pd
                    import matplotlib.pyplot as plt
                    import tensorflow as tf
                    from sklearn.preprocessing import MinMaxScaler
                    from sklearn.metrics import mean_squared_error
                    from tensorflow.keras.models import Sequential
                    from tensorflow.keras.layers import LSTM, Dropout, Dense
                    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

                    inputdf = input("Veri setinin giriniz: ")
                    # Veri setini yükle
                    df = pd.read_csv(inputdf)

                    # Veri setini incele
                    def check_df(dataframe, head=5):
                        print("******************** SHAPE ********************")
                        print(dataframe.shape)
                        print("******************** TYPES ********************")
                        print(dataframe.dtypes)
                        print("******************** HEAD ********************")
                        print(dataframe.head(head))
                        print("******************** TAIL ********************")
                        print(dataframe.tail(head))
                        print("******************** NA ********************")
                        print(dataframe.isnull().sum())

                    check_df(df)

                    # Tarih sütununu datetime formatına dönüştür
                    df['Date'] = pd.to_datetime(df['Date'])

                    # Kapanış fiyatını içeren sütunu seç
                    tesla_df = df[['Date', 'Close']]

                    # Veri setinin başlangıç ve bitiş tarihlerini kontrol et
                    print("Maximum Tarih: ", tesla_df['Date'].max())
                    print("Minimum Tarih: ", tesla_df['Date'].min())
                    print("Maximum Kapanış: ", tesla_df['Close'].max())
                    print("Minimum Kapanış: ", tesla_df['Close'].min())

                    # Tarih sütununu indeks olarak ayarla
                    tesla_df.set_index('Date', inplace=True)

                    # Veri setini görselleştir
                    #plt.figure(figsize=(12, 6))
                    #plt.plot(tesla_df['Close'], color='blue')
                    #plt.ylabel('Stock Price')
                    #plt.title('Bitcoin Stock Price')
                    #plt.xlabel('Time')
                    #plt.show()

                    # Veri setini ölçeklendir
                    scaler = MinMaxScaler(feature_range=(0, 1))
                    scaled_data = scaler.fit_transform(tesla_df)

                    # Eğitim ve test veri setlerini oluştur
                    train_size = int(len(scaled_data) * 0.8)
                    train_data = scaled_data[:train_size]
                    test_data = scaled_data[train_size:]

                    # Veri setini özelliklere ve hedef değişkene ayır
                    def create_features(data, lookback):
                        X, y = [], []
                        for i in range(lookback, len(data)):
                            X.append(data[i-lookback:i, 0])
                            y.append(data[i, 0])
                        return np.array(X), np.array(y)

                    lookback = 4
                    X_train, y_train = create_features(train_data, lookback)
                    X_test, y_test = create_features(test_data, lookback)

                    # Veri setinin şekillerini yeniden düzenle
                    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
                    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

                    # Modeli oluştur
                    #model = Sequential()
                    #model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], 1)))
                    #model.add(Dropout(0.2))
                    #model.add(Dense(1))

                    model = Sequential()
                    model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], 1), return_sequences=True))
                    model.add(LSTM(units=50, activation='relu', return_sequences=True))
                    model.add(LSTM(units=50, activation='relu'))
                    model.add(Dropout(0.2))
                    model.add(Dense(1))
                    model.summary()
                    # Modeli derle
                    model.compile(loss='mean_squared_error', optimizer='adam')

                    filep = "lstm_model_1"
                    # Modeli eğitim sürecini tanımla
                    callbacks = [EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='min'),
                                ModelCheckpoint(filepath=filep, monitor='val_loss', mode='min',
                                                save_best_only=True, save_weights_only=False, verbose=1)]

                    # Modeli eğit
                    history = model.fit(X_train, y_train, epochs=123, batch_size=37,
                                        validation_data=(X_test, y_test), callbacks=callbacks, shuffle=False)

                    # Modelin performansını değerlendir
                    train_predict = model.predict(X_train)
                    test_predict = model.predict(X_test)

                    # Ölçeklemeyi tersine çevirerek tahminleri gerçek değerlere dönüştür
                    train_predict = scaler.inverse_transform(train_predict)
                    test_predict = scaler.inverse_transform(test_predict)

                    # RMSE değerlerini hesapla
                    train_rmse = np.sqrt(mean_squared_error(tesla_df[lookback:train_size], train_predict))
                    test_rmse = np.sqrt(mean_squared_error(tesla_df[train_size + lookback:], test_predict))

                    # Tahminleri içeren veri setlerini oluştur
                    train_prediction_df = tesla_df.copy()
                    train_prediction_df.iloc[lookback:train_size, 0] = train_predict[:, 0]

                    test_prediction_df = tesla_df.copy()
                    test_prediction_df.iloc[train_size + lookback:, 0] = test_predict[:, 0]

                    # Tahminleri görselleştir
                    #plt.figure(figsize=(14, 5))
                    #plt.plot(tesla_df, label='Real Values')
                    #plt.plot(train_prediction_df, color='blue', label='Train Predicted')
                    #plt.plot(test_prediction_df, color='red', label='Test Predicted')
                    #plt.ylabel('Stock Values')
                    #plt.xlabel('Time')
                    #plt.legend()
                    #plt.show()

                    import pandas as pd
                    import numpy as np
                    from sklearn.preprocessing import MinMaxScaler
                    from tensorflow.keras.models import load_model
                    import os

                    # Eğittiğiniz modelin kaydedildiği h5 dosyasının adı
                    model_filename = filep

                    # Önceki verileri içeren dönem uzunluğu (lookback) ve tahmin edilecek dönem uzunluğu
                    # Önceki verileri içeren dönem uzunluğu (lookback) ve tahmin edilecek dönem uzunluğu
                    lookback = 4
                    prediction_period = 4

                    # Veri setini yükle
                    df = pd.read_csv(inputdf)

                    # Veri setini datetime formatına dönüştür
                    df['Date'] = pd.to_datetime(df['Date'])

                    # Kapanış fiyatlarını içeren sütunu seç
                    bitcoin_df = df[['Date', 'Close']]

                    # Tarih sütununu indeks olarak ayarla
                    bitcoin_df.set_index('Date', inplace=True)

                    # Veri setini ölçeklendir
                    scaler = MinMaxScaler(feature_range=(0, 1))
                    scaled_data = scaler.fit_transform(bitcoin_df)

                    # Modeli yükle
                    model = load_model(model_filename)

                    # En son veri setinin dönem uzunluğu kadarını al
                    recent_data = scaled_data[-lookback:]

                    # Veriyi yeniden şekillendir
                    recent_data = np.reshape(recent_data, (1, lookback, 1))

                    # Tahmin yap
                    predicted_price = model.predict(recent_data)

                    # Tahmini tersine çevirerek gerçek değere dönüştür
                    predicted_price = scaler.inverse_transform(predicted_price)[0][0]

                    print(f"Train RMSE: {train_rmse}")
                    print(f"Test RMSE: {test_rmse}")
                    model_success = (1 - train_rmse / 67549.14) * 100 , (1 - test_rmse / 67549.14) * 100
                    print(model_success)
                    loss = model.evaluate(X_test, y_test, batch_size=20)
                    print("\nTest loss: %.1f%%" % (100.0 * loss))
                    print("\n4 gün sonrasının tahmini fiyat:", predicted_price)
                    bekle(1)
                    os.remove(inputdf)
                    print(f"\n Sevgili kullanıcı, veri karışıklığını önlemek amacıyla oluşturduğunuz '{inputdf}' dosyası silinmiştir lstm data yazarak tekrar oluşturabilirsiniz...")
                elif secim1 == "2":
                    import csv
                    import datetime
                    import cryptocompare
                    import numpy as np
                    import pandas as pd
                    import matplotlib.pyplot as plt
                    import tensorflow as tf
                    from sklearn.preprocessing import MinMaxScaler
                    from sklearn.metrics import mean_squared_error
                    from tensorflow.keras.models import Sequential
                    from tensorflow.keras.layers import LSTM, Dropout, Dense
                    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

                    input1 = input("\nGeçimiş değerlerini çekmek istediğiniz kripto paranın sembolik adını yazınız örneğin 'BTC': ")
                    date_input = input("\nVeri setinde olmasını istediğiniz son tarihi sayıların arasına "+"'.' "+"yerine "+"'-' "+"koyarak tarih,ay,gün sırasıyla yazınız yazınız. örneğin 2023-10-01: " )
                    def get_historical_btc_price(start_date, end_date):
                        historical_data = cryptocompare.get_historical_price_day(input1, currency='USD', toTs=datetime.datetime.strptime(end_date, '%Y-%m-%d'))
                        prices = []
                        for data in historical_data:
                            date = datetime.datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d')
                            price = data['close']
                            prices.append((date, price))
                            if date == start_date:
                                break
                        return prices

                    # Örnek kullanım
                    start_date = date_input
                    end_date = date_input
                    historical_prices = get_historical_btc_price(start_date, end_date)

                    # CSV dosyasına yazma
                    filename1 = input1+'_prices.csv'
                    with open(filename1, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Date', 'Close'])
                        writer.writerows(historical_prices)

                    print(input1+f" değerleri '{filename1}' dosyasına kaydedildi.")
                    bekle(1)
                    inputdf = filename1
                    # Veri setini yükle
                    df = pd.read_csv(inputdf)

                    # Veri setini incele
                    def check_df(dataframe, head=5):
                        print("******************** SHAPE ********************")
                        print(dataframe.shape)
                        print("******************** TYPES ********************")
                        print(dataframe.dtypes)
                        print("******************** HEAD ********************")
                        print(dataframe.head(head))
                        print("******************** TAIL ********************")
                        print(dataframe.tail(head))
                        print("******************** NA ********************")
                        print(dataframe.isnull().sum())

                    check_df(df)

                    # Tarih sütununu datetime formatına dönüştür
                    df['Date'] = pd.to_datetime(df['Date'])

                    # Kapanış fiyatını içeren sütunu seç
                    tesla_df = df[['Date', 'Close']]

                    # Veri setinin başlangıç ve bitiş tarihlerini kontrol et
                    print("Maximum Tarih: ", tesla_df['Date'].max())
                    print("Minimum Tarih: ", tesla_df['Date'].min())
                    print("Maximum Kapanış: ", tesla_df['Close'].max())
                    print("Minimum Kapanış: ", tesla_df['Close'].min())

                    # Tarih sütununu indeks olarak ayarla
                    tesla_df.set_index('Date', inplace=True)

                    # Veri setini görselleştir
                    #plt.figure(figsize=(12, 6))
                    #plt.plot(tesla_df['Close'], color='blue')
                    #plt.ylabel('Stock Price')
                    #plt.title('Bitcoin Stock Price')
                    #plt.xlabel('Time')
                    #plt.show()

                    # Veri setini ölçeklendir
                    scaler = MinMaxScaler(feature_range=(0, 1))
                    scaled_data = scaler.fit_transform(tesla_df)

                    # Eğitim ve test veri setlerini oluştur
                    train_size = int(len(scaled_data) * 0.8)
                    train_data = scaled_data[:train_size]
                    test_data = scaled_data[train_size:]

                    # Veri setini özelliklere ve hedef değişkene ayır
                    def create_features(data, lookback):
                        X, y = [], []
                        for i in range(lookback, len(data)):
                            X.append(data[i-lookback:i, 0])
                            y.append(data[i, 0])
                        return np.array(X), np.array(y)

                    lookback = 4
                    X_train, y_train = create_features(train_data, lookback)
                    X_test, y_test = create_features(test_data, lookback)

                    # Veri setinin şekillerini yeniden düzenle
                    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
                    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

                    # Modeli oluştur
                    #model = Sequential()
                    #model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], 1)))
                    #model.add(Dropout(0.2))
                    #model.add(Dense(1))

                    model = Sequential()
                    model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], 1), return_sequences=True))
                    model.add(LSTM(units=50, activation='relu', return_sequences=True))
                    model.add(LSTM(units=50, activation='relu'))
                    model.add(Dropout(0.2))
                    model.add(Dense(1))
                    model.summary()
                    # Modeli derle
                    model.compile(loss='mean_squared_error', optimizer='adam')

                    filep = "lstm_model_1"
                    # Modeli eğitim sürecini tanımla
                    callbacks = [EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='min'),
                                ModelCheckpoint(filepath=filep, monitor='val_loss', mode='min',
                                                save_best_only=True, save_weights_only=False, verbose=1)]

                    # Modeli eğit
                    history = model.fit(X_train, y_train, epochs=123, batch_size=37,
                                        validation_data=(X_test, y_test), callbacks=callbacks, shuffle=False)

                    # Modelin performansını değerlendir
                    train_predict = model.predict(X_train)
                    test_predict = model.predict(X_test)

                    # Ölçeklemeyi tersine çevirerek tahminleri gerçek değerlere dönüştür
                    train_predict = scaler.inverse_transform(train_predict)
                    test_predict = scaler.inverse_transform(test_predict)

                    # RMSE değerlerini hesapla
                    train_rmse = np.sqrt(mean_squared_error(tesla_df[lookback:train_size], train_predict))
                    test_rmse = np.sqrt(mean_squared_error(tesla_df[train_size + lookback:], test_predict))

                    # Tahminleri içeren veri setlerini oluştur
                    train_prediction_df = tesla_df.copy()
                    train_prediction_df.iloc[lookback:train_size, 0] = train_predict[:, 0]

                    test_prediction_df = tesla_df.copy()
                    test_prediction_df.iloc[train_size + lookback:, 0] = test_predict[:, 0]

                    # Tahminleri görselleştir
                    #plt.figure(figsize=(14, 5))
                    #plt.plot(tesla_df, label='Real Values')
                    #plt.plot(train_prediction_df, color='blue', label='Train Predicted')
                    #plt.plot(test_prediction_df, color='red', label='Test Predicted')
                    #plt.ylabel('Stock Values')
                    #plt.xlabel('Time')
                    #plt.legend()
                    #plt.show()

                    import pandas as pd
                    import numpy as np
                    from sklearn.preprocessing import MinMaxScaler
                    from tensorflow.keras.models import load_model
                    import os

                    # Eğittiğiniz modelin kaydedildiği h5 dosyasının adı
                    model_filename = filep

                    # Önceki verileri içeren dönem uzunluğu (lookback) ve tahmin edilecek dönem uzunluğu
                    # Önceki verileri içeren dönem uzunluğu (lookback) ve tahmin edilecek dönem uzunluğu
                    lookback = 4
                    prediction_period = 4

                    # Veri setini yükle
                    df = pd.read_csv(inputdf)

                    # Veri setini datetime formatına dönüştür
                    df['Date'] = pd.to_datetime(df['Date'])

                    # Kapanış fiyatlarını içeren sütunu seç
                    bitcoin_df = df[['Date', 'Close']]

                    # Tarih sütununu indeks olarak ayarla
                    bitcoin_df.set_index('Date', inplace=True)

                    # Veri setini ölçeklendir
                    scaler = MinMaxScaler(feature_range=(0, 1))
                    scaled_data = scaler.fit_transform(bitcoin_df)

                    # Modeli yükle
                    model = load_model(model_filename)

                    # En son veri setinin dönem uzunluğu kadarını al
                    recent_data = scaled_data[-lookback:]

                    # Veriyi yeniden şekillendir
                    recent_data = np.reshape(recent_data, (1, lookback, 1))

                    # Tahmin yap
                    predicted_price = model.predict(recent_data)

                    # Tahmini tersine çevirerek gerçek değere dönüştür
                    predicted_price = scaler.inverse_transform(predicted_price)[0][0]

                    print(f"Train RMSE: {train_rmse}")
                    print(f"Test RMSE: {test_rmse}")
                    model_success = (1 - train_rmse / 67549.14) * 100 , (1 - test_rmse / 67549.14) * 100
                    print(model_success)
                    loss = model.evaluate(X_test, y_test, batch_size=20)
                    print("\nTest loss: %.1f%%" % (100.0 * loss))
                    print("\n4 gün sonrasının tahmini fiyat:", predicted_price)
                    bekle(1)
                    os.remove(inputdf)
                    print(f"\n Sevgili kullanıcı, veri karışıklığını önlemek amacıyla oluşturduğunuz '{inputdf}' dosyası silinmiştir lstm data yazarak tekrar oluşturabilirsiniz...")


            elif "text generate" in user_input or "metin yaz" in user_input or "metin oluştur" in user_input:
                from tensorflow.keras.callbacks import LambdaCallback
                from tensorflow.keras.models import Sequential
                from tensorflow.keras.layers import Dense, LSTM
                from tensorflow.keras.optimizers import RMSprop
                from tensorflow.keras.utils import get_file
                import numpy as np
                import random
                import sys
                import io
                import requests
                import re
                import logging
                import os

                logging.disable(logging.WARNING)
                os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

                r = requests.get("https://data.heatonresearch.com/data/t81-558/text/treasure_island.txt")
                raw_text = r.text
                print(raw_text[0:1000])

                processed_text = raw_text.lower()
                processed_text = re.sub(r'[^\x00-\x7f]', r'', processed_text)

                print('corpus length:', len(processed_text))

                chars = sorted(list(set(processed_text)))
                print('total chars:', len(chars))
                char_indices = dict((c, i) for i, c in enumerate(chars))
                indices_char = dict((i, c) for i, c in enumerate(chars))

                # cut the text in semi-redundant sequences of maxlen characters
                maxlen = 40
                step = 3
                sentences = []
                next_chars = []
                for i in range(0, len(processed_text) - maxlen, step):
                    sentences.append(processed_text[i: i + maxlen])
                    next_chars.append(processed_text[i + maxlen])
                print('nb sequences:', len(sentences))

                print(sentences)

                print('Vectorization...')
                x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
                y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
                for i, sentence in enumerate(sentences):
                    for t, char in enumerate(sentence):
                        x[i, t, char_indices[char]] = 1
                    y[i, char_indices[next_chars[i]]] = 1

                # build the model: a single LSTM
                print('Build model...')
                model = Sequential()
                model.add(LSTM(128, input_shape=(maxlen, len(chars))))
                model.add(Dense(len(chars), activation='softmax'))

                optimizer = RMSprop(lr=0.01)
                model.compile(loss='categorical_crossentropy', optimizer=optimizer)

                model.summary()

                def sample(preds, temperature=1.0):
                    # helper function to sample an index from a probability array
                    preds = np.asarray(preds).astype('float64')
                    preds = np.log(preds) / temperature
                    exp_preds = np.exp(preds)
                    preds = exp_preds / np.sum(exp_preds)
                    probas = np.random.multinomial(1, preds, 1)
                    return np.argmax(probas)

                def on_epoch_end(epoch, _):
                    # Function invoked at end of each epoch. Prints generated text.
                    print("******************************************************")
                    print('----- Generating text after Epoch: %d' % epoch)

                    start_index = random.randint(0, len(processed_text) - maxlen - 1)
                    for temperature in [0.2, 0.5, 1.0, 1.2]:
                        print('----- temperature:', temperature)

                        generated = ''
                        sentence = processed_text[start_index: start_index + maxlen]
                        generated += sentence
                        print('----- Generating with seed: "' + sentence + '"')
                        sys.stdout.write(generated)

                        for i in range(400):
                            x_pred = np.zeros((1, maxlen, len(chars)))
                            for t, char in enumerate(sentence):
                                x_pred[0, t, char_indices[char]] = 1.

                            preds = model.predict(x_pred, verbose=0)[0]
                            next_index = sample(preds, temperature)
                            next_char = indices_char[next_index]

                            generated += next_char
                            sentence = sentence[1:] + next_char

                            sys.stdout.write(next_char)
                            sys.stdout.flush()
                        print()

                # Fit the model
                print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

                model.fit(x, y,
                        batch_size=128,
                        epochs=60,
                        callbacks=[print_callback])

            else:
                print("Wix: " + responses["diğerleri"])

    def developer():
        while True:
            print("Uygulamada yeniyseniz help() yazarak neler yapabildiğimi görebilirsiniz...")
            user_input = input("Geliştirici: ")
            user_input = user_input.lower().strip()

            if user_input in responses:
                print("Wix: " + responses[user_input])

            elif "çıkış" in user_input or "çıkış yap" in user_input or "exit" in user_input or "stop" in user_input or "bitir" in user_input or "durdur" in user_input:
                time.sleep(1)
                print("")
                print("Çıkış yapılıyor iyi günler dilerim")
                print("")
                time.sleep(1)
                break

            elif "help()" in user_input or "help" in user_input:
                help_developer()

            elif "a dead man is dead for good" in user_input:
                bekle(1)
                print("")
                print("Admin kullanıcı ortamına geçiliyor...")
                print("")
                bekle(2)
                admin()

            elif "lstm data" in user_input or "lstm data list" in user_input:
                import csv
                import datetime
                import cryptocompare

                input1 = input("Geçimiş değerlerini çekmek istediğiniz kripto paranın sembolik adını yazınız örneğin 'BTC': ")
                def get_historical_btc_price(start_date, end_date):
                    historical_data = cryptocompare.get_historical_price_day(input1, currency='USD', toTs=datetime.datetime.strptime(end_date, '%Y-%m-%d'))
                    prices = []
                    for data in historical_data:
                        date = datetime.datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d')
                        price = data['close']
                        prices.append((date, price))
                        if date == start_date:
                            break
                    return prices

                # Örnek kullanım
                start_date = '2022-06-01'
                end_date = '2023-06-30'

                historical_prices = get_historical_btc_price(start_date, end_date)

                # CSV dosyasına yazma
                filename1 = input1+'_prices.csv'
                with open(filename1, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Date', 'Close'])
                    writer.writerows(historical_prices)

                print(input1+f" değerleri '{filename1}' dosyasına kaydedildi.")

            elif "lstm" in user_input:

                import numpy as np
                import pandas as pd
                import matplotlib.pyplot as plt
                import tensorflow as tf

                from prophet import Prophet

                from sklearn.preprocessing import MinMaxScaler
                from sklearn.metrics import mean_squared_error

                from tensorflow.keras.models import Sequential
                from tensorflow.keras.layers import Conv2D, Flatten, MaxPooling2D, Dense, LSTM, Dropout, SpatialDropout2D
                from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

                import warnings
                warnings.filterwarnings('ignore')

                import os
                os.environ['TF_CPP_LOG_LEVEL'] = '3'
                tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

                print("")
                file = input("Wix: Okumak istediğiniz dosyayı lstm datada verilen dosya adını yazınız ve sonuna '.csv' YAZMAYINIZ: ")
                df = pd.read_csv(file + ".csv")

                from pandas.io.formats.style_render import DataFrame
                def check_df(dataframe, head=5):
                    print("******************** SHAPE ********************")
                    print(dataframe.shape)
                    print("******************** TYPES ********************")
                    print(dataframe.dtypes)
                    print("******************** HEAD ********************")
                    print(dataframe.head(head))
                    print("******************** TAIL ********************")
                    print(dataframe.tail(head))
                    print("******************** NA ********************")       #veri kaybını gösterir.
                    print(dataframe.isnull().sum())

                print("")
                check_df(df)
                print("")

                x = df['Date']
                y = df['Close']
                plt.plot(x,y)
                plt.xlabel('Time Scale')
                plt.ylabel('usd')

                df['Date'] = pd.to_datetime(df["Date"])

                df_data = df[['Date','Close']]

                df_data.rename(columns={"Date":"ds"}, inplace=True)
                df_data.rename(columns={"Close":"y"}, inplace=True)

                model = Prophet()
                model.fit(df_data)

                future = model.make_future_dataframe(periods=60)

                forecast = model.predict(future)
                df_forecast= forecast[["ds", "yhat","yhat_lower","yhat_upper"]]
                pd.set_option('display.max_rows', df_forecast.shape[0]+1)
                print("")
                print(df_forecast)
                print("")

            else:
                print("Wix" + responses["diğerleri"])

    def default():
        while True:
            print("Uygulamada yeniyseniz help() yazarak neler yapabildiğimi görebilirsiniz...")
            user_input = input("Kullanıcı: ")
            user_input = user_input.lower().strip()

            if user_input in responses:
                print("Wix: " + responses[user_input])

            elif "çıkış" in user_input or "çıkış yap" in user_input or "exit" in user_input or "stop" in user_input or "bitir" in user_input or "durdur" in user_input:
                bekle(1)
                print("")
                print("Çıkış yapılıyor iyi günler dilerim")
                print("")
                bekle(1)
                break

            elif "help()" in user_input or "help" in user_input:
                help_default()

            elif "change default to developer" in user_innput:
                developer()

            else:
                print("Wix" + responses["diğerleri"])

    def admin():
        print("Uygulamada yeniyseniz help() yazarak neler yapabildiğimi görebilirsiniz...\n")
        bekle(1)
        print("lstm fonksiyonu başatılıyor...\n")
        bekle(1)
        lstm()

        while True:
            user_input = input("Admin: ")

            cleaned_input = ''.join(c for c in user_input if c.isalnum() or c.isspace())

            # Küçük harflere dönüştürme ve özel karakterleri temizleme
            user_input = cleaned_input.lower().strip()

            # Kullanıcının girişine en uygun yanıtı bulma
            if user_input in responses:
                print("Wix: " + responses[user_input])

            elif "teşekkür ederim" in user_input or "teşekkürler" in user_input or "eyw" in user_input or "eyv" in user_input or "saolasın" in user_input or "saol" in user_input or "sağol" in user_input or "sağolasın" in user_input:
                print("Wix: " + responses["teşekkür ederim"])

            elif "help" in user_input or "help()" in user_input:
                help_aras()

            elif "araştır" in user_input:
                arastir = "araştır"
                new_sentence = user_input.replace(arastir, "")
                webbrowser.open_new_tab("https://www.google.com/search?q=+" + encode_url(new_sentence))

                if "wikipedia" in user_input:
                    sentence1 = new_sentence.replace("wikipedia","")
                    get_wikipedia_summary(sentence1)
                    summary = get_wikipedia_summary(sentence1)
                    print(summary)
                else:
                    print("Araştırılacak içerik bulunamadı, lüften tekrar deneyiniz...")


            elif "wikipedia" in user_input or "wiki" in user_input:
                    wikipedia = "wikipedia"
                    sentence2 = user_input.replace(wikipedia, "")
                    get_wikipedia_summary(sentence2)
                    summary = get_wikipedia_summary(sentence2)
                    print(summary)

            elif "kimdir" in user_input or "kim" in user_input:
                kim = "kim"
                kimdir = "kimdir"

                if "kim" in user_input:
                    new_sentence_kim = user_input.replace(kim, "")
                    webbrowser.open_new_tab("https://www.google.com/search?q=+" + new_sentence_kim)

                elif "kimdir" in user_input:
                    new_sentence_kimdir = user_input.replace(kimdir, "")
                    webbrowser.open_new_tab("https://www.google.com/search?q=+" + new_sentence_kimdir)

                else:
                    print("Wix bu kişiyle alakalı google'da bir şey bulamadı")

            elif "ip" in user_input or "ipconfig" in user_input or "ifconfig" in user_input or "ip sorgusu" in user_input:
                ip()

            elif "veri çek" in user_input or "veri" in user_input:
                uludag()

            elif "çıkış" in user_input or "çıkış yap" in user_input or "exit" in user_input or "stop" in user_input or "bitir" in user_input or "durdur" in user_input:
                bekle(1)
                print("")
                print("Çıkış yapılıyor iyi günler dilerim Aras")
                print("")
                bekle(1)
                break

            elif "sayı tahmin" in user_input or "sayı tahmin oyunu" in user_input or "tahmin oyunu" in user_input or "oyun oyna" in user_input or "sayı oyunu" in user_input:
                random_sayi = random.randint(0,5)
                sayi = int(input("Wix: 0 ile 5 arasında bir sayı giriniz: "))

                if sayi != random_sayi:
                    print("Wix: tahmin yanlış tekrar deneyin")
                    bekle(1)
                else:
                    print("Wix: doğru tahmin")

            elif "şifre oluştur" in user_input or "sifrele" in user_input or "şifre yaz" in user_input or "şifre" in user_input:
                sifrele()

            elif "fake generator" in user_input or "info generator" in user_input or "fake info generator" in user_input or "fake info" in user_input or "fake infos" in user_input:
                account_generate()

            elif "open" in user_input:
                word_list = user_input.split(" ")
                index_open = word_list.index("open")

                if("chatopenaicom" in word_list[index_open + 1]):
                    url = "https://" + word_list[index_open + 1]
                    url = url.replace("chatopenai", "chat.openai")
                    url = url.replace("com", ".com")
                    webbrowser.open_new_tab(url)

                elif ("com" in word_list[index_open + 1]):
                    com = ".com"
                    url = "https://" + word_list[index_open + 1]
                    url_new = url.replace("com", com)
                    webbrowser.open_new_tab(url_new)
                elif("net" in word_list[index_open + 1]):
                    url = "https://" + word_list[index_open + 1]
                    url = url.replace("https", "http")  # HTTPS'i HTTP ile değiştiriyoruz
                    url = url.replace(".com", "")
                    url = url.replace("net", "")
                    url = url + ".net"
                    webbrowser.open_new_tab(url)
                else:
                    url = "https://" + word_list[index_open + 1] + ".com"
                    webbrowser.open_new_tab(url)

            elif "çeviri" in user_input or "çevir" in user_input or "translate" in user_input:
                if "çeviri" in user_input:
                    ceviri = user_input.replace("çeviri" ,"")
                    webbrowser.open_new_tab("https://translate.google.com.tr/?sl=en&tl=tr&text=" + ceviri + "&op=translate")
                elif "çevir" in user_input:
                    ceviri2 = user_input.replace("çevir", "")
                    webbrowser.open_new_tab("https://translate.google.com.tr/?sl=en&tl=tr&text=" + ceviri2 + "&op=translate")
                elif "translate" in user_input:
                    ceviri3 = user_input.replace("translate", "")
                    webbrowser.open_new_tab("https://translate.google.com.tr/?sl=en&tl=tr&text=" + ceviri3 + "&op=translate")

            elif "şaka yap" in user_input or "şaka yaz" in user_input or "şaka" in user_input or "beni biraz güldür" in user_input or "bizi güldür" in user_input:
                rando = random.randint(0,5)
                saka = sakalar[rando]
                print("")
                print(saka)
                print("")

            elif "yapılacaklar listesi" in user_input or "yapılacaklar" in user_input or "to do list" in user_input:
                to_do_list()

            elif "lstm data" in user_input:
                import csv
                import datetime
                import cryptocompare

                input1 = input("Geçimiş değerlerini çekmek istediğiniz kripto paranın sembolik adını yazınız örneğin 'BTC': ")
                date_input = input("\nVeri setinde olmasını istediğiniz son tarihi sayıların arasına "+"'.' "+"yerine "+"'-' "+"koyarak tarih,ay,gün sırasıyla yazınız yazınız. örneğin 2023-10-01: " )
                def get_historical_btc_price(start_date, end_date):
                    historical_data = cryptocompare.get_historical_price_day(input1, currency='USD', toTs=datetime.datetime.strptime(end_date, '%Y-%m-%d'))
                    prices = []
                    for data in historical_data:
                        date = datetime.datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d')
                        price = data['close']
                        prices.append((date, price))
                        if date == start_date:
                            break
                    return prices

                # Örnek kullanım
                start_date = date_input
                end_date = date_input
                historical_prices = get_historical_btc_price(start_date, end_date)

                # CSV dosyasına yazma
                filename1 = input1+'_prices.csv'
                with open(filename1, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Date', 'Close'])
                    writer.writerows(historical_prices)

                print(input1+f" değerleri '{filename1}' dosyasına kaydedildi.")

            elif "lstm" in user_input:
                print("Hakkınızı kullandınız...")  
            else:
                print("Wix" + responses["diğerleri"])


    while True:
        def usb():
            dosya_yolu = "D:\sa.txt"

            while True:
                try:    
                    with open(dosya_yolu, "r") as dosya:
                        icerik = dosya.read()
                        if "Aras Tokdemir" in icerik:
                            aras()

                except FileNotFoundError:
                    print("Dosya bulunamadı")
                    bekle(1)
                
                except Exception as e:
                    print("Bir hata oluştu: ", str(e))
                    bekle(1)


        print("")
        print("1. Kayıt ol")
        print("2. Giriş yap")
        print("3. Admin girişi")
        print("4. Çıkış yap")
        print("")
        secim = input("Seçiminizi yapın: ")
        print("")

        if secim == '1':
            kullanici = kayit_olustur()
            kullanici_kaydet(kullanici)
            print("")
            bekle(1)
            print("Kayıt başarılı!")
            bekle(1)

        elif secim == '2':
            kullanici_giris()

        elif secim == '3':
            if admin_giris():
                # Admin menüsü veya işlemleri buraya ekleyebilirsiniz
                pass

        elif secim == "Aras":
            bekle(1)
            print("Giriş başarılı!")
            bekle(1)
            aras()
        
        elif secim == "5":
           inptt1 = input("\n bu özellik windows kullanıcıları içindir devam etmek için enter tuşuna basabilirsiniz, exit için çıkış yazmanız yeterli: ")
           inptt1 = inptt1.lower().strip()
           if inptt1 == "exit":
            break
           else:
            usb()

        elif secim == '4' or secim == 'exit' or secim == 'çıkış' or secim == 'cıkıs' or secim == 'stop' or secim == "bitir" or "durdur" in secim:
            bekle(1)
            print("Sistem kapanıyor...\n")
            bekle(1)
            print("by Aras Tokdemir")
            break

        else:
            print("Geçersiz seçim. Tekrar deneyin.")
wix()