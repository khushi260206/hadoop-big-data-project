import subprocess
import time

def run_command(cmd):
    """Runs a system command and returns the execution time in seconds."""
    start_time = time.time()
    # Runs the docker command to interact with the Hadoop cluster
    process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    end_time = time.time()
    
    if process.returncode != 0:
        print(f"Error running command: {cmd}")
        print(process.stderr.decode())
        return None
        
    return round(end_time - start_time, 3)

print("Starting Hadoop Performance Benchmarks...")
print("=========================================")

# Define the targets inside Docker Hadoop
# We run the commands through docker exec since Hadoop lives inside the container
paths = {
    "Replication (3x)": "/replicated",
    "Erasure Coding (RS 3,2)": "/erasure-coded"
}

# Run the tests 3 times per the project instructions
for run in range(1, 4):
    print(f"\n--- RUN NUMBER {run} ---")
    
    for name, hdfs_path in paths.items():
        print(f"\nTesting: {name}")
        
        # 1. Measure Large File UPLOAD
        upload_cmd = f"docker exec -t namenode hdfs dfs -put -f /large_test_file.txt {hdfs_path}/"
        # Before running, we need to make sure the container has access to the file.
        # To keep it dead simple, let's copy the file into the container first.
        subprocess.run(f"docker cp large_test_file.txt namenode:/large_test_file.txt", shell=True)
        
        upload_time = run_command(upload_cmd)
        if upload_time:
            print(f"  -> Large File Upload Time: {upload_time} seconds")
            
        # 2. Measure Large File DOWNLOAD
        download_cmd = f"docker exec -t namenode hdfs dfs -get -f {hdfs_path}/large_test_file.txt /dev/null"
        download_time = run_command(download_cmd)
        if download_time:
            print(f"  -> Large File Download Time: {download_time} seconds")

print("\n=========================================")
print("Benchmarks complete! Write down these numbers for your final report.")
