from numpy.linalg import matrix_power
import numpy as np

VISTING_JAIL_SQUARE = 10
GO_TO_JAIL_SQUARE = 30
JAIL_SQUARE_1 = 40
JAIL_SQUARE_2 = 41
JAIL_SQUARE_3 = 42
GO_SQUARE = 0



PROB_OF_TRIPLE_DOUBLES = (1/6)**3
EMPTY_DISTRIBUTION = [0 for i in range(43)]




CHANCE_DISTRIBUTION_NON_RELATIVE = [1/9,0,0,0,0,1/9,0,0,0,0,0,1/9,0,0,0,0,0,0,0,0,0,0,0,0,1/9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1/9,1/9,0,0]

PROB_TO_MOVE_ON_CHANCE = 9/16

PROB_TO_MOVE_ON_COMMUNITY = 2/16
COMMUNITY_CHEST_DISTRIBUTION = EMPTY_DISTRIBUTION.copy()
COMMUNITY_CHEST_DISTRIBUTION[JAIL_SQUARE_1] = 1/2
COMMUNITY_CHEST_DISTRIBUTION[GO_SQUARE] = 1/2


GO_TO_JAIL_DISTRIBUTION = EMPTY_DISTRIBUTION.copy()
GO_TO_JAIL_DISTRIBUTION[JAIL_SQUARE_1] = 1


def combineDistributions(dist1,probOfDist1, dist2, probOfDist2):

  newDist = [probOfDist1 * dist1[i] + probOfDist2 * dist2[i] for i in range(len(dist1))]


  return newDist


def nextItemInSortedCircularList(l, item):

  for num in l:

    if(num> item):

      return num 
  
  return l[0]




def genMatrix():

  mtrx = []

  ## base distribution

  for i in range(40):

    default = [1/36,2/36,3/36,4/36,5/36]


    defaultR = default.copy()
    defaultR.reverse()


    distributionTemplate = default + [6/36] + defaultR



    offset1 = [0 for i in range(i+2)]
    offset2 = [0 for i in range(40-(i+11))]

    done = offset1 + distributionTemplate + offset2

    if(len(done) > 40):

      for j in range(40,len(done)):

        done[j % 40] = done[j] 

    ## add extra jail states to keep square matrix
    mtrx.append( done[0:40] + [0,0,0] )





  
  


  # adding 1/6 ^ 3 go to jail to each square

  for i in range(len(mtrx)-3):

    mtrx[i] = combineDistributions(mtrx[i], 1-PROB_OF_TRIPLE_DOUBLES, GO_TO_JAIL_DISTRIBUTION, PROB_OF_TRIPLE_DOUBLES )




  squares = {
  'chance': [7,22,36],
  'community': [2,17,33]
  }

  UTILITY_SQUARES = [12,28]
  RAILROAD_SQUARES = [5,15,25,35]






  for square in squares['chance']:


    CHANCE_RELATIVE_DISTRIBUTION = CHANCE_DISTRIBUTION_NON_RELATIVE.copy()

    ## add relatives to chance

    ## back 3 spaces

    CHANCE_RELATIVE_DISTRIBUTION[square - 3] += 1/9

    ## nearest railroad

    CHANCE_RELATIVE_DISTRIBUTION[nextItemInSortedCircularList(RAILROAD_SQUARES, square)] += 1/9



    ## nearest utility
    CHANCE_RELATIVE_DISTRIBUTION[nextItemInSortedCircularList(UTILITY_SQUARES, square)] += 1/9
    # print(square)
    # print(nextItemInSortedCircularList(RAILROAD_SQUARES, square))
    # print(CHANCE_RELATIVE_DISTRIBUTION[nextItemInSortedCircularList(RAILROAD_SQUARES, square)])
    mtrx[square] = combineDistributions(mtrx[square], 1-PROB_TO_MOVE_ON_CHANCE, CHANCE_RELATIVE_DISTRIBUTION, PROB_TO_MOVE_ON_CHANCE)





  for square in squares['community']:

     mtrx[square] = combineDistributions(mtrx[square], 1-PROB_TO_MOVE_ON_COMMUNITY, COMMUNITY_CHEST_DISTRIBUTION, PROB_TO_MOVE_ON_COMMUNITY)

  dist1 = mtrx[VISTING_JAIL_SQUARE].copy()

  mtrx.append(dist1)
  mtrx.append(EMPTY_DISTRIBUTION.copy())
  mtrx.append(EMPTY_DISTRIBUTION.copy())


  # doublesRole = EMPTY_DISTRIBUTION.copy()

  # doublesRole[VISTING_JAIL_SQUARE+2] = 1/6
  # doublesRole[VISTING_JAIL_SQUARE+4] = 1/6
  # doublesRole[VISTING_JAIL_SQUARE+6] = 1/6
  # doublesRole[VISTING_JAIL_SQUARE+8] = 1/6
  # doublesRole[VISTING_JAIL_SQUARE+10] = 1/6
  # doublesRole[VISTING_JAIL_SQUARE+12] = 1/6


  # # print(len(doublesRole))

  # dist1 = EMPTY_DISTRIBUTION.copy()




  # dist1[JAIL_SQUARE_2] = 1

  # mtrx.append( combineDistributions(dist1, 5/6, doublesRole ,1/6) )

  # dist2 = EMPTY_DISTRIBUTION.copy()


  # dist2[JAIL_SQUARE_3] = 1



  # mtrx.append(combineDistributions(dist2, 5/6, doublesRole ,1/6))

  # dist3 = mtrx[VISTING_JAIL_SQUARE].copy()



  # mtrx.append(dist3)
  

  for i in range(len(mtrx)):



    temp = mtrx[i][GO_TO_JAIL_SQUARE]

    mtrx[i][JAIL_SQUARE_1] += temp

    mtrx[i][GO_TO_JAIL_SQUARE] = 0





  return mtrx

    



transition_matrix = np.array(genMatrix())

# for row in genMatrix():
#     print(row)


longterm = matrix_power(transition_matrix, 100)

percentToSquare = {}
squareToProbability = {}

for square, probability in enumerate(longterm[0]):

  # print(i, square)

  percentToSquare[probability] = square
  squareToProbability[square] = probability

temp = longterm[0]

temp.sort()

np.flip(temp, 0)




properties = ['Go', 'Mediterranean Avenue ', 'Community Chest 1', 'Baltic Avenue', 'Income Tax', 'Reading Railroad', 'Oriental Avenue', 'Chance 1', 'Vermont Avenue', 'Connecticut Avenue', 'Visiting Jail', 'St. Charles Place', 'Electric Company', 'States Avenue', 'Virginia Avenue', 'Pennsylvania Railroad', 'St. James Place', 'Community Chest 2', 'Tennessee Avenue', 'New York Avenue', 'Free Parking', 'Kentucky Avenue', 'Chance 2', 'Indiana Avenue', 'Illinois Avenue', 'B&O Railroad', 'Atlantic Avenue', 'Ventnor Avenue', 'Water Works', 'Marvin Gardens', 'Go To Jail', 'Pacific Avenue', 'North Carolina Avenue', 'Community Chest', 'Pennsylvania Avenue', 'Short Line', 'Chance 3', 'Park Place', 'Luxury Tax', 'Boardwalk', "Jail State 1", "Jail State 2", "Jail State 3"]

for num in temp:

  print(properties[ percentToSquare[num]]  , " - ", num * 100)



groups = [
  [1,3],
  [12,28],
  [6,8,9],
  [5,15,25,35],
  [11,13,14],
  [16,18,19],
  [21,23,24],
  [26,27,29],
  [31,32,34],
  [37,39]
]





def sumGroup(group):

  sum = 0

  for square in group:

    sum += squareToProbability[square]

  return sum



groups.sort(key = sumGroup)

groups.reverse()


print("Ranking by probability of landing")

for i, group in enumerate( groups):

  print("\n")

  print("Rank", i+1, "Group: -", format( sumGroup(group) * 100, '.1f'), "\n")

  for square in group:

    print(properties[square])

print("Ranking by expected value")

costOfMonopoly = {
    str([1,3]):620,
    str([6,8,9]):1070,
    str([5,15,25,35]):800,
    str([11,13,14]):1940,
    str([16,18,19]):2060,
    str([21,23,24]):2930,
    str([26,27,29]):3050,
    str([31,32,34]):3920,
    str([37,39]):2750,
    str([12,28]): 400
}
squareToMaxRent = {
    1:250,
    3:450,
    6:550,
    8:550,
    9:600,
    11:750,
    12:70,
    13:750,
    14:900,
    16:950,
    18:950,
    19:1000,
    21:1050,
    23:1050,
    24:1100,
    26:1150,
    27:1150,
    28:70,
    29:1200,
    31:1275,
    32:1275,
    34:1400,
    37:1500,
    39:2000,
    5:200,
    15:200,
    25:200,
    35:200
}

def sumGroupExpectedValue(group):

  expectedValueAfter100Turns = 0

  for square in group:

    expectedValueAfter100Turns += (squareToProbability[square] * 100) * squareToMaxRent[square] 

  return expectedValueAfter100Turns - costOfMonopoly[str(group)]

groups.sort(key=sumGroupExpectedValue)

groups.reverse()


for i, group in enumerate( groups):

  print("\n")

  print("Rank", i+1, "Group: -", format( sumGroupExpectedValue(group) , '.1f'), "\n")

  for square in group:

    print(properties[square])








