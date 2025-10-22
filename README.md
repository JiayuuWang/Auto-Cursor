# 基于图形用户界面（GUI）的 cursor manipulator

## 其功能是：

通过操作图形界面，操控cursor,并可实现自我迭代,完成一个真实项目

## 具体操作过程是：

1. 发送初始prompt给cursor
2. 等待cursor完成任务
3. 根据cursor的输出，判断是否需要继续迭代
4. 如果需要继续迭代，则发送新的prompt
5. 如果不需要继续迭代，则结束