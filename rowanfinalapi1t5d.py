#The script that talks with the Rowan API.
#Uploads and sanitizes the pdbs in the chosen folder and then proceeds to dock
#them with a chosen ligand


import rowan
import time
import json
import shutil
from pathlib import Path
from rowan import smiles_to_stjames, submit_docking_workflow

# Rowan API key
rowan.api_key = "INSERT API KEY HERE"

# --- Configuration ---
protein_folder = Path(r"C:\Users\sixte\AppData\Local\Schrodinger\PyMOL2\mutants_pmpnn_1t5d")
ligand_smiles = "[O-]C(=O)c1ccc(C(=O)[O-])cc1"
workflow_base_name = "Docking_"
pocket_box = [[-19, 95, 18], [15, 17, 12]]  # Box coordinates


# Convert SMILES once
ligand_molecule = smiles_to_stjames(ligand_smiles)

# === STAGE 1: Submit all workflows ===
submitted_workflows = []

for pdb_file in protein_folder.glob("*.pdb"):
    protein_name = pdb_file.stem
    workflow_name = f"{workflow_base_name}{protein_name}"
    print(f"\n--- Submitting workflow for: {protein_name} ---")

    try:
        protein = rowan.upload_protein(protein_name, pdb_file)
        protein.sanitize()
        time.sleep(2)

        workflow = submit_docking_workflow(
            protein=protein.uuid,
            pocket=pocket_box,
            initial_molecule=ligand_molecule,
            do_csearch=True,
            do_optimization=True,
            name=workflow_name,
        )

        print(f"Submitted: {workflow.uuid}")
        submitted_workflows.append({
            "protein_name": protein_name,
            "pdb_path": str(pdb_file),
            "workflow_uuid": workflow.uuid
        })

    except Exception as e:
        print(f"Failed to submit workflow for {protein_name}: {e}")

