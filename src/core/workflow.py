import pyautogui
import time
import numpy as np
from clients import openrouter_client, closeai_client, gemini_client
import base64
from google.genai import types
TERMINAL_REGION = (1423,788,2530,1500)
CURSOR_REGION = (450,50,970,1180)

def enter_wait_mode():
  """进入等待模式，等待cursor完成任务"""
  while (True):
    print("waiting for cursor to finish the task...")
    time.sleep(30)
    img_pre=pyautogui.screenshot(f'statics/img_{time.time()}.png',region=CURSOR_REGION)
    time.sleep(3)
    img_next=pyautogui.screenshot(f'statics/img_{time.time()}.png',region=CURSOR_REGION)
    image1 = np.array(img_pre)
    image2 = np.array(img_next)
    diff = np.abs(image1 - image2)
    diff = diff.mean()
    if diff < 10:
      # 如果diff小于10，则认为cursor已经完成任务,跳出循环
      print("cursor has finished the task")
      break
    else:
      print("cursor is still generating code, please wait...")
      time.sleep(30)
def generate_init_prompt(user_input: str):
  """将用户输入转化为cursor友好的prompt"""
  system_prompt = """Here are several rules you must follow:
  1.Do not interact with humans while performing your task.
  2.After each round of task completion, summarize your progress in a paragraph. Note: Do not create a new file, just place this summary in the dialog box.
  3.After each round of task completion, provide a test script (usually by running a file: python file_path). Only display the script, do not engage in human-computer interaction.
  """
  user_prompt = f"""User input: {user_input}"""

  return system_prompt+user_prompt


def generate_refine_prompt(user_input: str,refine_advice: str):
  """在循环中，根据cursor的输出， refine prompt"""
  return user_input+refine_advice

def init_request(prompt: str):
  """第一次对cursor发起请求
  工作流程：
  1.点击右上角最小化按钮，切换到待测项目空间
  2.移动鼠标指针到输入框，输入prompt
  3.点击发送按钮，发送prompt
  
  """
  # 点击右上角最小化按钮，切换到待测项目空间
  pyautogui.click(2390,20,duration=1)
  time.sleep(3)
  # 移动鼠标指针到输入框，输入prompt
  pyautogui.click(1000,150,duration=1)
  time.sleep(3)
  # 输入prompt
  pyautogui.typewrite(prompt,interval=0.1)
  time.sleep(3)
  # 点击发送按钮，发送prompt
  pyautogui.click(1378,254,duration=1)
  time.sleep(3)


def request_in_the_loop(prompt: str):
  """在循环中，对cursor发起请求"""
  pass


def extract_unit_test_script():
  """从cursor的输出中提取单元测试脚本"""
  file_path = f'statics/img_{time.time()}.png'
  pyautogui.screenshot(file_path,region=CURSOR_REGION)
  with open(file_path, 'rb') as f:
    b64_image = base64.b64encode(f.read()).decode("utf-8")
  prompt = f'''Extract the unit test script from the screenshot.
  Common unit test scripts are usually by running a file like this: python file_path.py
  Return only the script.
  '''
  config = types.GenerateContentConfig(
  response_mime_type="application/json"
  )
  response = gemini_client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
      types.Part.from_bytes(
        data=b64_image,
        mime_type='image/png',
      ),
      prompt
    ],
    config=config
  )
  return response.text
def extract_cursor_output():
  """提取cursor的输出,主要提取总结信息"""
  file_path = f'statics/img_{time.time()}.png'
  pyautogui.screenshot(file_path,region=CURSOR_REGION)
  with open(file_path, 'rb') as f:
    b64_image = base64.b64encode(f.read()).decode("utf-8")
  prompt = f'''Extract the cursor summary information from the screenshot.
  Return only the summary information, and do not include any other information.
  '''
  config = types.GenerateContentConfig(
  response_mime_type="application/json"
  )
  response = gemini_client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
      types.Part.from_bytes(
        data=b64_image,
        mime_type='image/png',
      ),
      prompt
    ],
    config=config
  )
  return response.text
def extract_terminal_info():
  """提取终端的信息
  工作流程：
  1.移动鼠标指针到终端界面右下角
  2.持续点击鼠标左键，滑动到终端左上角，选中全部信息，松开鼠标
  3.键盘输入：ctrl+c，复制全部信息
  """
  pass

def generate_refine_advice(cursor_main_output: str,terminal_info: str):
  """生成"continue/stop"和改良建议"""
  pass
def conduct_unit_test(unit_test_script: str):
  """在终端进行单元测试
  工作流程：
  1.鼠标移动到terminal界面并单击
  2.输入单元测试脚本
  3.按回车键执行
  """