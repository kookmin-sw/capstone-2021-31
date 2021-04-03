import csv
import pandas as pd
from konlpy.tag import Okt
from collections import Counter
import numpy as np
import os
import glob
from datetime import datetime, timedelta
from enum import Enum, auto
from filter_keyword import *

TMP = '_v2'
CRAWLING_FOLDER_PATH = '../../data/crawling_data'
KEYWORD_FOLDER_PATH = '../../data/hot_keyword_data'

FILTER_KEYWORD = read_filterList(empty=False)

WEIGHT = [1,1,1,1,1,
          1,1,1,1,1,
          1,1,1,1,1,
          1,1,1,1,1]
#
# WEIGHT = [4, 4, 3, 3, 2,
#           2, 2, 2, 2, 2,
#           1, 1, 1, 1, 1,
#           1, 1, 1, 1, 1, ]


# OUTPUT TYPE Enum initial
class OUTPUT_TYPE(Enum):
    DAILY = 'D'
    WEEKLY = 'W'
    TOTAL = 'T'


def get_WEIGHT(size=200):
    weight = np.array(WEIGHT, dtype=np.int32)[:, np.newaxis]
    section = np.ones(200//len(WEIGHT))[np.newaxis]
    res = weight * section
    res = res.reshape(-1)
    res = res.astype(np.int32)
    return res


def get_daily_df(someday_date, folder_path) -> pd.DataFrame:
    li = []
    dfd = pd.DataFrame()
    some_date_str = someday_date.strftime('%y_%m_%d')

    files_path = os.path.join(folder_path, some_date_str + "_??.csv")
    all_files = glob.glob(files_path)

    for file_path in all_files:
        dfd = pd.read_csv(file_path, encoding='utf8')
        print('dfd shape', dfd.shape)
        li.append(dfd)

    if len(li):  # check if li is empty
        dfd = pd.concat(li, axis=0, ignore_index=True)

    return dfd


def get_dataFrame(today_date: datetime, folder_path, output_type: OUTPUT_TYPE) -> pd.DataFrame:
    """
    :param path:
    :param type:
        'd' = get daily keyword
        'w' = get weekly keyword
        't' = get total keywodf_initrd
    :return:
    """
    li = []
    df = pd.DataFrame()

    # get one day`s dataFrame
    if output_type == OUTPUT_TYPE.DAILY:
        df = get_daily_df(today_date, folder_path)

    # get one week`s dataFrame
    elif output_type == OUTPUT_TYPE.WEEKLY:
        # get monday of a specific week
        firstday = today_date - timedelta(days=today_date.weekday())

        for i in range(7):
            some_date = firstday + timedelta(days=i)

            dfd = get_daily_df(some_date, folder_path)
            li.append(dfd)

        df = pd.concat(li, axis=0, ignore_index=True)

    # get total dataFrame
    elif output_type == OUTPUT_TYPE.TOTAL:
        files_path = os.path.join(folder_path, "*.csv")
        all_files = glob.glob(files_path)

        for file_path in all_files:
            dfd = pd.read_csv(file_path, encoding='utf8')
            li.append(dfd)
        df = pd.concat(li, axis=0, ignore_index=True)
    else:
        print('타입을 올바르게 선언하세요')

    return df


def set_output_filename(some_date: datetime, output_type):
    result = 'error.csv'
    some_date_str = some_date.strftime('%y-%m-%d')
    today_date_str = datetime.today().strftime('%y-%m-%d')

    if output_type == OUTPUT_TYPE.DAILY:
        result = f'D_{some_date_str}[{today_date_str}]{TMP}.csv'

    elif output_type == OUTPUT_TYPE.WEEKLY:
        week_number = (some_date.day - 1) // 7 + 1
        result = f'W_{some_date.strftime("%y")}-{some_date.month:0>2}_{week_number:0>2}[{today_date_str}]{TMP}.csv'

    elif output_type == OUTPUT_TYPE.TOTAL:
        result = f'T_[{today_date_str}]{TMP}.csv'
    else:
        result = 'error.csv'

    return result


def post_process_df(df: pd.DataFrame):
    df_result = df

    # NaN 값 ''로 대체
    df_result = df.fillna('')
    # 사이트 url 제거
    df_result.replace(
        to_replace='(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?',
        value='', regex=True, inplace=True)
    # 특수문자 제거
    df_result.replace(to_replace='[^\w\s,`]', value='', regex=True, inplace=True)

    # 필터목록 키워드 제거
    # df_result['description'] = df_result['description'].str.replace(pat=r''+'|'.join(FILTER_KEYWORD)+'',  repl=r'', regex=True)
    df_result.replace(to_replace='|'.join(FILTER_KEYWORD), value='', regex=True, inplace=True)

    print('df_result', df_result.shape)

    return df_result


def get_corpus(df, attrs=['title'], weight=np.ones(20)):
    corpus_np = np.empty((1,200))
    for attr in attrs:
        line_list = []
        attr_np = df[attr].values.flatten()

        attr_np = attr_np.reshape(len(attr_np)//200, 200)

        corpus_np = np.vstack((corpus_np, attr_np))

    ## 가중치 부여
    corpus_np = np.delete(corpus_np, 0, 0)
    weight_np =get_WEIGHT()

    corpus_np = corpus_np * weight_np
    corpus_np = np.ravel(corpus_np)

    corpus = ''.join(corpus_np)
    return corpus


def get_keywords(corpus):
    # 분석기 선언
    nlpy_ko = Okt()

    # 명사만 추출
    nouns = nlpy_ko.nouns(corpus)
    count = Counter(nouns)

    result = []
    tags = []

    for n, c in count.most_common():  # 상위 20개 저장
        dics = {'keyword': n, 'count': c}
        if len(dics['keyword']) >= 2 and len(tags) <= 49:
            result.append(dics)
            tags.append(dics['keyword'])

    return result


if __name__ == "__main__":
    ## 입출력 변수 설정
    output_type = OUTPUT_TYPE.DAILY
    some_date_str = '21-03-24'
    some_date = datetime.today() - timedelta(days=0) if some_date_str == '' else datetime.strptime(some_date_str,'%y-%m-%d')
    #attrs = ['title', 'description', 'tags']
    attrs = ['title', 'description']

    print(set_output_filename(some_date, output_type))
    ## 크롤링 파일 불러오기
    df_init = get_dataFrame(some_date, CRAWLING_FOLDER_PATH, output_type)

    ## 크롤링 데이터 후처리
    print('{work:-^20}'.format(work='processing'))
    df = post_process_df(df_init)

    ## 말뭉치 얻기
    print('{work:-^20}'.format(work='get corpus'))
    corpus = get_corpus(df, attrs)

    # # ## 키워드 추출
    print('{work:-^20}'.format(work='get keyword'))
    keywords_list = get_keywords(corpus)

    # ## 결과 저장
    output_path = os.path.join(KEYWORD_FOLDER_PATH, set_output_filename(some_date, output_type))
    df_output = pd.DataFrame(keywords_list).sort_values(by='count', ascending=False)

    df_output.to_csv(output_path)
    print('result =',set_output_filename(some_date, output_type))