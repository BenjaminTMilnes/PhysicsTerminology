import os
import json
import re


class Compiler (object):

    def getTermFilePaths(self):
        filePaths = []

        for a in os.listdir("../data"):
            if a.endswith(".term"):
                filePaths.append(os.path.join("../data", a))

        return filePaths

    def addItalicTags(self, text):
        n = 0
        t = ""

        for c in text:
            if c == "*" and n == 0:
                t += "<i>"
                n = 1
            elif c == "*" and n == 1:
                t += "</i>"
                n = 0
            else:
                t += c

        return t

    def compileTerm(self, filePath):

        with open(filePath, "r", encoding="utf-8") as fileObject:
            lines = fileObject.readlines()
            lines = [l.strip() for l in lines if l.strip() != ""]

            term = {}

            term["Reference"] = lines[0]
            term["URLReference"] = term["Reference"].lower()
            term["Text"] = lines[1]
            term["IPA"] = lines[2]

            t = lines[3].split(";")

            if t[0] == "noun":
                term["PartOfSpeech"] = "noun"

                for u in t[1:]:
                    if u.strip().startswith("plural:"):
                        plural = u.strip()[7:].strip()
                        term["Plural"] = plural
                    if u.strip().startswith("adjectival:"):
                        adjectivalForm = u.strip()[11:].strip()
                        term["AdjectivalForm"] = adjectivalForm
                        
            if len(lines) > 4:

                term["ShortDescription"] = lines[4]
                term["LongDescription"] = lines[5]

                lines = lines[6:]
                section = ""

                for line in lines:
                    if line.startswith("etymology:"):
                        section = "etymology"
                        continue

                    if section == "etymology":
                        term["Etymology"] = self.addItalicTags(line.strip())
                        section = ""

            return term

    def compile(self):

        termFilePaths = self.getTermFilePaths()

        terms = [self.compileTerm(filePath) for filePath in termFilePaths]

        data = {}

        data["Terms"] = terms

        print(data)

        with open("../data/compiled.json", "w", encoding="utf-8") as fileObject:
            json.dump(data, fileObject, indent=4)

        with open("../web/terminology.json", "w", encoding="utf-8") as fileObject:
            json.dump(data, fileObject, indent=4)


if __name__ == "__main__":
    compiler = Compiler()

    compiler.compile()
