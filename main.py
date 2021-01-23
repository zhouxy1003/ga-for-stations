from genetic_algorithm import *

if __name__ == "__main__":
    p = Problem(30, 5, 40, 0)  # 站点数，车辆数，车的容量，源点id
    cvrp_ga = GASolution(p, 30, 500)  # 染色体个数，迭代次数
    cvrp_ga.Solve()