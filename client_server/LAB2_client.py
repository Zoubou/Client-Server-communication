from LAB2_HeaderFile import *
from LAB2_server import *


def run_client(data):
    serverIP = "127.0.0.1" 
    serverPort = 40404
    clientTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        
        clientTCPSocket.connect((serverIP, serverPort))
        print(f"Connected to server at IP {serverIP}, port {serverPort}")

        helloMessage = "Hello Server, update this array"
        clientTCPSocket.send(helloMessage.encode())

        serverHelloMessage = clientTCPSocket.recv(1024).decode()
        print(f"Server says: {serverHelloMessage}")

        if serverHelloMessage == "Hello Client, here is the updated array":
            
            clientRequestMessage = "Give me the updated array"
            clientTCPSocket.send(clientRequestMessage.encode())
            clientTCPSocket.send(data)

            updated_array = clientTCPSocket.recv(131072)
            exec_Time = clientTCPSocket.recv(1024)
    
            desiriallized_updated_array = pickle.loads(updated_array)
            exec_Time = pickle.loads(exec_Time)
            print(desiriallized_updated_array)
            print("Execution time : " + str(exec_Time))

        elif serverHelloMessage == "Received an unrecognized message from client.":
            clientTCPSocket.close()
            print("Failed to establish connection.")

    except Exception as ex:
        print(f"Exception occurred: {ex}")

    finally:
        clientTCPSocket.close()
        print("Connection closed.")

#################################################################################################################

def createRandomInstance():

    userChoice = []
    while len(userChoice) < 1:

        userChoice = input(bcolors.QUESTION +'Determine the input size (i.e., the number of randomly chosen integers whose square to calculate): ' + bcolors.ENDC).split(',')

        if not (len(userChoice) == 1):
            print(bcolors.ERROR + "ERROR-01: Incomprehensible input provided. Try again..." + bcolors.ENDC)
            userChoice = []
            continue

        try:
            inputSize = int( userChoice[0] )
        except ValueError:
            print(bcolors.ERROR + "ERROR-02: Non-integer input size provided. Try again..." + bcolors.ENDC)
            userChoice = []
            continue

        if inputSize < 1 or inputSize > maxInputSize:
            print(bcolors.ERROR + f"ERROR-03: Input size provided is not from [1,{maxInputSize}]. Try again..." + bcolors.ENDC)
            userChoice = []
            continue
                
        inputNumbersList = []
        for k in range(inputSize):
           newRandomNumber = random.randint(1,10000)
           inputNumbersList.append(newRandomNumber)

    return(inputSize,inputNumbersList)

##################################################################################################################

def getSolutionMethodFromUser(inputSize):
   
    print(bcolors.QUESTION + MINUSLINE + '''
    Do the calculations with:
        (1) one single-threaded process                    --> press [1]
        (2) one independent process per per calculation    --> press [2]
        (3) a given pool of independent processes          --> press [3,<number of processes in pool>]
        (4) a single multithreaded process                 --> press [4,<number threads to use>]
        (0) EXIT                                           --> press [0]''' + bcolors.ENDC)

    userChoice = []

    while len(userChoice) < 1:
        userChoice = input(bcolors.QUESTION \
                           + MINUSLINE \
                           + '\nProvide your selections as comma-separated numbers (e.g., 1 for case (1), or 4,10 for case (4) with 10 threads):\n' \
                           + bcolors.ENDC).split(',')

        try:
            calculationMethod = int( userChoice[0] )
        except ValueError:
            print(bcolors.ERROR + "ERROR-04: Non-integer calculation method provided. Try again..." + bcolors.ENDC)
            userChoice = []
            continue

        if calculationMethod == 0:  #user requested to EXIT...
            return([0,0])
        
        if calculationMethod == 1:

            return([1,1])
            #makeComputationsWithOneProcess()
    
        if calculationMethod == 2: 

            if inputSize > maxNumberOfProcesses:
                print(bcolors.ERROR + f"ERROR-05: Required number of processes exceeds the maximum number of processes = {maxNumberOfProcesses}. Try again..." + bcolors.ENDC)
                userChoice = []
                continue

            return([2,inputSize])        
            #makeComputationsWithConcurrentProcesses()

        if calculationMethod == 3:
 
            if not (len(userChoice) == 2):
                print(bcolors.ERROR + "ERROR-06: Number of processes is missing. Try again..." + bcolors.ENDC)                
                userChoice = []
                continue

            try:
                numberOfProcesses = int( userChoice[1] )
            except ValueError:
                print(bcolors.ERROR + "ERROR-07: Non-integer number of processes provided. Try again..." + bcolors.ENDC)
                userChoice = []
                continue

            if numberOfProcesses < 1 or numberOfProcesses > maxNumberOfProcesses: 
                print(bcolors.ERROR + f"ERROR-08: Number of processes is NOT in [1,{maxNumberOfProcesses}]. Try again..." + bcolors.ENDC)                
                userChoice = []
                continue
        
            return([3,min(inputSize,numberOfProcesses)])
            #makeComputationsWithPoolOfProcesses(numberOfProcesses = numberOfProcesses)

        elif calculationMethod == 4:

            if not (len(userChoice) == 2):
                print(bcolors.ERROR + "ERROR-09: Number of Threads is missing. Try again..." + bcolors.ENDC)                
                userChoice = []
                continue

            try:
                numberOfThreads = int( userChoice[1] )
            except ValueError:
                print(bcolors.ERROR + "ERROR-10: Non-integer number of threads provided. Try again..." + bcolors.ENDC)
                userChoice = []
                continue

            if numberOfThreads < 1 or numberOfThreads > maxNumberOfThreads: 
                print(bcolors.ERROR + f"ERROR-11: Number of threads is NOT in [1,{maxNumberOfThreads}]. Try again..." + bcolors.ENDC)                
                userChoice = []
                continue
            
            return([4,min(inputSize,numberOfThreads)])            
            #makeComputationsWithOneMultithreadedProcess(number_threads_per_process=numberOfThreads)

        else:
            print(bcolors.ERROR + "ERROR-12: Wrong calculation method provided. Try again..." + bcolors.ENDC)
            userChoice = []
            continue


if __name__ == "__main__":
    os.system('cls')

    inputSize,inputNumbersList = createRandomInstance()

    solutionMethod = getSolutionMethodFromUser(inputSize)

    data = [inputSize, inputNumbersList, solutionMethod]

    serialized_data = pickle.dumps(data)
           
    run_client(serialized_data)

    