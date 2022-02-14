#17.30

import sqlite3
import sys
import time 
import hashlib
import smtplib
import string
import random
from tkinter import E
from twilio.rest import Client 

account_sid = "AC57a9d64dab50a5f85b98627871d5253f"
auth_Token = "368a3239915ffb92342134582ca17f4d"


supportedMails = ["@gmail.com", "@hotmail.com", "@outlook.com"]
specialChars = ['~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']
sender_Email = "furkanesen1900@gmail.com"
sender_Password = 'jpdkvjsclttdcvww'

attempts = 3 
total_Time = 0
# aryüz fln


def fixer():
        global attempts
        if attempts >= 1:
            print('Bir hata meydana geldi, tekrar deneyin.')
            attempts -= 1
        else: 
            print('Son hakkınızı da kullandınız, program kapatılıyor...')
            sys.exit()
def calcTime(func):
    def inner(*args, **kwargs):
        global total_Time
        start = time.time()
        callBack = func(*args, **kwargs)
        finito = time.time()
        total_Time += (finito - start)
        return callBack 
    return inner
@calcTime
def topla(a, b):
    return a + b 
topla(10, 10)

def isAccountExists(username, email):
    with sqlite3.connect('main.db') as connection:
        cursor = connection.cursor()
        fetchedGuys = cursor.execute(f'SELECT * FROM accounts WHERE username = "{username}" OR email = "{email}"')
        if len(fetchedGuys.fetchall()) >= 1:
            return True 
        else: 
            return False

def simulate_Loginned(username):
    while True:
        gotten = input(f"""
Hesabınıza hoş geldiniz, {username}!

Hesabınızın detaylarını görüntülemek için -> 1
Hesabınızın bilgilerini değiştirmek için -> 2
Hesabınızdan çıkış sağlamak için -> 3

Lütfen bir şey seçiniz.\n""") 
        try:
            gotten = int(gotten)
            if gotten >= 1 and gotten <= 3:
                if gotten == 1:
                    # hesap info göster
                    print('Hesap bilgileriniz veritabanından çekiliyor, lütfen bekleyiniz.')
                    id = getCredits(username, 'id')
                    username = username 
                    email = getCredits(username, 'email')
                    phonenumber = getCredits(username, 'phonenumber')
                    global total_Time
                    inp = input(f"""
Kullanıcı ID: {str(id)}
Kullanıcı adı: {username}

Kullanıcı E-Posta: {email}
Kullanıcı Telefon Numarası: {phonenumber}\n\n(İşlem {str(total_Time)} sn sürdü!)\n""") 
                    if inp == 0: pass 
                    else: sys.exit()
                    total_Time = 0
                elif gotten == 2:
                    # değişim
                    while True:
                        stuff = input("""
Kullanıcı adınızı değiştirmek için -> 1
Şifrenizi değiştirmek için -> 2
Elektronik postanızı değiştirmek için -> 3
Telefon numaranızı değiştirmek için -> 4.
Çift Aşamalı Doğrulama durumunu değiştirmek için -> 5.

Geri dönmek için -> 0.
\n""")
                        try: 
                            stuff = int(stuff)
                            if stuff >= 0 and stuff <= 5:
                                confirmation_Password = input('Bilgilerinizi değişmek için şifrenizi giriniz: \t')
                                if isPass_True(username,confirmation_Password) == True:
                                    if stuff >= 1 and stuff <= 4:
                                        newValue = input('Yeni değeri giriniz: \t')
                                        if stuff == 1:
                                            # kullanıcı adı değiştir
                                            if isAltsValid(username=newValue) == True:
                                                changeCredits(username, 'username', newValue)
                                            pass 
                                        elif stuff == 2:
                                            # şifre değiştir
                                            if isAltsValid(password=newValue) == True:
                                                changeCredits(username, 'password', newValue, True)
                                            pass 
                                        elif stuff == 3:
                                            # eposta değiştir
                                            if isAltsValid(email=newValue) == True:
                                                changeCredits(username, 'email', newValue)
                                            pass 
                                        elif stuff == 4:
                                            # telno değiştir
                                            if isAltsValid(phonenumber=newValue) == True:
                                                changeCredits(username, 'phonenumber', newValue)
                                            pass 
                                    elif stuff == 5:
                                        # 2factorial auth
                                        newValue = int(not bool(int(getCredits(username, 'twoFactorialAuth'))))
                                        if getCredits(username, 'phonenumber') == 'Bilinmiyor':
                                            print('Bu işlem için önce telefonunuzu doğrulamalısınız.')
                                        else:
                                            changeCredits(username, 'twoFactorialAuth', newValue)
                                        pass
                                    else:
                                        time.sleep(1)
                                        pass
                                else:
                                    raise print('Şifreniz hatalı!')
                            else:
                                raise print("Yanlış bir şey girdiniz...")
                        except: 
                            pass 
                    pass 
                elif gotten == 3:
                    print('Başarıyla çıkış yaptınız!')
                    sys.exit()
            else:
                raise print('Belirsiz bir ifade girişi yaptınız.')
        except:
            pass 

def isAltsValid(username="violenceDeveloper", email="furkanesen1900@gmail.com", password="furkan_2005F!!?wda", phonenumber="+905465952986"):
    if len(username) <= 5: raise print('Kullanıcı adınız en az beş karakter uzunluğunda olmaldır.')
    elif (username.isupper() or username.islower()) == True: raise print('Kullanıcı adınızıda büyük harf ve küçük harfler bulunmalıdır.')
    elif any(filter(lambda x: email.endswith(x),supportedMails)) == False: raise print('Desteklenmeyen eposta biçimi.')
    elif any(filter(lambda x: x.isdigit(),password)) == False: raise print('Şifrenizde numerik karakter bulunmalı.')
    elif any(filter(lambda x: x in specialChars, password)) == False: raise print('Şifrenizde özel karakterler bulunmalı.')
    elif len(phonenumber) != 13 and phonenumber.startswith('+') == False: raise print('Telefon numaranız geçersiz.')
    elif isAccountExists(username, email) == True: raise print('Böyle bir email ya da kullanıcı adına ait hesap var.')
    else: return True

def createAccount(username, email, password):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    with sqlite3.connect('main.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO accounts(username, email, password, phonenumber) VALUES("{username}", "{email}", "{password}", "Bilinmiyor")')
        connection.commit()
        print('Hesabınız başarıyla oluşturulmuştur!')


def changeCredits(username, creditType, newValue, willBeHashed=False):
    if willBeHashed == True:
        newValue = hashlib.md(newValue.encode('utf-8')).hexdigest()
    with sqlite3.connect('main.db') as connection:
        print(newValue)
        cursor = connection.cursor()
        result = cursor.execute(f'SELECT `{creditType}` FROM accounts WHERE username = "{username}"')
        fetched = result.fetchone()
        if fetched[0] != newValue:
            cursor.execute(f'UPDATE accounts SET `{creditType}` = "{newValue}" WHERE username = "{username}"')
            connection.commit()
            print(f'{creditType} başarıyla {newValue} olarak değiştirildi')
        else:
            print('Aynı değerler.')

def isPass_True(username, password):
    with sqlite3.connect('main.db') as connection:
        cursor = connection.cursor()
        results = cursor.execute(f'SELECT password FROM accounts WHERE username = "{username}" OR email = "{username}"')
        fetched = results.fetchone()
        if fetched:
            return (hashlib.md5(password.encode('utf-8')).hexdigest() == fetched[0]) 
def createCode():
    alpha = list(string.ascii_lowercase)
    random.shuffle(alpha)
    code = "".join(alpha[:5])
    return code
@calcTime
def getCredits(username, type):
    with sqlite3.connect('main.db') as connection:
        cursor = connection.cursor()
        results = cursor.execute(f'SELECT {type} FROM accounts WHERE username = "{username}" OR email = "{username}"')
        fetched = results.fetchone()
        if fetched:
            return fetched[0]
def inside(gotten):
    if gotten == 1:
        # giriş yapma
        print('Hesabınıza giriş yapmak için gerekli bilgileri giriniz.')
        time.sleep(1)
        username_Or_email = input('Kullanıcı adı ya da eposta adresi: \t')
        password = input('Şifre: \t')
        print('Sunucuya giriş yapmak için istek gönderildi.')
        if isAccountExists(username_Or_email, username_Or_email) == True: 
            if isPass_True(username_Or_email, password) == True:
                # bilgiler doğru, auth kontrolü yap ( 2 auth factor )
                if getCredits(username_Or_email, 'twoFactorialAuth') == 0:
                    print('Başarıyla giriş yaptınız.')
                    simulate_Loginned(username_Or_email)
                else:
                    # sms gönder
                    receiver_Num = getCredits(username_Or_email, 'phonenumber')
                    if receiver_Num != 'Bilinmiyor':
                        code = createCode()
                        client = Client(account_sid, auth_Token)
                        client.messages.create(to=receiver_Num, from_='+18124585769', body=code)
                        codeInput = input('Telefonunuza gönderilen 2-Factorial-Auth referanslı kodu giriniz. \t')
                        if str(codeInput) == str(code):
                            print('Başarılıyla giriş yaptınız.')
                            simulate_Loginned(username_Or_email)
                        else:
                            print('Kod hatalı, program kapatılıyor!')
                            time.sleep(2)
                            sys.exit()
                    time.sleep(1)
                    pass
            else: 
                print('Şifreniz hatalı!')
        else:   
            print('Böyle bir hesap bulunamadı.')
    elif gotten == 2:
        # kayıt olma 
        print('Sizden istenecek olan bilgileri doğru olarak giriniz.')
        time.sleep(1)
        username = input('Kullanıcı adı: \t')
        email = input('Elektronik Postanız: \t')
        password = input('Şifreniz: \t')
        validator = isAltsValid(username, email, password)
        if validator == True:
            # her şey doğrudur
            # hesabı açacağız
            print('Sunucuya hesap oluşturmak için istek gönderildi.')
            createAccount(username, email, password)
    elif gotten == 3:
        # şifre unutma
        method = input("""
Şifrenizi telefonla kurtarmak için -> 1
Şifrenizi eposta ile kurtarmak için -> 2\n""")
        try: 
            method = int(method)
            if method >= 1 and method <= 2:
                username = input('Kullanıcı adınızı giriniz: \t')
                if isAccountExists(username, username) == True:
                    if method == 2:
                        print('Eposta adresinize mail gönderiliyor...')
                        receiver_Email = getCredits(username, 'email')
                        code = createCode()
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(sender_Email, sender_Password)
                        server.sendmail(sender_Email, receiver_Email, code)
                        code_Client_Entered = input('Epostanıza gönderilen 6 haneli kodu girin(VIOLENCE referanslı): \t')
                        if code_Client_Entered == code:
                            print('Hesabınıza geçici olarak giriş yaptınız, şifrenizi değiştirmenizi öneririz.')
                            simulate_Loginned(username)
                        else: 
                            print('İşlem iptal edildi!')
                        # telle kurtar
                    elif method == 1:
                        # maille kurtar
                        print('Telefonunuza mesaj gönderiliyor...')
                        receiver_Num = getCredits(username, 'phonenumber')
                        if receiver_Num != 'Bilinmiyor':
                            code = createCode()
                            client = Client(account_sid, auth_Token)
                            client.messages.create(to=receiver_Num, from_='+18124585769', body=code)
                            code_Client_Entered = input('Telefonunuza gönderilen 6 haneli kodu girin(VIOLENCE referanslı): \t')
                            if code_Client_Entered == code:
                                print('Hesabınıza geçici olarak giriş yaptınız, şifrenizi değiştirmenizi öneririz.')
                                simulate_Loginned(username)
                            else: 
                                print('İşlem iptal edildi!')
                        else:
                            print('hesabınıza kayıtlı telefon no yok')
                else:
                    print('Böyle bir hesap bulunamadı.')
            else:   
                print('Böyle bir method bulunamadı.')
        except: 
            pass 

gotten = input("""
Uygulamaya hoş geldiniz.

1 - Giriş Yapın
2 - Kayıt Olun
3 - Şifremi Unuttum

Birini seçiniz.\n""") 
try: 
    gotten = int(gotten)
    if gotten >= 1 and gotten <= 3:
        inside(gotten)
    else:
        pass 
except:     
    pass
