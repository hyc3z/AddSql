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

def removeBracketContent(str):
    return re.split('\(|（', removeLF(str))[0]

def CharField(str, ignoreBracket=True):
    if ignoreBracket:
        processed_str = removeBracketContent(str)
    return "{} = models.CharField(\"{}\", max_length=20)".format(getStrAllAplha(processed_str), processed_str)

def DecimalField(str, ignoreBracket=True, max_digits=8, decimal_places=2):
    if ignoreBracket:
        processed_str = removeBracketContent(str)
    return "{} = models.DecimalField(\"{}\", max_digits={}, decimal_places={})".format(getStrAllAplha(processed_str), processed_str, max_digits, decimal_places)

def IntegerField(str, ignoreBracket=True):
    if ignoreBracket:
        processed_str = removeBracketContent(str)
    return "{} = models.IntegerField(\"{}\")".format(getStrAllAplha(processed_str), processed_str)

def CustomField(fieldname, str, ignoreBracket=True):
    if ignoreBracket:
        processed_str = removeBracketContent(str)
    return "{} = models.{}Field(\"{}\")".format(getStrAllAplha(processed_str), fieldname, processed_str)

def readConfig(filename="model_description.txt", encoding='utf-8'):
    buffer = WriteBuffer([importStr("models", "django.db")])

    with open(filename, 'r', encoding=encoding) as f:
        for i in f.readlines():
            if i[-2] in [":","："]:
                buffer.resetIndent()
                buffer.append("\n")
                buffer.append(annotateStr(i[:-2]))
                buffer.append(classStr(getStrAllAplha(i[:-2])))
                buffer.indent()
            else:
                field_lists = re.split(',|，', removeLF(i))
                for field in field_lists:
                    if len(field) > 0:
                        buffer.unindent()
                        buffer.append(annotateStr(field))
                        buffer.indent()
                        if "数量" in field:
                            buffer.append(IntegerField(field))
                        elif any(name in field for name in ["单价", "总价"]):
                            buffer.append(DecimalField(field))
                        elif "日期" in field:
                            buffer.append(CustomField("Date", field))
                        elif "时间" in field:
                            buffer.append(CustomField("DateTime", field))
                        else:
                            buffer.append(CharField(field))
        # buffer.preview()
        buffer.writeOut()



def main():
    readConfig()


if __name__ == '__main__':
    main()
