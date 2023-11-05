import random
import tracemalloc
import time

class ArrayGenerator:
    START = 0
    END = 20000

    def __init__(self, n, seed=10):
        self.n = n
        self.seed = seed
        self.arrays = {
            'Randomized': None,
            'Sorted': None,
            'Reversed': None
        }

    def generate_list(self):
        random.seed(self.seed) # Agar dataset reproducible

        self.arrays['Randomized'] = [
            random.randint(ArrayGenerator.START, ArrayGenerator.END)
            for _ in range(self.n)
        ]
        self.arrays['Sorted'] = sorted(self.arrays['Randomized'])
        self.arrays['Reversed'] = self.arrays['Sorted'][::-1]

    def write_to_file(self):
        if self.arrays['Randomized']:
            with open(f"randomized_{self.n}_seed{self.seed}.txt", "w") as file:
                for num in self.arrays['Randomized']:
                    file.write(f"{num}\n")
        if self.arrays['Sorted']:
            with open(f"sorted_{self.n}_seed{self.seed}.txt", "w") as file:
                for num in self.arrays['Sorted']:
                    file.write(f"{num}\n")
        if self.arrays['Reversed']:
            with open(f"reversed_{self.n}_seed{self.seed}.txt", "w") as file:
                for num in self.arrays['Reversed']:
                    file.write(f"{num}\n")


def randomized_quicksort(A, left, right):
    if left < right:
        final_pivot_pos = randomized_partition(A, left, right)
        randomized_quicksort(A, left, final_pivot_pos - 1)
        randomized_quicksort(A, final_pivot_pos + 1, right)

def randomized_partition(A, left, right):
    rand = random.randrange(left, right)
    A[rand], A[right] = A[right], A[rand]

    pivot = A[right]
    last_filled = left - 1
    for i in range(left, right):
        if A[i] <= pivot:
            last_filled += 1
            A[last_filled], A[i] = A[i], A[last_filled]
    last_filled += 1
    A[last_filled], A[right] = A[right], A[last_filled]

    return last_filled


def cbis(A):
    POP = 0
    for i in range(1, len(A)):
        key = A[i]
        if key >= A[POP]:
            place = binary_loc_finder(A, POP + 1, i - 1, key)
        else:
            place = binary_loc_finder(A, 0, POP - 1, key)
        POP = place
        place_inserter(A, place, i)
    return A

def binary_loc_finder(A, start, end, key):
    if start == end:
        if A[start] > key:
            return start
        else:
            return start + 1
    if start > end:
        return start
    else:
        mid = (start + end) // 2
        if A[mid] < key:
            return binary_loc_finder(A, mid + 1, end, key)
        elif A[mid] > key:
            return binary_loc_finder(A, start, mid - 1, key)
        else:
            return mid
        
def place_inserter(A, start, end):
    temp = A[end]
    for k in range(end, start, -1):
        A[k] = A[k - 1]
    A[start] = temp


def run_cbis(A):
    tracemalloc.start()
    start_time = time.time()

    cbis(A)

    end_time = time.time()

    used_memory = tracemalloc.get_traced_memory()[1]/1024
    tracemalloc.stop()

    time_taken = (end_time - start_time) * 1000

    return (used_memory, time_taken)

def run_randomized_quicksort(A):
    right = len(A) - 1

    tracemalloc.start()
    start_time = time.time()

    randomized_quicksort(A, 0, right)

    end_time = time.time()

    used_memory = tracemalloc.get_traced_memory()[1]/1024
    tracemalloc.stop()

    time_taken = (end_time - start_time) * 1000

    return (used_memory, time_taken)



if __name__ == '__main__':
    small_arrs = ArrayGenerator(200)
    med_arrs = ArrayGenerator(2000)
    large_arrs = ArrayGenerator(20000)

    for arrs in [small_arrs, med_arrs, large_arrs]:
        arrs.generate_list()
        arrs.write_to_file()
        for (arr_type, arr) in arrs.arrays.items():
            copy_arr = arr.copy() # agar array di dalam objek ArrayGenerator tidak berubah
            memory_cbis, time_cbis = run_cbis(copy_arr)
            copy_arr = arr.copy() # agar array di dalam objek ArrayGenerator tidak berubah
            memory_quick, time_quick = run_randomized_quicksort(copy_arr)

            print("="*40)
            print(f"{arr_type} array dengan ukuran {arrs.n}:")
            print(f"Time (quicksort): {time_quick} ms")
            print(f"Time (cbis)     : {time_cbis} ms")
            print(f"Memory (quicksort)  : {memory_quick} KB")
            print(f"Memory (cbis)       : {memory_cbis} KB")
            print()