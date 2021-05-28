gameBoard = [
        [ 0, 0, 1],
        [ 0, 1, 0],
        [ 1, 0, 1]
    ]

# check diags
diags = [ [], [] ]
for line in range( len(gameBoard) ):
    for column in range( len( gameBoard[0] ) ):
        print(line, column)
        if line == column:
            diags[ 0 ].append( gameBoard[ line ][ column ] )
        elif line + column == 2:
            print("truc", line, column)
            diags[ 1 ].append( gameBoard[ line ][ column ] )

print(diags)

for diag in diags:
    if diag == [ 1, 1, 1]:
        print(1)
        break
    elif diag == [ 2, 2, 2]:
        print(2)
        break

