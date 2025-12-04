import math
import random


def binary_search(target: float, sorted_array: list) -> tuple:
    low: int = 0
    high: int = len(sorted_array) - 1
    iterations: int = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2

        if sorted_array[mid] < target:
            low = mid + 1
        else:
            upper_bound = sorted_array[mid]
            high = mid - 1
            if math.isclose(sorted_array[mid], target, rel_tol=0.0001):
                break

    return (iterations, upper_bound)


def main():
    data = [value*0.001 for value in range(0, 1010, 10)]
    print(f"find 0.0 in list: {binary_search(0, data)}")
    print(f"find {data[len(data)//2]} in_list {binary_search(data[len(data)//2], data)}")
    print(f"find {data[len(data)-1]} {binary_search(data[len(data)-1], data)}")

    random_search_iterations: int = 10
    while random_search_iterations > 0:
        value: float = data[random.randint(0, len(data)-1)]
        print(f"find {value} in list: {binary_search(value, data)}")
        random_search_iterations -= 1


if __name__ == "__main__":
    main()
