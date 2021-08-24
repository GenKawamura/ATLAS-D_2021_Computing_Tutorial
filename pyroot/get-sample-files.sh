#!/bin/bash

dataset=valid2.117050.PowhegPythia_P2011C_ttbar.digit.AOD.e2657_s1933_s1964_r5534
num_files=1
protocol=gsiftp
rucio_account=gkawamur

usage="$0 [options]

 -n:  number of files [default: $num_files]
 
"

if [ $# -eq 0 ]; then
    echo "$usage"
    exit 0
fi


#--------------------------
# Getopt
#--------------------------
while getopts "n:hv" op
  do
  case $op in
      n) num_files=$OPTARG
          ;;
      h) echo "$usage"
          exit 0
          ;;
      v) echo "$version"
          exit 0
          ;;
      ?) echo "$usage"
          exit 0
          ;;
  esac
done


## Loading rucio env
setupATLAS(){
    export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
    source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh ""
}
setupATLAS
[ -z "$RUCIO_ACCOUNT" ] && export RUCIO_ACCOUNT=$rucio_account
lsetup rucio

## Selecting a file
for i in $(seq 1 $num_files)
do
    remote_file=$(rucio list-file-replicas $dataset --protocol $protocol | grep "\.root" | shuf | head -n 1 | perl -pe "s/^.*($protocol.*?) .*$/\1/g")
    [ -z "$remote_file" ] && echo "rucio cannot find a file" && exit -1
    [ -e $dataset/$(basename $remote_file) ] && continue
    
    [ ! -e $dataset ] && mkdir -v $dataset
    echo "Downloading [$(basename $remote_file)] from [$remote_file]"
    uberftp $remote_file file:////$PWD/$dataset/$(basename $remote_file)
done
