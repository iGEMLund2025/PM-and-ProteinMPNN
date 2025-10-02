#Description:
#Highlights the selection of resides that is your active site
#Colours the residues close to your ligand red
#Compares the residues close to your ligand with the chosen active site and colours matching residues blue
#If you have loaded a selection of several ligands and named them "..._ligand"
#the script checks which of the ligands fit the binding site the best

from pymol import cmd

# Gets object names
objects = cmd.get_names()

# Selects known binding site from paper
kbs = cmd.select("known_binding_site", "resi 184+207+208+209+249+280+303+305+310+311")

# Colors the binding site yellow
cmd.color("yellow", "known_binding_site")


ligands   = [obj for obj in objects if obj.endswith('_ligand')]

# Gets residues for known binding site
residues_kbs = set()
cmd.iterate('known_binding_site', "residues.add((chain, resi, resn))", space={"residues": residues_kbs})

# Track best match
best_match_count = 0
best_ligand_indices = []
matching_data = {}

# Loop over ligands to determine proposed binding sites
for i, ligand in enumerate(ligands):
    pbs_name = f'proposed_binding_site{i}'
    cmd.select(pbs_name, f'({receptors[0]} within 5.0 of {ligand})')

    residues_pbs = set()
    cmd.iterate(pbs_name, "residues.add((chain, resi, resn))", space={"residues": residues_pbs})

    matching_residues = [res for res in residues_pbs if res in residues_kbs]
    match_count = len(matching_residues)
    matching_data[i] = {
        "count": match_count,
        "residues": matching_residues,
        "resi_numbers": [res[1] for res in matching_residues]
    }

    # Update best match info
    if match_count > best_match_count:
        best_match_count = match_count
        best_ligand_indices = [i]
    elif match_count == best_match_count:
        best_ligand_indices.append(i)

# Handle coloring and output
for i in range(len(ligands)):
    cmd.color('red', f'proposed_binding_site{i}')  # All proposed binding sites are red

print('Known binding site is yellow')
print('Proposed binding sites are red')

if best_match_count == 0:
    print('There are no matching residues')
elif len(best_ligand_indices) == 1:
    i = best_ligand_indices[0]
    matching_resi = "+".join(matching_data[i]["resi_numbers"])
    cmd.select(f'matching_residues{i}', f'resi {matching_resi}')
    cmd.color("blue", f'matching_residues{i}')

    final_matching_residues = set()
    cmd.iterate(f'matching_residues{i}', "residues.add((chain, resi, resn))", space={"residues": final_matching_residues})

    print('Matching residues are blue')
    print(f'Matching residues = {final_matching_residues}')
    print(f'The ligand with the highest number of matching residues is: {ligands[i]}')
else:
    print(f'Multiple ligands have the same number of matching residues ({best_match_count})')
    print('Ligands with highest match count:')
    for i in best_ligand_indices:
        print(f'- {ligands[i]}')
