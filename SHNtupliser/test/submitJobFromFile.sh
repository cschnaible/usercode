#!/usr/bin/env bash

#nrEventsPerJob=10000 #dont think this does anything

datasetFile=$1
datasetPattern=$2
live=$3
datasetAntiPattern=$4
#for entry in `grep $dataset $datasetFile | awk -F "&" '{print $1}'`
for entry in `grep $datasetPattern $datasetFile | grep -v $datasetAntiPattern | sed 's| ||g'`
do
#line=`grep $e`ntry $datasetFile`
line=$entry

datasetPath=`echo $line | awk -F "&" '{print $1}'`
dataset=`echo $datasetPath | awk -F "/" '{print $2}'`
nrEvents=`echo $line | awk -F "&" '{print $2}'`
weight=`echo $line | awk -F "&" '{print $4*$5}'`
cmsswVersion=`echo $datasetPath | awk -F "/" '{print $3}'`
outputFile=${dataset}_ntuples_${cmsswVersion}_SHv17.root

#the output directory /pnfs/pp.rl.ac.uk/data/cms/store/user/harper/$outputPath

outputPath=383/v17/$dataset/
#the output directory /pnfs/pp.rl.ac.uk/data/cms/store/user/harper/$outputPath


baseCfg="shNtupliser_mc.py"
#baseCfg="runSHNtupliser_base.cfg"

#nrJobs=`echo $nrEvents/$nrEventsPerJob + 1 | bc`
nrJobs=`echo $line | awk -F "&" '{print $7}'`
datasetCode=`echo $line | awk -F "&" '{print $6}'`


if [[ "$live" == "ON" ]] ; then
echo about to submit for real ./submitCrabJob.sh $datasetPath $nrEvents $nrJobs $outputFile $outputPath $datasetCode $weight $baseCfg $dbsUrl 
sleep 5s
./submitCrabJob.sh $datasetPath $nrEvents $nrJobs $outputFile $outputPath $datasetCode $weight  $baseCfg $dbsUrl
#sleep 30m
else
echo ./submitCrabJob.sh $datasetPath $nrEvents $nrJobs $outputFile $outputPath $datasetCode $weight $baseCfg $dbsUrl


fi

done