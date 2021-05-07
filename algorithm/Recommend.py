import math


class RecommendItemCF:
    def __init__(self, train_file):
        """传入数据为一个用户-书籍键值对。而书籍中是书籍-评分键值对。字典中套字典"""
        self.train = train_file


    def item_similarity(self):
        # 建立物品-物品的同现矩阵
        C = dict()  # 物品-物品的同现矩阵
        N = dict()  # 物品被多少个不同用户购买
        for user, items in self.train.items():
            for i in items.keys():
                N.setdefault(i, 0)
                N[i] += 1
                C.setdefault(i, {})
                for j in items.keys():
                    if i == j:
                        continue
                    C[i].setdefault(j, 0)
                    C[i][j] += 1
        # 计算相似度矩阵
        self.W = dict()
        for i, related_items in C.items():
            self.W.setdefault(i, {})
            for j, cij in related_items.items():
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))
        return self.W

    def recommend(self, user, k=3, n=10):
        """给用户user推荐，前K个相关用户的n项item"""
        rank = dict()
        action_item = self.train[user]   # 用户user产生过行为的item和评分
        for item, score in action_item.items():
            for j, wj in sorted(self.W[item].items(), key=lambda x: x[1], reverse=True)[0:k]:
                if j in action_item.keys():
                    # 如果这项物品用户已经产生过行为（看过，评过分），就不推荐这项物品
                    continue
                rank.setdefault(j, 0)
                rank[j] += score * wj
        return dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:n])
