
def get_titles(file_path):
    titles = []
    for line in open(file_path):
        fields = line.strip().split('\t')
        if len(fields) == 3:
            rh, yh, title = fields
            titles.append((None, title))
        elif len(fields) == 4:
            id, rh, yh, title = fields
            titles.append((id, title))
        elif len(fields) == 6:
            rh, yh, chrome, acq, watch, title = fields
            titles.append((None, title))
        elif len(fields) == 7:
            id, rh, yh, chrome, acq, watch, title = fields
            titles.append((id, title))
    return titles

titles1 = get_titles('titlelist.txt')
titles2 = get_titles('titlelist_2021.txt')

for id, title in titles1:
    if title not in [title2 for id2, title2 in titles2]:
        print("'{}',".format(title))

print('-' * 40)

for id, title in titles2:
    if title not in [title2 for id2, title2 in titles1]:
        print("'{}',".format(id))
