"""Contains the generation of test data"""
import csv
from AlgorithmComparisonTool import AlgorithmComparisonTool


def collect_successful_runs():
    comparison_tool = AlgorithmComparisonTool()


    with open("experiment_data/only_successes.csv", "w") as datafile:
        csv_writer = csv.writer(datafile)
        num_algs = 2
        
        # Write header of data file
        header_row = []
        for i in range(num_algs):
            headers = ["Algorithm", "Square Size", "Total Path Distance", "Total Energy Cost", "Total Traversal Time", ""]
            for header_item in headers:
                header_row.append(header_item)
        header_row.append("Energy Cost Difference")
        header_row.append("Energy Cost/Distance")
        header_row.append("Energy Cost Savings")
        header_row.append("Total Runs")
        csv_writer.writerow(header_row) 
        
        total_runs = 0
        num_successes = 0
        while num_successes < 50 and total_runs < 5000:
                total_runs += 1
                square_size = 50
                comparison_tool.env_graph = comparison_tool.auto_create_graph(square_size, square_size)
                
                start_cell = (0,0)
                end_cell = (square_size - 1, square_size - 1)

                alg_names = ["A*", "Energy Cost A*"]

                # Collect A* data
                a_star_path, _,_ = comparison_tool.run_algorithm("A*", comparison_tool.env_graph, start_cell, end_cell)
                a_star_diagnostic_dict = comparison_tool.get_path_diagnostic_data(a_star_path)
                a_star_cost = a_star_diagnostic_dict["total_energy_cost"]

                # Collect Energy Cost A* data
                en_star_path, _,_ = comparison_tool.run_algorithm("Energy Cost A*", comparison_tool.env_graph, start_cell, end_cell)
                en_star_diagnostic_dict = comparison_tool.get_path_diagnostic_data(en_star_path)               
                en_star_cost = en_star_diagnostic_dict["total_energy_cost"]
                

                # Check for differences in energy cost
                if a_star_cost != en_star_cost and a_star_cost != 0:
                    energy_cost_diff = a_star_cost - en_star_cost
                    success = en_star_cost < a_star_cost
                    if success:
                        print(f"Energy cost difference: {energy_cost_diff}")
                        num_successes += 1
                        data_row = get_data_row(square_size, alg_names, [a_star_diagnostic_dict, en_star_diagnostic_dict])
                        energy_cost_savings = energy_cost_diff / a_star_cost
                        data_row.append(energy_cost_savings)
                        data_row.append(total_runs)
                        csv_writer.writerow(data_row)


def main():
    comparison_tool = AlgorithmComparisonTool()


    with open("experiment_data/thesis_sample.csv", "w") as datafile:
        csv_writer = csv.writer(datafile)
        num_algs = 2
        
        # Write header of data file
        header_row = []
        for i in range(num_algs):
            headers = ["Algorithm", "Square Size", "Total Path Distance", "Total Energy Cost", "Total Traversal Time", ""]
            for header_item in headers:
                header_row.append(header_item)
        header_row.append("Energy Cost Difference")
        header_row.append("Distance/Energy Cost")
        csv_writer.writerow(header_row) 
        
        num_runs = 2
        for i in range(num_runs):

            for square_size in range (5, 11):
                comparison_tool.env_graph = comparison_tool.auto_create_graph(square_size, square_size)
                
                start_cell = (0,0)
                end_cell = (square_size - 1, square_size - 1)

                alg_names = ["A*", "Energy Cost A*"]

                # Collect A* data
                a_star_path, _,_ = comparison_tool.run_algorithm("A*", comparison_tool.env_graph, start_cell, end_cell)
                a_star_diagnostic_dict = comparison_tool.get_path_diagnostic_data(a_star_path)
                a_star_cost = a_star_diagnostic_dict["total_energy_cost"]
                
                #print("A* cost:", a_star_cost)

                # Collect Energy Cost A* data
                en_star_path, _,_ = comparison_tool.run_algorithm("Energy Cost A*", comparison_tool.env_graph, start_cell, end_cell)
                en_star_diagnostic_dict = comparison_tool.get_path_diagnostic_data(en_star_path)               
                en_star_cost = en_star_diagnostic_dict["total_energy_cost"]
                
                csv_writer.writerow(get_data_row(square_size, alg_names, [a_star_diagnostic_dict, en_star_diagnostic_dict]))

                
                #print("Energy Cost A* cost:", en_star_cost)

                # Check for differences in energy cost, and if there is one, record the env
                if a_star_cost != en_star_cost:
                    print(f"Energy cost difference: {a_star_cost - en_star_cost}")
                    success = "success" if en_star_cost < a_star_cost else "fail"
                    filename = f"{square_size}x{square_size}_env_{success}.json"
                    comparison_tool.write_env_to_file(filename)

def get_data_row(square_size, alg_names, alg_diagnostic_dicts):
    data_row = []
    
    for i in range(len(alg_names)):
        alg_name = alg_names[i]
        alg_diagnostic_dict = alg_diagnostic_dicts[i]
        data = [
            alg_name,
            square_size,
            round(alg_diagnostic_dict["total_distance"], 2),
            round(alg_diagnostic_dict["total_energy_cost"], 2),
            round(alg_diagnostic_dict["time_to_traverse"], 2),
            ""
            ]
        for entry in data:
            data_row.append(entry)

    alg_1_cost = alg_diagnostic_dicts[0]["total_energy_cost"]
    alg_2_cost = alg_diagnostic_dicts[1]["total_energy_cost"]
    
    data_row.append(alg_1_cost - alg_2_cost)
    if alg_2_cost != 0:
        data_row.append(alg_2_cost/alg_diagnostic_dicts[1]["total_distance"])

    return data_row


if __name__ == "__main__":
    # main()
    collect_successful_runs()