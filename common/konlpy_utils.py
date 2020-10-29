from konlpy.tag import *
from enum import Enum


class TokenMode(Enum):
    hannanum = 1
    kkma = 2
    komoran = 3
    mecab = 4
    okt = 5

hannanum = Hannanum() # 한나눔. KAIST Semantic Web Research Center 개발.
kkma = Kkma()         # 꼬꼬마. 서울대학교 IDS(Intelligent Data Systems) 연구실 개발.
komoran = Komoran()   # 코모란. Shineware에서 개발.
# mecab = Mecab()       # 메카브. 일본어용 형태소 분석기를 한국어를 사용할 수 있도록 수정.
    # Install guide : https://i-am-eden.tistory.com/9
okt = Okt()           # Open Korean Text: 오픈 소스 한국어 분석기. 과거 트위터 형태소 분석기.


def tokeniz_morphs(string, mode=TokenMode.okt):
    if mode is TokenMode.hannanum:
        morphs = hannanum.morphs(string)
    elif mode is TokenMode.kkma:
        morphs = kkma.morphs(string)
    elif mode is TokenMode.komoran:
        morphs = komoran.morphs(string)
    elif mode is TokenMode.mecab:
        # morphs = mecab.morphs(string)
        print("Mecab는 추가설치가 필요합니다.")
    elif mode is TokenMode.okt:
        morphs = okt.morphs(string)
    return morphs

def tokeniz_nouns(string, mode=TokenMode.okt):
    if mode is TokenMode.hannanum:
        nouns = hannanum.nouns(string)
    elif mode is TokenMode.kkma:
        nouns = kkma.nouns(string)
    elif mode is TokenMode.komoran:
        nouns = komoran.nouns(string)
    elif mode is TokenMode.mecab:
        # nouns = mecab.nouns(string)
        print("Mecab는 추가설치가 필요합니다.")
    elif mode is TokenMode.okt:
        nouns = okt.nouns(string)
    return nouns

def tokeniz_pos(string, mode=TokenMode.okt):
    if mode is TokenMode.hannanum:
        pos = hannanum.pos(string)
    elif mode is TokenMode.kkma:
        pos = kkma.pos(string)
    elif mode is TokenMode.komoran:
        pos = komoran.pos(string)
    elif mode is TokenMode.mecab:
        # pos = mecab.pos(string)
        print("Mecab는 추가설치가 필요합니다.")
    elif mode is TokenMode.okt:
        pos = okt.pos(string)
    return pos




