## Making basic environments
mkdir source build run
cd build
asetup AthAnalysis,21.2.90,here
mv CMakeLists.txt ../source/
cmake $TestArea/../source
source $TestArea/*/setup.sh

## Copying my sample job option file
cd $TestArea/../run/
cp -v ../myJobOptions.py .
cp -v ../get-sample-files.sh .

