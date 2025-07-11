#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
import json
import sys
import argparse
import time
import textwrap

#TODO: make it dynamic
def getAnalysisTool(name,si):
    if name == 'load':
        return TraceAnalysisCpuLoad(si)
    elif name == 'list':
        return TraceAnalysisList(si)
    else:
        return None

if __name__ == '__main__':
    defaultOutput = 'trace.json'
    #arguments (no default arg for -i and -o to get None if not defined)
    parser = argparse.ArgumentParser(description='Use the trace tookit to get information on Trampoline based application behavior. 2 input modes for now: json file or serial line.',
    formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
    '''\
        --------------------------------
        Examples: 
          # read from serial line,  output log to stdout. Stop acquisition with Ctrl+C
            {0} -i /dev/ttyACM0,9600
          # read from serial line, and store raw events in trace.json
            {0} -i /dev/ttyACM1,9600 -o trace.json         
          # read a json trace file, output cpu load analysis on stdout
            {0} -i trace.json -a load
          # read from serial line, store raw events (no analysis), and perform analysis to stdout
            {0} -i /dev/ttyACM1,9600 -a load -o trace.json 

        If no input argument given, same as '-i trace.json', output on stdout.
    '''.format(sys.argv[0])))
    parser.add_argument("-i", "--input", type=str, nargs='?', default='trace.json', metavar='input', help='input can either be a saved file (json format), or the serial line to get events. In that last case, the device name and the speed should be given, e.g. "/dev/ttyACM0,9600" (default %(default)s)')
    parser.add_argument("-o", "--output", type=str, nargs='?', const=defaultOutput, metavar='outputFile', help='Store the raw event list into a JSON format for later use.')
    parser.add_argument("-a", "--analysis", type=str, nargs='?', const='all', choices=['load','list'],default=None,metavar='data', help="Analysis tool to apply on the trace: allowed 'load','list' (default %(default)s)")
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help="verbose mode")
    args = parser.parse_args()

    #first, get access to files.
    traceToolFolder = "../../extra/trace-tools"
    sys.path.append(traceToolFolder)
    sys.path.append(traceToolFolder+'/analysis')
    try:
        import StaticInfo
        import TraceReader
        import TraceEvaluate
        import TraceAnalysis
        from TraceAnalysisCpuLoad import *
        from TraceAnalysisList import *
    except ImportError:
        print("I can't find trace tools scripts")
        print("=> searched in '"+traceToolFolder+"'")
        print("Maybe the TRAMPOLINE_BASE_PATH is not correctly set in your .oil file")
        print("Correct it and run goil again.")
        sys.exit(1)

    #reader    => getting raw events
    inputParams=args.input.split(',') #is there a coma in the input? yes => serial, no => file.
    if len(inputParams) == 2: # serial
        reader   = TraceReader.TraceReaderSerial(inputParams,args.verbose)
    else:                     # then file.
        reader   = TraceReader.TraceReaderFile(args.input)

    #output
    outputToFile = False
    if args.output:
        outputToFile = True
        rawEventList = []
    #read static information
    si = StaticInfo.StaticInfo('ecu_com/tpl_static_info.json')
    #evaluator => from raw events and Static info. Get events
    evaluate = TraceEvaluate.TraceEvaluate(si)
    analysisTool = getAnalysisTool(args.analysis,si)

    #end of config. main loop
    try:
        for rawEvent in reader.getEvent():
            if outputToFile:
                rawEventList.append(rawEvent)
            if analysisTool: #analysis (maybe with output)
                event = evaluate.evaluate(rawEvent)
                analysisTool.handleEvent(event)

    except KeyboardInterrupt:
        pass #done be Ctrl+C at the end of the serial acquisition
    reader.stop()
    if outputToFile:
        if args.verbose:
            print('save to '+args.output)
        with open(args.output, "w") as outfile:
            json.dump(rawEventList, outfile, indent=2)
    if analysisTool:
        analysisTool.stop()

