from tqdm import tqdm
import requests
from time import perf_counter
from utils import generate_box
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

    num_requests = 100
    timing_results = []
    api_host = "http://localhost"
    boxes_endpoint = "boxes/"

    boxes_url = urljoin(api_host, boxes_endpoint)
    final_count = 0

    for i in tqdm(range(num_requests)):
        final_count = i
        box_data = get_box_data(generate_box(0, 1000))
        start = perf_counter()
        response = requests.post(boxes_url, json=box_data)
        end = perf_counter()
        if response.status_code == 200:
            timing_results.append(end - start)
        else:
            print(f"Response Error. Status Code: {response.status_code}\n"
                  f"Response Data:\n{response.json()}")

    avg_time = statistics.mean(timing_results)
    fast_time = min(timing_results)
    slow_time = max(timing_results)
    first_time = None
    if len(timing_results) > 0:
        first_time = timing_results[0]
    last_time = None
    if len(timing_results) > 1:
        last_time = timing_results[-1]
    # TODO: print ms
    print("Results:\n"
          f"Total Requests: {final_count + 1}\n"
          f"Average Response Time: {avg_time}s\n"
          f"Fastest Time: {fast_time}\n"
          f"Slowest TIme: {slow_time}\n"
          f"First Time: {first_time}\n"
          f"Last Time: {last_time}")
