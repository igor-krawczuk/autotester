In the course of my masters thesis I need to characterize new electronic devices. 
In order to do it a) less tediously and b) better, I am trying to automate it.
There are my attempts.

# Current features

## NaiveTester

A very simple test agent which expects a state estimator, high level planner and low level planner(i.e. executor) and will
simply run the next actions. 

The NaiveX classes are all very simple rule systems that exist mainly to specify a workable interface for more complex agents.

They do however already serve a purpose for me, for doing exploratory testing with preset values.

## Upcoming features

I want to try some machine learning approaches, mainly

* HMM (Hidden Markov Model)
* reinforcement learning
* LSTM

in order to improve the  state estimation and high level planning.
