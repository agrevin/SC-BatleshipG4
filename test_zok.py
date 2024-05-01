import subprocess

# Generate a witness for specific inputs
nonce = 12345
ships = [0, 0, 1, 1, 1, 1, 2, 2, 0, 3, 3, 0, 4, 4, 1, 5, 5, 1, 6, 6, 0, 7, 7, 0, 8, 8, 1, 9, 9, 1]



subprocess.run(["zokrates", "compute-witness", "-a", str(nonce)] + [str(ship) for ship in ships])

# Export the verifier
subprocess.run(["zokrates", "export-verifier"])
