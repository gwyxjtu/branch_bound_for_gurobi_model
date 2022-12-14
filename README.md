# 分支定界法求解MIP问题


## 算法思想

分支定界法是本科运筹学课程中学习的求解整数规划的算法之一，分支定界算法的核心思想就是分枝和剪枝。当我们不考虑所求解必须是整数这个条件时，用单纯形法可求出最优解，但是这个解往往不全是整数，因此我们采用剪枝的方式一点一点缩小范围，直到所求解为整数解。

+ 分枝定界法是一种基于“树”结构的搜索或遍历方法
+ 分枝定界法中的整数性判断不会在本质上引起数值困难
+ 定界是为了避免无效的分枝搜索，恰当的分枝有助于更好定界
+ 分枝定界法是部分枚举而不是穷举

## 使用方法

import class文件，输入gurobi建立好的模型和模型中的binary variable的name list即可。

具体可以参考 `test_branchbound.py`。
