from bs4 import BeautifulSoup
import re
import os


def build_bridge(start, end, path):
    def build_tree(start, end, path):
        link_re = re.compile(r"(?<=/wiki/)[\w()]+")
        files = dict.fromkeys(os.listdir(path), False)
        current_links = [start]
        while current_links:
            new_links = []
            for name in current_links:
                with open("{}{}".format(path, name)) as data:
                    links = re.findall(link_re, data.read())
                for link in links:
                    if files.get(link) is False:
                        files[link] = name
                        if link == end:
                            return files
                        new_links.append(link)
            current_links = new_links

    files = build_tree(start, end, path)
    current_link, bridge = end, [end]
    while current_link != start:
        current_link = files[current_link]
        bridge.append(current_link)
    return bridge


def parse(start, end, path):
    bridge = build_bridge(start, end, path)

    out = {}
    for file in bridge:
        with open("{}{}".format(path, file)) as data:
            soup = BeautifulSoup(data, "lxml")
            body = soup.find(id="bodyContent")

            imgs = len(body.find_all('img', width=lambda x: int(x or 0) > 199))
            headers = sum(
                1 for tag in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if tag.get_text()[0] in "ETC"
            )
            lists = sum(1 for tag in body.find_all(['ol', 'ul']) if not tag.find_parent(['ol', 'ul']))

            tag = body.find_next("a")
            linkslen = -1
            while (tag):
                curlen = 1
                for tag in tag.find_next_siblings():
                    if tag.name != 'a':
                        break
                    curlen += 1
                if curlen > linkslen:
                    linkslen = curlen
                tag = tag.find_next("a")

            out[file] = [imgs, headers, linkslen, lists]

    return out