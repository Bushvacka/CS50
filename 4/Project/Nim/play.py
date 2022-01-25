from nim import train, play
import time
start = time.time()
ai = train(10000)
print("Training Completed in {:.2f} seconds".format((time.time() - start)))
play(ai)
