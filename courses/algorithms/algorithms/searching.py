def binary_search(arr, x):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == x:
            return mid
        if arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1




def interpolation_search(arr, x):
    low, high = 0, len(arr) - 1
    while low <= high and arr[low] <= x <= arr[high]:
        if low == high:
            return low if arr[low] == x else -1
        if arr[high] == arr[low]: # avoid division by zero
            pos = low
        else:
            pos = low + ((high - low) * (x - arr[low])) // (arr[high] - arr[low])
        if pos < low or pos > high:
            return -1
        if arr[pos] == x:
            return pos
        if arr[pos] < x:
            low = pos + 1
        else:
            high = pos - 1
    return -1