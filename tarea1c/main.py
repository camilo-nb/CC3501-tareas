import os
import sys

from view.view import start
from data.mydata import d

if __name__ == "__main__":
    
    print(
        """
                                                           
                                            88                   
                                            88                   
                                            88                   
           ,adPPYba, 8b,dPPYba,  ,adPPYYba, 88   ,d8  ,adPPYba,  
           I8[    "" 88P'   `"8a ""     `Y8 88 ,a8"  a8P_____88  
            `"Y8ba,  88       88 ,adPPPPP88 8888[    8PP"""""""  
           aa    ]8I 88       88 88,    ,88 88`"Yba, "8b,   ,aa  
           `"YbbdP"' 88       88 `"8bbdP"Y8 88   `Y8a `"Ybbd8"'  
                                                                                                           
        """
    )
    # https://ascii.co.uk/art/snake
    
    args = {
        "n": False,
        "w": False,
        "h": False,
        "fps": False,
        "s": False
    }
    
    for i, arg in enumerate(sys.argv):
        
        if arg == "-n" or arg == "--dimension":
            
            try:

                if not sys.argv[i+1].isdigit():
                    raise Exception(f"{arg} must be a positive integer")
                
                else:
                    d["n"] = int(sys.argv[i+1])+2

            except IndexError:
                raise Exception(f"no {arg} argument given")

            except ValueError:
                raise Exception(f"{arg} must be a positive integer")
            
            else:
                d.dump()
                args["n"] = True
                
        if arg == "-w" or arg == "--width":
            
            try:

                if not sys.argv[i+1].isdigit():
                    raise Exception(f"{arg} must be a positive integer")
                
                else:
                    d["w"] = int(sys.argv[i+1])

            except IndexError:
                raise Exception(f"no {arg} argument given")

            except ValueError:
                raise Exception(f"{arg} must be a positive integer")
            
            else:
                d.dump()
                args["w"] = True
                
        if arg == "-h" or arg == "--height":
            
            try:

                if not sys.argv[i+1].isdigit():
                    raise Exception(f"{arg} must be a positive integer")
                
                else:
                    d["h"] = int(sys.argv[i+1])

            except IndexError:
                raise Exception(f"no {arg} argument given")

            except ValueError:
                raise Exception(f"{arg} must be a positive integer")
            
            else:
                d.dump()
                args["h"] = True
    
        if arg == "-f" or arg == "--fps":
            
            try:

                if not sys.argv[i+1].isdigit():
                    raise Exception(f"{arg} must be a positive integer")
                
                else:
                    d["fps"] = int(sys.argv[i+1])

            except IndexError:
                raise Exception(f"no {arg} argument given")

            except ValueError:
                raise Exception(f"{arg} must be a positive integer")
            
            else:
                d.dump()
                args["fps"] = True
                
        if arg == "-s" or arg == "--sound":
            
            try:
                
                if sys.argv[i+1] == "on":
                    d["s"] = True
                elif sys.argv[i+1] == "off":
                    d["s"] = False
                else:
                    raise Exception(f"{arg} must be on or off")
                
            except IndexError:
                raise Exception(f"no {arg} argument given")
                
            else:
                d.dump()
                args["s"] = True
                
    if args["n"]:
        
        if not "w" in d.data:
            d["w"] = 800
            d.dump()
        if not "h" in d.data:
            d["h"] = 600
            d.dump()
        if not "fps" in d.data:
            d["fps"] = 10
            d.dump()
        if not "s" in d.data:
            d["s"] = True
            d.dump()
            
        start()
        
    else:
        raise Exception(
            u"""\n
            ┌──────────────────────────────────────────────┐
            │         please enter the dimensions          │
            │             of the square grid               │
            │           using -n or --dimension            │
            └──────────────────────────────────────────────┘\n
            """
        )