import ROOT
import sys
import os
from array import array
import argparse
from util import *

def main(args):
    data_file = ROOT.TFile(args.input_file)
    t_directory_file = data_file.Get("VSTAnalysis")

    data = t_directory_file.Get("event") 

    data = get_event(data, args.event, args.absolute)

    header = data.header_data[args.fem]
    print header.PrintRaw()
    print header.Print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = with_location_args(parser)

    parser.add_argument("-i", "--input_file", default="output.root")
    parser.add_argument("-f", "--fem", type=int, default=0)
    
    main(parser.parse_args())
