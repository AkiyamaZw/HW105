# 知识点
## lab1
* 理清Orientation/Rotation, Position/Transition(Offset)在算法描述中的区别。
* BVH读取时，保证父节点的下标序号一定位于子节点前。
* 计算节点Orientation的公式
  $$
  Q_0 = R_0,
  Q_i = Q_{i-1} * R_i
  $$

* 计算节点Position的公式
  $$P_i = P_{i-1} + Q_{i-1}l_i$$

