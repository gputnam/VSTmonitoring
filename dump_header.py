import ROOT
import sys
import os
from array import array
import argparse

def main(args):
    data_file = ROOT.TFile(args.input_file)
    t_directory_file = data_file.Get("VSTAnalysis")

    data = t_directory_file.Get("event") 
    data.GetEntry(args.entry)

    header = data.header_data[args.fem]
    print header.PrintRaw()
    print header.Print()

if __name__ == "__main__":
    """
    buildpath = os.environ["SBNDDAQ_ANALYSIS_BUILD_PATH"]
    if not buildpath:
        print "ERROR: SBNDDAQ_ANALYSIS_BUILD_PATH not set"
        sys.exit() 
    ROOT.gROOT.ProcessLine(".L " + buildpath + "/libsbnddaq_analysis_data_dict.so")
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", default="output.root")
    parser.add_argument("-f", "--fem", type=int, default=0)
    parser.add_argument("-e", "--entry", type=int, default=0)
    
    main(parser.parse_args())
