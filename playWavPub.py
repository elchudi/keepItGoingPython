import pyaudio
import wave
import sys
import zmq

context   = zmq.Context(1)
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5563")



def play(filepath):
    chunk = 1024
    wf = wave.open(filepath, 'rb')
    p = pyaudio.PyAudio()

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
    while data != '':
        #print wf.tell()
        data = wf.readframes(chunk)
        stream.write(data)
        publisher.send_multipart(["B", str(wf.tell()-chunk)])

    stream.close()
    p.terminate()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Plays a wave file.\n\n" +\
              "Usage: %s filename.wav" % sys.argv[0]
        sys.exit(-1)
    play(sys.argv[1]) 
