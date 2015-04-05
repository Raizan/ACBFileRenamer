"""
    Written by  : Raizan
    Date        : April 5th, 2015

    Script for renaming files uploaded by AnimeChiby.com
    Two patterns covered in this script: Mediafire and Mega

    Rename files in a folder to "[Anime Title] [#Episode].mkv"
    Example: "637_smc_19_hd_hs_acb.mkv" to "Sailor Moon Crystal 19.mkv"
"""

import os
import sys
import json
from pprint import pprint

# JSON anime_dictionary full path
dictionary_path = "/home/reisuke/PycharmProjects/ACBFileRenamer/anime_dictionary.json"

# Open dictionary and read as json object
anime_dictionary = open(dictionary_path, "r+")
dictionary_read = json.loads(anime_dictionary.read())


def rename_files(path):
    file_list = os.listdir(path)
    file_qty = len(file_list)
    counter = 1

    for file_name in file_list:
        splitted = file_name.split('_')

        # Downloaded from Mediafire
        if len(splitted) == 6:
            print "Processing: ", file_name, " (", counter, "/", file_qty, ")"
            counter += 1

            initial = splitted[1].lower()
            # Check if initial is in dictionary
            if initial in dictionary_read["anime_dictionary"]:
                episode = splitted[2]  # Episode number
                full_title = dictionary_read["anime_dictionary"][initial]
                os.rename(file_name, full_title + " " + episode + ".mkv")


        # Downloaded from Mega
        elif len(splitted) == 5:
            print "Processing: ", file_name, " (", counter, "/", file_qty, ")"
            counter += 1

            initial = splitted[0].lower()
            # Check if initial is in dictionary
            if initial in dictionary_read["anime_dictionary"]:
                episode = splitted[1]  # Episode number
                full_title = dictionary_read["anime_dictionary"][initial]
                os.rename(file_name, full_title + " " + episode + ".mkv")

if __name__ == "__main__":
    arguments = sys.argv[1:]
    if arguments[0] == "dict":
        # Close file open session
        anime_dictionary.close()

        if arguments[1] == "list":
            pprint(dictionary_read)

        elif arguments[1] == "update":
            initial = arguments[2]
            full_title = arguments[3]

            anime_dictionary = open(dictionary_path, "w+")

            dictionary_read["anime_dictionary"][initial] = full_title

            anime_dictionary.write(json.dumps(dictionary_read))
            anime_dictionary.close()

        elif arguments[1] == "delete":
            initial = arguments[2]

            anime_dictionary = open(dictionary_path, "w+")

            del dictionary_read["anime_dictionary"][initial]

            anime_dictionary.write(json.dumps(dictionary_read))
            anime_dictionary.close()

    elif arguments[0] == "execute":
        path = os.path.abspath(arguments[1])
        rename_files(path)

    elif arguments[0] == "help":
        print
        print "To use these commands, create alias acb='python /path/to/acb_renamer_script'"
        print "If you don't want to that, then just replace 'acb' with 'python /path/to/acb_renamer_script'"
        print
        print "Usage: acb [command]"
        print "'acb help' : will print this message"
        print "'acb dict list' : print list of anime title you have"
        print "'acb dict update [anime initial] [anime full title]' : update your anime dictionary with that anime"
        print "'acb dict update [anime initial] [anime full title]' : delete that anime initial from dictionary"
        print "'acb execute [path/to/folder]' : automatically rename all files to format specified by this script"
        print