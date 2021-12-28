import requests,random,json,os,time
from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Pool
cwd = os.getcwd()
random_angka = random.randint(100,999)
random_angka_dua = random.randint(10,99)
header = {"accept-encoding": "gzip, deflate",
         "content-type": "application/json; charset=utf-8",
        
            "cookie": '_ga=GA1.2.1036020596.1640522998; _gid=GA1.2.534966263.1640522998; cto_bundle=HIJ0z19kUSUyQkNDYzdSR3BKZUhMeW43OExzeEJJV0FwVnNneE03JTJCUUdtZlNyUWhXOGFFT1hzVVB0WkJWJTJCenBhRGclMkIxa2lpWFRORHpCUGF4YVFLUFZzUUdPNWMlMkZWamFuNnI3cXBTbWg5RlExWmh3aEliM2hUcGJ5SlhFaXVFYnprbDU3ZTNZZG1HbVplcTFJYk9EMFFmR3NwN0x3JTNEJTNE; __gads=ID=e1d3c2949c7c834e:T=1640523001:RT=1640523079:S=ALNI_MZRY7sti32QDIM6pYtglv1VnHE37g',
            
            "content-type": "application/json",
        
            "referer": "https://getnada.com/?fbclid=IwAR1wF7PqZG3CMbiGPh9fUMEjilRA2Sy8rVZ-4LSKgLZM0JN8-1APvRMbSSU",
            
            "user-agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }

def sign_up(k):
    k = k
    file_list_akun = "prefix.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    prefix = myfile_akun.read()
    
    prefix_email = prefix.split("@")
    get_mail = prefix_email[1]
    get_user = prefix_email[0]
    email = get_user+f"{k}"+"@"+get_mail
    file_list_akun = "password.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    password = myfile_akun.read()
     
    r = requests.post('https://picsart.com/sign-up', json={f"email":f"{email}","password":f"{password}","isLocal":"false"},headers=header)
 
    soup = BeautifulSoup(r.text, 'html.parser')
    res = json.loads(soup.text)
    if res["message"] == "You are registered successfully":
        print(f"[*] [{email} "+res["message"])     
    else:
        print(f"[*] [{email} "+res["message"])
    n=1
    while True:
        
        if n == 5:
            print("[*] Verification Failed!")
            break
        URL = f'https://getnada.com/api/v1/inboxes/{email}'
        r = requests.get(URL).json()
        #getting the latest message
        
        try:
            global uid
            sleep(2)
            uid = r['msgs'][0]['uid']
        
            mes = requests.get(f'https://getnada.com/api/v1/messages/html/{uid}')
            mes1 = BeautifulSoup(mes.content,'html.parser')
            get_data = mes1.prettify()
            get_data = get_data.split('href="https://picsart.com/activate/')
            get_data = get_data[1].split('style="display: block; padding-left: 45px;')
            get_data = get_data[0]
            get_data = get_data.split('"')
            url_activation = f' https://picsart.com/activate/{get_data[0]}'
            #print(f'[*] URL Activation: {url_activation}')
            
            requests.get(f'https://picsart.com/activate/{get_data[0]}')
            print(f"[*] [{email} Verification Success!")
            with open('ress.txt','w') as f:
                f.write(f"{email}|{password}\n")
            break
        except IndexError:
            print(f"[*] [{email} Your Email doesn't have a new message, Reload!")
            n = n+1
      

if __name__ == '__main__':
    global prefix
    global password
    print("[*] Auto Creator PicsArt and Activation!")
    prefix = input("[*] Main Email: ")
    password = input("[*] Password: ")
    jumlah = input("[*] Multiprocessing: ")
    with open('password.txt','w') as f:
        f.write(password)
    loop_input = int(input("[*] How Much Account: "))
    with open('loop.txt','w') as f:
        f.write('')
    with open('prefix.txt','w') as f:
        f.write(prefix)
    for i in range(1, loop_input+1):
        with open('loop.txt','a+') as f:
            f.write(f'{i}\n')
    file_list_akun = "loop.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    akun = myfile_akun.read()
    list_accountsplit = akun.split()
    k = list_accountsplit
    start = time.time()
    with Pool(int(jumlah)) as p:  
        p.map(sign_up, k)
        
    print(f"[*] {len(k)} Account Done Registrated!")
    end = time.time()
    print("[*] Time elapsed: ", start - end)
