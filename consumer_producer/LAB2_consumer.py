from LAB2_HeaderFile import *

def on_request(ch, method, properties, body):
    print("Received a new message!")
    deserialized_data = pickle.loads(body)

    inputSize = deserialized_data[0]
    inputNumbersList = deserialized_data[1]
    solutionMethod = deserialized_data[2]
    
    if solutionMethod[0] == 1:
        result, exec_Time = makeComputationsWithOneProcess(inputSize, inputNumbersList)

    elif solutionMethod[0] == 2:
        result, exec_Time = makeComputationsWithConcurrentProcesses(inputSize, inputNumbersList)

    elif solutionMethod[0] == 3:
        result, exec_Time = makeComputationsWithPoolOfProcesses(inputSize, inputNumbersList, numberOfProcesses = solutionMethod[1])
                    
    elif solutionMethod[0] == 4:
        result, exec_Time = makeComputationsWithOneMultithreadedProcess(inputSize, inputNumbersList, numberOfThreadsPerProcess=solutionMethod[1])
                
    else: 
        result = "Program terminated"
        exec_Time = 0

    data = [result, exec_Time]
    serialized_response = pickle.dumps(data)

    ch.basic_publish(exchange='', routing_key='response_queue', body=serialized_response)
    print("Processed data and sent response.")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run_consumer():

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    request_queue = 'request_queue'
    response_queue = 'response_queue'
    channel.queue_declare(queue=request_queue)
    channel.queue_declare(queue=response_queue)

    channel.basic_consume(queue=request_queue, on_message_callback=on_request)

    print("Waiting for messages...")
    channel.start_consuming()


########### Calculation of the square of a single number ########### 
def calculate_square(inputTriple):
    thread_name = inputTriple[0]
    number = inputTriple[1]
    result = inputTriple[2]

    result.append(number*number)
    time.sleep(1)

    print(f'{thread_name}: The square of ' + str(number) + ' is ' + str(number*number))


########### Calculation of the square of many numbers ########### 
def calculate_many_squares(inputTriple):
    thread_name = inputTriple[0]
    number = inputTriple[1]
    result = inputTriple[2]

    for n in range(len(number)):
        result.append(number[n]*number[n])
        print(f'{thread_name}: The square of ' + str(number[n]) + ' is ' + str(number[n]*number[n]))
        time.sleep(1)


def makeComputationsWithOneProcess(inputSize,inputNumbersList):
    result = []
    drawLine(20, '=')
    
    start_Time = time.time()
    for n in range(len(inputNumbersList)):
        inputTriple = ("", inputNumbersList[n], result)
        calculate_square(inputTriple)

    end_Time = time.time()

    exec_Time = end_Time - start_Time

    print("Execution time : " + str(exec_Time))
    return (result, exec_Time)



def makeComputationsWithConcurrentProcesses(inputSize,inputNumbersList):
    manager = mp.Manager()
    result = manager.list()
    process = []

    start_Time = time.time()
    for n in range(len(inputNumbersList)):
        inputTriple = (f"process-{n}", inputNumbersList[n], result)
        p = mp.Process(target=calculate_square, args=(inputTriple,))
        process.append(p)
        p.start()

    for n in range(len(inputNumbersList)):
        p.join()

    end_Time = time.time()

    exec_Time = end_Time - start_Time

    print("Execution time : " + str(exec_Time))
    
    return (list(result), exec_Time)



def makeComputationsWithPoolOfProcesses(inputSize, inputNumbersList, numberOfProcesses):
    manager = mp.Manager()
    result = manager.list()

    start_Time = time.time()

    with mp.Pool(numberOfProcesses) as pool:
        
        chunk_size = (len(inputNumbersList) + numberOfProcesses - 1) // numberOfProcesses
        chunks = [inputNumbersList[i:i + chunk_size] for i in range(0, len(inputNumbersList), chunk_size)]

        inputTriples = [(f"Process-{i}", chunk, result) for i, chunk in enumerate(chunks)]

        pool.map(calculate_many_squares, inputTriples)

    end_Time = time.time()

    exec_Time = end_Time - start_Time
    print("Execution time : " + str(exec_Time))

    return (list(result), exec_Time)


def makeComputationsWithOneMultithreadedProcess(inputSize, inputNumbersList, numberOfThreadsPerProcess):
    threads = []
    result = []  

    
    chunk_size = (len(inputNumbersList) + numberOfThreadsPerProcess - 1) // numberOfThreadsPerProcess
    chunks = [inputNumbersList[i:i + chunk_size] for i in range(0, len(inputNumbersList), chunk_size)]

    inputTriples = [(f"thread-{i}", chunk, result) for i, chunk in enumerate(chunks)]

    start_Time = time.time()

    for inputTriple in inputTriples:
        t = threading.Thread(target=calculate_many_squares, args=(inputTriple,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_Time = time.time()

    exec_Time = end_Time - start_Time
    print("Execution time : " + str(exec_Time))

    return (result, exec_Time)

if __name__ == "__main__":
      
    run_consumer()