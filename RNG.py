mod = 20.0
mutliplier = 10.0
increment = 1.0
floatSeed = 0.0


def seedDefine():
    seed = input("Enter a seed between 0 and 20: ")
    print('Seed is:',seed)
    return seed

def seedCheck():
    if floatSeed > 20.0:
        print("Seed value too high!")
        exit()
    else:
        print("Seed value within acceptable range")

floatSeed = float(seedDefine())
seedCheck()
print('Seed as a float is:', floatSeed)
