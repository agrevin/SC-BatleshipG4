import os
import subprocess

class LaunchProofSetup:
    def __init__(self):
        self.BattleGroundProofDirect = f'{os.getcwd()}/BattleGround_proof'
        self.AliveProofDirect = f'{os.getcwd()}/AliveProof'
        self.ShotProofDirect = f'{os.getcwd()}/Shot_proof'

        
        self.launch_proofing_setup(self.AliveProofDirect,f'zokrates compile -i AliveProof.zok')
        self.launch_proofing_setup(self.ShotProofDirect,f'zokrates compile -i Shot_proof.zok')
        self.launch_proofing_setup(self.BattleGroundProofDirect,f'zokrates compile -i BattleGround_proof.zok')

    def launch_proofing_setup(self,direct ,compile_command:str):
        
        os.chdir(direct)

        try:
            # Execute the compute-witness command
            compute_witness_process = subprocess.run(compile_command, shell=True, check=True, capture_output=True)
            #print(f"Output: {compute_witness_process.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}") 

        setup_command = f'zokrates setup'

        try:
            setup_process = subprocess.run(setup_command, shell=True, check=True, capture_output=True)
                #print(f"Output: {generate_proof_process.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}") 

if __name__ == '__main__':
    start_setup = LaunchProofSetup()