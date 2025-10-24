import argparse
import sys
import time
import logging
import pyautogui
from src.core.workflow import workflow


def main():
  """命令行入口函数"""
  parser = argparse.ArgumentParser(
    description="自动化Cursor工作流 - 自我迭代地操控Cursor完成任务",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
示例:
  python main.py --input "I want to build a game of tic tac toe in python."
  python main.py -i "Create a web scraper for news articles"
  python main.py --input "Build a calculator app" --delay 3
  python main.py -i "Build a todo app" -d 3 -r 10
    """
  )
  
  parser.add_argument(
    '-i', '--input',
    type=str,
    required=True,
    help='用户输入的任务描述 (必需)'
  )
  
  parser.add_argument(
    '-d', '--delay',
    type=int,
    default=5,
    help='启动前的延迟时间(秒), 默认为5秒'
  )
  
  parser.add_argument(
    '-r', '--max-rounds',
    type=int,
    default=5,
    help='最大迭代轮数, 默认为5轮'
  )
  
  args = parser.parse_args()
  
  # 配置日志
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
      logging.FileHandler('workflow.log', encoding='utf-8'),
      logging.StreamHandler(sys.stdout)
    ]
  )
  
  logging.info("="*60)
  logging.info("Auto-Cursor Workflow 启动")
  logging.info(f"用户输入: {args.input}")
  logging.info(f"启动延迟: {args.delay}秒")
  logging.info(f"最大轮数: {args.max_rounds}轮")
  logging.info("="*60)
  
  # 启动延迟
  if args.delay > 0:
    logging.info(f"等待 {args.delay} 秒后开始...")
    time.sleep(args.delay)
  
  # 执行工作流
  result = workflow(args.input)
  
  logging.info("="*60)
  logging.info(f"工作流结束: {result}")
  logging.info("="*60)
  
  # 将鼠标移动到安全位置
  pyautogui.moveTo(20, 20)

if __name__ == "__main__":
  main()