import time
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # interactive backend
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify


app = Flask(__name__)



def time_complexity_visualizer(algorithm, n_min, n_max, n_step):
    times = []
    input_sizes = list(range(n_min, n_max + n_step, n_step))
    
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()
    ax.set_xlabel('Input size')
    ax.set_ylabel('Running time (seconds)')
    ax.set_title('Algorithm time complexity visualization (Live)')
    line, = ax.plot([], [], 'o-')
    
    for i, n in enumerate(input_sizes):
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)
        
        # Update plot with new data point
        line.set_data(input_sizes[:i+1], times)
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.01)  # Small pause to allow plot to refresh
    
    plt.ioff()  # Disable interactive mode
    plt.show()  # Keep plot open

def linear_search(n):
    for i in range(n):
        if i == n-1:
            return i


def bubble_sort(n):
    arr = np.random.randint(0, 100, n)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def binary_search(n):
    arr = sorted(np.random.randint(0, 100, n))
    target = arr[-1]
    left, right = 0, n - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def nested_loops(n):
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
    return count



# time_complexity_visualizer(bubble_sort, 10, 10000, 10)
# time_complexity_visualizer(linear_search, 10, 10000, 10)
# time_complexity_visualizer(binary_search, 10, 5000, 10)
# time_complexity_visualizer(nested_loops, 10, 3000, 10)


algo = {
    "bubble_sort": bubble_sort,
    "linear_search": linear_search,
    "binary_search": binary_search,
    "nested_loops": nested_loops
}

@app.route("/analyze", methods=["GET"])
def analyze():
    algo_name = request.args.get("algorithm", "bubble_sort").strip('"')
    n_min = int(request.args.get("n_min", 10))
    n_max = int(request.args.get("n_max", 1000))
    n_step = int(request.args.get("n_step", 10))
    
    if algo_name not in algo:
        return jsonify({"error": "Algorithm not found"}), 404
    
    algorithm_value = algo[algo_name]

    fromTime = time.time()
    time_complexity_visualizer(algorithm_value, n_min, n_max, n_step)

    toTime = time.time()

    totalTime = toTime - fromTime
    
    return jsonify({"status" : 200, "message": f"{algo_name} visualization completed.", "n_min": n_min, "n_max": n_max, "n_step": n_step, "total_time": totalTime})


if __name__ == "__main__":
    app.run(port=3000)