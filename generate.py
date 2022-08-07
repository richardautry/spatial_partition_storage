from tqdm import tqdm
import requests
from time import perf_counter_ns
from utils import generate_box, generate_box_per_partition, format_perf_time
from requests.compat import urljoin
import statistics


def get_box_data(box_array):
    data = {
        "x_min": min(box_array[0]),
        "x_max": max(box_array[0]),
        "y_min": min(box_array[1]),
        "y_max": max(box_array[1]),
        "z_min": min(box_array[2]),
        "z_max": max(box_array[2]),
    }
    for key, value in data.items():
        data[key] = int(value)
    return data


if __name__ == "__main__":

    num_requests = 10
    partition_size = 100
    timing_results = []
    api_host = "http://localhost"
    boxes_endpoint = "boxes/"

    boxes_url = urljoin(api_host, boxes_endpoint)
    final_count = 0
    box_generator = generate_box_per_partition(0, 1000, partition_size, dimensions=["x", "y", "z"])
    # Step through partitions
    i = 0
    for box_kwargs in tqdm(list(box_generator)[:num_requests]):
        # Create boxes per partition
        final_count = i
        box_data = get_box_data(generate_box(**box_kwargs))
        start = perf_counter_ns()
        response = requests.post(boxes_url, json=box_data)
        end = perf_counter_ns()
        if response.status_code == 200:
            timing_results.append(end - start)
        else:
            print(f"Response Error. Status Code: {response.status_code}\n"
                  f"Response Data:\n{response.json()}")
        i += 1

    first_time = 0
    if len(timing_results) > 0:
        first_time = timing_results[0]
    last_time = 0
    if len(timing_results) > 1:
        last_time = timing_results[-1]

    results_message = {
        "Average Time: %s": statistics.mean(timing_results),
        "Fastest Time: %s": min(timing_results),
        "Slowest Time: %s": max(timing_results),
        "First Time: %s": first_time,
        "Last Time: %s": last_time
    }

    # TODO: print ms
    print("Results:\n"
          f"Total Requests: {final_count + 1}")

    for message, result in results_message.items():
        print(message % format_perf_time(result))
