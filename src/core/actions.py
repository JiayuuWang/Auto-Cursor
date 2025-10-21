from clients import openrouter_client
import base64
import time
import pyautogui
import re




def click(click_object: str, extra_desc: str = None):
    """Find the object in the screenshot and click it"""
    # 1. 获取桌面原始大小
    width, height = pyautogui.size()
    # 2. 截取桌面截图
    screenshot = pyautogui.screenshot()
    # 3. 保存截图
    filename = f"screenShot_{time.time()}.png"
    screenshot.save(f"outputs/screenshots/{filename}")

    prompt = f'where is the {click_object}? The additional description about this objectis {extra_desc}. Return only one position in format of (x,y).'
    with open(f"outputs/screenshots/{filename}", 'rb') as f:
      b64_image = base64.b64encode(f.read()).decode("utf-8")

    # 4. 使用UI-TARS-1.5-7b识别截图中的浏览器图标
    completion = openrouter_client.chat.completions.create(
    extra_body={},
    model="bytedance/ui-tars-1.5-7b",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/png;base64,{b64_image}"
            }
          }
        ]
      }
    ]
    )
    result = completion.choices[0].message.content
    # 5. 用正则表达式解析位置信息："(x,y)"
    position = re.search(r'\((\d+),(\d+)\)', result)
    x=int(position.group(1))
    y=int(position.group(2))
    print("position:", x, y)
    # 6. 根据模型识别结果，点击浏览器图标
    pyautogui.moveTo(x, y,duration=1)
    pyautogui.click(x, y)
    return f"clicked the {click_object} at position ({x}, {y})"
def press_enter():
  """
  Press the enter key. Normally used after you have typed your input and want to submit it.
  """
  pyautogui.press("enter")
  return f"pressed the enter key"
def typing(text:str):
  """
  Type the text into the input field
  """
  pyautogui.typewrite(text,interval=0.1)
  return f"typed the text: {text}"
def press_key(key:str):
  """
  Press the key
  """
  pyautogui.press(key)
  return f"pressed the key: {key}"

def hot_key_copy():
  """
  Copy the selected text
  """
  pyautogui.hotkey("ctrl", "c")
  return f"copied the selected text"

  
def hot_key_paste():
  """
  Paste the copied text
  """
  pyautogui.hotkey("ctrl", "v")
  return f"pasted the copied text"



def hot_key_select_all():
  """
  Select all the text
  """
  pyautogui.hotkey("ctrl", "a")
  return f"selected all the text"
def describe_screenshot():
  """Describe the screenshot"""
  screenshot_path=f"outputs/screenshots/screenShot_{time.time()}.png"
  pyautogui.screenshot(screenshot_path)
  with open(screenshot_path, "rb") as image_file:
    b64_image = base64.b64encode(image_file.read()).decode("utf-8")
    prompt = f"""Describe this screenshot. Mainly focus on current focused window and current mouse cursor position.
    """
  completion = openrouter_client.chat.completions.create(
    extra_body={},
    model="bytedance/ui-tars-1.5-7b",
    messages=[
      {"role": "user", "content": [{"type": "text", "text": prompt},
      {"type": "image_url", "image_url": {
        "url": f"data:image/png;base64,{b64_image}"
      }}]},
    ]
  )
  return completion.choices[0].message.content