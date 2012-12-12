# -*- coding: utf-8 -*-
"""Copyright (c) 2012, www.tsuyukimakoto.com
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, 
      this list of conditions and the following disclaimer in the documentation 
      and/or other materials provided with the distribution.
    * Neither the name of the everes nor the names of its contributors may be 
      used to endorse or promote products derived from this software without 
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF 
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""

import re

import sublime
import sublime_plugin

line_start_re = re.compile(r'^\|\s+')
line_end_re = re.compile(r'\s+\|$')
line_middle_re = re.compile(r'\s+\|\s+')


def _tab_line(value):
    '''Convert like below.
    | 1 | some value | others | -> 1\\tsome value\\tothers
    '''
    value = line_start_re.sub('', value)
    value = line_end_re.sub(r'\n', value)
    return line_middle_re.sub(r'\t', value)


class MysqlResultFormatCommand(sublime_plugin.TextCommand):
    """ Convert MySQL select result to tab separated

    Copy and paste it to spread sheet easily.
    """
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                selection = sublime.Region(0, self.view.size())
            else:
                selection = region
            try:
                data = self.view.substr(selection)
                data = ''.join(map(_tab_line, data.split('\n')))
                self.view.replace(edit, selection, data)
            except Exception, e:
                sublime.status_message(str(e))
