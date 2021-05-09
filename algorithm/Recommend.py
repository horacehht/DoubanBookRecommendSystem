import math
import numpy as np


class RecommendItemCF:
    def __init__(self, train_file):
        """传入数据为所有用户-书籍键值对。而书籍中是书籍-评分键值对。字典中套字典"""
        self.train = train_file
        self.user_num = len(self.train.keys())
        self.book_num = self.get_book_num()

    def get_book_num(self):
        self.books = set()
        for books_and_scores in self.train.values():
            for book in books_and_scores:
                self.books.add(book)  # 用内置函数来加快运行速度
        return len(self.books)

    def ItemSimilarity(self):
        """
        C：同现矩阵
        N：某个item的用户集合
        W：相似度矩阵
        """
        # self.books的索引其实就建立了数字到书的映射
        self.books = list(self.books)
        C = np.zeros([self.book_num, self.book_num])  # 物品-物品的同现矩阵
        N = np.zeros([self.book_num])  # 每本书被多少个用户看过
        # 得到同现矩阵
        for user, books_and_scores in self.train.items():
            for book_A in books_and_scores.keys():
                N[self.books.index(book_A)] += 1
                for book_B in books_and_scores.keys():
                    if book_A == book_B:
                        # 自己跟自己不用计算次数
                        continue
                    C[self.books.index(book_A)][self.books.index(book_B)] += 1

        # 计算物品相似度矩阵
        self.W = np.zeros([self.book_num, self.book_num])
        for i in range(self.book_num):
            for j in range(self.book_num):
                if i == j:
                    continue
                self.W[i][j] = C[i][j]/math.sqrt(N[i]*N[j])

        return self.W

    def recommend(self, user, n=20):
        """给用户user推荐兴趣度最高的n本书"""
        # 建立用户评分列向量,n*1，没评分过的计为0
        user_score_v = np.zeros([self.book_num, 1])
        user_score = self.train[user]
        for book, score in user_score.items():
            user_score_v[self.books.index(book)] = score

        # 物品相似度矩阵*用户评分矩阵
        interest = np.dot(self.W, user_score_v)  # 兴趣度向量
        # 排序后推出最高的n本书籍
        interest_rank_index = np.argsort(interest.T[0])[::-1][:n]
        rec_books = [self.books[i] for i in interest_rank_index]
        return rec_books
