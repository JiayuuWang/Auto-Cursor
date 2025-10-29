# GUI-based Cursor Manipulator

## Demo:
<video src="statics/demo-1.mp4" width="100%" height="100%" controls="controls"></video>

## Features:

Manipulate Cursor through GUI operations with self-iteration capabilities to complete real projects

## Workflow Process:

1. Send initial prompt to Cursor
2. Wait for Cursor to complete the task
3. Determine whether to continue iteration based on Cursor's output
4. If continuation is needed, send a new prompt
5. If no continuation is needed, end the process

## Configuration Guide

### Region Configuration

Before running the program, configure the region coordinates in `config.yaml` according to your screen resolution and window layout:

```yaml
# Timestamp region (used to detect if Cursor has finished the task)
timestamp_region:
  x: 340      # Top-left corner X coordinate
  y: 160      # Top-left corner Y coordinate
  width: 80   # Region width
  height: 20  # Region height

# Terminal region (used to capture terminal output)
terminal_region:
  x: 2050
  y: 875
  width: 450
  height: 625

# Cursor window region (used to capture Cursor's output)
cursor_region:
  x: 450
  y: 50
  width: 970
  height: 1180
```

### How to Configure Region Coordinates

1. Open Cursor editor and terminal window, arrange them according to your working layout
2. Use screenshot tools or mouse position tools to determine the coordinates of each region
3. Modify the coordinate values in `config.yaml`
4. Region format description:
   - `x, y`: Screen coordinates of the top-left corner of the region
   - `width, height`: Width and height of the region (in pixels)



