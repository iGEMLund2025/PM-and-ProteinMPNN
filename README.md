# Point Mutations and Protein MPNN Pipeline 
Point mutations offer a rational design tool to subtly reshape the active site and potentially introduce new ligand recognition. Our pipeline uses docking and cofolding simulations to test the effect of single-residue substitutions in residues identified to contact the ligand in the binding site. The model prioritizes mutations predicted to improve binding using computational scoring functions. In parallel, we incorporated ProteinMPNN into our pipeline, a sequence design tool that optimizes protein backbones by generating new, stable amino acid sequences compatible with a given structure.

## Scripts for Protein MPNN and Point Mutation Screening Process

- `Binding_site_comparisons.py` - Highlights selected active site residues, colors residues near the ligand (red), and marks overlaps with the active site (blue). For multiple ligands `_ligand`, evaluates which fits best in the binding site.

- `extract_box.py` - Extracts the coordinates of a box around a selection of residues.

- `mutations.py` - Generates 19 mutatated pdbs for all residues of interest and names them appropriately.

- `rowanfinalapi1t5d.py` - Script that talks with the Rowan API. Uploads and sanitizes the pdbs in the chosen folder and then proceeds to dock them with a chosen ligand.

#### ProteinMMPNN scripts (found in the ProteinMPNN folder)

- `1_1t5d_proteinmpn.sh` - Script that runs proteinMPNN for the 1t5d.pdb file (needs to be downloaded) and its previosuly jsonl mask files (generated from MSA). Paths can be edited in the Variables section. 

- `1_5bst_proteinmpn.sh` - Script that runs ProteinMPNN for the 5bst.pdb file (needs to be downloaded) and its previosuly jsonl mask files (generated from MSA). Paths can be edited in the Variables section. 

- `2_Results_rename.py` - Renames the resulting fasta files from ProteinMPNN (`1_1t5d_proteinmpn.sh` , `1_5bst_proteinmpn.sh`), so that the new file names include the theresholds, shells, and enzyme. Removes any unncessary naming. 

- `3_20_best_global.py` - Iterates over all the resulting ProteinMPNN fasta files (which have been renamed with the `2_Results_rename.py` script), obtaines the best 20 sequences accordign to global score, and places them in a matrix with relevant info (score, header, and sequence). 
