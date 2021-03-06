from fman import DirectoryPaneCommand, show_alert, load_json, save_json, show_prompt, show_quicksearch, QuicksearchItem, show_status_message, clear_status_message
from core.quicksearch_matchers import contains_chars
from core.commands import _get_thirdparty_plugins, _THIRDPARTY_PLUGINS_DIR
from fman.url import basename, dirname, join, as_human_readable, as_url
from fman.fs import exists, mkdir, touch, delete, iterdir
import os

NOTESDIR = None
NOTESDIRNAME = 'notesdir'
PROJECTDIR = os.path.expanduser("~") + "/.currentprojectdir"
#
# Class:        Notes
#
# Description:  This class is a subclass of DirectoryPaneCommand. It is 
#               used to open a note file in the `.notes` subdirectory 
#               in the user's defined editor. It will create the `.notes` directory 
#               if it doesn't already exist. It will also save the new 
#               directory in the list of note directories.
#
class Notes (DirectoryPaneCommand):
    def __call__(self, url=None):
        pm = False
        if(exists(PROJECTDIR)):
            projDir = ""
            with open(PROJECTDIR) as f:
                projDir = f.read()
            if not projDir == "":
                pm = True
                pnotesDir = projDir + "/.notes/"

        #
        # Get the current directory.
        #
        notePath = join(self.pane.get_path(), "/.notes/")
 
        #
        # Get either the current cursor file or the file
        # sent in the url command.
        #
        cursorFile = self.pane.get_file_under_cursor()
        if cursorFile == None and url == None:
            show_alert('Nothing is selected.')
            return

        if not url == None:
            cursorFile = url
            #
            # Change the notes directory to the directory of the file sent.
            #
            notePath = join(dirname(url), "/.notes/")

        #
        # If the current directory is under the current project, put 
        # the notes in the project's note directory.
        #
        if pm:
            if as_human_readable(notePath).find(projDir) != -1:
                notePath = as_url(pnotesDir)

        #
        # If the notes directory doesn't exist, create it.
        #
        if not exists(notePath):
            mkdir(notePath)
            saveNotesDir(notePath)

        #
        # Open the note file for the file or directory.
        #
        cfName = basename(cursorFile)
        cfNoteFile = join(notePath, cfName + ".md")

        #
        # If the OpenWithEditor plugin is loaded, use it to edit 
        # the file. Otherwise, use the system edit command. The 
        # touch command will create the file if it doesn't exist.
        #
        touch(cfNoteFile)
        if (_THIRDPARTY_PLUGINS_DIR + "/OpenWithEditor") in _get_thirdparty_plugins():
            self.pane.run_command("my_open_with_editor", args={'url': cfNoteFile})
        else:
            self.pane.run_command("open_with_editor", args={'url': cfNoteFile})

#
# Function:         getNotesDir
#
# Descriptions:     This function will retrieve the list of note directories. It 
#                   loads the first time from the json list and then keeps the list 
#                   in a global variable.
#
def getNotesDir():
    global NOTESDIR, NOTESDIRNAME
    if NOTESDIR == None:
        NOTESDIR = load_json(NOTESDIRNAME,default=[])
    return(NOTESDIR)

#
# Function:         saveNotesDir
#
# Description:      This function will save a new entry into the notes directory 
#                   list if it isn't already in it. It then saves it to the disk 
#                   as well.
#
def saveNotesDir(newDir):
    global NOTESDIR
    notes = getNotesDir()
    if not newDir in notes:
        NOTESDIR = notes.append(newDir)
        saveNotesDirDisk()

#
# Function:         saveNotesDirDisk
#
# Description:      This function saves the list of note directories into a json 
#                   file.
#
def saveNotesDirDisk():
    global NOTESDIR, NOTESDIRNAME
    save_json(NOTESDIRNAME, NOTESDIR)

def removeNoteDir(noteDir):
    global NOTESDIR
    notes = getNotesDir()
    NOTESDIR = notes.remove(noteDir)
    saveNotesDirDisk()

#
# Class:        GoToNoteDir
#
# Description:  A Pane command to jump to a notes directory.
#
class GoToNoteDir(DirectoryPaneCommand):
    #
    # This directory command is for selecting a note directory 
    # and going to that directory.
    #
    def __call__(self):
        show_status_message('Select Note Directory')
        result = show_quicksearch(self._suggest_directory)
        if result:
            query, dirName = result
            self.pane.set_path(dirName)
        clear_status_message()

    def _suggest_directory(self, query):
        directories = getNotesDir()
        for dirName in directories:
            match = contains_chars(dirName.lower(), query.lower())
            if match or not query:
                yield QuicksearchItem(dirName, highlight=match)

#
# Class:        RemoveNote
#
# Description:  A Pane command will delete the selected note.
#
class RemoveNote(DirectoryPaneCommand):
    #
    # This directory command is for selecting a note in the current note directory 
    # in order to delete it.
    #
    def __call__(self):
        show_status_message('Delete Note...')
        result = show_quicksearch(self._suggest_note)
        if result:
            query, dirName = result
            noteDir = self.pane.get_path()
            delete(noteDir + "/.notes/" + dirName)
            noteDirList = iterdir(noteDir + "/.notes")
            numNotes = sum(1 for _ in noteDirList)
            if numNotes == 0:
                delete(noteDir + "/.notes")
                removeNoteDir(noteDir + "/.notes/")
        clear_status_message()

    def _suggest_note(self, query):
        noteDir = self.pane.get_path()
        noteDirList = iterdir(noteDir + "/.notes")
        for noteName in noteDirList:
            match = contains_chars(noteName.lower(), query.lower())
            if match or not query:
                yield QuicksearchItem(noteName, highlight=match)

#
# Class:        EditNotes
#
# Description:  A Pane command will allow the user to select from all
#               note files to edit one.
#
ALLNOTES = None
class EditNotes(DirectoryPaneCommand):
    #
    # This directory command is for selecting a note in the current note directory 
    # in order to delete it.
    #
    def __call__(self):
        global ALLNOTES

        show_status_message('Edit Note...')
        ALLNOTES = []
        for notedir in getNotesDir():
            for notesindir in iterdir(notedir):
                ALLNOTES.append(notedir + notesindir)
        result = show_quicksearch(self._suggest_note)
        if result:
            query, noteFile = result
            if (_THIRDPARTY_PLUGINS_DIR + "/OpenWithEditor") in _get_thirdparty_plugins():
                self.pane.run_command("my_open_with_editor", args={'url': noteFile})
            else:
                self.pane.run_command("open_with_editor", args={'url': noteFile})
        clear_status_message()

    def _suggest_note(self, query):
        global ALLNOTES
        for noteName in ALLNOTES:
            match = contains_chars(noteName.lower(), query.lower())
            if match or not query:
                yield QuicksearchItem(noteName, highlight=match)

