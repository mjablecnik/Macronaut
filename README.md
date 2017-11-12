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
                   [--speed SPEED] [--output-path OUTPUT_PATH]
  
  optional arguments:
    -h, --help                      show this help message and exit
    --record                        Only record keyboard inputs and save into raw_data
                                    format.
    --compile                       Compile raw_data format into python runable script
                                    which is saved into OUTPUT_PATH.
    --play                          Play macro script.
    --name NAME                     Change name of macro script.
    --speed SPEED                   Setup how fast you want it.
    --output-path OUTPUT_PATH       Setup path where save generated macro script.
  ```

## Special thanks:

 - [xdotool](http://www.semicomplete.com/projects/xdotool/): Tool lets you simulate keyboard input and mouse activity.
 - [Pynput](https://github.com/moses-palmer/pynput): Library for control and monitor input devices.



## Authors:

 - Martin Jablečník


