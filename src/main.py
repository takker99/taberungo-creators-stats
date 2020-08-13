import requests
import datetime
from pyquery import PyQuery as pq

def getUserNameFromId(userId):
    url=f'https://www.nicovideo.jp/user/{str(userId)}'
    print(f'Access to {url}...')
    dom = pq(url)
    result=dom('head').find('meta[property="profile:username"]').attr['content']
    print(f'Success! userName = {result}')
    return result


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
    now_month = datetime.datetime.now()
    for i in range(now_month.month):
        for j in range(16):
            data_range = {'_limit': 100,
                          'filters[startTime][gte]': f'2020-0{1+i}-01T00:00:00+09:00',
                          'filters[startTime][lt]': f'2020-0{2+i}-01T00:00:00+09:00',
                          '_offset': j*100}
            print(f'getting data: [{j*100}, {j*100+99}[')
            response = requests.get(
                'https://api.search.nicovideo.jp/api/v2/video/contents/search', params={**options, **data_range})
            # 全て取得し終えたら終了する
            if (response.json()['data'] == []):
                print('skip')
                break
            # print(response.json())
            temp += response.json()['data']

    print('Finish loading all data')

    print('Analyzing data...')

    # 投稿者ごとに動画をまとめる
    # - userIdを投稿者名に変換する
    # - 上位20人分を取り出す
    result = {temp[i]['userId']: [temp[j]['title'] for j in range(
        len(temp)) if temp[j]['userId'] == temp[i]['userId']]for i in range(len(temp))}
    sorted_result = { getUserNameFromId(item[0]):item[1] for item in sorted(
        result.items(), key=lambda x: len(x[1]), reverse=True)[:20] }

    print('Finish analyzing')
    # 取得結果の確認
    for key in sorted_result.keys():
        print(
            f'creator = {key}\tn = {len(sorted_result[key])}')

    print('Writing to the text file...')
    # fileに書き込む
    with open(f'dist/taberungo-list.txt', encoding='utf-8', mode='w') as file:
        for key in sorted_result.keys():
            file.write(f' 投稿者: [{key}]')
            file.write('\n')
            file.write(
                '\n'.join([f'  [{title}]'for title in sorted_result[key]]))
            file.write('\n\n')
    print('Successfully finished!')


if __name__ == "__main__":
    getVideoInfo()
