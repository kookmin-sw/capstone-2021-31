
def read_filterList()->list:
    with open('filtering_file.txt', 'r', encoding='utf8') as f:
        filter_list = f.read().splitlines()
        return filter_list


def sort_filterList():
    words = []

    with open('filtering_file.txt', 'r', encoding='utf8') as f:
        words = f.read().splitlines()

    words.sort()

    with open('filtering_file.txt', 'w', encoding='utf8') as f:
        f.write('\n'.join(words))

if __name__ == "__main__":
    words = read_filterList()
    print(words)


