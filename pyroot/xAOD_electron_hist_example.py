#!/usr/bin/env python

# based on an example here: https://twiki.cern.ch/twiki/bin/view/AtlasComputing/SoftwareTutorialxAODEDM#PyROOT_with_the_xAOD

import sys, os, time, glob, re
import getopt
import ROOT


def main(argv):
    # parsing command arguments
    inputfile='input.txt'
    outputfile='hist.root'
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'xAOD_electron_hist_example.py -i [inputfile] -o [outputfile]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'xAOD_electron_hist_example.py -i [inputfile] -o [outputfile]'
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
            
    print 'Input file is', inputfile
    print 'Output file is', outputfile


    # Set up ROOT and RootCore:
    ROOT.gROOT.Macro( '$ROOTCOREDIR/scripts/load_packages.C' )
    
    # Initialize the xAOD infrastructure: 
    ROOT.xAOD.Init()

    # a histogram for our output
    outfile=ROOT.TFile.Open(outputfile,"RECREATE")
    pthist=ROOT.TH1F("pt","pt;p_{T} [GeV];Entries / 10 GeV",100,0,1000)

    treeName = "CollectionTree" # default when making transient tree anyway

    # Loop on the input files.  There are surely ways to chain the trees together,
    # which is left as an exercise to the reader.
    for i in ([file for file in open(inputfile).read().strip().split(',')]):
        print "Opening file "+i
        f = ROOT.TFile.Open(i)
        
        if not f:
            print "Couldn't open input file "+i+"...  will not continue."
            sys.exit(1)
            pass

        # Make the "transient tree":
        t = ROOT.xAOD.MakeTransientTree( f, treeName)

        # Print some information:
        print( "Number of input events: %s" % t.GetEntries() )
        for entry in xrange( t.GetEntries() ):
            t.GetEntry( entry )
            print( "Processing run #%i, event #%i" % ( t.EventInfo.runNumber(), t.EventInfo.eventNumber() ) )
            print( "Number of electrons: %i" % len( t.ElectronCollection ) )
            # loop over electron collection
            for el in t.ElectronCollection:
                pthist.Fill(el.pt()/1000.)
                pass # end for loop over electron collection
            pass # end loop over entries
        f.Close()
        pass

    outfile.cd()
    pthist.Write()
    outfile.Close()
    
    sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])
