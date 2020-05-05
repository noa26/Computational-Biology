from cellular_automaton import CellularAutomaton

N = 200
M = 200
LIMIT = 1000
PRINT_FORMAT = "{0}, {1}, {2}\n"


def log_contagion(n, p, f, k=0):

    corona = CellularAutomaton(N, M, p, k=k)
    corona.add_organisms(n)
    rounds = 0

    f.write(PRINT_FORMAT.format('p', 'rounds', 'infected'))
    f.write(PRINT_FORMAT.format(p, rounds, corona.infected_count))

    while corona.infected_count < len(corona.organisms) and rounds < LIMIT:
        corona.move_all()
        corona.update_states()
        rounds += 1
        f.write(PRINT_FORMAT.format(p, rounds, corona.infected_count))


def log_delayed_isolation(n, p, f, k):

    p1, p2, p3, p4 = p

    k_delay_interval = 30
    k_index = 0

    FORMAT = "{0}, {1}, {2}, {3}, {4}\n"
    corona1 = CellularAutomaton(N, M, p1, k=k[0])
    corona2 = CellularAutomaton(N, M, p2, k=k[0])
    corona3 = CellularAutomaton(N, M, p3, k=k[0])
    corona4 = CellularAutomaton(N, M, p3, k=k[0])

    corona1.add_organisms(n)
    corona2.add_organisms(n)
    corona3.add_organisms(n)
    corona4.add_organisms(n)

    f.write(FORMAT.format('rounds',
                          'p = ' + str(p1),
                          'p = ' + str(p2),
                          'p = ' + str(p3),
                          'p = ' + str(p4)))

    rounds = 0

    f.write(FORMAT.format(rounds,
                          corona1.infected_count,
                          corona2.infected_count,
                          corona3.infected_count,
                          corona4.infected_count))

    while rounds < LIMIT and (corona1.infected_count < n or corona2.infected_count < n
                              or corona3.infected_count < n or corona4.infected_count < n):

        if rounds % k_delay_interval and k_index < 4:
            corona1.K = k[k_index]
            corona2.K = k[k_index]
            corona3.K = k[k_index]
            corona4.K = k[k_index]
            k_index += 1

        corona1.move_all()
        corona1.update_states()

        corona2.move_all()
        corona2.update_states()

        corona3.move_all()
        corona3.update_states()

        corona4.move_all()
        corona4.update_states()

        rounds += 1
        f.write(FORMAT.format(rounds,
                              corona1.infected_count,
                              corona2.infected_count,
                              corona3.infected_count,
                              corona4.infected_count))


def log_k_influence(n, p, f, k):

    FORMAT = "{0}, {1}, {2}, {3}, {4}, {5}\n"

    coronas = []
    for val in k:
        corona = CellularAutomaton(N, M, p, k=val)
        corona.add_organisms(n)
        coronas.append(corona)

    f.write("rounds," + str(",".join(["k = " + str(val) for val in k])) + "\n")

    rounds = 0

    f.write(str(rounds) + ", " + ",".join([str(corona.infected_count) for corona in coronas]) + "\n")

    running = [True for _ in coronas]

    while rounds < LIMIT:

        for corona in coronas:
            i = coronas.index(corona)
            if running[i]:
                corona.move_all()
                corona.update_states()
                if corona.infected_count == n:
                    running[i] = False

        rounds += 1
        f.write(str(rounds) + ", " + ",".join([str(corona.infected_count) for corona in coronas]) + "\n")

        if not any(running):
            break


def main():

    # p_values = [0.1, 0.3, 0.5, 0.7]
    # # n_values = [2500, 5000, 10000, 20000, 40000]
    # n_values = [1630]
    # k_values = [0, 0, 0, 0]
    #
    # for n in n_values:
    #     with open(str(n) + "_analysis.csv", "w+") as f:
    #         log_delayed_isolation(n, p_values, f, k_values)
    #     print("finished", n)
    #
    # print("end")

    # k_values = [1, 7, 3, 3]
    #
    # for n in n_values:
    #     with open(str(n) + "_analysis_delayed_k_1_7_3_3.csv", "w+") as f:
    #         log_delayed_isolation(n, p_values, f, k_values)
    #     print("finished", n)
    # print("end of k_1_7_3_3")

    n_values = [10000]
    k_values = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    for n in n_values:
        with open(str(n) + "_K_analysis.csv", "w+") as f:
            log_k_influence(n, 0.3, f, k_values)
            print("finished", n)

    print("end at last")


if __name__ == "__main__":
    main()
