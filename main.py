import argparse
import sys
import time
import logging
import pyautogui
from src.core.workflow import workflow


def main():
  """Command-line entry point function"""
  parser = argparse.ArgumentParser(
    description="Automated Cursor Workflow - Self-iteratively control Cursor to complete tasks",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
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
    help='User input task description (required)'
  )
  
  parser.add_argument(
    '-d', '--delay',
    type=int,
    default=5,
    help='Delay time before startup (seconds), default is 5 seconds'
  )
  
  parser.add_argument(
    '-r', '--max-rounds',
    type=int,
    default=5,
    help='Maximum iteration rounds, default is 5 rounds'
  )
  
  args = parser.parse_args()
  
  # Configure logging
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
      logging.FileHandler(f'outputs/workflow_{time.time()}.log', encoding='utf-8'),
      logging.StreamHandler(sys.stdout)
    ]
  )
  
  logging.info("="*60)
  logging.info("Auto-Cursor Workflow Started")
  logging.info(f"User Input: {args.input}")
  logging.info(f"Startup Delay: {args.delay} seconds")
  logging.info(f"Max Rounds: {args.max_rounds} rounds")
  logging.info("="*60)
  
  # Startup delay
  if args.delay > 0:
    logging.info(f"Waiting {args.delay} seconds before starting...")
    time.sleep(args.delay)
  
  # Execute workflow
  result = workflow(args.input)
  
  logging.info("="*60)
  logging.info(f"Workflow Completed: {result}")
  logging.info("="*60)
  
  # Move mouse to safe position
  pyautogui.moveTo(200, 200)

if __name__ == "__main__":
  main()
