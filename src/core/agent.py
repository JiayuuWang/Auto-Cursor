import pyautogui
from clients import openrouter_client, closeai_client
from actions import click, describe_screenshot, typing, hot_key_copy, hot_key_paste, hot_key_select_all, press_enter
from actions import press_key
import json
import time
import base64
class Agent:
    def __init__(self, agent_name:str,model: str = "gpt-5",user_input: str = None,system_prompt: str = None):
        self.agent_name = agent_name
        self.model = model
        self.user_input = user_input
        self.system_prompt = system_prompt
        self.messages = []
        self.tools = []
    

    def delete_screenshot_info_message(self):
        """将已经使用过的截图base64编码信息从消息历史中删除，节省上下文空间"""
        for message in self.messages:
            if "data:image/png;base64:" in str(message):
                self.messages.remove(message)
                return

    
    def _execute_tool(self, tool_name: str, arguments: dict):
        """执行指定名称的工具函数，传入相应的参数
        
        通过反射机制动态获取函数对象，无需手动维护映射字典
        """
        try:
            # 尝试从 globals() 中获取函数对象
            tool_function = globals().get(tool_name)
            
            # 检查是否找到了函数且是可调用的
            if tool_function is None or not callable(tool_function):
                return f"Error: Tool '{tool_name}' not found or not callable"
            
            # 执行函数并返回结果
            result = tool_function(**arguments)
            return result
        except TypeError as e:
            # 参数错误（例如缺少必需参数或参数类型不匹配）
            return f"Error: Invalid arguments for {tool_name}: {str(e)}"
        except Exception as e:
            # 其他执行错误
            return f"Error executing {tool_name}: {str(e)}"

    def add_tool(self, tool: dict):
        self.tools.append(tool)
    
    def run(self, max_iterations: int = 10):
        self.messages.append({"role": "system", "content": self.system_prompt})
        self.messages.append({"role": "user", "content": self.user_input})
        
        for iteration in range(max_iterations):
            print(f"\n=== iteration {iteration + 1} ===")
            if iteration>0:
                # # 判断cursor是否已经生成完毕
                # screenshot_path_pre=f"outputs/screenshots/screenShot_{time.time()}.png"
                # screenshot_path_next=f"outputs/screenshots/screenShot_{time.time()}.png"
                # pyautogui.screenshot(screenshot_path_pre)
                # time.sleep(3)
                # pyautogui.screenshot(screenshot_path_next)
                # if screenshot_path_pre == screenshot_path_next:
                #     print("cursor is still generating code, please wait...")
                #     time.sleep(30)
                #     continue
                pass

            screenshot_path=f"outputs/screenshots/screenShot_{time.time()}.png"
            time.sleep(1)
            current_screenshot=pyautogui.screenshot()
            current_screenshot.save(screenshot_path)
            with open(screenshot_path, "rb") as image_file:
                b64_image = base64.b64encode(image_file.read()).decode("utf-8")
            message={
                "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """This is current screenshot. You should analyze this screenshot, look at previous messages and the original user input to determine what to do next. Return your thought in this format:
                            1. What progress have I made so far?
                            2. What's the current situation? Summarize in a short sentence.
                            3. What's the next ONE step? Return in a short sentence.
                            """
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{b64_image}"
                            }
                        }
                    ]
                }
            self.messages.append(message)
            
            response = closeai_client.chat.completions.create(
                model=self.model,
                messages=self.messages, 
            )

            self.delete_screenshot_info_message()
            thinking_message = response.choices[0].message
            print("thought:", thinking_message.content)
            self.messages.append(thinking_message)

            response = closeai_client.chat.completions.create(
                model=self.model,
                messages= [{"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.user_input},
                {"role": "assistant", "content": thinking_message.content},
                ], 
                tools=self.tools,
                tool_choice="auto"
            )
            tool_message = response.choices[0].message
            # 如果没有工具调用，说明任务完成
            if not tool_message.tool_calls:
                print("Mission completed:", tool_message.content)
                return tool_message.content
            
            # 将包含 tool_calls 的 assistant 消息添加到历史记录
            self.messages.append(tool_message)
            
            # 执行工具调用
            for tool_call in tool_message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                print(f"action: call {tool_name}, arguments: {arguments}")
                
                # 执行工具
                tool_result = self._execute_tool(tool_name, arguments)
            

                tool_result = f"{tool_result}"
                
                print(f"observe: {tool_result}")
                
                # 添加工具结果到消息历史
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                })
        
        return "reach the maximum number of iterations, the task may not be completed",self.messages









if __name__ == "__main__":
  pyautogui.click(2390,20)
  time.sleep(3)
  system_prompt = """You are a helpful assistant that can use tools to complete tasks by observing the screen and taking actions.
  Here is some experience :
  - 1. When you have already opened a browser, you need to find the search box(almost in the center of the screen) and search for the target website.
  - 2. When you finish typing your query, you need to press the enter key or click the search button to submit your query.
  
  """
  user_input = "Open a browser(like edge), search 'google ai studio' and enter its official website(normally the first result). Then create a new chat and send a message: 'Hello, how are you?' to ai model"
  agent_1= Agent(agent_name="agent_1",system_prompt=system_prompt,user_input=user_input)
  agent_1.add_tool(
     {
        "type": "function",
        "function": {
            "name": "click",
            "description": "Find the specified object and click it",
            "parameters": {
                "type": "object",
                "properties": {
                    "click_object": {
                        "type": "string",
                        "description": "The description of the object to click, such as 'submit button', 'search box' etc."
                    },
                    "extra_desc": {
                        "type": "string",
                        "description": "Additional description information, helping to more accurately locate the object"
                    }
                },
                "required": ["click_object"]
            }
        }
    })
  agent_1.add_tool({
        "type": "function",
        "function": {
            "name": "typing",
            "description": "Type(keyboard input) text at the current position. Normally used when you want to input text into a text box or a search box.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to type"
                    }
                },
                "required": ["text"]
            }
        }
    })
  agent_1.add_tool({
        "type": "function",
        "function": {
            "name": "press_enter",
            "description": "Press the enter key. Normally used after you have typed your input and want to submit it.",
            "parameters": {}
        }
    })
  agent_1.add_tool({
        "type": "function",
        "function": {
            "name": "press_key",
            "description": "Press the specified key",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "The key to press, such as 'enter' etc."
                    }
                },
                "required": ["key"]
            }
        }
    })


#   system_prompt = """You are a cursor(An ai coding IDE) manipulator. You are given a idea to complete. You need to use cursor to build this from scratch. What you can do are:
#   1. You can input your instruction to cursor in the input box of cursor in the right side of the screen.
#   2. You can click "send" button(a white button with an arrow icon below the input box) to send your instruction to cursor.
#   3. You follow cursor's response click "accept" or "run" to continue the task.
#   The possible workflow is:
#   1. Polish user's input and type it into the input box of cursor and submit.
#   2. If cursor is generating code, you need to **wait** for it to finish. Don't send another instruction until it's finished.
#   3. Follow cursor's response click "accept" or "run" button to continue the task.
#   4. Once the task is completed, you should run the project to see if it's working.
#   """
#   user_input = """I wang to use cursor to build a simple game of tic tac toe in python."""
  try:
    result,messages = agent_1.run(max_iterations=20)
    print(result)
    print(messages)
  except Exception as e:
    pyautogui.click(1875,1565)
    print(e)
  pyautogui.click(1875,1565)