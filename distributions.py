import ROOT
import sys
import os
from array import array
import argparse

def rms(channel_data):
    return channel_data.rms
 
def weak_peak(channel_data):
    sub_peak_max = -500
    sub_peak_min = 500
    for pair in channel_data.noise_ranges:
        for i in range(pair[0], pair[1]):
            if channel_data.waveform[i] > sub_peak_max:
                sub_peak_max = channel_data.waveform[i]
            if channel_data.waveform[i] < sub_peak_min:
                sub_peak_min = channel_data.waveform[i]
    n_weak_peaks = 0
    for peak in channel_data.peaks:
        if peak.amplitude < 0 and peak.amplitude + 30 > sub_peak_min:
            n_weak_peaks += 1
        elif peak.amplitude > 0 and peak.amplitude - 30 < sub_peak_min:
            n_weak_peaks += 1
    return 100*float(n_weak_peaks)

def n_peaks(channel_data):
    return float(len([x for x in channel_data.peaks if x.is_up]))

def main(args):
    data_file = ROOT.TFile(args.input_file)
    t_directory_file = data_file.Get("VSTAnalysis")

    event_tree = t_directory_file.Get("event")
 
    if args.data == "weak_peak":
        data_fun = weak_peak
    elif args.data == "occupancy":
        data_fun = n_peaks
    else: # for baseline, mean_peak_height, rms
        data_fun = lambda data: getattr(data, args.data)

    if args.data == "weak_peak" or args.data == "occupancy":
        hist = ROOT.TH1F(args.data, args.data, 20, 0., 100.)
    elif args.data == "rms":
        hist = ROOT.TH1F(args.data, args.data, 100, 0., 5.)
    elif args.data == "baseline":
        hist = ROOT.TH1F(args.data, args.data, 100, -10., 10.)
    elif args.data == "mean_peak_height":
        hist = ROOT.TH1F(args.data, args.data, 100, 20., 100.)

    event_tree.GetEntry(0)
    data = [0 for x in range(len(event_tree.channel_data))]
    n_events = 0.
    for event in event_tree:
        for channel in event.channel_data:
            if channel.empty:
                continue
            if args.per_event:
                hist.Fill(data_fun(channel))
            else:
                data[channel.channel_no] = (n_events * data[channel.channel_no] + data_fun(channel)) / (n_events + 1.)
        n_events += 1

    if not args.per_event:
        if args.verbose_data:
            for i, d in enumerate(data):
                print i, d
        for d in data:
            hist.Fill(d)
    plot(hist, args)

def plot(hist, args):
    canvas = ROOT.TCanvas("canvas", "Histo Canvas", 250,100,700,500)
    hist.Draw()
    hist.SetTitle("Weak Peak Distribution")
    hist.GetXaxis().SetTitle(args.data)
    hist.GetYaxis().SetTitle("Number of Channels")
    canvas.Update()
    if args.wait:
       raw_input("Press Enter to continue...")
    if args.save:
       canvas.SaveAs(args.output + ".pdf")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = with_io_args(parser)

    parser.add_argument("-d", "--data", default="rms")
    parser.add_argument("-p", "--per_event", action="store_true")
    parser.add_argument("-v", "--verbose_data", action="store_true")
    
    main(parser.parse_args())
