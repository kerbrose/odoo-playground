# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 All Rights Reserved
#
# Created on Feb 22, 2017
#
# @author: kerbrose (Khaled Said)
# @contact: kerbrose  ==> hotmail  ==> com
#####################################

from datetime import timedelta
from odoo import api, models, fields

class LibraryLoanWizard(models.TransientModel):
    _inherit = 'library.loan.wizard'
    
    def _prepare_loan(self, book):
        values = super(LibraryLoanWizard, self)._prepare_loan(book)
        loan_duration = self.member_id.loan_duration
        today_str = fields.Date.context_today()
        today = fields.Date.from_string(today_str)
        expected = today + timedelta(days=loan_duration)
        values.update({ 'expected_return_date': fields.Date.to_string(expected)})
        return values