#!/bin/bash

# Set variables
MPNN_PATH=~/ProteinMPNN  
PDB=~/drylab_igem/proteinmpn_part/Proteins_pdbs/5bst.pdb
FIXED_DIR=~/drylab_igem/proteinmpn_part/Fixed_positions/5bst
OUT_BASE=~/drylab_igem/proteinmpn_part/Results/5bst


conda activate proteinmpnn

# Loop over all *_binmask.json files 
for FIXED_JSON in "$FIXED_DIR"/*.jsonl
do
    # Get base name for output subfolder
    MASK_NAME=$(basename "$FIXED_JSON" _binmask.json)
    OUTDIR="${OUT_BASE}/${MASK_NAME}"

    mkdir -p "$OUTDIR"

    echo "Running ProteinMPNN for mask: $MASK_NAME"

    python "$MPNN_PATH/protein_mpnn_run.py" \
        --pdb_path "$PDB" \
        --fixed_positions_json "$FIXED_JSON" \
        --out_folder "$OUTDIR" \
        --num_seq_per_target 16 \
        --sampling_temp "0.1 0.2 0.3" \
        --batch_size 8 \

    echo "Done for $MASK_NAME"
done


