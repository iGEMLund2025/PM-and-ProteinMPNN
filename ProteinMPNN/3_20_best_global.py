# -*- coding: utf-8 -*-

"""Filter best 20 sequences regarding global score"""

import os
import re

base_dir = os.getcwd()

for subdir in os.listdir(base_dir):
    subpath = os.path.join(base_dir, subdir)
    seqs_path = os.path.join(subpath, "seqs")
    #Search all .fa files in the seqs folder
    if os.path.isdir(seqs_path):
        for filename in os.listdir(seqs_path):
            if filename.endswith(".fa") or filename.endswith(".fasta"):
                file_path = os.path.join(seqs_path, filename)
                # Parse sequences and their scores 
                with open(file_path, "r") as f:
                    lines = f.readlines()

                entries = []
                for i in range(0, len(lines), 2):
                    header = lines[i].strip()
                    seq = lines[i+1].strip() if i+1 < len(lines) else ""
                    match = re.search(r'global_score=([0-9.]+)', header)
                    if match:
                        score = float(match.group(1))
                        entries.append((score, header, seq))

                # Order by score and get 20 best por score 
                top20 = sorted(entries, reverse=True)[:20]

                # Save new file
                out_file = os.path.join(seqs_path, filename.replace('.fa', '_top20.fa').replace('.fasta', '_top20.fa'))
                with open(out_file, "w") as out:
                    for score, header, seq in top20:
                        out.write(f"{header}\n{seq}\n")

                print(f"Saved top 20 to {out_file}")

