import sys
    
def transcribe(path):
    transcript = "Put your transcription function here."
    return transcript

def main(): 
    path = sys.stdin.read()
    transcript = transcribe(path)
    sys.stdout.write(transcript)

main()