import math
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class DpRecommend:
    def __init__(self, train_file, user):
        self.train = train_file
        self.epsilon = 1  # 隐私参数ε
        self.user_num = len(self.train.keys())
        self.users = list(self.train.keys())
        self.users_map = {self.users[i]: i for i in range(self.user_num)}  # 用户与索引的映射
        self.user = user
        self.user_index = self.users_map[self.user_index]
        self.book_num = self.get_book_num()
        self.books = list(self.books)
        self.books_map = {self.books[i]: i for i in range(self.book_num)}  # 书与索引的映射

    def get_book_num(self):
        """获得书的总数和书的集合"""
        self.books = set()
        for books_and_scores in self.train.values():
            for book in books_and_scores:
                self.books.add(book)  # 用内置函数来加快运行速度
        return len(self.books)

    def get_user_books_matrix(self):
        # 获得用户-物品矩阵
        self.user_books_matrix = np.zeros([self.user_num, self.book_num])
        for user, books_and_ratings in self.train.items():
            for book, rating in books_and_ratings.items():
                self.user_books_matrix[self.users_map[user]][self.books_map[book]] = rating

    def get_item_similarity(self, changed_user_books_matrix):
        """这里传入一个改变了的用户-书籍矩阵，方便之后计算dp的相关参数"""
        item_similarity = cosine_similarity(changed_user_books_matrix.T)
        return item_similarity

    def PNS(self, k):
        pass

    def get_RS(self, i, j):
        """
        Recommendation-Aware Sensitivity，论文第3页右下角
        当删除掉用户的一个评分记录时，两个物品相似度的最大变化RS(i, j)
        :param i: 物品i
        :param j: 物品j
        :return: RS(i, j)
        """
        # 删除用户评分记录，只需要将user对应的评分改为0即可
        # 1.选出用户评分过的物品
        user_rating_record = self.user_books_matrix[self.user_index]  # 用户评分记录
        index_array = np.array(range(len(user_rating_record)))  # 索引行
        with_index_rating = np.stack((user_rating_record, index_array))  # 这是个两行的矩阵
        # with_index_rating第一行是用户的评分记录，第二行是对应的索引
        rated_index = with_index_rating[1][with_index_rating[0] != 0]  # 得到用户评分过物品的索引
        changed = self.user_books_matrix
        original_item_similarity = self.get_item_similarity(self.user_books_matrix)
        difference = []
        for item_index in rated_index:
            # 依此删除用户的一项评分记录，记录最大的物品相似度变化
            changed[self.user_index][item_index] = 0  # 删除该项评分
            changed_item_similarity = self.get_item_similarity(changed)  # 获得变更后的物品相似度矩阵
            difference.append( abs(original_item_similarity[i][j] - changed_item_similarity[i][j]) )
            # 补回用户的该项评分记录
            changed = self.user_books_matrix

        # 返回物品相似度的最大变化
        return max(difference)

    def get_omega(self, s_k, k, item_index):
        """算出参数值ω，论文第4页右下角"""
        rou = 0.5  # 论文中的ρ
        v = 0  # 评分向量的最大长度
        for i in range(self.user_num):
            v = max(v, sum(self.user_books_matrix[i] != 0))

        RS = 0
        for j in range(self.book_num):
            if j == item_index:
                continue
            else:
                RS = max(RS, self.get_RS(item_index, j))

        omega = min(s_k, 4*k*RS/self.epsilon*math.log(k*(v-k)/rou))
        return omega