import wave
from time import sleep
import time
import numpy as np
import threading
from multiprocessing import Queue, Process

from micReceiver    import micRecieve  
from accelReciever  import accelRecieve

import sys



def recordLauncher(length,fileName):

    micQue = Queue(maxsize=1)
    accelQue = Queue(maxsize=1)
    micDataProcess = Process(target=micRecieve,args=(micQue,))
    accelDataProcess = Process(target=accelRecieve,args=(accelQue,))    
    micDataProcess.start()
    accelDataProcess.start()

    micFrames = b''
    accelFrames = []
    startTime = time.time()

    # micOut = wave.open('recording/' + fileName + "Mic.wav",'wb')
    # micOut.setnchannels(2)
    # micOut.setsampwidth(3)
    # micOut.setframerate(32000)

    f = open('recording/' + fileName + "Accel",'w')
    while time.time() - startTime < length:
        if not micQue.empty():
            micFrames += micQue.get()
        if not accelQue.empty():
            accelFrames.extend(accelQue.get())

    # print(f'micFrames.size: {len(micFrames)}')
    # print(f'accelFrames.size: {len(accelFrames)} {ac')


    micDataProcess.terminate()
    accelDataProcess.terminate()
    # return
    #writting
    with wave.open('recording/' + fileName + "Mic.wav",'wb') as micOut:
        micOut.setnchannels(2)
        micOut.setsampwidth(3)
        micOut.setframerate(32000)
        micOut.writeframesraw(micFrames)

    with open('recording/' + fileName + "Accel",'w') as f:
        for i in accelFrames:
            f.write(str(i) + '\n')

    


def main():
    # print("In main where does this thread disappear too?",flush=True)

    # length = int(input("Length? "))
    # fileName = input("FileName? ")
    if len(sys.argv) != 3:
        print("Must enter length and subFileName")
    else:
        try:
            length = int(sys.argv[1])
            fileName = sys.argv[2]
            recordLauncher(length,fileName)
        except Exception as e:
            print(f"There was an exception: {e}")

if __name__ == "__main__":
    main()
