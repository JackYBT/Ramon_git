import sys
def main():
    Dictionary = {"01":"A", "1000":"B", "1010":"C", "100":"D", "0":"E", "0010":"F",
                  "110":"G", "0000":"H", "00":"I", "0111":"J","101":"K","0100":"L",
                  "11":"MM","10":"N", "111":"O", "0110":"P", "1101":"Q", "010":"R",
                  "000":"S", "1":"T", "001":"U","0001":"V","011":"W","1001":"X",
                  "1011":"Y", "1100":"Z"}

    for line in sys.stdin:
        print(Dictionary[line.strip('\n')])
        print(line)

if __name__ == "__main__":
    main()