import numpy as np
from scipy.spatial.transform import Rotation as R
from bvh_loader import BVHLoader

def load_motion_data(bvh_file_path):
    """part2 辅助函数，读取bvh文件"""
    with open(bvh_file_path, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith('Frame Time'):
                break
        motion_data = []
        for line in lines[i+1:]:
            data = [float(x) for x in line.split()]
            if len(data) == 0:
                break
            motion_data.append(np.array(data).reshape(1,-1))
        motion_data = np.concatenate(motion_data, axis=0)
    return motion_data



def part1_calculate_T_pose(bvh_file_path):
    """请填写以下内容
    输入： bvh 文件路径
    输出:
        joint_name: List[str]，字符串列表，包含着所有关节的名字
        joint_parent: List[int]，整数列表，包含着所有关节的父关节的索引,根节点的父关节索引为-1
        joint_offset: np.ndarray，形状为(M, 3)的numpy数组，包含着所有关节的偏移量

    Tips:
        joint_name顺序应该和bvh一致
    """
    bvh_data = BVHLoader(bvh_file_path)
    joint_name = bvh_data.get_joint_names()
    joint_parent = bvh_data.get_parents()
    joint_offset = bvh_data.get_offset()
    for idx, i in enumerate(zip(joint_name, joint_offset, joint_parent)):
        print(idx, i)
    return joint_name, joint_parent, joint_offset


def part2_forward_kinematics(joint_name, joint_parent, joint_offset, motion_data, frame_id):
    """请填写以下内容
    输入: part1 获得的关节名字，父节点列表，偏移量列表
        motion_data: np.ndarray，形状为(N,X)的numpy数组，其中N为帧数，X为Channel数
        frame_id: int，需要返回的帧的索引
    输出:
        joint_positions: np.ndarray，形状为(M, 3)的numpy数组，包含着所有关节的全局位置
        joint_orientations: np.ndarray，形状为(M, 4)的numpy数组，包含着所有关节的全局旋转(四元数)
    Tips:
        1. joint_orientations的四元数顺序为(x, y, z, w)
        2. from_euler时注意使用大写的XYZ
    """
    assert(frame_id < motion_data.shape[0])
    frame_motion_data = motion_data[frame_id].reshape(-1, 3)
    quats = R.from_euler('XYZ', frame_motion_data[1:], degrees=True).as_quat()

    # 0. 根节点可以先设置
    joint_positions = [frame_motion_data[0]]
    joint_orientations = [quats[0]]
    quat_index = 1

    for idx, name in enumerate(joint_name):
        if name.endswith("_end"):
            quats = np.insert(quats, idx, [0,0,0,1], axis=0)

    # 1. 计算每个节点的orientation和position
    for i in range(1, len(joint_parent)):
        parent_Q = R.from_quat(joint_orientations[joint_parent[i]])
        # 计算节点Q与r
        rotation = parent_Q * R.from_quat(quats[i])
        joint_orientations.append(rotation.as_quat())
        joint_positions.append(joint_positions[joint_parent[i]] + parent_Q.apply(joint_offset[i]))

    joint_positions, joint_orientations = np.array(joint_positions), np.array(joint_orientations)
    return joint_positions, joint_orientations


def part3_retarget_func(T_pose_bvh_path, A_pose_bvh_path):
    """
    将 A-pose的bvh重定向到T-pose上
    输入: 两个bvh文件的路径
    输出:
        motion_data: np.ndarray，形状为(N,X)的numpy数组，其中N为帧数，X为Channel数。retarget后的运动数据
    Tips:
        两个bvh的joint name顺序可能不一致哦(
        as_euler时也需要大写的XYZ
    """
    motion_data = None
    return motion_data
