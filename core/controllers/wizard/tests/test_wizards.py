'''
test_wizards.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''

import os

from core.controllers.w3afCore import w3afCore
from core.controllers.misc.factory import factory

from core.data.options.optionList import optionList


class test_wizards(object):

    unique_wizard_ids = []
    
    def test_all_wizards(self):
        mod = 'core.controllers.wizard.wizards.%s'
        w3af_core = w3afCore()
        
        for filename in os.listdir('core/controllers/wizard/wizards/'):
            wizard_id, ext = os.path.splitext(filename)
        
            if wizard_id == '__init__' or ext == '.pyc':
                continue

            klass = mod % wizard_id
            wizard_inst = factory( klass, w3af_core )
            
            yield self._test_wizard, wizard_inst
    
    def _test_wizard(self, wizard_inst):
        '''
        @see test_questions.py for a complete test of questions.py and all the
             instances of that class that live in the questions directory.
        '''
        wid = wizard_inst.getName()
        assert wid != ''
        assert wid not in self.unique_wizard_ids
        self.unique_wizard_ids.append( wid )
        
        assert len(wizard_inst.getWizardDescription()) > 30
        
        while True:
            question = wizard_inst.next()
            if question is None:
                break
            else:
                opt = question.getOptionObjects()
                filled_opt = self._correctly_fill_options(opt)
                wizard_inst.setAnswer(filled_opt)
    
    def _correctly_fill_options(self, option_list):
        '''
        @return: A correctly completed option list, simulates a user that knows
                 what he's doing and doesn't make any mistakes.
        '''
        values = {
                  'target': 'http://www.w3af.org',
                  'targetOS': 'Unix',
                  'targetFramework': 'PHP'
                 }
        
        for option in option_list:
            value = values.get( option.getName(), 'abc' )
            option.setValue(value)
        
        return option_list
    
        
        
            
