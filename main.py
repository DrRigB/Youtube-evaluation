import subprocess
print("this is working")

def  run_text():
    print("Extracting video....")
    subprocess.run(["python", "youtube_text.py"])

def run_summerization():
    print("Running summerization...")
    subprocess.run(["python", "summerization.py"])

if __name__ == "__main__":
    run_text()
    run_summerization()
    print("End of process...")

