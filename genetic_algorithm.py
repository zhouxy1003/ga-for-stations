import random


class Station:
    s_id = 0
    weight = 0

    def __init__(self, s_id, weight):
        self.s_id = s_id
        self.weight = weight


class Vehicle:
    v_id = 0
    load = 0
    capacity = 40

    def __init__(self, v_id, load, capacity):
        self.v_id = v_id
        self.load = load
        self.capacity = capacity


class Problem:
    n_stations = 30
    n_vehicles = 5
    depot = 0
    capacity = 40
    stations = []
    vehicles = []

    def __init__(self, n_stations, n_vehicles, capacity, depot):
        self.n_stations = n_stations
        self.n_vehicles = n_vehicles
        self.depot = depot
        self.capacity = capacity
        for i in range(n_stations):
            self.stations.append(Station(i+1, 6))  # 这里把weight改一下
        for i in range(n_vehicles):
            self.vehicles.append(Vehicle(i, 0, capacity))


class GASolution:
    chromosomes = []  # 所有染色体
    iterators = []  # 用于分隔车辆
    costs = []  # 每条染色体的目标函数值
    stations = []
    vehicles = []
    n_stations = 30
    n_vehicles = 5
    depot = 0
    capacity = 40
    n_chromosomes = 30  # 染色体个数，即解的个数
    generations = 500  # 迭代次数
    best = 0  # 最优的染色体编号

    def __init__(self, p, n_chromosomes, generations):
        self.n_stations = p.n_stations
        self.n_vehicles = p.n_vehicles
        self.depot = p.depot
        self.capacity = p.capacity
        self.stations = p.stations
        self.vehicles = p.vehicles
        self.n_chromosomes = n_chromosomes
        self.generations = generations

        self.GenerateRandomSolutions()
        for i in range(self.n_chromosomes):
            self.MakeValid(i)
            self.costs.append(0)
        # self.GenerateGreedySolutions()
        self.CalculateTotalCost()  # 计算TSP的解
        self.best = self.costs.index(min(self.costs))  # 选出最优染色体

    def GenerateRandomSolutions(self):
        temp = []
        for i in range(self.n_stations):  # 生成站点序列
            temp.append(i+1)
        for i in range(self.n_chromosomes):  # 打乱站点顺序
            random.shuffle(temp)
            self.chromosomes.append(temp[:])
        for j in range(self.n_chromosomes):  # 初始化iterators
            temp_i = [0]
            for i in range(self.n_vehicles-1):
                s_id = random.randint(1, self.n_stations)
                temp_i.append(s_id)
            temp_i.append(self.n_stations)
            temp_i.sort()
            self.iterators.append(temp_i[:])

    def GenerateRandomIterSolution(self):
        temp = [0]
        for i in range(self.n_vehicles-1):
            s_id = random.randint(1, self.n_stations)
            temp.append(s_id)
        temp.append(self.n_stations)
        temp.sort()
        return temp

    def MakeValid(self, i):
        for j in range(self.n_vehicles-1):
            load = self.vehicles[j].load
            it = self.iterators[i][j]
            while it < self.iterators[i][j+1]:
                load = load + self.stations[self.chromosomes[i][it]-1].weight
                it = it + 1
            if load > self.capacity:
                self.iterators[i][j+1] = self.iterators[i][j+1] - 1
                j = j - 1

        for j in range(self.n_vehicles, 1, -1):
            load = self.vehicles[j-1].load
            it = self.iterators[i][j] - 1
            while it >= self.iterators[i][j - 1]:
                load = load + self.stations[self.chromosomes[i][it]-1].weight
                it = it - 1
            if load > self.capacity:
                self.iterators[i][j - 1] = self.iterators[i][j - 1] + 1
                j = j + 1

    def CheckValidity(self, i):
        for j in range(self.n_vehicles):
            load = 0
            it = self.iterators[i][j]
            while it < self.iterators[i][j+1]:
                load = load + self.stations[self.chromosomes[i][it]-1].weight
                it = it + 1
            if load > self.capacity:
                return 0
        return 1

    def CalculateTotalCost(self):
        for i in range(self.n_chromosomes):
            self.costs[i] = random.randint(1, 100)  # 一个接口，传递self.chromosomes[i]和self.iterators[i]，返回机器学习结果

    def CalculateCost(self, i):
        return random.randint(1, 100)  # 一个接口，传递self.chromosomes[i]和self.iterators[i]，返回机器学习结果

    def Solve(self):
        generation = 0
        while generation < self.generations:
            self.best = self.costs.index(min(self.costs))
            if random.randint(0, 9) % 2 == 0:  # 50%概率交叉
                self.AEXCrossover()
                self.best = self.costs.index(min(self.costs))
            if random.randint(0, 9) % 2 == 0:  # 50%概率iterator变异，左移
                r = random.randint(0, self.n_chromosomes-1)
                temp_i = self.iterators[r]
                self.MutateIterLeft(r, random.randint(0, self.n_vehicles))
                c = self.CalculateCost(r)
                if c < self.costs[r]:
                    self.costs[r] = c
                else:
                    self.iterators[r] = temp_i
                self.best = self.costs.index(min(self.costs))
            else:  # 50%概率iterator变异，右移
                r = random.randint(0, self.n_chromosomes - 1)
                temp_i = self.iterators[r]
                self.MutateIterRight(r, random.randint(0, self.n_vehicles))
                c = self.CalculateCost(r)
                if c < self.costs[r]:
                    self.costs[r] = c
                else:
                    self.iterators[r] = temp_i
                self.best = self.costs.index(min(self.costs))
            if random.randint(0, 99) < 50:  # 50%概率染色体变异，反转一个片段
                self.Mutate()
                self.best = self.costs.index(min(self.costs))
            if random.randint(0, 99) < 50:  # 50%概率染色体中两个站点交换
                self.RandomSwap()
                self.best = self.costs.index(min(self.costs))
            self.CalculateTotalCost()
            generation = generation + 1
        self.GenerateBestSolution()

    def AEXCrossover(self):  # 交叉操作
        p1 = self.TournamentSelection()
        p2 = self.TournamentSelection()
        child = []
        reached = set()
        itp1 = self.chromosomes[p1]
        itp2 = self.chromosomes[p2]
        child.append(itp1[0])  # 子染色体的起始站点
        reached.add(child[len(child) - 1])
        cnt = 0  # 记录奇偶次数
        while len(child) < self.n_stations:
            if cnt % 2 == 0:  # 交替在两个父染色体中查找下一个站点加入child中
                it2 = itp2.index(child[len(child) - 1])  # 查找child末尾元素在父染色体中的位置
                if it2 != self.n_stations - 1 and not (itp2[it2 + 1] in reached):
                    n2 = itp2[it2 + 1]
                else:
                    while 1:
                        it2 = it2 + 1
                        if it2 == self.n_stations:
                            it2 = 0
                        if not (itp2[it2] in reached):
                            n2 = itp2[it2]
                            break
                child.append(n2)
                reached.add(n2)
            else:
                it1 = itp1.index(child[len(child) - 1])
                if it1 != self.n_stations-1 and not (itp1[it1+1] in reached):
                    n1 = itp1[it1+1]
                else:
                    while 1:
                        it1 = it1 + 1
                        if it1 == self.n_stations:
                            it1 = 0
                        if not (itp1[it1] in reached):
                            n1 = itp1[it1]
                            break
                child.append(n1)
                reached.add(n1)
            cnt = cnt + 1
        self.chromosomes.append(child)

        r = random.randint(0, 100)  # 随机生成iterator
        if r < 20:
            self.iterators.append(self.GenerateRandomIterSolution())
        elif r < 60:
            self.iterators.append(self.iterators[p1])
        else:
            self.iterators.append(self.iterators[p2])
        self.MakeValid(self.n_chromosomes)
        if self.CheckValidity(self.n_chromosomes):
            self.costs.append(self.CalculateCost(self.n_chromosomes))
            self.InsertionBySimilarity()  # 删除一个不好的染色体
        else:
            self.chromosomes.pop()
            self.iterators.pop()

    def MutateIterLeft(self, i, j_in):
        if j_in == self.n_vehicles or j_in == 0:
            return 0
        if self.iterators[i][j_in] > self.iterators[i][j_in-1]:
            self.iterators[i][j_in] = self.iterators[i][j_in] - 1
        for j in range(j_in, self.n_vehicles-1):
            load = 0
            it = self.iterators[i][j]
            while it < self.iterators[i][j+1]:
                load = load + self.stations[self.chromosomes[i][it]-1].weight
                it = it + 1
            if load > self.capacity:
                self.iterators[i][j+1] = self.iterators[i][j+1] - 1
                j = j - 1
        for j in range(self.n_vehicles, 1, -1):
            load = 0
            it = self.iterators[i][j] - 1
            while it >= self.iterators[i][j - 1]:
                load = load + self.stations[self.chromosomes[i][it]-1].weight
                it = it - 1
            if load > self.capacity:
                self.iterators[i][j - 1] = self.iterators[i][j - 1] + 1
                j = j + 1
        return 1

    def MutateIterRight(self, i, j_in):
        if j_in == self.n_vehicles or j_in == 0:
            return 0
        if self.iterators[i][j_in] < self.iterators[i][j_in-1]:
            self.iterators[i][j_in] = self.iterators[i][j_in] + 1
        for j in range(self.n_vehicles, 1, -1):
            load = 0
            it = self.iterators[i][j] - 1
            while it >= self.iterators[i][j - 1]:
                load = load + self.stations[self.chromosomes[i][it]-1].weight
                it = it - 1
            if load > self.capacity:
                self.iterators[i][j - 1] = self.iterators[i][j - 1] + 1
                j = j + 1
        for j in range(j_in, self.n_vehicles-1):
            load = 0
            it = self.iterators[i][j]
            while it < self.iterators[i][j+1]:
                load = load + self.stations[self.chromosomes[i][it]-1].weight
                it = it + 1
            if load > self.capacity:
                self.iterators[i][j+1] = self.iterators[i][j+1] - 1
                j = j - 1
        return 1

    def Mutate(self):
        cnt = 0
        while cnt < 20:
            self.best = self.costs.index(min(self.costs))
            r = random.randint(0, self.n_chromosomes - 1)
            i1 = random.randint(1, self.n_stations - 1)
            i2 = random.randint(1, self.n_stations - 1)
            if i1 > i2:
                i1, i2 = i2, i1
            self.chromosomes[r][i1:i2 + 1] = self.chromosomes[r][i2:i1 - 1:-1]  # 反转i1与i2之间的站点
            temp_it = self.iterators[r]
            self.MakeValid(r)
            c = self.costs[r]
            self.costs[r] = self.CalculateCost(r)
            if c < self.costs[r]:  # 旧解更好，回滚
                self.chromosomes[r][i1:i2 + 1] = self.chromosomes[r][i2:i1 - 1:-1]
                self.costs[r] = c
                self.iterators[r] = temp_it
                cnt = cnt + 1
            elif self.CheckValidity(r):
                break

    def RandomSwap(self):
        cnt = 0
        while cnt < 20:
            self.best = self.costs.index(min(self.costs))
            r = random.randint(0, self.n_chromosomes - 1)
            i1 = random.randint(0, self.n_stations - 1)
            i2 = random.randint(0, self.n_stations - 1)
            self.chromosomes[r][i1], self.chromosomes[r][i2] = self.chromosomes[r][i2], self.chromosomes[r][i1]
            temp_it = self.iterators[r]
            self.MakeValid(r)
            c = self.costs[r]
            self.costs[r] = self.CalculateCost(r)
            if c < self.costs[r]:  # 旧解更好，回滚
                self.chromosomes[r][i2], self.chromosomes[r][i1] = self.chromosomes[r][i1], self.chromosomes[r][i2]
                self.costs[r] = c
                self.iterators[r] = temp_it
                cnt = cnt + 1
            elif self.CheckValidity(r):
                break

    def TournamentSelection(self):  # 随机选出3个染色体中最好的一个
        i1 = random.randint(0, self.n_chromosomes-1)
        i2 = random.randint(0, self.n_chromosomes-1)
        i3 = random.randint(0, self.n_chromosomes-1)
        if self.costs[i1] <= self.costs[i2] and self.costs[i1] <= self.costs[i3]:
            return i1
        elif self.costs[i2] <= self.costs[i1] and self.costs[i2] <= self.costs[i3]:
            return i2
        else:
            return i3

    def InsertionBySimilarity(self):
        self.best = self.costs.index(min(self.costs))
        flag = 1
        for i in range(self.n_chromosomes):  # 如果两个解的差距在2%以内，删除这个染色体
            if i != self.best and self.costs[self.n_chromosomes] - self.costs[i] < 2 * (self.costs[self.best] / 100.0):
                del self.chromosomes[i]
                del self.iterators[i]
                del self.costs[i]
                flag = 0
                break
        if flag:
            self.DeleteRandomChromosome()

    def DeleteRandomChromosome(self):
        r = random.randint(0, self.n_chromosomes)
        while r == self.best:
            r = random.randint(0, self.n_chromosomes)
        del self.chromosomes[r]
        del self.iterators[r]
        del self.costs[r]

    def GenerateBestSolution(self):
        self.best = self.costs.index(min(self.costs))
        print(self.chromosomes[self.best])
        print(self.iterators[self.best])
        print(self.costs[self.best])





