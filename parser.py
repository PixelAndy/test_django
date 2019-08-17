import requests
from bs4 import BeautifulSoup


# 1. GET data - ОК
# 2. how it works - ОК
# 3. eject temperature [+27,+25,+30...+28] - OK
# 4. eject time - OK
# 5. print clear output time and tmptre - OK
#    if need more days use ftab_X_content in "forecastDate" 6 3 (rigth now = 1)

def http_request(adress):
    '''make request and eject some info'''
    r = requests.get(adress)
    soup = BeautifulSoup(r.text, 'lxml')
    txt = soup.find('div', id="ftab_1_content").text
    return txt.strip()


def tempture(all_text):
    '''eject temperature from http_request'''
    temper_mix = []
    temper_C = []
    temper_F = []
    # search and eject all temperature in Fahrenheit and Celsius
    for search in range(0, len(all_text)):
        if all_text[search:search + 11] == 'Температура':
            temper_mix = all_text[search + 22:search + 249]
            break
    # split temperature-text to Celsius an Fahrenheit and make readyble them
    while temper_mix:
        temper_C.append(temper_mix[:4].strip() + ' C')
        temper_F.append(temper_mix[3:10].strip() + ' F')
        temper_mix = temper_mix[10:]
    return temper_C, temper_F


def time_is(all_text):
    '''eject time from http_request'''
    time = []
    today = []
    tomorrow = []
    # search time and eject full time-text
    for search in range(0, len(all_text)):
        if all_text[search:search + 15] == 'Местное время  ':
            time = all_text[search + 15:search + 63]
            # marker need for split day-text
            begin_marker = search - 1
            break
    # split text time for 2 part, today time and tomorrow
    while time[:2] != '00':
        today.append(time[:2])
        time = time[2:]
    while time:
        tomorrow.append(time[:2])
        time = time[2:]
    return today, tomorrow, begin_marker


def day_is(all_text, end_index):
    '''eject weekday from http_request'''
    # start from 11 - because we no need 'День недели'
    text = all_text[11:end_index].strip()
    # split day-text for today & tomorrow
    today, tomorrow = text[:text.find('З')], text[text.find('З'):]
    # make readyble text
    today = today[:7] + ' ' + today[7:].replace(',', ', ')
    tomorrow = tomorrow[:6] + ' ' + tomorrow[6:].replace(',', ', ')
    return today, tomorrow


def main():
    '''main parameters and output some info'''
    adress = 'https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A0%D0%BE' \
    '%D1%81%D1%82%D0%BE%D0%B2%D0%B5-%D0%BD%D0%B0-%D0%94%D0%BE%D0%BD%D1%83'
    read_html = http_request(adress)
    today_time, tomor_time, end_day_marker = time_is(read_html)
    today_day, tomor_day = day_is(read_html, end_day_marker)
    read_temp_C, read_temp_F = tempture(read_html)
    print('{} в {[0]}.00 будет {[0]} / {[0]} \n'.format(today_day, today_time, read_temp_C, read_temp_F))
    print('all data temp\n', read_temp_C, '\n')
    print('all data day\n', today_day, tomor_day, '\n')
    print('all data time\n', today_time, tomor_time)


if __name__ == '__main__':
    main()

