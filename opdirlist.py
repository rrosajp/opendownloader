import requests, bs4
import urllib.parse
import shutil, os

# Задаем имя открытой веб директории
u='http://tarsis.info/traum/_/_%D1%82%D0%B0%D0%B9%D0%BD%D0%BE%D0%B5/_%d1%8d%d0%b7%d0%be%d1%82%d0%b5%d1%80%d0%b8%d0%ba%d0%b0/'

# Если нету папки для сохранения айлов то создаем её
if not(os.path.exists('myfiles/')):
    os.makedirs('myfiles/')

# Функция скачивающая файл по его URL
def getmefile(url):
    # Формируем имя под которым файл будет сохранен
    filename = 'myfiles/'+url.split('/')[-1]
    # Преобразовываем русские символы в читаемый вид
    filename=urllib.parse.unquote(filename)
    # Проверяем нет ли файла чтобы не качать повторно
    if not(os.path.exists(filename)):
        print('Качаю: '+urllib.parse.unquote(url))
        # Пробуем сделать запрос на скачивание
        r = requests.get(url, stream=True)
        # Если запрос удачен то:
        if r.status_code == 200:
            # Записываем скачиваемый файл в файл с именем filename
            with open(filename, 'wb') as f1:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f1)
            f1.close()
        
# Рекурсивная функция получающая список всех файлов в каталоге и подкаалогах
def getfiles(url, prefix):
    # Получаем html код страницы со списком директорий  файлов
    s=requests.get(url)
    # Преобразуем в структуру beautiful soup
    b=bs4.BeautifulSoup(s.text, "html.parser")
    # Парсим все ссылки
    p=b.select('a')
    # Проходим все ссылки
    for x in p:
        try:
            z=x['href']
            # Если это каталог то:
            if(z[-1]=='/') and (z!='../') and not('arent' in x.text):
                # Рекурсивно вызываем эту же функцию для обхода подкаталога 
                getfiles(u+prefix+str(z),prefix+str(z))
            else:
                # Если это файл
                if(z!='../') and not('#' in z) and (z[-1]!='/') and ('.' in z):
                    # Качаем файл
                    getmefile(u+prefix+str(z))
        except:
            pass
        
# Делаем вызов рекурсивной функции для начала скачивания
getfiles(u,'')


        
