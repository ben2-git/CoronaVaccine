import sys
from repository import repo
from DTO import *


def main():
    repo.createTables()
    with open(sys.argv[1]) as file:
        configure(file)
    with open(sys.argv[2]) as file1:
        with open(sys.argv[3], 'w') as file2:
            orders(file1, file2)


def configure(file):
    lines = file.readlines()
    nums = lines[0].split(',')
    vac = int(nums[0])
    sup = vac + int(nums[1])
    clin = sup + int(nums[2])
    log = clin + int(nums[3].split('\n')[0])
    maxId = 0
    for ind in range(1, vac + 1):
        repo.vaccines.insert(Vaccine(*(lines[ind].split(','))))
        maxId = max(maxId, int(lines[ind].split(',')[0]))
    for ind in range(vac + 1, sup + 1):
        repo.suppliers.insert(Supplier(*(lines[ind].split(','))))
    for ind in range(sup + 1, clin + 1):
        repo.clinics.insert(Clinic(*(lines[ind].split(','))))
    for ind in range(clin + 1, log + 1):
        repo.logistics.insert(Logistic(*(lines[ind].split(','))))
    repo.vaccines.setId(maxId)


def orders(file1, file2):
    lines = file1.readlines()
    for line in lines:
        args = line.split(',')
        if len(args) == 3:
            repo.recShip(*args)
        if len(args) == 2:
            repo.sendShip(*args)
        summary(file2)


def summary(file):
    newline = repo.sumFile()
    file.write(','.join(newline)+"\n")


if __name__ == '__main__':
    main()
