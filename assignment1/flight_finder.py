"""
Name: Robert Moore
Student Number: 10179621

I certify that this submission contains my own work, except as noted.

"""
import argparse

def main():

    parser = argparse.ArgumentParser(description='Find the shortest flight combination from a to b.')
    parser.add_argument('file', type=str, help='location of flight data')
    parser.add_argument('origin', type=int, help='origin city')
    parser.add_argument('target', type=int, help='desired destination city')

    args = parser.parse_args()

    W, num_cities = load_flight_matrix(args.file)

    origin = args.origin
    target = args.target




    arival_time = [-1]*num_cities
    reached = [False]*num_cities
    estimate = [99999]*num_cities
    predecessor = [None]*num_cities
    cantidate = [False]*num_cities

    reached[origin] = True
    arival_time[origin] = 0
    estimate[origin] = 0
    predecessor[origin] = origin
    for i in range(0,num_cities):
        if len(W[origin][i]) > 0:
            cantidate[i] = True
            estimate[i] = W[origin][i][0][1]
            predecessor[i] = origin
        for flight in W[origin][i]:
            if flight[1] < estimate[i]:
                estimate[i]=flight[1]

    no_path = False
    base = origin
    while(arival_time[target]<0):
        best_cand_est = 99999

        for city in range(0, num_cities):
            if cantidate[city] and (estimate[city] < best_cand_est):
                base = city
                best_cand_est = estimate[base]
        reached[base] = True
        cantidate[base] = False
        arival_time[base] = best_cand_est

        for i in range(0, num_cities):
            if (len(W[base][i]) > 0) and not reached[i]:
                for flight in W[base][i]:
                    if (arival_time[base] < flight[0]) and (flight[1] < estimate[i]):
                        estimate[i] = flight[1]
                        cantidate[i] = True
                        predecessor[i] = base
        if sum(cantidate) == 0:
            no_path = True
            break

    if no_path:
        print('----------------------------')
        print(f'No availible path from {origin} to {target}')
        print('----------------------------')

    else:
        print(f'target is {target} and origin is {origin}')
        path_string = ''
        current_step = target
        while(current_step!=origin):
            path_string = f'\nFly from {predecessor[current_step]} to {current_step}' + path_string
            current_step = predecessor[current_step]

        print('----------------------------')
        print(f'Optimal route from {origin} to {target} : \n' + path_string + '\n')
        print(f'Arrive at {target} at time {arival_time[target]}')
        print('----------------------------')


def load_flight_matrix(file_name):
    '''load flight data from a file'''

    with open(file_name) as f:
        num_cities = int(f.readline())
        file = f.readlines()

    print(f'There are {num_cities} cities ')
    W=[]

    for i in range(0,num_cities):
        W.append([None]*num_cities)
        for j in range(0,num_cities):
            W[i][j]=[]

    for flight in file:
        flight_l = list(map(int, flight.split()))
        W[flight_l[0]][flight_l[1]].append((flight_l[2],flight_l[3]))

    return W, num_cities

if __name__ == '__main__':
    main()
