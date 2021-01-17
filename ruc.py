import logging

'''整理RIME自动生成的五笔词库'''

file = "/Users/huqi/Library/Rime/user.txt"      #user.txt文件地址
MAX_COUNT = 10                                  #使用次数为MAX_COUNT以下的词组，全部删除

HEADER_COUNT = 5
logging.basicConfig(level=logging.WARNING)

def data_to_str(data):
    str = "%s\t%s\t%s\n" % (data['word'], data['code'], data['count'])
    return str

def write_list(header, list, file):
    '''把整理好的词典写到文件中'''

    with open(file, 'w') as f:
        for h in header:
            f.writelines(h)

        for l in list:
            str = data_to_str(l)
            f.writelines(str)

def clear_list(list):
    '''整理词典'''

    result = []

    for l in list:
        if l['count'] >= MAX_COUNT:
            result.append(l)

    logging.info('result count:%s' % len(result))

    return result


def load_file(file):
    '''读取词典内容'''

    header = []
    list = []
    with open(file, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if i < HEADER_COUNT:
                header.append(line)
                continue

            body = {}
            word = ''
            code = ''
            count = 0
            enc = ''
            length = len(line.split())

            if length == 3:
                word, code, count = line.split()
            elif length == 4:
                word, enc, code, count = line.split()
            else:
                raise AssertionError

            logging.info('%s %s %s' % (word, code, count))

            body['word'] = word
            body['code'] = code
            body['count'] = int(count)

            list.append(body)

        return header, list

def main():
    header, list = load_file(file)
    result = clear_list(list)
    write_list(header, result, file)

if __name__ == "__main__":
    main()