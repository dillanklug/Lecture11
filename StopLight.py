import simpy
greenLight = True

def car(env, id):
  print('Car %d: Arrived at %d' % (id, env.now))
  #check to see if we can go, if not wait until we can.
  while greenLight == False:
    yield env.timeout(1)

  print('Car %d: Departed at %d' % (id,env.now))

def carArrival(env):
  #Cars arrive every 10 seconds
  carNum = 0
  while True:
    carNum = carNum + 1
    env.process(car(env, carNum))
    yield env.timeout(5)

def stopLight(env):
  global greenLight #we are going to modify a global variable so it must be declared.
  while True:
    #Cycle from green->yellow->red
    print("Green")
    greenLight = True
    yield env.timeout(30)
    print("Yellow")
    yield env.timeout(2)
    print("Red")
    greenLight = False
    yield env.timeout(20)

def main():
  env = simpy.Environment()
  env.process(carArrival(env))
  env.process(stopLight(env))
  env.run(until=100)
  print("Simulation comptete")

if __name__ == '__main__':
  main()
