#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///

import sys
import textwrap
from rich.console import Console
from rich.color import Color
from rich.style import Style

CLAUDE_COLOR = Color.from_rgb(217, 119, 87)
CLAUDE_STYLE = Style(color=CLAUDE_COLOR)

CLAUDE_ASCII = """\
         .%+*%        %%%               
          *#=+#      .%**               
           :%=*#     .##      #%%%.     
    #+      .%=*=    :#%    .#*=##      
   .@%%%-    .#+#:   +%=   ##=+%:       
     -%%%%*   :#+#.  #%  .%*=*%         
        %%%%#.  -=#  ## ##==#=          
           %%%%+-:++++++*-=%            
             =%#+::---::::=    +##%%@@@ 
 @%%*-.         +::::::::-#%@@%%%%#.    
  .-*#%%@@@@@@%%*::::::::-.             
               .**=::::::-#%%@@@%%%%%%. 
            #@%%  #*+-:::-:     .####%%.
         %%%%:  #%- **#*-=#%%           
      #%%%-    %%.  %  *#=  *%%         
    -@%#     -%%   .%   #%%.  #@%       
            #%*    %%    .%%*   -%#     
          .@%      %#      %%%          
         %@-      *%-       #%#         
                  %%.                   
"""

def create_speech_bubble(message, width=40):
    lines = []
    wrapped_text = textwrap.wrap(message, width - 4)  # Leave room for bubble edges
    
    if len(wrapped_text) == 1:
        line = wrapped_text[0]
        lines.append(f"< {line.ljust(width - 4)} >")
    else:
        lines.append(f"/ {wrapped_text[0].ljust(width - 4)} \\")
        for line in wrapped_text[1:-1]:
            lines.append(f"| {line.ljust(width - 4)} |")
        lines.append(f"\\ {wrapped_text[-1].ljust(width - 4)} /")
    
    # Calculate border
    border_top = " " + "_" * (width - 2)
    border_bottom = " " + "-" * (width - 2)
    
    return [border_top, *lines, border_bottom]

def claudesay(message):
    console = Console()
    bubble = create_speech_bubble(message)
    
    # Print the speech bubble
    for line in bubble:
        console.print(line, style=CLAUDE_STYLE)
    
    # Print the speech stem
    console.print("       \\", style=CLAUDE_STYLE)
    console.print("        \\", style=CLAUDE_STYLE)

    # Print Claude ASCII art
    for line in CLAUDE_ASCII.split('\n'):
        console.print(line, style=CLAUDE_STYLE)

def main():
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = sys.stdin.read().strip()
    
    if not message:
        print("Usage: claudesay <message> or echo <message> | claudesay", file=sys.stderr)
        sys.exit(1)
    
    claudesay(message)

if __name__ == "__main__":
    main()