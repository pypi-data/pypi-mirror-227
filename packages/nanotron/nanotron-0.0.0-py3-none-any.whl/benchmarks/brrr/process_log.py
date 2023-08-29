import csv
import os
import re


# Function to parse filenames
def parse_filename(filename):
    match = re.search(r"dp_(\d+)_pp_(\d+)_tp_(\d+)_seq_len_(\d+)", filename)
    if match:
        return {"dp": match.group(1), "pp": match.group(2), "tp": match.group(3), "seq_len": match.group(4)}
    else:
        return None


# Process the content of a log file
def process_file_content(filepath):
    max_tflops = 0
    desired_line = ""

    with open(filepath, "r") as f:
        for line in f:
            if "model_tflops_per_gpu" in line:
                current_tflops = float(re.search(r"model_tflops_per_gpu:\s+(\d+.\d+)", line).group(1))
                if current_tflops > max_tflops:
                    max_tflops = current_tflops
                    desired_line = line

    return desired_line


# Extract data from desired line
def extract_data(line):
    data = {}
    data["tokens_per_sec_per_gpu"] = re.search(r"tokens_per_sec_per_gpu:\s+([\d.E+-]+)", line).group(1)
    data["global_batch_size"] = re.search(r"global_batch_size:\s+(\d+)", line).group(1)
    data["model_tflops_per_gpu"] = re.search(r"model_tflops_per_gpu:\s+(\d+.\d+)", line).group(1)
    data["hardware_tflops_per_gpu"] = re.search(r"hardware_tflops_per_gpu:\s+(\d+.\d+)", line).group(1)

    return data


# Main processing
def process_logs(directory):
    results = []
    failed_files = []

    for filename in os.listdir(directory):
        if filename.endswith(".out"):
            parsed_name = parse_filename(filename)
            if parsed_name:
                line = process_file_content(os.path.join(directory, filename))
                if line:
                    data = extract_data(line)
                    results.append(
                        {
                            "dp": parsed_name["dp"],
                            "pp": parsed_name["pp"],
                            "tp": parsed_name["tp"],
                            "seq_len": parsed_name["seq_len"],
                            "tokens_per_sec_per_gpu": data["tokens_per_sec_per_gpu"],
                            "global_batch_size": data["global_batch_size"],
                            "model_tflops_per_gpu": data["model_tflops_per_gpu"],
                            "hardware_tflops_per_gpu": data["hardware_tflops_per_gpu"],
                        }
                    )
                else:
                    failed_files.append(filename)

    # Output to CSV
    with open("output.csv", "w", newline="") as csvfile:
        fieldnames = [
            "dp",
            "pp",
            "tp",
            "seq_len",
            "tokens_per_sec_per_gpu",
            "global_batch_size",
            "model_tflops_per_gpu",
            "hardware_tflops_per_gpu",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in results:
            writer.writerow(row)

    # Print the CSV content
    with open("output.csv", "r") as csvfile:
        print(csvfile.read())

    # Print the failed files
    if failed_files:
        print("\nFailed Files:")
        for f in failed_files:
            print(f)


if __name__ == "__main__":
    # directory = input("Please enter the log directory path: ")
    directory = "/fsx/kunhao/logs/benchmark/llama2_70b"
    process_logs(directory)
