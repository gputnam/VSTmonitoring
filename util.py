import ROOT
import argparse
import math

def get_event(tree, event, absolute):
    if not absolute:
        tree.GetEntry(event)
        return tree

    tree.GetEntry(0)
    if not hasattr(tree, "header_data"):
        raise ValueError("Input tree must have header_data in order to get data at absolute event number")

    event_0 = tree.header_data[0].event_number
    diff = event - event_0
    if diff < 0:
        raise ValueError("TTree event numbers start after requested event number")
    try:
        tree.GetEntry(diff)
    except: # will fail when diff is to big for the entries in the file
        raise ValueError("TTree event numbers end before requested event number")
    return tree

def with_io_args(parser):
    parser.add_argument("-i", "--input_file", default="output.root")
    parser.add_argument("-o", "--output", default="waveform")
    parser.add_argument("-w", "--wait", action="store_true")
    parser.add_argument("-s", "--save", action="store_true")
    return parser

def with_location_args(parser):
    parser.add_argument("-e", "--event", type=int, default=0)
    parser.add_argument("-a", "--absolute", action="store_true")
    return parser

