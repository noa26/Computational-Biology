from cellular_automaton import CellularAutomaton

N = 200
M = 200
LIMIT = 1000
PRINT_FORMAT = "{0}, {1}, {2}\n"


def log_contagion(n, p, f):

    corona = CellularAutomaton(N, M, p)
    corona.add_organisms(n)
    rounds = 0

    f.write(PRINT_FORMAT.format('p', 'rounds', 'infected'))
    f.write(PRINT_FORMAT.format(p, rounds, corona.infected_count))

    while corona.infected_count < len(corona.organisms) and rounds < LIMIT:
        corona.move_all()
        corona.update_states()
        rounds += 1
        f.write(PRINT_FORMAT.format(p, rounds, corona.infected_count))


def main():

    p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    n_values = [2000, 6000, 10000, 20000, 40000]

    for n in n_values:
        with open(str(n) + "_analysis.csv", "w+") as f:
            for p in p_values:
                log_contagion(n, p, f)
        print("finished", n)
    print("end")


if __name__ == "__main__":
    main()
