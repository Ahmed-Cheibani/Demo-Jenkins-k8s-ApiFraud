#!/bin/bash
if ( ! sh -c "kubectl get ns $1 -o name > /dev/null 2>&1" ) then
 echo "cree un namespace il n'existe pas "
else
 echo "$1 existe dans le cluster"
fi


if ( ! sh -c "kubectl get ns $1 -o name > /dev/null 2>&1" ) then
 echo "je dois le creé "
 kubectl get ns 
fi