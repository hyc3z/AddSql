import re

import pinyin


class WriteBuffer:

    def __init__(self, list):
        self.buffer = list
        self.indent_level = 0


    def append(self, str):
        self.buffer.append("{}{}".format("    "*self.indent_level,str))

    def indent(self):
        self.indent_level += 1

    def unindent(self):
        if self.indent_level >= 1:
            self.indent_level -= 1

    def resetIndent(self):
        self.indent_level = 0

    def preview(self):
        print("\n".join(self.buffer))

    def writeOut(self, filename="models.py"):
        with open(filename, 'w', encoding='utf-8') as of:
            of.write("\n".join(self.buffer))

def getStrAllAplha(str):
    return pinyin.get_initial(str, delimiter="")

def getStrFirstAplha(str):
    str = getStrAllAplha(str)
    str = str[0:1]
    return str

def classStr(classname):
    return "class {}(models.Model):\n".format(classname)

def importStr(importname, fromname=None):
    if fromname:
        return "from {} import {}".format(fromname, importname)
    else:
        return "import {}".format(importname)

def annotateStr(str):
    return "# {}".format(str)

def removeLF(str):
    return str.replace('\r\n', "").replace('\n',"")

def elColumnStr(str):
    str = removeBracketContent(str)
    return "<el-table-column prop=\"{}\" label=\"{}\" align=\"center\"></el-table-column>".format(getStrAllAplha(str), str)
def removeBracketContent(str):
    return re.split('\(|（', removeLF(str))[0]

def readConfig(filename="model_description.txt", encoding='utf-8'):
    buffer = WriteBuffer([])

    with open(filename, 'r', encoding=encoding) as f:
        for i in f.readlines():
            if i[-2] in [":", "："]:
                buffer.append(i)
            else:
                field_lists = re.split(',|，', removeLF(i))
                for field in field_lists:
                    if len(field) > 0:
                        buffer.append(elColumnStr(field))
        # buffer.preview()
        buffer.writeOut("vue.txt")



def main():
    readConfig()


if __name__ == '__main__':
    main()
