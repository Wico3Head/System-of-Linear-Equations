import random
from matrix import Matrix

while True:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    while True:
        unknowns = random.randint(2, 6)
        solutions = []
        equations = []

        for i in range(unknowns):
            solutions.append(random.randint(-10, 10))
            equations.append([])

        for i in range(unknowns):
            for j in range(unknowns):
                equations[i].append(random.randint(-8, 8))

        for i in range(unknowns):
            equations[i].append(sum([equations[i][j]*solutions[j] for j in range(unknowns)]))

        equationMatrix = Matrix(unknowns, unknowns)
        set_matrix = [[equations[i][j] for j in range(unknowns)] for i in range(unknowns)]
        equationMatrix.set(set_matrix)
        if equationMatrix.determinant() != 0:
            break

    print('Your equation is: ')
    for i in range(unknowns):
        text = ''
        for j in range(unknowns):
            coefficient = equations[i][j]
            if coefficient == 1 or coefficient == -1:
                text += str(coefficient)[:-1] + alphabet[j-unknowns] + ((' + ' if equations[i][j+1] > 0 else ' ') if j != unknowns - 1 else ' = ')
            elif coefficient != 0:
                text += str(coefficient) + alphabet[j-unknowns] + ((' + ' if equations[i][j+1] > 0 else ' ') if j != unknowns - 1 else ' = ')
            elif j == unknowns - 1:
                text += ' = '
            else:
                text += ' + ' if equations[i][j+1] > 0 else ' '

        text += str(equations[i][-1])
        print(text)

    while True:
        response = input('\nDo you wish to know the solution? (Y/N)\n')
        if response == 'Y':
            for i in range(unknowns):
                print('The value of ' + alphabet[i-unknowns] + ' is ' + str(solutions[i]))
            break
        elif response == 'N':
            break
        print('Invalid response')

    response = input('Do you want to keep using the program? (Y/N)\n')
    if response == 'N':
        break


