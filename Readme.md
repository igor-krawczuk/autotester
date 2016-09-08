[![Build Status](https://travis-ci.org/wojcech/autotester.svg?branch=master)](https://travis-ci.org/wojcech/autotester)
[![Coverity Scan Build Status](https://scan.coverity.com/projects/10104/badge.svg)](https://scan.coverity.com/projects/wojcech-autotester)

In the course of my masters thesis I need to characterize new electronic devices.
In order to do it a) less tediously and b) better, I am trying to automate it.
These are my attempts.
# WARNING: still a work in progress, and don't expect 100% clean code, since I am working on this as a break when doing measurements and working on other stuff. It is usable, but unstable


# Current features

## NaiveTester

A very simple test agent which expects a state estimator, high level planner and low level planner(i.e. executor) and will
simply run the next actions.

The NaiveX classes are all very simple rule systems that exist mainly to specify a workable interface for more complex agents.

They do however already serve a purpose for me, for doing exploratory testing with preset values.



## MailNotification

Get an Email when your tester is done, drink coffe before.Huzzah!


## Upcoming features

I want to try some machine learning approaches, mainly

* HMM (Hidden Markov Model)
* reinforcement learning
* LSTM

in order to improve the  state estimation and high level planning.
