# yep code is ugly, but it works
def calculate(data, findall):
    matches = findall(r"([abc])([+\-]?=)([abc])?([+\-])?((\d+)?)"
                      )  # Если придумать хорошую регулярку, будет просто
    for m in matches:
        if len(m[1]) == 1:
            if len(m[2]) == 0 and m[3] == '':
                data[m[0]] = int(m[-2] or 0)
            if len(m[2]) > 0 and m[3] == '':
                data[m[0]] = data.get(m[2], 0)
            if len(m[2]) > 0 and m[3] == '+':
                data[m[0]] = data.get(m[2], 0) + int(m[-2] or 0)
            if len(m[2]) > 0 and m[3] == '-':
                data[m[0]] = data.get(m[2], 0) - int(m[-2] or 0)
        elif m[1][0:1] == '+':
            if len(m[2]) == 0 and m[3] == '':
                data[m[0]] += int(m[-2] or 0)
            if len(m[2]) > 0 and m[3] == '':
                data[m[0]] += data.get(m[2], 0)
            if len(m[2]) > 0 and m[3] == '+':
                data[m[0]] += data.get(m[2], 0) + int(m[-2] or 0)
            if len(m[2]) > 0 and m[3] == '-':
                data[m[0]] += data.get(m[2], 0) - int(m[-2] or 0)
        elif m[1][0:1] == '-':
            if len(m[2]) == 0 and m[3] == '':
                data[m[0]] -= int(m[-2] or 0)
            if len(m[2]) > 0 and m[3] == '':
                data[m[0]] -= data.get(m[2], 0)
            if len(m[2]) > 0 and m[3] == '+':
                data[m[0]] -= data.get(m[2], 0) + int(m[-2] or 0)
            if len(m[2]) > 0 and m[3] == '-':
                data[m[0]] -= data.get(m[2], 0) - int(m[-2] or 0)

    return data


# editor solution

def calculate(data, findall):
    matches = findall(r"([abc])([+-]?)=([abc])?([+-]?\d+)?")
    for a, sign, b, number in matches:
        right = data.get(b, 0) + int(number or 0)
        if sign == "-":
            data[a] -= right
        elif sign == "+":
            data[a] += right
        else:
            data[a] = right
    return data
