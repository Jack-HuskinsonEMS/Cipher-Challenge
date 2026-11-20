import math
import random
import re

# --- INPUT ---
cipher = input("CIPHER: ")
cleanCipher = re.sub(r'[^A-Z]', '', cipher.upper())

MIN_BLOCK = int(input("Min block size to test (e.g., 2): "))
MAX_BLOCK = int(input("Max block size to test (e.g., 20): "))

# --- SCORING SETUP ---
QuadCount = {}
Total = 0
with open("english_quadgrams.txt") as file:
    for line in file:
        parts = line.strip().split()
        QuadCount[parts[0]] = int(parts[1])
        Total += int(parts[1])

QuadProbs = {quad: math.log10(count / Total) for quad, count in QuadCount.items()}
Default = math.log10(0.1 / Total)

def NgramAnalysis(text, QuadProbs):
    TotalScore = 0
    Evaled = len(text) - 3
    if Evaled <= 0:
        return Default
    for i in range(Evaled):
        TotalScore += QuadProbs.get(text[i:i+4], Default)
    return TotalScore / Evaled

# --- THE LOCAL ANA MAP ---
def MapLocalAna(cipher, mapping, blockSize):
    solv = []
    for i in range(0, len(cipher), blockSize):
        block = cipher[i:i+blockSize]
        for j in mapping:
            if j < len(block):
                solv.append(block[j])
    return "".join(solv)

# --- MUTATION OPERATOR ---
def mutate_mapping(mapping, blockSize):
    new_map = mapping[:]
    if blockSize < 2:
        return new_map
        
    if random.random() < 0.5 or blockSize < 3:
        pos1, pos2 = random.sample(range(blockSize), 2)
        new_map[pos1], new_map[pos2] = new_map[pos2], new_map[pos1]
    else:
        seg_len = random.randint(1, min(3, blockSize - 1))
        start = random.randint(0, blockSize - seg_len)
        segment = new_map[start:start+seg_len]
        rem = new_map[:start] + new_map[start+seg_len:]
        insert_pos = random.randint(0, len(rem))
        new_map = rem[:insert_pos] + segment + rem[insert_pos:]
    return new_map

# --- SOLVER FOR A SINGLE BLOCK SIZE ---
def solve_block_size(cipher_text, block_size, restarts=3, steps_per_run=15000):
    if block_size == 1:
        return NgramAnalysis(cipher_text, QuadProbs), [0], cipher_text

    # 1. Auto-calibrate T0 and T_final for this specific block size
    warm_map = list(range(block_size))
    warm_score = NgramAnalysis(MapLocalAna(cipher_text, warm_map, block_size), QuadProbs)
    downhill_diffs = []

    for _ in range(300):
        warm_map = mutate_mapping(warm_map, block_size)
        s = NgramAnalysis(MapLocalAna(cipher_text, warm_map, block_size), QuadProbs)
        d = s - warm_score
        if d < 0:
            downhill_diffs.append(abs(d))
        warm_score = s

    e_avg = sum(downhill_diffs) / len(downhill_diffs) if downhill_diffs else 0.05
    T0 = e_avg / -math.log10(0.80)
    T_final = e_avg / 5.0
    mult = (T_final / T0) ** (1 / steps_per_run)

    # 2. Run multi-restart simulated annealing
    best_score = -999.0
    best_mapping = None
    best_text = ""

    for _ in range(restarts):
        mapping = list(range(block_size))
        random.shuffle(mapping)
        temp_cipher = MapLocalAna(cipher_text, mapping, block_size)
        working_score = NgramAnalysis(temp_cipher, QuadProbs)
        T = T0

        for _ in range(steps_per_run):
            cand_map = mutate_mapping(mapping, block_size)
            test_cipher = MapLocalAna(cipher_text, cand_map, block_size)
            curr_score = NgramAnalysis(test_cipher, QuadProbs)
            diff = curr_score - working_score

            if diff > 0 or 10 ** (diff / T) > random.random():
                mapping = cand_map
                working_score = curr_score
                if curr_score > best_score:
                    best_score = curr_score
                    best_text = test_cipher
                    best_mapping = mapping[:]

            T = max(T_final, T * mult)

    return best_score, best_mapping, best_text

# --- BLOCK SIZE SCANNER LOOP ---
print(f"\nScanning block sizes {MIN_BLOCK} to {MAX_BLOCK} (Cipher length: {len(cleanCipher)})...\n")
print(f"{'Block':<6} | {'Best Score':<11} | {'Divisible?':<10} | {'Plaintext Preview'}")
print("-" * 85)

overall_best = (-999.0, 0, [], "")
results = []

for b in range(MIN_BLOCK, MAX_BLOCK + 1):
    # Scale steps slightly for larger block sizes
    steps = min(30000, max(10000, b * 1200))
    score, mapping, text = solve_block_size(cleanCipher, b, restarts=3, steps_per_run=steps)
    
    div_flag = "YES" if len(cleanCipher) % b == 0 else "no"
    results.append((score, b, mapping, text))
    print(f"{b:<6} | {score:<11.4f} | {div_flag:<10} | {text[:52]}")

    if score > overall_best[0]:
        overall_best = (score, b, mapping, text)

# --- FINAL SUMMARY ---
best_score, best_b, best_map, best_text = overall_best
print("\n" + "=" * 85)
print(f"WINNER -> Block Size: {best_b} | Score: {best_score:.5f}")
print(f"Best Mapping: {best_map}")
print(f"Full Decrypted Text:\n{best_text}")
