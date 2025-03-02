
# This file is used to generate the data for the graph on the website. The graph will display the start and end dates of the contracts.

def graph_structure(start_dates_list,contract_name_list):

    graph_list = [{"x": start_dates_list[i], "name": contract_name_list[i]} for i in range(len(start_dates_list))]

    return graph_list

