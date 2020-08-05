import requests


def getVideoInfo():
    '''
    投稿者と動画名を組みにしたリストを取得する
    '''
    # niconico contents search APIに投げるparameter
    options = {
        'q': 'たべるんごのうた',
        'targets': 'tagsExact',
        'fields': 'userId,title',
        '_sort': '-startTime',
        '_context': 'taberungo-creators-stats',
    }
    temp = []
    for i in [0, 4]:
        for j in range(16):
            data_range = {'_limit': 100,
                          'filters[startTime][gte]': f'2020-0{1+i}-01T00:00:00+09:00',
                          'filters[startTime][lt]': f'2020-0{4+i}-01T00:00:00+09:00',
                          '_offset': j*100}
            print(f'getting data: [{j*100}, {j*100+99}[')
            response = requests.get(
                'https://api.search.nicovideo.jp/api/v2/video/contents/search', params={**options, **data_range})
            # 全て取得し終えたら終了する
            if (response.json() == []):
                break
            # print(response.json())
            temp += response.json()['data']
    print('Finish loading all data')
    for j in range(len(temp)):
        print(f'creator = {temp[j]["userId"]}\ttitile = {temp[j]["title"]}')

    result = {temp[i]['userId']: [temp[j]['title'] for j in range(
        len(temp)) if temp[j]['userId'] == temp[i]['userId']]for i in range(len(temp))}
    sorted_result = sorted(
        result.items(), key=lambda x: len(x[1]), reverse=True)

    print('Finish analyzing')
    for j in range(len(sorted_result)):
        print(
            f'creator = {sorted_result[j][0]}\tn = {len(sorted_result[j][1])}')

    # fileに書き込む
    with open(f'dist/taberungo-list.txt', encoding='utf-8', mode='w') as file:
        for i in range(len(sorted_result)):
            file.write(f'[{str(sorted_result[i][0])}]')
            file.write('\n')
            file.write(
                '\n'.join([f' [{title}]'for title in sorted_result[i][1]]))
            file.write('\n')


if __name__ == "__main__":
    getVideoInfo()
