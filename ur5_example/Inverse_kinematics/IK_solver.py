import ikpy.chain
import numpy as np

class IK_solver:
    def __init__(self, urdf_file_path):
        # Initialize the robot chain from the URDF file
        self.chain = ikpy.chain.Chain.from_urdf_file(urdf_file_path)
    
    def solve_ik(self, target_position):
        # Solve the inverse kinematics problem and return the joint values
        return self.chain.inverse_kinematics(target_position)
    
    def get_real_position(self, joint_values):
        # Compute the forward kinematics to get the real end-effector position from the joint values
        real_frame = self.chain.forward_kinematics(joint_values)
        return real_frame[:3, 3]  # Extract the position vector from the transformation matrix

