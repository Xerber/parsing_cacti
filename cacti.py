import requests
from bs4 import BeautifulSoup as bs
from pythonping import ping
import time
import config

#--Функция прочёсывает кактус и заполняет список занятых IP + делает список свободыных IP
def ip_bring(wrange):
    all_ip=[]
    r = session.post('http://'+config.ip+'/host.php?sort_column=hostname&sort_direction=ASC&host_template_id=-1&host_status=-1&filter='+wrange+'&host_rows=5000&page=1',data=login_data,headers=headers)
    soup = bs(r.text, 'lxml')
    trs = soup.find_all('tr',attrs={'bgcolor':{'#E7E9F2','#F5F5F5'}})
    for tr in trs:
        all_ip.append(tr.find_all('td')[-5].text)
    print('Диапазон: '+wrange+'\nЗанято: '+str(len(all_ip))+'\nСвободно: '+str((250-len(all_ip))))
    free_ip=[]
    free=5
    while free<255:
        if wrange+str(free) not in all_ip:
            free_ip.append(wrange+str(free))
        free+=1
    if output.lower()in('да','lf','yes'):
        print('Свободные IP:')
        for ip in free_ip[0:hm_out]:
            print(ip)
    if check.lower()in('да','lf'):
        warn_ip=[]
        start_time = time.time()
        for ip in free_ip:
            response_list=ping(ip,verbose=False, count=1, timeout=0.1)
            if response_list._responses[0].success:
                warn_ip.append(str(ip))
        if len(warn_ip)!=0:
            print("Обнаружены не добавленные айпи:\n"+str(warn_ip))
        else:
            print('--- Занятых IP нет. На проверку затрачено: %s секунд ---' % (time.time() - start_time))
    else: print('---------------------------')

#--
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
login_data = {
        'login_username':config.username,
        'login_password':config.password,
        'action':'login'}

session = requests.session()
r = session.get('http://'+config.ip+'/index.php',headers=headers)
soup = bs(r.content, 'lxml')
while True:
    print('---------Параметры---------')
    wrange=input('Введите диапазон айпи. Пример: 10.4.9.\n')
    check=input('Проверять на занятость? Да/Нет\n')
    output=input('Выводить свободные айпи? Да/Нет\n')
    if output.lower()in('да','lf','yes'):
        hm_out=int(input('Какое количество ip выводить?\n'))
    print('---------------------------')


    if wrange.lower()in('все','all'):
        wrange=['10.4.9.','10.6.0.','10.6.1.','10.6.2.','10.6.3.','10.6.4.','10.6.5.','10.6.6.','10.6.7.']
        for dest in wrange:
            ip_bring(dest)
    else:
        ip_bring(wrange)
