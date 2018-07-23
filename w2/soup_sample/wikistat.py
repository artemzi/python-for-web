from bs4 import BeautifulSoup
import re
import os
import json

# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    files = dict.fromkeys(os.listdir(path), [])

    with open(path + start, 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find('div', {'id': 'bodyContent'})
    for a in root.findAll('a'):
        if a.has_attr('title') and a.text in files:
            if a['title'] not in files[start]:
                files[start].append({'title': a['title'], 'href': a['href']})

    with open('data.json', 'w') as f:
        json.dump(files, f)
    return files


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    files = build_tree(start, end, path)
    bridge = []
    # TODO Добавить нужные страницы в bridge
    return bridge


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    bridge = [end, start] # build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        # TODO посчитать реальные значения
        imgs = 0  # Количество картинок (img) с шириной (width) не меньше 200
        headers = 0  # Количество заголовков, первая буква текста внутри которого: E, T или C
        linkslen = 0  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        lists = 0  # Количество списков, не вложенных в другие списки

        for img in body.findAll('img'):
            if img.has_attr('width'):
                if int(img['width']) >= 200:
                    imgs += 1

        for h in body.find_all(re.compile(r'h\d+')):
            if h.text[0] in ['E', 'T', 'C']:
                headers += 1

        current = 0
        for a in body.findAll('a'):
            sibling = a.find_next_sibling()
            if sibling:
                for s in sibling:
                    if s.name == 'a':
                        current += 1
            if current > linkslen:
                linkslen = current
                current = 0

        for el in body.find_all(['ul', 'ol']):
            if el.parent.name not in 'li':
                lists += 1

        out[file] = [imgs, headers, linkslen, lists]

    return out

if __name__ == '__main__':
    print(parse('Stone_Age', 'Python_(programming_language)', './wiki/'))