#!/bin/bash
set -x
help()
{
   # Display Help
   echo
   echo "This script interacts with the manage task API"
   echo
   echo "Syntax: ./task_manager.sh [-m|h]"
   echo "Example : ./task_manager.sh -m GET"
   echo "options:"
   echo "m     HTTP method name[GET|POST|PUT|DELETE]"
   echo "h     Print this Help."
   echo
   echo "Pre-requisites :"
   echo "This microservice is created on Flask framework."
   echo "Flask should be installed. Task data should be given in"
   echo "'config/task_data.conf' file. Example : title='Define server'"
   echo
}

while getopts ":m:h" option; do
   case $option in
      m) methodname="$OPTARG";;
      h) # display Help
         help
         exit;;
     \?) # incorrect option
         echo "Error: Invalid option"
         exit;;
   esac
done

############################################################
#                       Main program                       #
############################################################

if [ "$#" -eq  "0" ]
   then
     echo "No arguments supplied"
     echo "###############################################################"
     ./task_manager.sh -h
     echo "###############################################################"
     exit 1
fi

###########################################################
#      task input data file                               #
###########################################################
FILE=config/task_data.conf
if [ -f "$FILE" ]; then
    echo "$FILE exists."
    source $FILE
fi

BASE_URL="http://localhost:5000/taskdb/tasks"

if [ -z "$methodname" ]; then
	echo "Please pass HTTP method name."
	exit 1
fi	

if [ "$methodname" == "GET" ]; then
	echo "###############################################################"
	echo "Fetching all task data"
	curl -i $BASE_URL
	echo "###############################################################"
	echo "Fetching specific task data"
	curl -i ${BASE_URL}/${taskID}
elif [ "$methodname" == "DELETE" ]; then
	echo "###############################################################"
	echo "Deleting task data for taskId : $taskID"
	curl -i -X ${methodname} ${BASE_URL}/${taskID}
elif [ "$methodname" == "POST" ]; then
        echo "Creating new task data"
	echo "###############################################################"
        curl -i -H "Content-Type: application/json" -X ${methodname} -d "{\"id\":$taskID,\"title\":\"$title\",\"due_date\":\"$due_date\",\"status\":\"$status\"}" ${BASE_URL}
elif [ "$methodname" == "PUT" ]; then
        echo "Updating task data for taskId : $taskID"
	echo "###############################################################"
        curl -i -H "Content-Type: application/json" -X ${methodname} -d "{\"title\":\"$title\",\"due_date\":\"$due_date\",\"status\":\"$status\"}" ${BASE_URL}/${taskID}
fi
