#Description:
#After loading your protein of interest in pymol and selected your
#residues of interest the script generates 19 mutatated pdbs for all residues
#and names them appropriately


from pymol import cmd
import os

# Settings
pdb_file = r"C:\Users\sixte\OneDrive\Desktop\Skola\Bioinformatics\Docking project\ProteinMPNN 1t5d\Final sequnces PDB modified coordinates\E_1t5d.pdb"
selection = "selection_to_mutate"  # Your selection of residues
output_folder = "mutants_pmpnn_1t5d"
amino_acids = [
    "ALA", "ARG", "ASN", "ASP", "CYS",
    "GLN", "GLU", "GLY", "HIS", "ILE",
    "LEU", "LYS", "MET", "PHE", "PRO",
    "SER", "THR", "TRP", "TYR", "VAL"
]

# Make output folder
os.makedirs(output_folder, exist_ok=True)

# Extract residue info from selection
model = cmd.get_model(selection)
unique_residues = {(atom.chain, atom.resi, atom.resn) for atom in model.atom}

pdb_basename = os.path.basename(pdb_file).replace('.pdb', '')

for chain, resi, original_resn in unique_residues:
    resi_str = str(resi)
    for aa in amino_acids:
        if aa == original_resn:
            continue  # Skip original amino acid

        # Reload clean structure each time
        cmd.reinitialize()
        cmd.load(pdb_file, "protein")

        # Mutate
        cmd.wizard("mutagenesis")
        cmd.do(f"refresh_wizard")
        cmd.get_wizard().do_select(f"/protein//{chain}/{resi_str}/")
        cmd.get_wizard().set_mode(aa)
        cmd.get_wizard().apply()

        # Save
        out_name = f"{pdb_basename}{chain}_{resi_str}_{original_resn}_to_{aa}.pdb"
        out_path = os.path.join(output_folder, out_name)
        cmd.save(out_path, "protein")

        cmd.set_wizard()  # Turn off wizard
