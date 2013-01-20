from __future__ import division
import pyaudio
import wave
import sys
import zmq
import ntplib
from time import ctime

context   = zmq.Context(1)
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5563")



def play(filepath):
    chunk = 1024
    wf = wave.open(filepath, 'rb')
    p = pyaudio.PyAudio()
    rate = wf.getframerate()
    # open stream
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # read data
    #data = wf.readframes(chunk)
    data = True
    # play stream
    i = 0;
    #c = ntplib.NTPClient()
    #response = c.request('nist1-ny.ustiming.org', version=3)
    #stime = int(response.orig_time * 1000)
    #print stime
    #publisher.send_multipart(["S", str(stime)])
    while data != '':
        i = i + 1
        #print wf.tell()
        data = wf.readframes(chunk)
        stream.write(data)
        
        if(not i % 223):
            publisher.send_multipart(["B", str(wf.tell()-chunk)])
            publisher.send_multipart(["SECS", str((wf.tell()-chunk)/rate)])
       
    stream.close()
    p.terminate()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Plays a wave file.\n\n" +\
              "Usage: %s filename.wav" % sys.argv[0]
        sys.exit(-1)
    play(sys.argv[1]) 
