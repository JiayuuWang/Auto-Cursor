import pyautogui
import time
import numpy as np
from .clients import openrouter_client, closeai_client, gemini_client
import base64
from google.genai import types
import json
import logging
TIMESTAMP_REGION = (340,160,80,20)
TERMINAL_REGION = (1450,850,1050,650)
CURSOR_REGION = (450,50,970,1180)

def enter_wait_mode():
  """进入等待模式，等待cursor完成任务"""
  while (True):
    logging.info("waiting for cursor to finish the task...")
    time.sleep(20)
    current_timestamp_patch=f'statics/img_{time.time()}.png'
    pyautogui.screenshot(current_timestamp_patch,region=TIMESTAMP_REGION)
    with open(current_timestamp_patch, 'rb') as f:
      b64_image1 = base64.b64encode(f.read()).decode("utf-8")
    prompt = f"Extract the text in this image.Return only the text, and do not include any other information."
    config = types.GenerateContentConfig(
    response_mime_type="application/json"
    )
    response = gemini_client.models.generate_content(
      model='gemini-2.5-flash',
      contents=[
        types.Part.from_bytes(
          data=b64_image1,
          mime_type='image/png',
        ),
        prompt
      ],
      config=config
    )
    text = response.text
    if "AM" in text or "PM" in text:
      logging.info("Cursor has finished the task")
      break
    else:
      logging.info("Cursor is still generating...")
def generate_init_prompt(user_input: str):
  logging.info("Generating initial prompt...")
  """将用户输入转化为cursor友好的prompt"""
  system_prompt = "Here are several rules you must follow: 1.Do not interact with humans while performing your task. 2.After each round of task completion, summarize your progress in a paragraph. Note: Do not create a new file, just place this summary in the dialog box. 3.After each round of task completion, provide a test script (usually by running a file: python file_path). Only display the script, do not engage in human-computer interaction. 4.The test result must only be in the form of printed output to the console."

  user_prompt = f"User input: {user_input}"

  return system_prompt+user_prompt


def generate_refine_prompt(user_input: str,refine_advice: str):
  """在循环中，根据cursor的输出， refine prompt"""
  prompt = f"Refine the user input based on the refine advice. User input at the start of this round: {user_input} Refine advice in this round: {refine_advice}Return only the refined user input, and do not include any other information."
  response=closeai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
  )
  return response.choices[0].message.content

def init_request(prompt: str):
  """第一次对cursor发起请求
  工作流程：
  1.点击右上角最小化按钮，切换到待测项目空间
  2.移动鼠标指针到输入框，输入prompt
  3.键盘敲击enter,发送prompt
  
  """
  logging.info("Initiating request...")
  # 点击右上角最小化按钮，切换到待测项目空间
  # pyautogui.click(2390,20,duration=1)
  time.sleep(3)
  # 移动鼠标指针到输入框，输入prompt
  logging.info(f"Moving mouse to position (1000, 150) and clicking")
  pyautogui.click(1000,120,duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(3)
  # 输入prompt
  logging.info(f"Typing prompt: {prompt[:50]}..." if len(prompt) > 50 else f"Typing prompt: {prompt}")
  pyautogui.typewrite(prompt,interval=0.1)
  time.sleep(3)
  # 点击发送按钮，发送prompt
  logging.info("Pressing 'enter' key to send prompt")
  pyautogui.press("enter")
  time.sleep(3)
  logging.info("Request sent successfully")

def request_in_the_loop(prompt: str):
  """在循环中，对cursor发起请求
  工作流程：
  1.把控制台信息粘贴到输入框
  2.把prompt输入到输入框
  3.点击发送按钮
  """
  logging.info("Starting request in the loop...")
  # 复制控制台信息
  copy_terminal_info()
  # 移动鼠标指针到聊天框输入框
  logging.info(f"Moving mouse to position (1300, 1400) and clicking")
  pyautogui.click(1300,1400,duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(3)
  # 输出请求前缀
  logging.info("Typing prefix: 'This is the result of the test scripts in the terminal: '")
  pyautogui.typewrite("This is the result of the test scripts in the terminal: ",interval=0.1)
  time.sleep(1)
  # 粘贴信息
  logging.info("Pressing 'Ctrl+V' to paste terminal info")
  pyautogui.hotkey("ctrl", "v")
  time.sleep(3)
  logging.info("Pasted the copied text to the chat")
  # 输入prompt
  logging.info(f"Typing refined prompt: {prompt[:50]}..." if len(prompt) > 50 else f"Typing refined prompt: {prompt}")
  pyautogui.typewrite(prompt,interval=0.1)
  time.sleep(3)
  # 键盘敲击enter,发送prompt
  logging.info("Pressing 'enter' key to send prompt")
  pyautogui.press("enter")
  time.sleep(3)
  logging.info("Request in the loop completed")


def extract_unit_test_script():
  """从cursor的输出中提取单元测试脚本"""
  logging.info("Extracting unit test script...")
  file_path = f'statics/img_{time.time()}.png'
  logging.info(f"Taking screenshot of CURSOR_REGION {CURSOR_REGION} and saving to {file_path}")
  pyautogui.screenshot(file_path,region=CURSOR_REGION)
  with open(file_path, 'rb') as f:
    b64_image = base64.b64encode(f.read()).decode("utf-8")
  prompt = f"Extract the unit test script from the screenshot. Common unit test scripts are usually by running a file like this: python file_path.py. Return only the script without quotation marks."
  logging.info("Sending screenshot to Gemini for unit test script extraction")
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
  extracted_script = response.text.strip()
  logging.info(f"Successfully extracted unit test script: {extracted_script}")
  return extracted_script
def extract_cursor_output():
  """提取cursor的输出,主要提取总结信息"""
  logging.info("Extracting cursor output...")
  file_path = f'statics/img_{time.time()}.png'
  logging.info(f"Taking screenshot of CURSOR_REGION {CURSOR_REGION} and saving to {file_path}")
  pyautogui.screenshot(file_path,region=CURSOR_REGION)
  with open(file_path, 'rb') as f:
    b64_image = base64.b64encode(f.read()).decode("utf-8")
  prompt = f"Extract the cursor summary information from the screenshot. Return only the summary information, and do not include any other information."
  logging.info("Sending screenshot to Gemini for cursor output extraction")
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
  logging.info("Successfully extracted cursor output")
  return response.text

def copy_terminal_info():
  """复制终端的信息
  工作流程：
  1.移动鼠标指针到终端界面右下角
  2.持续点击鼠标左键，滑动到终端左上角，选中全部信息，松开鼠标
  3.双击右键
  4.选择"复制"
  """
  logging.info("Copying terminal info...")
  # 移动鼠标指针到终端界面右下角
  bottom_right_x = TERMINAL_REGION[0]+TERMINAL_REGION[2]
  bottom_right_y = TERMINAL_REGION[1]+TERMINAL_REGION[3]
  logging.info(f"Moving mouse to terminal bottom-right corner ({bottom_right_x}, {bottom_right_y}) and clicking")
  pyautogui.click(bottom_right_x, bottom_right_y, duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(3)
  # 持续点击鼠标左键，滑动到终端左上角，选中全部信息，松开鼠标
  top_left_x = TERMINAL_REGION[0]
  top_left_y = TERMINAL_REGION[1]
  logging.info(f"Dragging mouse from ({bottom_right_x}, {bottom_right_y}) to terminal top-left corner ({top_left_x}, {top_left_y})")
  pyautogui.dragTo(top_left_x, top_left_y, duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position after drag: {current_pos}")
  time.sleep(3)
  # 双击右键
  right_click_x = TERMINAL_REGION[0]+200
  right_click_y = TERMINAL_REGION[1]+200
  logging.info(f"Double right-clicking at position ({right_click_x}, {right_click_y})")
  pyautogui.doubleClick(right_click_x, right_click_y, duration=1, button='right')
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(3)
  # 选择"复制"
  copy_option_x = TERMINAL_REGION[0]+200+100
  copy_option_y = TERMINAL_REGION[1]+200+165
  logging.info(f"Clicking 'Copy' option at position ({copy_option_x}, {copy_option_y})")
  pyautogui.click(copy_option_x, copy_option_y, duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(3)
  logging.info("Successfully copied terminal info to clipboard")



def extract_terminal_info():
  """提取终端的信息"""
  logging.info("Extracting terminal info...")
  file_path = f'statics/img_{time.time()}.png'
  pyautogui.screenshot(file_path,region=TERMINAL_REGION)
  with open(file_path, 'rb') as f:
    b64_image = base64.b64encode(f.read()).decode("utf-8")
  prompt = f"Extract the terminal information from the screenshot. Return only the terminal information, and do not include any other information."
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
  logging.info("Extracted terminal info")
  return response.text


def generate_refine_advice(user_input: str,cursor_main_output: str,terminal_info: str):
  """生成"continue/stop"和改良建议"""
  prompt = f"Generate 'continue/stop' and refine advice based on the user input, cursor main output, and terminal information. User input: {user_input} Cursor main output in this round: {cursor_main_output} Terminal information in this round: {terminal_info} Refine advice focuses on : what else I can do to make the project better. It should be a paragraph. Return your response in the following JSON format: {{ 'action': 'continue' or 'stop', 'advice': 'your detailed refine advice here' }}"
  logging.info("Generating refine advice...")
  responce=closeai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    response_format={"type": "json_object"}
  )
  result = json.loads(responce.choices[0].message.content)
  logging.info("Generated refine advice")
  return result["action"],result["advice"]
def conduct_unit_test(unit_test_script: str):
  """在终端进行单元测试
  工作流程：
  1.鼠标移动到terminal界面并单击
  2.输入单元测试脚本
  3.按回车键执行
  """
  logging.info(f"Conducting unit test with script: {unit_test_script}")
  terminal_click_x = TERMINAL_REGION[0]+TERMINAL_REGION[2]
  terminal_click_y = TERMINAL_REGION[1]+TERMINAL_REGION[3]
  logging.info(f"Moving mouse to terminal position ({terminal_click_x}, {terminal_click_y}) and clicking")
  pyautogui.click(terminal_click_x, terminal_click_y, duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(3)
  # 如果unit_test_script被引号包裹，则去掉引号
  if unit_test_script.startswith("\"") and unit_test_script.endswith("\""):
    unit_test_script = unit_test_script[1:-1]
    logging.info(f"Removed quotes from script, now: {unit_test_script}")
  logging.info(f"Typing unit test script: {unit_test_script}")
  pyautogui.typewrite(unit_test_script,interval=0.1)
  time.sleep(3)
  logging.info("Pressing 'enter' key to execute unit test script")
  pyautogui.press("enter")
  time.sleep(10)
  logging.info("Unit test execution completed")
  return f"conducted the unit test"






def workflow(user_input: str):
  """自我迭代地操控cursor，完成任务"""
  round_count = 1
  init_prompt = generate_init_prompt(user_input)
  init_request(init_prompt)
  while (True):
    if round_count > 5:
      break
    logging.info(f"Round {round_count} starts")
    round_count += 1
    # 进入等待模式，等待cursor完成任务
    enter_wait_mode()
    # cursor输出完毕，进行测试
    cursor_main_output = extract_cursor_output()
    unit_test_script = extract_unit_test_script()
    conduct_unit_test(unit_test_script)
    terminal_info=extract_terminal_info()
    # 决定是否继续循环
    action,refine_advice = generate_refine_advice(user_input,cursor_main_output,terminal_info)
    if action == "stop":
      break
    else:
      # 继续优化prompt，并重新请求cursor进行下一轮迭代
      prompt = generate_refine_prompt(user_input,refine_advice)
      request_in_the_loop(prompt)

  logging.info("Task completed")
  return "任务完成"


if __name__ == "__main__":
  time.sleep(5)
  copy_terminal_info()