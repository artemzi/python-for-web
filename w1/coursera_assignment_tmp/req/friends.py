import requests

# yep it's public
ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'

# – Для получения id пользователя по username или user_id:

# https://api.vk.com/method/users.get?v=5.71&access_token=<token>&user_ids=<user_id>

# – Для получения списка друзей:

# https://api.vk.com/method/friends.get?v=5.71&access_token=<token>&user_id=<user_id>&fields=bdate

def get_user_id(uid):
    payload = {'v': '5.71', 'access_token': ACCESS_TOKEN, 'user_ids': uid}
    return requests.get('https://api.vk.com/method/users.get', params=payload)


def get_friends_ages(id):
    payload = {
        'v': '5.71',
        'access_token': ACCESS_TOKEN,
        'user_id': id,
        'fields': 'bdate'
    }
    friends = requests.get(
        'https://api.vk.com/method/friends.get', params=payload)

    ages = []
    for f in friends.json()['response']['items']:
        date = f.get('bdate', '')
        d = date.split(".")
        if len(d) == 3: # append only dates with year
            ages.append(2018 - int(d[-1]))
    return ages

def comparator(age, count):
    return

def calc_age(uid):
    id = get_user_id(uid).json()['response'][0]['id']
    ages = get_friends_ages(id)
    hset = {}
    for a in ages:
        if a not in hset:
            hset[a] = 0
        hset[a] += 1

    res = []
    for age, count in hset.items():
        res.append((age, count))
    # список пар (<возраст>, <количество друзей с таким возрастом>),
    # отсортированный по убыванию по второму ключу (количество друзей)
    # и по возрастанию по первому ключу (возраст)
    return sorted(res, key=lambda e: (e[1] * -1, e[0]))


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
