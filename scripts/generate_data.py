import os

print("Generating benchmark files...")

# Scenario A: One large file (approx 100 Megabytes)
large_file_path = "large_test_file.txt"
with open(large_file_path, "w") as f:
    for _ in range(2000000):
        f.write("Hadoop Erasure Coding vs Replication Benchmark Data File\n")
print(f"Created {large_file_path}")

# Scenario B: 100 small files (10 Kilobytes each)
small_files_dir = "small_files"
os.makedirs(small_files_dir, exist_ok=True)
for i in range(1, 101):
    with open(f"{small_files_dir}/small_{i}.txt", "w") as f:
        f.write("Small file data piece\n" * 400)
print("Created 100 small files inside 'small_files/' directory.")
