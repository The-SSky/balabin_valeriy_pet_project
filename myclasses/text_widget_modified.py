# this code was taken from stackoverflow
# i understand how pop up window is made but
# I dont really understand in depth how custom event works
# event is needed for 'ctrl-z' feature to be available

import tkinter as tk


class ModifiedMixin:
    '''
    Class to allow a Tkinter Text widget to notice when it's modified.

    To use this mixin, subclass from Tkinter.Text and the mixin, then write
    an __init__() method for the new class that calls _init().

    Then override the beenModified() method to implement the behavior that
    you want to happen when the Text is modified.
    '''

    def _init(self):
        '''
        Prepare the Text for modification notification.
        '''

        # Clear the modified flag, as a side effect this also gives the
        # instance a _resetting_modified_flag attribute.
        self.clearModifiedFlag()

        # Bind the <<Modified>> virtual event to the internal callback.
        self.bind('<<Modified>>', self._beenModified)

    def _beenModified(self, event=None):
        '''
        Call the user callback. Clear the Tk 'modified' variable of the Text.
        '''

        # If this is being called recursively as a result of the call to
        # clearModifiedFlag() immediately below, then we do nothing.
        if self._resetting_modified_flag:
            return

        # Clear the Tk 'modified' variable.
        self.clearModifiedFlag()

        # Call the user-defined callback.
        self.beenModified(event)

    def beenModified(self, event=None):
        '''
        Override this method in your class to do what you want when the Text
        is modified.
        '''
        pass

    def clearModifiedFlag(self):
        '''
        Clear the Tk 'modified' variable of the Text.

        Uses the _resetting_modified_flag attribute as a sentinel against
        triggering _beenModified() recursively when setting 'modified' to 0.
        '''

        # Set the sentinel.
        self._resetting_modified_flag = True

        try:

            # Set 'modified' to 0.  This will also trigger the <<Modified>>
            # virtual event which is why we need the sentinel.
            self.tk.call(self._w, 'edit', 'modified', 0)

        finally:
            # Clean the sentinel.
            self._resetting_modified_flag = False


# pop-up menu
class PopUpMenu:
    def __init__(self, master, text):
        self.text = text
        self.master = master
        self.menu = tk.Menu(master, tearoff=0)
        self.menu.add_command(label='Cut', command=self.cut)
        self.menu.add_command(label='Copy', command=self.cpy)
        self.menu.add_command(label='Paste', command=self.pste)
        self.menu.add_command(label='Select All', command=self.slect)

    def cut(self):
        self.text.event_generate('<<Cut>>')

    def cpy(self):
        self.text.event_generate('<<Copy>>')

    def pste(self):
        self.text.event_generate('<<Paste>>')

    def slect(self):
        self.text.event_generate('<<SelectAll>>')

    def popup(self, event):
        # self.text.event_generate('<Button-1>', x=event.x, y=event.y)
        self.text.focus_set()
        self.menu.post(event.x_root, event.y_root)


class TextE(ModifiedMixin, tk.Text):
    '''
    Subclass both ModifiedMixin and Tkinter.Text.
    '''

    def __init__(self, *args, outer, **kwargs):

        # Create self as a Text.
        tk.Text.__init__(self, *args, **kwargs)

        # Initialize the ModifiedMixin.
        self._init()

        self.inner = outer

        self.rclick = PopUpMenu(self.master, self)
        self.bind('<Button-3><ButtonRelease-3>',
                  lambda e: self.rclick.popup(e))
        self.bind('<Key>', self._onKeyRelease, '+')

    def _onKeyRelease(self, event):
        print(event.keycode)
        ctrl = (event.state & 0x4) != 0

        if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
            self.event_generate("<<Cut>>")

        if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
            self.event_generate("<<Paste>>")

        if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
            self.event_generate("<<Copy>>")

        if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
            self.event_generate("<<SelectAll>>")


    def beenModified(self, event=None):
        return self.inner()
