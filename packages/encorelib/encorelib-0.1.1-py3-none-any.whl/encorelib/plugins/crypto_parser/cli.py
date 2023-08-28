VERSION = 0.01

VALID_EXCHANGES = {
    ''
}


def main():
    # 1) Print Plugin`s Data
    print(f"""
   ____________  ______  __________ 
  / ____/ __ \ \/ / __ \/_  __/ __ \\
 / /   / /_/ /\  / /_/ / / / / / / /
/ /___/ _, _/ / / ____/ / / / /_/ / 
\____/_/ |_| /_/_/     /_/  \____/  
            ____  ___    ____  _____ __________ 
           / __ \/   |  / __ \/ ___// ____/ __ \\
          / /_/ / /| | / /_/ /\__ \/ __/ / /_/ /
         / ____/ ___ |/ _, _/___/ / /___/ _, _/ 
        /_/   /_/  |_/_/ |_|/____/_____/_/ |_|
Version: {VERSION}
""")

    # 2) Start Echo
    while True:

        # 1 Get exchange
        while True:
            exchange = input('What exhanges do you want to parse?: ').split(',')






if __name__ == '__main__':
    main()
