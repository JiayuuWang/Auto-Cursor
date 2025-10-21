from core.actions import openrouter_client, closeai_client



def workflow_1():
  """
  1. 打开浏览器
  2. 进入google ai studio官网
  3. 登录google ai studio官网
  4. 选择模型类型
  5. 在输入框中输入query
  6. 点击运行按钮
  7. 等待片刻，获取模型推理结果
  8. 关闭浏览器
  """
  history=""
  user_query=""
  task_guidelines="""
  任务总览：
  1. 打开浏览器
  2. 进入google ai studio官网（https://aistudio.google.com/）
  3. 登录google ai studio官网(如果需要登录的话)
  4. 在输入框中输入user_query
  5. 点击运行按钮
  6. 等待片刻，获取模型推理结果
  7. 将结果粘贴会本地
  """
  