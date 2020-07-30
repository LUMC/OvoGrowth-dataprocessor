string=$1
set -f                      # avoid globbing (expansion of *).
array=(${string//,/ })
file_string=""
for i in "${!array[@]}"
do
    file_string=${file_string}"input/${array[i]}/genes.tsv "
done
cat ${file_string} | sort | uniq > $2