# -*- coding: utf-8 -*-
"""
File to rename each fasta resulting from Proteinmpn with their JSON´s shell and threshold, so the name contains the
thresholds and shells it was run and for which enzyme. 

"""

import os
import glob

# Get the current working directory 
base_dir = os.getcwd()

# Loop over all subfolders
for subfolder in os.listdir(base_dir):
    subfolder_path = os.path.join(base_dir, subfolder)
    if os.path.isdir(subfolder_path):
        # Find any .fasta file in the subfolder 
        fasta_files = glob.glob(os.path.join(subfolder_path, "*.fasta"))
        for fasta in fasta_files:
            # Build the new file name: use the subfolder name and .fasta extension
            # Remove .json.jsonl or .jsonl if present in the folder name
            clean_name = subfolder.replace('.json.jsonl','').replace('.jsonl','')
            new_fasta = os.path.join(subfolder_path, f"{clean_name}.fasta")
            if fasta != new_fasta:  
                print(f"Renaming {fasta} -> {new_fasta}")
                os.rename(fasta, new_fasta)
