## Notes

Plugin for [fman.io](https://fman.io) to give the ability to add notes to files and 
directories.

You can install this plugin by pressing `<shift+cmd+p>` to open the command pallet. 
Then type `install plugin`. Look for the `Notes` plugin and select it.

### Usage

Select a file or directory and press **`<shift>+n`**. The associated note will be 
displayed for reading or editing. All notes are in the current directory in a new 
`.notes` subdirectory. The name for the note file associated with a directory or 
file is that directory or file name with the `.md` extension.

If you have the [Open With Editor](https://github.com/raguay/OpenWithEditor) plugin installed and configured, then this 
plugin will use the editor your select with that plugin to edit the notes file.
Otherwise, it will use the fman's built-in `open_with_editor`  command to edit 
the file with a system defined program.

Also, if the [ProjectManager](https://github.com/raguay/ProjectManager) plugin is installed and the current file is in the 
current project, then the note will be placed into the projects notes directory.

There are also some commands:

| Command | Description |
| --- | ------ |
| Notes | This is the command tied to `<shift>+n` to create a note for the file or directory under the cursor. |
|Go To Note Dir | This command will allow you to go to one of the note directories. |
| Remove Note | This command allows you to remove a note file in the current directory. |

### Features

 - Attach notes to files and directories.
 - Go to the note directories
 - Remove a note file for a file or directory.
 - Put notes in the Project Manager plugins notes directory.

