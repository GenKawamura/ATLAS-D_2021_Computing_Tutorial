theApp.EvtMax = 500

import AthenaPoolCnvSvc.ReadAthenaPool

svcMgr += CfgMgr.AthenaEventLoopMgr (EventPrintoutInterval = 100)

import glob
fileInputs = glob.glob('valid2.117050.PowhegPythia_P2011C_ttbar.digit.AOD.e2657_s1933_s1964_r5534/*')
svcMgr.EventSelector.InputCollections = fileInputs

# Fetch the AthAlgSeq, i.e., one of the existing master sequences where one should attach all algorithms                                                                     
algseq = CfgMgr.AthSequencer ("AthAlgSeq")

# Select muons above a pt threshold and                                                                                                                                      
# create an output muon container only with the selected muons                                                                                                               
algseq += CfgMgr.ParticleSelectionAlg ( "MyMuonSelectionAlg",
                                       InputContainer      = "Muons",
                                       OutputContainer     = "SelectedMuons",
                                       Selection           = "Muons.pt > 15.0*GeV"
                                       )

# Build all possible di-muon combinations and call the result viable Z-boson candidates                                                                                      
algseq += CfgMgr.ParticleCombinerAlg ( "MyZmumuBuilderAlg",
                                      InputContainerList = [ "SelectedMuons", "SelectedMuons" ],
                                      OutputContainer    = "ZmumuCands",
                                      SetPdgId           = 23 # This is a Z boson                                                                                            
                                      )

# ====================================================================                                                                                                       
# Define your output root file holding the histograms using MultipleStreamManager                                                                                            
# ====================================================================                                                                                                       
rootStreamName = "TutoHistStream"
rootFileName=   "TutoHistFile.root"
rootDirName=    "/Hists"
from OutputStreamAthenaPool.MultipleStreamManager import MSMgr
MyFirstHistoXAODStream = MSMgr.NewRootStream ( rootStreamName, rootFileName )

# Now, import the new histogram manager and histogram tool                                                                                                                   
#from HistogramUtils.HistogramManager import HistogramManager as HistMgr
#histMgr = HistMgr ( "MyHistMgr",
#                   RootStreamName = rootStreamName,
#                   RootDirName    = rootDirName
#                   )

# Import the 1-d and 2-d histograms from ROOT                                                                                                                                
from ROOT import TH1F, TH2F
# Adding a few histograms to the histogram manager                                                                                                                           
# Note the different methods of doing this (they are all equivalent)                                                                                                         
#from HistogramUtils.HistogramTool import HistogramTool as HistTool
#histMgr += ( TH1F ("mueta", "#eta^{#mu}", 50, -2.7, 2.7), "Muons.eta" )
#histMgr.add( TH1F ("mupt", "p_{t}^{#mu}", 50, 0.0, 100.0), "Muons.pt / GeV " )
#histMgr.add( TH1F ("Zmass", "m^{Z}", 50, 50.0, 150.0), "ZmumuCands.m / GeV " )
#histMgr += HistTool ( TH2F ("muptvsmueta", "p_{t}^{#mu} vs. #eta^{#mu}", 50, 0.0, 100.0, 50, -2.7, 2.7), "Muons.pt / GeV ", "Muons.eta" )

# ====================================================================                                                                                                       
# Create a subsequence:                                                                                                                                                      
# Remember that a subsequece stops its execution for a given event after an algorithm                                                                                        
# that declares that that event doesn't pass a certain selection. This special type of                                                                                       
# sub-sequence additionally handles histogram booking, cloning, and scheduling.                                                                                              
# ====================================================================                                                                                                       
#subSeq = CfgMgr.AthAnalysisSequencer ("AnaSubSeq",
#                                     HistToolList = histMgr.ToolList()
#                                     )
#algseq += subSeq

# Make a cut: check that we have at least one Z-boson candidate                                                                                                              
subSeq = CfgMgr.CutAlg ("CutZExists", Cut = "count(ZmumuCands.pt > -100.0*GeV) >= 1" )

# Make another cut: check the invariant mass of the di-muon system                                                                                                           
subSeq += CfgMgr.CutAlg ("CutZMass", Cut = "count(ZmumuCands.m > 70.0*GeV) >= 1" )

# ====================================================================                                                                                                       
# Create a new xAOD:                                                                                                                                                         
# ====================================================================                                                                                                       
from OutputStreamAthenaPool.MultipleStreamManager import MSMgr
xAODStreamName = "MyFirstXAODStream"
xAODFileName = "myXAOD.pool.root"
MyFirstXAODStream = MSMgr.NewPoolRootStream ( xAODStreamName, xAODFileName )

MyFirstXAODStream.AddItem (['xAOD::MuonContainer#Muons'])
MyFirstXAODStream.AddItem (['xAOD::MuonAuxContainer#MuonsAux.'])
MyFirstXAODStream.AddItem (['xAOD::CompositeParticleContainer#ZmumuCands'])
MyFirstXAODStream.AddItem (['xAOD::CompositeParticleAuxContainer#ZmumuCandsAux.'])

# Only events that pass the filters listed below are written out                                                                                                             
# AcceptAlgs  = logical OR of filters                                                                                                                                        
# RequireAlgs = logical AND of filters                                                                                                                                       
# VetoAlgs = logical NOT of filters                                                                                                                                          
MyFirstXAODStream.AddAcceptAlgs ( ["CutZMass"] )
