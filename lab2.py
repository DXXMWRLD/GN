from typing import List
from math import log2, ceil
from random import randrange

# Библиотека для crc64
!pip install crc64iso
from crc64iso.crc64iso import crc64

def __hamming_common(src: List[List[int]], s_num: int, encode=True) -> int:
    s_range = range(s_num)
    errors = 0
    for i in src:
        sindrome = 0
        for s in s_range:
            sind = 0
            for p in range(2 ** s, len(i) + 1, 2 ** (s + 1)):
                for j in range(2 ** s):
                    if (p + j) > len(i):
                        break
                    sind ^= i[p + j - 1]
            if encode:
                i[2 ** s - 1] = sind
            else:
                sindrome += (2 ** s * sind)
        if (not encode) and sindrome:
            try:
                i[sindrome - 1] = int(not i[sindrome - 1])
            except IndexError:
                errors += 1
    return errors

def hamming_encode(msg: str, mode: int = 8) -> str:
    result = ""
    msg_b = msg.encode("utf8")
    s_num = ceil(log2(log2(mode + 1) + mode + 1))
    bit_seq = []
    for byte in msg_b:
        bit_seq += list(map(int, f"{byte:08b}"))
    res_len = ceil((len(msg_b) * 8) / mode)
    bit_seq += [0] * (res_len * mode - len(bit_seq))
    to_hamming = []
    for i in range(res_len):
        code = bit_seq[i * mode:i * mode + mode]
        for j in range(s_num):
            code.insert(2 ** j - 1, 0)
        to_hamming.append(code)
    errors = __hamming_common(to_hamming, s_num, True)
    for i in to_hamming:
        result += "".join(map(str, i))
    return result


def hamming_decode(msg: str, mode: int = 8):
    result = ""
    s_num = ceil(log2(log2(mode + 1) + mode + 1))
    res_len = len(msg) // (mode + s_num)
    code_len = mode + s_num
    to_hamming = []
    for i in range(res_len):
        code = list(map(int, msg[i * code_len:i * code_len + code_len]))
        to_hamming.append(code)
    errors = __hamming_common(to_hamming, s_num, False)
    for i in to_hamming:
        for j in range(s_num):
            i.pop(2 ** j - 1 - j)
        result += "".join(map(str, i))
    msg_l = []
    for i in range(len(result) // 8):
        val = "".join(result[i * 8:i * 8 + 8])
        msg_l.append(int(val, 2))
    try:
        result = bytes(msg_l).decode("utf8")
    except UnicodeDecodeError:
        pass
    return result, errors


def noizer(msg: str, mode: int) -> str:
    seq = list(map(int, msg))
    s_num = ceil(log2(log2(mode + 1) + mode + 1))
    code_len = mode + s_num 
    cnt = len(msg) // code_len
    result = ""
    for i in range(cnt):
        to_noize = seq[i * code_len:i * code_len + code_len]
        noize = randrange(code_len)
        to_noize[noize] = int(not to_noize[noize])
        result += "".join(map(str, to_noize))
    return result


def noizer2(msg: str, mode: int) -> str:
    seq = list(map(int, msg))
    s_num = ceil(log2(log2(mode + 1) + mode + 1))
    code_len = mode + s_num 
    cnt = len(msg) // code_len
    result = ""
    for i in range(0, cnt, 3):
        to_noize = seq[i * code_len:i * code_len + code_len]
        noize1 = randrange(code_len)
        noize2 = randrange(code_len)
        to_noize[noize1] = int(not to_noize[noize1])
        to_noize[noize2] = int(not to_noize[noize2])
        result += "".join(map(str, to_noize))
    return result


if __name__ == '__main__':
    # Длинна слова с контрольными битами: 86. Исключая 1, 2, 4, 8, 16, 32, 64 получаем 79
    MODE = 79  
    msg = """ChatGPT был доработан поверх GPT-3.5 с использованием методов обучения как с учителем, так и с подкреплением[7]. В обоих подходах использовались люди-тренеры для улучшения производительности модели. В случае обучения с учителем модель была снабжена беседами, в которых тренеры играли обе стороны: пользователя и помощника по искусственному интеллекту. На этапе подкрепления инструкторы-люди сначала оценивали ответы, которые модель создала в предыдущем разговоре. Эти оценки были использованы для создания моделей вознаграждения, на которых модель была дополнительно доработана с использованием нескольких итераций Proximal Policy Optimization[8][9]. Алгоритмы Proximal Policy Optimization имеют преимущество по затратам по сравнению с алгоритмами Region Policy Optimization; они сводят на нет многие дорогостоящие в вычислительном отношении операции с более высокой производительностью[10][11]. Модели были обучены в сотрудничестве с Microsoft на их суперкомпьютерной инфраструктуре Azure.
По сравнению со своим предшественником, InstructGPT, ChatGPT пытается уменьшить количество вредных и вводящих в заблуждение ответов. Например, в то время как InstructGPT воспринимает сообщение о том, что Христофор Колумб прибыл в США в 2015 году как правдивое, ChatGPT использует информацию о путешествиях Колумба и информацию о современном мире, включая восприятие личности Колумба, чтобы построить ответ, предполагающий, что произошло бы, если бы Колумб приплыл в США в 2015 году[8]. Данные в распоряжении у ChatGPT включают в себя справочные страницы, информацию об интернет-феноменах и информацию о языках программирования[12].
В отличие от большинства чат-ботов, ChatGPT отслеживает состояние пользователя, запоминая предыдущие вопросы и ответы, данные ему в том же разговоре, что, по мнению некоторых журналистов, позволит использовать ChatGPT в качестве персонализированного терапевта[13]. В попытке предотвратить выдачу оскорбительных результатов от запросов пользователей и получение оскорбительных ответов, в ChatGPT запросы фильтруются через API модерации, а потенциально расистские или сексистские подсказки отклоняются[8][13]. 
ChatGPT имеет множество ограничений. Модель вознаграждения ChatGPT, разработанная с учётом человеческого надзора, может быть чрезмерно оптимизирована и, таким образом, снижать производительность, представляя собой закон Гудхарта[14]. При обучении рецензенты предпочитали более длинные ответы, независимо от фактического понимания или фактического содержания[8]. Данные у ChatGPT могут страдать от алгоритмической предвзятости; ответы, включающие расплывчатые описания людей, таких как генеральный директор, могут генерировать ответ, предполагающий, что такой человек, например, является белым мужчиной[15]."""
    
    print(f'\n0) Сообщение:\n\n{msg}')
    checksum = crc64(msg)
    print(f'Контрольная сумма: {checksum}')
    print('\n1) Без ошибок\n')
    enc_msg = hamming_encode(msg, MODE)
    print(f'Кодированное сообщение:\n{enc_msg}')
    dec_msg, err = hamming_decode(enc_msg, MODE)
    print(f'Декодированное сообщение:\n{dec_msg}')
    print(f'Новая контрольная сумма: {crc64(dec_msg)} ')
    print(f'Значения сумм совпадают:{crc64(dec_msg) == checksum}')
    print(f'Совпадение текстов: {msg == dec_msg}')
    print('\n2) Не более 1 ошибки на слово\n')
    noize_msg = noizer(enc_msg, MODE)
    print(f'Кодированное сообщение:\n{noize_msg}')
    dec_msg, err = hamming_decode(noize_msg, MODE)
    print(f'Декодированное сообщение:\n{dec_msg}')
    print(f'Контрольная сумма: {crc64(dec_msg)} ')
    print(f'Значения сумм совпадают:{crc64(dec_msg) == checksum}')
    print(f'Совпадение текстов: {msg == dec_msg}')
    print('\n3) До двух ошибок на каждое 3-ое слово\n')
    noize_msg = noizer2(enc_msg, MODE)
    print(f'Кодированное сообщение:\n{noize_msg}')
    dec_msg, err = hamming_decode(noize_msg, MODE)
    print(f'Декодированное сообщение:\n{dec_msg}')
    print(f'Контрольная сумма: {crc64(dec_msg)} ')
    print(f'Значения сумм совпадают:{crc64(dec_msg) == checksum}')
    print(f'Количество обнаруженных ошибок: {err}')
