from matrix import Matrix

def intCheck(num):
    try:
        int(num)
    except:
        print("Invalid input")
        return False
    return True

def floatCheck(num):
    try:
        float(num)
    except:
        print("Invalid input")
        return False
    return True

def main():
    subs = "₀₁₂₃₄₅₆₇₈₉"
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    print("This program solves systems of linear eqations using matrices\n")
    unknowns = input("Please enter the number of unknowns in your simultaneous equations: ")
    while not intCheck(unknowns):
        unknowns = input("Please enter the number of unknowns in your simultaneous equations: ")
    unknowns = int(unknowns)

    simultaneousEqua = Matrix(unknowns, unknowns)
    count = 0
    for i in range(unknowns):
        text = ""
        for j in range(unknowns):
            count += 1
            text += "a" + (subs[count] if count < 10 else (subs[count//10] + subs[count%10])) + " " + alphabet[-unknowns + j] + (" + " if j != unknowns - 1 else " ")
        text += "= " + alphabet[8 + i]
        print(text)
    print("Let this be your system of linear equations")          

    count = 0
    for i in range(unknowns):
        for j in range(unknowns):
            count += 1
            coefficient = input("Enter the value of a" + (subs[count] if count < 10 else (subs[count//10] + subs[count%10])) + ": ")
            while not floatCheck(coefficient):
                coefficient = input("Enter the value of a" + (subs[count] if count < 10 else (subs[count//10] + subs[count%10])) + ": ")
            coefficient = float(coefficient)
            simultaneousEqua.matrix[i, j] = coefficient

    resultMatrix = Matrix(unknowns, 1)
    for i in range(unknowns):
        result = input("Enter the value of " + alphabet[8 + i] + ": ")
        while not floatCheck(result):
            result = input("Enter the value of " + alphabet[8 + i] + ": ")
        resultMatrix.matrix[i, 0] = float(result)

    if simultaneousEqua.determinant() == 0:
        print("This system of linear equation has either 0 or infinitely many solutions")
    else:
        answer = simultaneousEqua.inverse()*resultMatrix
        for i in range(unknowns):
            print("The value of " + alphabet[-unknowns + i] + " is " + str(int(answer.matrix[i, 0]) if answer.matrix[i, 0]%1 == 0 else round(answer.matrix[i, 0], 3)))

if __name__ == "__main__":
    main()