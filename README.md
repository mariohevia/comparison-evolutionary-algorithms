# Comparison and modification of self-adjusting evolutionary algorithms.
## Abstract
Evolutionary algorithms (EA) are population-based optimization algorithms that mimic
evolution to search for an (near-)optimal solution. A key topic in EA research is the
amount of evaluations or generations used to solve a problem. The research is generally
focused on parameter optimization and most of the research focuses on static parameters,
but lately started to focus on dynamic parameters that are success based and does not
need information about the problem.

The aim of the project is to make empirical evaluations of some of these success based
parameter optimizitations. The main algorithms that are tested in the project are the
self-adjusting mutation rate (1 + λ) EA (Doerr et al., 2017), self-adjusting offspring
population size (1 + λ) EA (Jansen et al., 2005) and the self-adjusting (1 + (λ, λ))
GA (Doerr and Doerr, 2015). They are compared with the toy problems OneMax,
LeadingOnes, Makespan Scheduling and SufSamp. Afterwards several modifications
are made to find insights and improvements on the original algorithms.
In this work is shown a comparison and discussion of the optimization times, and
a proposed new metric to capture the parallel and sequential optimization time. From
the modifications made a new selection scheme emerged that improves up to 20% in the
number of evaluations needed by the self-adjusting (1 + (λ, λ)) GA on OneMax.

## Run demo

To run a demo on a Jupyter notebook, you can download open comparison-evolutionary-algorithms/code/Demo.ipynb 
and try three different algorithms solving the OneMax problem. It also has a presentation format.

## Run code

To run the code use the python program comparison-evolutionary-algorithms/code/master.py and run it using the
command-line arguments explained on comparison-evolutionary-algorithms/Dissertation Report.pdf or use the 
argument -h when running the script to get more information on usage.
