# Lecture 11 - Simulation in Python

## SimPy
SimPy is a library framework for [discrete-event simulations](https://en.wikipedia.org/wiki/Discrete-event_simulation). This is a really useful way of running simulations on the following type of events:
- Customer Arrival/Departure
- Transportation Logistics
- Supply Chain
- Project Planning


First we need to install the SimPy libraries. In your CodeSpace terminal, type: 
```
pip install simpy
```
## Basic Concept
Simpy uses a process known as a **generator**. These processes have the ability to ***yield*** which suspends the process. An important version of this is the ***Timeout*** which allows the process the sleep for a given time.
### Our first process
We will use the example of a car process. The car will be driving and parking for a while.

Code these examples in **SimPyTest.py**
```
def car(env):
  print('Start parking at %d' % env.now)
  parking_duration = 5
  yield env.timeout(parking_duration)

  print('Start driving at %d' % env.now)
  trip_duration = 2
  yield env.timeout(trip_duration)
```

Now that we have created a car process, we will need to have an environment for that process to live. We will create this within a main() method.
```
import simpy
def main():
  env = simpy.Environment()
  env.process(car(env))

  env.run(until=15) #go for 15 units

main()
```
The car is able to park and drive in the time provided. We could add additional cars as new processes or have the existing cars do more than the two moves (park then drive).

### Multiple processes
Modify your car process from before to add two parameters for their **id** and their **speed**
```
def car(env, id, speed):
  print('Car %d: Start parking at %d' % (id, env.now))
  parking_duration = speed
  yield env.timeout(parking_duration)

  print('Car %d: Start driving at %d' % (id,env.now))
  trip_duration = 2
  yield env.timeout(trip_duration)
```
We also need to change our main() function to call this in a different way.
```
def main():
  env = simpy.Environment()
  env.process(car(env, 1, 5))
  env.process(car(env, 2, 10))

  env.run(until=20)
```

## Continuous processes
Each of our car examples, only ran once but you could see a situation where the process continues as long as the simulation is going. Essentially we will create an infinite loop within the process.

### Fast & Slow Clocks
```
def clock(env, name, tick):
  while True: #Never-ending loop
    print(name, env.now)
    yield env.timeout(tick)

def main():
  env = simpy.Environment()
  env.process(clock(env, 'tick', 1))
  env.process(clock(env, 'tock', .5))
  env.run(until=10)
```
- What happens if you change the **until** value?
- Could you add a third clock with a different rate?

## Processes running simultaneously
The following code is in **StopLight.py**

Imagine that we have a traffic light as a process that cycles between green, yellow, and red.
```
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
```
In this example we are using 30 seconds for the green light, 2 seconds for the yellow, and 20 seconds for the red light.

Now we want to run parallel processes for the cars that will interact with the light. A single car will be similar to our earlier example:
```
def car(env, id):
    print('Car %d: Arrived at %d' % (id, env.now))
    #check to see if we can go, if not wait until we can.
    while greenLight == False:
        yield env.timeout(1)

    print('Car %d: Departed at %d' % (id,env.now))
```
The car will check to see if the light is green and if not, it will wait a second before checking again. As soon as the light is green it will depart.

We want multiple cars so we need yet another process to handle the arrival of new cars.
```
def carArrival(env):
    #Cars arrive every 5 seconds
    carNum = 0
    while True:
        carNum = carNum + 1
        env.process(car(env, carNum))
        yield env.timeout(5)      
```
This process will spawn a new car every 5 seconds. The cars are then their own processes and will wait until they have had a chance to go before proceeding through the light.

Finally we need to look at our main() method to control all of the different processes.

```
import simpy
greenLight = True

def main():
    env = simpy.Environment()
    env.process(carArrival(env))
    env.process(stopLight(env))
    env.run(until=100)
    print("Simulation comptete")

if __name__ == '__main__':
    main()
```
This is a very basic simulation of a traffic light. A few things we could do to make the simulation more accurate.
- Put the cars in a queue when they get to the light if it is red or if there is a stopped car in front of them.
- Log the data for further exploration
- Include more than one direction at the light.
