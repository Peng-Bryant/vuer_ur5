from asyncio import sleep
from pathlib import Path
import numpy as np
from Inverse_kinematics.IK_solver import *
from vuer import Vuer, VuerSession
from vuer.schemas import Urdf, AmbientLight, DirectionalLight, group, Movable, Gripper, DefaultScene

pi = 3.1415
URDF_PATH = '../assets/ur5.urdf'
app = Vuer(static_root=Path(__file__).parent / "../assets")
position_value = []
ik_solver = IK_solver(URDF_PATH)


@app.add_handler("OBJECT_MOVE" )
async def on_move(event, sess: VuerSession):
    position_value.append(event.value['position'])
    # print(event.value)


@app.spawn(start=True)
async def main(sess: VuerSession):
    sess.upsert @ AmbientLight(intensity=1, key='ambient')
    sess.upsert @ DirectionalLight(intensity=1, key='default-light')
    sess.upsert @ group(
        group(key="robot"),
        rotation=[-np.pi / 2, 0, 0],
        key="robot-root"
    )
    sess.set @ DefaultScene(
            Urdf(
                src="http://localhost:8012/static/ur5.urdf",
                jointValues={
            'shoulder_pan_joint': 0,
            'shoulder_lift_joint': 0,
            'elbow_joint': 0,
            'wrist_1_joint': 0,
            'wrist_2_joint': 0,
            'wrist_3_joint': 0,
            'ee_fixed_joint': 0,
                },
                key="robot",
            ),
            position=[0, 0, 0.3],
            scale=0.4,
        grid=True,
    )
    sess.upsert @ Urdf(
        src="http://localhost:8012/static/ur5.urdf",
        jointValues={
            # 'shoulder_pan_joint': 0,
            # 'shoulder_lift_joint': 0,
            # 'elbow_joint': 0,
            # 'wrist_1_joint': 0,
            # 'wrist_2_joint': 0,
            # 'wrist_3_joint': 0,
            # 'ee_fixed_joint': 0,
            # 'base_link-base_fixed_joint': 0,
            # 'wrist_3_link-tool0_fixed_joint': 0,
            # 'tool0_fixed_joint-tool_tip': 0,
            # 'world_joint': 0,
            # 'rotated_base-base_fixed_joint': 0
        },
        key="robot",
    )

    # now add the target block
    sess.upsert @ Movable(
        Gripper(),
        position=[0.5, 0, 0.5],
        key="gripper-target"
    )

    sess.upsert @ Movable(
        Gripper(),
        position=[0.5, 0, 0.5],
        key="gripper-syn"
    )


    # can await for onload event instead
    await sleep(1)
    # frame = (await sess.grab_render()).value['frame']
    # print(len(frame))

    i = 0
    joint_position = []
    while True:
    #     sess.update @ Movable(
    #     Gripper(),
    #     position=[0.5, (i%100)*0.02, 0.5],
    #     key="gripper-target"
    # )
        position = position_value[-1]
        joint_position.append(ik_solver.solve_ik(position))
        
        if(i%100 == 1):
            print(joint_position[-1])

        sess.update @ Movable(
        Gripper(),
        position=[position[0]+0.4,position[1]+0.4,position[2]+0.4],
        key="gripper-syn"
    )

        await sleep(0.016)
        i += 1

