import pyaudio
import wave
import sys
import zmq

context    = zmq.Context(1)
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5563")
subscriber.setsockopt(zmq.SUBSCRIBE, "B")


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
    data = wf.readframes(chunk)

    # play stream
    while True:
        # Read envelope with address
        [address, contents] = subscriber.recv_multipart()
        wf.setpos(int(contents))
        #data = 
        stream.write(wf.readframes(chunk))
        #print wf.tell() - int(contents)
        #print("[%s] %s\n" % (address, contents))
        #print("[%s] %s\n" % ("self", wf.tell()))
        """
        while data != '':
            print wf.tell()
            publisher.send_multipart(["B", str(wf.tell())])
        """
    #stream.close()
    #p.terminate()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Plays a wave file.\n\n" +\
              "Usage: %s filename.wav" % sys.argv[0]
        sys.exit(-1)
    play(sys.argv[1]) 
