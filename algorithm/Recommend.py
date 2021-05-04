import pymysql
import math
import datetime
import numpy as np

NumOfBooks = 3000


def getW(user_books):
    """
    计算 书籍相似度矩阵W
    W[u][v]表示物品u和物品v的相似度
    C[u][v]表示喜欢u又喜欢v物品的用户有多少个
    N[u]表示有多少用户喜欢物品u
    :param user_books: 用户及其评分过的书
    :return: 书籍相似度矩阵W，书籍相关矩阵
    """
    W = np.zeros([NumOfBooks, NumOfBooks], dtype=float)
    C = np.zeros([NumOfBooks, NumOfBooks], dtype=float)
    N = np.zeros([NumOfBooks], dtype=float)  # 列向量

    book_relatedbooks = dict()

    for user, books in user_books:
        for bookA in books:
            N[bookA] += 1
            for bookB in books:
                if bookA == bookB:
                    continue
                if bookA not in book_relatedbooks:
                    book_relatedbooks[bookA] = set()
                book_relatedbooks[bookA].add(bookB)
                C[bookA][bookB] += (1/math.log(1+len(books)*1.0))  # 这个公式是Itemcf-IUF的分子部分

    for bookA in range(1, NumOfBooks):
        if bookA in book_relatedbooks:
            for bookB in book_relatedbooks[bookA]:
                W[bookA][bookB] = C[bookA][bookB]/math.sqrt(N[bookA]*N[bookB])

    return W, book_relatedbooks


def k_similar_book(W, book_relatedbooks, k):
    """

    :param W:
    :param book_relatedbooks:
    :param k: k个类似的书籍
    :return: 返回一个字典，key是每个item，value是item对应的k个最相似的物品
    """
    begin = datetime.datetime.now()

    k_similar = dict()
    for i in range(1, NumOfBooks):
        relatedbooks = dict()
        try:
            for x in book_relatedbooks[i]:
                relatedbooks[x] = W[i][x]
            relatedbooks = sorted(relatedbooks.items(), key=lambda: x:x[1], reverse=True)
            k_similar[i] = set(dict(relatedbooks[0:k])) # 返回k个与书籍i最相似的书籍
        except KeyError:
            print(i, " 没有相关书籍")
            k_similar[i] = set()
            for x in range(1, k+1):
                k_similar[i].add(x)
    end = datetime.datetime.now()
    print('共花费', (end - begin).seconds, "秒计算好")
    return k_similar

def GetRecommendation(user, user_books, W, relatedbooks,k ,N ,k_similar_books):
    """

    :param user: 目标用户
    :param user_books: user->books
    :param W: 物品相似度矩阵W
    :param relatedbooks: books->相关的book
    :param k: 从目标用户历史兴趣列表中选取k个与推荐item最为相似的物品
    :param N: 给目标用户推荐N本书籍
    :param k_similar_items: 一个字典，key是书，value是该书对应的k个最相似的书籍
    :return:
    """
    rank = dict()  # key是电影id，value是兴趣大小

    for i in range(NumOfBooks):
        rank[i] = 0

    possible_recommend = set()
    for book in user_books[user]:
        possible_recommend = possible_recommend.union(relatedbooks[book])

    for book in possible_recommend:
        k_books = k_similar_books[book]
        for i in k_books:
            if i in user_books[user]:
                rank[book] += 1.0*W[book][i]

    for rank_key in rank:
        if rank_key in user_books[user]:
            rank[rank_key] = 0

    return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])

def rec_hot_books():
