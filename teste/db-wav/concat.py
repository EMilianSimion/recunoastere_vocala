import os

source = "teste/"
arr = os.listdir(source)
for d in arr:
    intermediar = source + d + '/wav'
    newArr = os.listdir(intermediar)
    # if len(newArr) > 15:
    #     i = (int(len(newArr) / 3)) * 3 - 1
    #     print(i)
    #     print(intermediar)
    #     while i - 2 >= 0:
    #         print(f"{newArr[i]} {newArr[i - 1]} {newArr[i - 2]}")
    #         os.system(
    #             f'sox {intermediar}/{newArr[i]} {intermediar}/{newArr[i - 1]} {intermediar}/{newArr[i - 2]} {intermediar}/final{i}.wav')
    #         i -= 3
    print(intermediar)
    for i in range(len(newArr)):
        print(newArr[i])
