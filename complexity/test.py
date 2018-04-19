
def fun(x):
    sum = 0
    for i in range(x):
        sum += 1


def fun2(x):
    sum = 0
    for i in range(x):
        for y in range(x):
            sum += 1


def qsort(arr, l=0, r=None):
    if r is None:
        r = len(arr) - 1
    i, j = l, r
    pivot = arr[int((l + r) / 2)]
    while i <= j:
        while arr[i] < pivot:
            i += 1
        while arr[j] > pivot:
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
    if l < j:
        qsort(arr, l, j)
    if r > i:
        qsort(arr, i, r)
