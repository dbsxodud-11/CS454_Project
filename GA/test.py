if __name__ == "__main__" :

    arr = [[1, 0], [2, 3]]
    temp = arr[0]
    arr[0] = arr[1]
    arr[1] = temp

    for i in arr :
        print(i, end = "")