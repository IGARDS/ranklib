#!/bin/bash

RUNNING_DIR=`dirname "$0"`
$RUNNING_DIR/generic_wrapper.py $1 $2 | egrep -v Academic | egrep ^\{
