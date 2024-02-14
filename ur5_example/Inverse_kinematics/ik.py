import ikpy.chain
import numpy as np



my_chain = ikpy.chain.Chain.from_urdf_file("../asserts/ur5.urdf")
target_position = [ 0.1, -0.2, 0.4]
print("The angles of each joints are : ", my_chain.inverse_kinematics(target_position))

real_frame = my_chain.forward_kinematics(my_chain.inverse_kinematics(target_position))

print("Computed position vector : %s, original position vector : %s" % (real_frame[:3, 3], target_position))