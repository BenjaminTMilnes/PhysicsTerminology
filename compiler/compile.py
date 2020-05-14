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

            t = lines[2].split(";")

            if t[0] == "noun":
                term["PartOfSpeech"] = "noun"

                for u in t[1:]:
                    if u.strip().startswith("plural:"):
                        plural = u.strip()[7:].strip()
                        term["Plural"] = plural
                    if u.strip().startswith("adjectival:"):
                        adjectivalForm = u.strip()[11:].strip()
                        term["AdjectivalForm"] = adjectivalForm

            if len(lines) > 3:

                term["ShortDescription"] = lines[3]
                term["LongDescription"] = ""
                term["Etymology"] = ""

                lines = lines[4:]
                section = ""

                for line in lines:
                    if line.startswith("description:"):
                        section = "description"
                        continue

                    if line.startswith("etymology:"):
                        section = "etymology"
                        continue
                    
                    if line.startswith("ipa:"):
                        section = ""
                    
                    if line.startswith("wikipedia:"):
                        section = ""

                    if section == "description":
                        term["LongDescription"] += "<p>" + self.addItalicTags(line.strip()) + "</p>"

                    if section == "etymology":
                        term["Etymology"] += "<p>" + self.addItalicTags(line.strip()) + "</p>"

                    if line.startswith("ipa:"):
                        ipa = line[4:].strip()
                        term["IPA"] = ipa

                    if line.startswith("wikipedia:"):
                        url = line[10:].strip()
                        term["WikipediaURL"] = url
                        
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
