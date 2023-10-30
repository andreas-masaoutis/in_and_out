# in and out: User Documentation

The main objective of this piece of software is to transform a CSV file, with entry and exit data from a keycard entrance system, to specific insights.

So. let's get started

## Where you can find the computed solution
The main outcome is a set of three files with answers to the three questions posed. You can find these answers in the folder 

>    ~ / in_and_out / data / output /

In there, there are three CSV files (first.csv, second.csv, third.csv) with the answers to the three questions respectively.

## How to recompute the solution

If you so wish to recompute the solution then you have a series of options at you disposal.

### Prerequisites
In order to run the solution you need a Python installation on you local machine or a Docker installation. 

For Python, the solution is tested with versions 3.10 and 3.11, and it should work with prior ones as well.

For Docker Engine we have used version 20.10.21, and it should work with other versions as well. 


### Steps

First, you have to download this repository from GitHub, if you have not done so already. In the initial page of the [repo](https://github.com/andreas-masaoutis/in_and_out) the green button with the tag 'Code' gives you different options for doing so.

Once you have the repo downloaded on your machine you can:

- Run with Python:

Open a terminal and navigate to 

>    ~ / in_and_out / main /

where you can find the file solution.py. 

With: 

>    python solution.py

the solution script will compute the answers once more.

- Run with Docker (and Python):
(We assume that the Docker service is running. If not, activate the service following the instructions for your OS)

Open a terminal and navigate to

>    ~ / in_and_out /

where the docker-compose.yml file is located

The command:

>   docker-compose build

will create the solution image, and with

> docker-compose up

you will get the script to recompute the solution


In both cases:
- 1. the answers will be saved in:

>    ~ / in_and_out / data / output /

- 2. the terminal will print on-screen a verification that the solution is active, and
        - either a warning message if something went wrong
        - or a verification that the solution is complete along with info on how much space was used, and how much time it took.

### Errors, bad data and logging 

In case there is any problem and a warning message appears on-screen, you can take a look at the file logger.log found at 

>    ~ / in_and_out / main /

that contains more detailed information for the error.

Be advised that whenever the raw data contain badly formatted data, the offending data is placed on the file

> ~ / in_and_out / data / bad_data / bad_data.csv

for further inspection, and it is not considered for the computation of the solution. It is therefore good practice to inspect the logger file to make sure that everything ran smooth.

## Configuration

In case you want to modify the input or output you have the following options:

### Use another input file
You can simply change the input file and compute the solution for the new file. Mind you, that by default the answers are given for the month of February, so a file with other dates will produce empty results

### Modify the solution parameters
There are three kinds of parameters that a user can change:

- 1. The locations of the input data and output folder

In the folder 

>    ~ / in_and_out / main /

you can find the file solution_config.py and modify the above options.
