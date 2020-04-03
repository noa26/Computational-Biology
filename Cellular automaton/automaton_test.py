from cellular_automaton import CellularAutomaton


corona = CellularAutomaton(5, 5)
print(corona.automaton)


x = input("number of organisms: ")
corona.add_organisms(int(x))
print(corona.automaton)

while input('continue? y/n') == 'y':
    corona.move_all()
    print(corona.automaton)
    print()
    corona.update_states()
    print(corona.automaton)
    if len(corona.organisms) == corona.infected_count:
        break

print("end:)")
