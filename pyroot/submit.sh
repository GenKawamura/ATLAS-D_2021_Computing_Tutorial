## Set nickname or Rucio account
nickname=""

## Checking nickname info
if [ -z "$nickname" ]; then
    ## Extracting a nickname from user certificate
    nickname=$(voms-proxy-info --all | grep nickname | awk '{print $5}')

    ## Still missing
    [ -z "$nickname" ] && echo "nickname is empty" && exit -1
fi

datetime=$(date -u +%Y%m%d%H%M%S)
inDS="valid2.117050.PowhegPythia_P2011C_ttbar.digit.AOD.e2657_s1933_s1964_r5534"
outDS="user.${nickname}.tutorial.pyroot.xAOD.v2018_${datetime}"
infile="input.txt"
outfile="hist.root"

prun --useRootCore --inDS=$inDS --forceStaged --outDS=$outDS --outputs=$outfile --nFiles=100 --nFilesPerJob=1 --exec="echo %IN > $infile; xAOD_electron_hist_example.py -i $infile -o $outfile"

