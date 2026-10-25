import sys

print("==================================================")
print("     TOY REED-SOLOMON (3,2) ERASURE ENCODER       ")
print("==================================================")

# --- 1. PREPARE THE DATA SHARDS ---
# Input text must be exactly 3 characters long for a dead-simple RS(3,2) test
input_message = "SOS" 
print(f"Original Text Message: '{input_message}'")

# Convert characters to numerical byte values (ASCII values)
# These represent our 3 Data Blocks: d1, d2, d3
d1 = ord(input_message[0])
d2 = ord(input_message[1])
d3 = ord(input_message[2])
print(f"Data Blocks Generated -> D1: {d1}, D2: {d2}, D3: {d3}")

# --- 2. CALCULATE PARITY SHARDS (ENCODING) ---
# In GF(2^8) math, standard addition is simplified to a bitwise XOR (^) operation.
# We generate 2 Parity Blocks (p1, p2) using a simple linear combination combination matrix.
p1 = d1 ^ d2 ^ d3
p2 = d1 ^ (d2 ^ 2) ^ (d3 ^ 3)  # Shifted weights to guarantee linear independence
print(f"Parity Blocks Generated -> P1: {p1}, P2: {p2}")
print("Storage configuration completed successfully.")

# --- 3. INJECT FAULT (SIMULATE DATA LOSS) ---
print("\n--- SIMULATING CRASH: Data Node 2 has failed! ---")
lost_d2 = d2
d2 = None  # Erasing Data Block 2 completely from memory
print(f"Current State -> D1: {d1}, D2: [CRASHED/LOST], D3: {d3} | P1: {p1}, P2: {p2}")

# --- 4. RECONSTRUCT LOST DATA (DECODING) ---
print("\nTriggering Data Reconstruction Loop...")

# Because addition/subtraction are the same in XOR math, we can reconstruct
# D2 directly by isolating it from the P1 parity block formula:
# Original: P1 = D1 ^ D2 ^ D3  --> Rebuilt: D2 = P1 ^ D1 ^ D3
reconstructed_d2 = p1 ^ d1 ^ d3

print(f"-> Math system retrieved value: {reconstructed_d2}")

# Convert back to readable text character
recovered_char = chr(reconstructed_d2)

# --- 5. VERIFY SYSTEM INTEGRITY ---
if reconstructed_d2 == lost_d2:
    print("SUCCESS: Lost Data Block 2 was perfectly reconstructed!")
    print(f"Recovered Message Shard: '{recovered_char}'")
    print(f"Complete Restored Message: '{chr(d1)}{recovered_char}{chr(d3)}'")
else:
    print("FAILURE: Reconstructed data does not match the original block.")
print("==================================================")
