# Macronaut
Macronaut is simple macro creator for simplification repetitive tasks.


### Installation:

  ```
  sudo ./install.sh
  ```
  
### Run:
  ```
  $ ./macronaut --help
  usage: macronaut [-h] [--record] [--compile] [--play] [--name NAME]
                   [--speed SPEED] [--verbose] [--output-path OUTPUT_PATH] [--version]
  
  optional arguments:
    -h, --help                      Show this help message and exit
    --record                        Only record keyboard inputs and save into raw_data format.
    --compile                       Compile raw_data format into python runable script which is saved into OUTPUT_PATH.
    --play                          Play macro script.
    --name NAME                     Change name of macro script.
    --speed SPEED                   Setup how fast you want it.
    --verbose                       Print output into stdout.
    --output-path OUTPUT_PATH       Setup path where save generated macro script.
    --version                       Show program's version number and exit
  ```

## Special thanks:

 - [xdotool](http://www.semicomplete.com/projects/xdotool/): Tool lets you simulate keyboard input and mouse activity.
 - [Pynput](https://github.com/moses-palmer/pynput): Library for control and monitor input devices.



## Authors:

 - Martin Jablečník


