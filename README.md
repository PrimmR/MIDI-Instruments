# Midi Instrument Changer
A simple tool that allows you to edit the instrument change events in a MIDI file.

This is intended for simple MIDI songs, so if your file has many instrument changes throughout it, you may find it easier to use a MIDI compatible DAW.

## Usage
Either drag the MIDI file onto the python script, or pass the file as the first argument to the script in a terminal.

If the program detects a valid MIDI file, you should see a table with headers as follows:

**Byte** - The location of the instrument change event in the file. Used as an ID.  
**Channel** - The channel that the change applies to. Ranges from 0-15. A channel can only use one instrument at once and switches them using a change event.  
**Instrument** - The current instrument ID that the change event sets the channel to.  
**Location** - A rough estimate of how far through the track the change occurs. The first event will rarely be on 0%.

Now select the event that you to edit the instrument of. Sometimes MIDI exporters put additional events before ones that are actually used, so you may need to look for the first Channel 0 event instead of the first event in the list, if you are looking for the first instrument used.

You can now input the instrument ID to change the following part of the track to its corresponding instrument.
General Midi instrument IDs can be found in [this list](Instruments.txt).

Repeat for all the change events you want to edit, then input **S** to save.
In playback, your MIDI file should now be using the instruments you selected!