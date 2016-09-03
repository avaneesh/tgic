# tgic_core.py
# Copyright (C) 2016-2017 Avaneesh Kadam <avaneesh.kadam@gmail.com>
# 
# This file is part of TGIC
#    TGIC's Grep In Colors
#       or simply
#    Thank God Its Colored
#
# TGIC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TGIC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TGIC.  If not, see <http://www.gnu.org/licenses/>.

# This module is the core logic of parsing text based notes/cheets file
# and creating DB out of it. It also provides search of this DB and 
# then Colored rendering which is one of the main objectives of TGIC.


import re
from enum import Enum

r_tag = re.compile("^#t .*")
r_comment = re.compile("^#*")

class CheetsSectionDB:
    def __init__(self):
        self.all_sections = []
        self.curr_section_id = 0

    def __repr__(self):
        return "Total Cheet sections: %d" % (len(self.all_sections))

    @property
    def next_section_id(self):
        self.curr_section_id = self.curr_section_id +1
        return self.curr_section_id



class TagDB:
    def __init__(self):
        #self.all_tags = []
        self.tags_dict = {}
        self.curr_tag_id = 0

    def __repr__(self):
        return "Total unique Tags: %d" % (len(self.tags_dict))

    @property
    def next_tag_id(self):
        self.curr_tag_id = self.curr_tag_id +1
        return self.curr_tag_id

    def get_tag_by_name(self, tag_name, current_section):
        if tag_name not in self.tags_dict:
            t = Tag(tag_name, self)
            self.tags_dict[tag_name] = t
        else:
            t = self.tags_dict[tag_name]
        # Append "current cheeet section" in Tag
        t.cheet_sections.append(current_section)
        # Append Tag in "current cheeet section"
        current_section.tags.append(t)
        #print "\n Adding ", tag_name ," to Cheet section, ", current_section.section_id, "tags: ", str(len(current_section.tags))
            

class Tag:
    def __init__(self, tag_name, tagsDB):
        self.tag_name = tag_name
        #tagsDB.all_tags.append(self)
        self.tag_id = tagsDB.next_tag_id
        
        # TODO: List of Tuple(section and confidence of this tag)
        self.cheet_sections = []

    def __repr__(self):
        # TODO: use self.cheet_sections
        return "-Tag ID,name: %d, %s. In %d cheet sections -"  \
            % (self.tag_id, self.tag_name, len(self.cheet_sections))

class LineType(Enum):
    tag = 1
    comment = 2
    normal = 3

class Line:

    def __init__(self, line):
        self.line = line
        self.line_type = Line.get_type(line)

    def __repr__(self):
        return "%s: %s" % (self.line_type, self.line)

    @staticmethod
    def get_type(line):
        if line.startswith("#t "):
            return LineType.tag
        if line.startswith("#") and not line.startswith("^#t "):
            return LineType.comment
        return LineType.normal

    @property
    def isTag(self):
        return self.line_type == LineType.tag
    @property
    def isComment(self):
        return self.line_type == LineType.comment
    @property
    def isNormalCheet(self):
        return self.line_type == LineType.normal

    def get_tags_from_tag_line(self, tagsDB, current_section):
        if not self.isTag:
            raise ValueError("Not a Tag line: ", self.line)
        # Remove first 3 characters and then split
        curr_line_tags = self.line[3:].split()
        for tag_name in curr_line_tags:
            t = tagsDB.get_tag_by_name(tag_name, current_section)
    



class CheetSection:
    def __init__(self, cheetsDB):
        cheetsDB.all_sections.append(self)
        self.section_id = cheetsDB.next_section_id
        self.tags = []
        # List of lines of type "class Line"
        self.lines = []
        #print "\n Creating Cheet section, ", self.section_id, "tags: ", str(len(self.tags)), "ID: ", id(self)

    def __repr__(self):
        return "Section ID: %d tags(%d): %s. Total lines: %d" % (self.section_id, len(self.tags), self.tags, len(self.lines))

    def get_local_confidence_for_tag(self, tag):
        # keep it simple for now
        return 1 / len(self.tags)


def readCheetsDbFile(filename, cheetsDB, tagsDB):
    ''' Read cheets.db file to populate cheetsDB and tagsDB
    '''
    with open(filename) as f:
        for line_string in f:
            line = Line(line_string)
            if line.isTag:
                # Create new section
                current_section = CheetSection(cheetsDB)
                line.get_tags_from_tag_line(tagsDB, current_section)
                
            if not current_section:
                # To skip initial lines in file before first tag if any
                continue

            current_section.lines.append(line)

def get_sections(cheetsDB, tagsDB, andList, orList):
    '''
        orList has list of andList of Tags
            cheets.py gdb,gdbserver expand,install important
                >> Will search for sections matching gdb & gdbserver OR expand & install OR important
        returns: list of sections
    '''

                
if __name__ == '__main__':
    cheetsDB = CheetsSectionDB() 
    tagsDB = TagDB() 
    readCheetsDbFile('cheets.db', cheetsDB, tagsDB)

    import pprint
    pp = pprint.PrettyPrinter(depth=6)

    print "\nAll tags: "
    pp.pprint(tagsDB.tags_dict)
    #print "\nAll gdb Sections: "
    #pp.pprint(tagsDB.tags_dict['gdb'].cheet_sections)
