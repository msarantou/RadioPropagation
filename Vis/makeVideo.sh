simFile="../Output/SimulationSetup.nc"
for file  in "$@"
do
    echo "$file"
    ./Visualization.py $simFile $file &

done
