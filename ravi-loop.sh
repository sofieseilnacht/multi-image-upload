#!/bin/bash

#set -x
## set reasonable defaults
imagedir="./images"
logdir="./logs"
ravi_exec="./Ravi.py"

usage() { echo "Usage: $0 [-i <imagedir>] [-l <logdir>]" 1>&2; exit 1; }

while getopts "i:l:" opt; do
    case "${opt}" in
        i)
            imagedir=${OPTARG}
            ;;
        l)
            logdir=${OPTARG}
            ;;
        ?)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

## check if directories exist
if [ -z "${imagedir}" ] || [ -z "${logdir}" ]; then
    usage
    exit -1
fi

## list the *jobinfo.json files in the logdir and put into jobinfo_files variable
jobinfo_files=$(find $logdir -name '*-jobinfo.json' -print )

## iterate through directories in the image directoru
for jobinfo in $jobinfo_files
do
    ra=$(jq .calibration.ra $jobinfo)
    dec=$(jq .calibration.dec $jobinfo)
    org_filename=$(jq .original_filename $jobinfo)
    org_filename="${org_filename%\"}"
    org_filename="${org_filename#\"}"
    nova_name="${org_filename%.*}"
    job_prefix=${jobinfo%%-*}
    job_id=$(basename $job_prefix)
    nova_dir=$(dirname $jobinfo)

    echo "./Ravi.py --SN $nova_name --SNlogs $nova_dir --SNdir $imagedir/$org_filename --SNcoord $ra $dec --jobid $job_id >> $nova_dir/ravi.log"
    eval "./Ravi.py --SN $nova_name --SNlogs $nova_dir --SNdir $imagedir/$org_filename --SNcoord $ra $dec --jobid $job_id >> $nova_dir/ravi.log"

    # dump fits headers for easy reading
    #fitsfile="$(nova_dir)/($job_id)-($job_id)new.fits"
    #eval "fitsheader --table ascii.csv $(fitsfile) > $(fitsfile).headers.csv"

    sleep 15
done

