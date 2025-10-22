from core.clients import openrouter_client, closeai_client
import time
from core.workflow import *
def workflow(user_input: str):
  """自我迭代地操控cursor，完成任务"""
  init_prompt = generate_init_prompt(user_input)
  init_request(init_prompt)
  while (True):
    # 进入等待模式，等待cursor完成任务
    enter_wait_mode()
    # cursor输出完毕，进行测试
    cursor_main_output = extract_cursor_output()
    unit_test_script = extract_unit_test_script()
    conduct_unit_test(unit_test_script)
    terminal_info=extract_terminal_info()
    # 决定是否继续循环
    continue_flag,refine_advice = generate_refine_advice(cursor_main_output,terminal_info)
    if continue_flag == False:
      break
    # 继续优化prompt，并重新请求cursor进行下一轮迭代
    prompt = generate_refine_prompt(user_input,refine_advice)
    request_in_the_loop(prompt)
  return "任务完成"

def test_1():
  user_input = "I want to build a simple game of tic tac toe in python."
  init_prompt = generate_init_prompt(user_input)
  init_request(init_prompt)

if __name__ == "__main__":
  test_1()

