import time


length = 0
start = time.time()


while length != 60:
    end = time.time()
    length = end - start

print("One minute has passed")