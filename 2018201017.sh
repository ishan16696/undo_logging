#!/bin/bash
if [ "$#" -eq 1 ] ; then
python3 2018201017_2.py $1
fi
if [ "$#" -eq 2 ] ; then
python3 2018201017_1.py $1 $2
fi