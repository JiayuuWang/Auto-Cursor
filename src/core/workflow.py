import pyautogui
import time
from .clients import closeai_client, gemini_client
import base64
from google.genai import types
import json
import logging
from .constants import TIMESTAMP_REGION, TERMINAL_REGION, CURSOR_REGION, Prompts
def enter_wait_mode():
  """Enter wait mode, waiting for Cursor to complete the task"""
  while (True):
    logging.info("waiting for cursor to finish the task...")
    time.sleep(20)
    current_timestamp_patch=f'statics/img_{time.time()}.png'
    pyautogui.screenshot(current_timestamp_patch,region=TIMESTAMP_REGION)
    with open(current_timestamp_patch, 'rb') as f:
      b64_image1 = base64.b64encode(f.read()).decode("utf-8")
    prompt = Prompts.EXTRACT_TIMESTAMP
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
  """Convert user input into Cursor-friendly prompt"""
  system_prompt = Prompts.SYSTEM_PROMPT

  api_config_prompt = Prompts.api_config_template()

  print(api_config_prompt)

  user_prompt = f"User input: {user_input}"

  return system_prompt+user_prompt+api_config_prompt


def generate_refine_prompt(user_input: str,refine_advice: str):
  """In the loop, refine prompt based on Cursor's output"""
  prompt = Prompts.refine_prompt_template(user_input, refine_advice)
  response=closeai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
  )
  return response.choices[0].message.content

def init_request(prompt: str):
  """Make the first request to Cursor
  Workflow:
  1. Click the minimize button in the top-right corner to switch to the test project workspace
  2. Move mouse pointer to input box and type the prompt
  3. Press enter to send the prompt
  
  """
  logging.info("Initiating request...")
  # Click the minimize button in the top-right corner to switch to the test project workspace
  # pyautogui.click(2390,20,duration=1)
  time.sleep(3)
  # Move mouse pointer to input box and type the prompt
  logging.info(f"Moving mouse to position (1000, 150) and clicking")
  pyautogui.click(1000,120,duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(3)
  # Type the prompt
  logging.info(f"Typing prompt: {prompt[:50]}..." if len(prompt) > 50 else f"Typing prompt: {prompt}")
  pyautogui.typewrite(prompt,interval=0.1)
  time.sleep(3)
  # Press send button to send the prompt
  logging.info("Pressing 'enter' key to send prompt")
  pyautogui.press("enter")
  time.sleep(3)
  logging.info("Request sent successfully")

def request_in_the_loop(prompt: str):
  """Make request to Cursor in the loop
  Workflow:
  1. Paste console information to input box
  2. Type prompt to input box
  3. Click send button
  """
  logging.info("Starting request in the loop...")
  # Copy console information
  copy_terminal_info()
  # Move mouse pointer to chat input box
  logging.info(f"Moving mouse to position (1300, 1400) and clicking")
  pyautogui.click(1300,1400,duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(3)
  # Output request prefix
  logging.info(f"Typing prefix: '{Prompts.TEST_RESULT_PREFIX}'")
  pyautogui.typewrite(Prompts.TEST_RESULT_PREFIX,interval=0.1)
  time.sleep(1)
  # Paste information
  logging.info("Pressing 'Ctrl+V' to paste terminal info")
  pyautogui.hotkey("ctrl", "v")
  time.sleep(3)
  logging.info("Pasted the copied text to the chat")
  # Type the prompt
  logging.info(f"Typing refined prompt: {prompt[:50]}..." if len(prompt) > 50 else f"Typing refined prompt: {prompt}")
  pyautogui.typewrite(prompt,interval=0.1)
  time.sleep(3)
  # Press enter to send the prompt
  logging.info("Pressing 'enter' key to send prompt")
  pyautogui.press("enter")
  time.sleep(3)
  logging.info("Request in the loop completed")


def extract_unit_test_script():
  """Extract unit test script from Cursor's output"""
  logging.info("Extracting unit test script...")
  file_path = f'statics/img_{time.time()}.png'
  logging.info(f"Taking screenshot of CURSOR_REGION {CURSOR_REGION} and saving to {file_path}")
  pyautogui.screenshot(file_path,region=CURSOR_REGION)
  with open(file_path, 'rb') as f:
    b64_image = base64.b64encode(f.read()).decode("utf-8")
  prompt = Prompts.EXTRACT_UNIT_TEST
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
  """Extract Cursor's output, mainly extract summary information"""
  logging.info("Extracting cursor output...")
  file_path = f'statics/img_{time.time()}.png'
  logging.info(f"Taking screenshot of CURSOR_REGION {CURSOR_REGION} and saving to {file_path}")
  pyautogui.screenshot(file_path,region=CURSOR_REGION)
  with open(file_path, 'rb') as f:
    b64_image = base64.b64encode(f.read()).decode("utf-8")
  prompt = Prompts.EXTRACT_CURSOR_OUTPUT
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
  """Copy terminal information
  Workflow:
  1. Move mouse pointer to bottom-right corner of terminal
  2. Click and hold left mouse button, drag to top-left corner of terminal to select all, release mouse
  3. Double right-click
  4. Select "Copy"
  """
  logging.info("Copying terminal info...")
  # Move mouse pointer to bottom-right corner of terminal
  bottom_right_x = TERMINAL_REGION[0]+TERMINAL_REGION[2]
  bottom_right_y = TERMINAL_REGION[1]+TERMINAL_REGION[3]
  logging.info(f"Moving mouse to terminal bottom-right corner ({bottom_right_x}, {bottom_right_y}) and clicking")
  pyautogui.click(bottom_right_x, bottom_right_y, duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(3)
  # Click and hold left mouse button, drag to top-left corner to select all, release mouse
  top_left_x = TERMINAL_REGION[0]
  top_left_y = TERMINAL_REGION[1]
  logging.info(f"Dragging mouse from ({bottom_right_x}, {bottom_right_y}) to terminal top-left corner ({top_left_x}, {top_left_y})")
  pyautogui.dragTo(top_left_x, top_left_y, duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position after drag: {current_pos}")
  time.sleep(3)
  # Double right-click
  right_click_x = TERMINAL_REGION[0]+200
  right_click_y = TERMINAL_REGION[1]+200
  logging.info(f"Double right-clicking at position ({right_click_x}, {right_click_y})")
  pyautogui.doubleClick(right_click_x, right_click_y, duration=1, button='right')
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(3)
  # Select "Copy"
  copy_option_x = TERMINAL_REGION[0]+200+100
  copy_option_y = TERMINAL_REGION[1]+200+165
  logging.info(f"Clicking 'Copy' option at position ({copy_option_x}, {copy_option_y})")
  pyautogui.click(copy_option_x, copy_option_y, duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(3)
  logging.info("Successfully copied terminal info to clipboard")



def extract_terminal_info():
  """Extract terminal information"""
  logging.info("Extracting terminal info...")
  file_path = f'statics/img_{time.time()}.png'
  pyautogui.screenshot(file_path,region=TERMINAL_REGION)
  with open(file_path, 'rb') as f:
    b64_image = base64.b64encode(f.read()).decode("utf-8")
  prompt = Prompts.EXTRACT_TERMINAL_INFO
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
  """Generate 'continue/stop' and refine advice"""
  prompt = Prompts.generate_refine_advice_template(user_input, cursor_main_output, terminal_info)
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
  """Conduct unit test in terminal
  Workflow:
  1. Move mouse to terminal interface and click
  2. Press ctrl+c
  3. Type unit test script
  4. Press enter to execute
  """
  logging.info(f"Conducting unit test with script: {unit_test_script}")
  terminal_click_x = TERMINAL_REGION[0]+TERMINAL_REGION[2]
  terminal_click_y = TERMINAL_REGION[1]+TERMINAL_REGION[3]
  logging.info(f"Moving mouse to terminal position ({terminal_click_x}, {terminal_click_y}) and clicking")
  pyautogui.click(terminal_click_x, terminal_click_y, duration=1)
  current_pos = pyautogui.position()
  logging.info(f"Current mouse position: {current_pos}")
  time.sleep(1)
  # Press ctrl+c
  logging.info("Pressing 'ctrl+c' to refresh terminal")
  pyautogui.hotkey("ctrl", "c")
  time.sleep(1)
  # If unit_test_script is wrapped in quotes, remove them
  if unit_test_script.startswith("\"") and unit_test_script.endswith("\""):
    unit_test_script = unit_test_script[1:-1]
    logging.info(f"Removed quotes from script, now: {unit_test_script}")
  logging.info(f"Typing unit test script: {unit_test_script}")
  pyautogui.typewrite(unit_test_script,interval=0.1)
  time.sleep(3)
  logging.info("Pressing 'enter' key to execute unit test script")
  pyautogui.press("enter")
  time.sleep(60)
  logging.info("Unit test execution completed")
  return f"conducted the unit test"






def workflow(user_input: str):
  """Self-iteratively control Cursor to complete tasks"""
  round_count = 1
  init_prompt = generate_init_prompt(user_input)
  init_request(init_prompt)
  while (True):
    if round_count > 5:
      break
    logging.info(f"Round {round_count} starts")
    round_count += 1
    # Enter wait mode, waiting for Cursor to complete the task
    enter_wait_mode()
    # Cursor output completed, conduct testing
    cursor_main_output = extract_cursor_output()
    unit_test_script = extract_unit_test_script()
    conduct_unit_test(unit_test_script)
    terminal_info=extract_terminal_info()
    # Decide whether to continue the loop
    action,refine_advice = generate_refine_advice(user_input,cursor_main_output,terminal_info)
    if action == "stop":
      break
    else:
      # Continue to optimize prompt and request Cursor for the next iteration
      prompt = generate_refine_prompt(user_input,refine_advice)
      request_in_the_loop(prompt)

  logging.info("Task completed")
  return "Task completed"

