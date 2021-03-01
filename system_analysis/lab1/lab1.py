from decimal import Decimal
from collections import namedtuple
from copy import deepcopy

from ortools.graph import pywrapgraph

inf = 1000000000000

ProviderSuplierWay = namedtuple(
    'ProviderSuplierWay', ['provider', 'suplier', 'cost', 'flow'])


def solve_min_cost_max_flow(
        start_nodes, end_nodes, capacities, unit_costs, supplies):
    min_cost_flow = pywrapgraph.SimpleMinCostFlow()
    ribs_len = len(start_nodes)
    nodes_len = len(supplies)

    for i in range(0, ribs_len):
        min_cost_flow.AddArcWithCapacityAndUnitCost(
            start_nodes[i], end_nodes[i], capacities[i], unit_costs[i])

    for i in range(0, nodes_len):
        min_cost_flow.SetNodeSupply(i, supplies[i])

    supplied_paths = []
    if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
        for i in range(min_cost_flow.NumArcs()):
            cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)

            if min_cost_flow.Flow(i) > 0 and min_cost_flow.Tail(i) > 0 and min_cost_flow.Head(i) < nodes_len - 1:
                psw = ProviderSuplierWay(
                    provider=min_cost_flow.Tail(i),
                    suplier=min_cost_flow.Head(i),
                    cost=cost, flow=min_cost_flow.Flow(i))
                supplied_paths.append(psw)

        return min_cost_flow.OptimalCost(), supplied_paths
    else:
        return -1, supplied_paths


def generate_dist_price(dist, km_price, downtime_price):
    max_exponent = 0
    dist_price = deepcopy(dist)

    for i in range(len(dist_price)):
        for j in range(len(dist_price[i])):
            dist_price[i][j] = dist_price[i][j] * km_price + downtime_price[j]

            curr_exponent = Decimal(dist_price[i][j]).as_tuple().exponent * -1
            max_exponent = max(min(curr_exponent, 9), max_exponent)

    power = 10 ** max_exponent
    for i in range(len(dist_price)):
        for j in range(len(dist_price[i])):
            dist_price[i][j] = int(dist_price[i][j] * power)

    return (dist_price, power)


def generate_input_data(providers, supliers, dist_price):
    supl_len = len(supliers)
    prov_len = len(providers)
    nodes_len = prov_len + supl_len + 2

    start_nodes = []
    end_nodes = []
    capacities = []
    unit_costs = []

    for prov_ind in range(prov_len):
        start_nodes.append(0)
        end_nodes.append(prov_ind + 1)
        capacities.append(providers[prov_ind])
        unit_costs.append(0)

    for prov_ind in range(1, prov_len + 1):
        for offset in range(1, supl_len + 1):
            supl_ind = prov_len + offset

            start_nodes.append(prov_ind)
            end_nodes.append(supl_ind)
            capacities.append(inf)
            unit_costs.append(dist_price[prov_ind - 1][offset - 1])

    for supl_ind in range(supl_len):
        node_ind = supl_ind + prov_len + 1

        start_nodes.append(node_ind)
        end_nodes.append(nodes_len - 1)
        capacities.append(supliers[supl_ind])
        unit_costs.append(0)

    supplies = [0] * nodes_len
    supplies[0] = sum(providers)
    supplies[nodes_len - 1] = -sum(supliers)

    return (start_nodes, end_nodes, capacities, unit_costs, supplies)


def main():
    providers = [40, 30, 20, 60]
    supliers = [70, 30, 50]

    km_price = 20 / 100 * 2.5
    downtime_price = [mins * 5 for mins in [15, 10, 20]]
    dist = [
        [100, 10, 100],
        [80, 20, 50],
        [35, 50, 50],
        [100, 70, 100]
    ]
    dist_price, power = generate_dist_price(dist, km_price, downtime_price)

    service_price = 100 * 2
    workers_salary = 430 * 4

    input_data = generate_input_data(providers, supliers, dist_price)

    min_price, supplied_paths = solve_min_cost_max_flow(*input_data)
    if min_price != -1:
        total_price = (min_price / power) + service_price + workers_salary
        for i in range(len(supplied_paths)):
            print(
                f'Provider {supplied_paths[i].provider} supplied {supplied_paths[i].flow} with cost of {supplied_paths[i].cost / power} to supplier {supplied_paths[i].suplier}')
        print("\nTotal minimum price: ", total_price)
    else:
        print('There was an issue with the min cost flow input.')


if __name__ == '__main__':
    main()
