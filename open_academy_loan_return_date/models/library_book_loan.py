# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 All Rights Reserved
#
# Created on Feb 22, 2017
#
# @author: kerbrose (Khaled Said)
# @contact: kerbrose  ==> hotmail  ==> com
#####################################

from odoo import api, models, fields

class LibraryBookLoan(models.Model):
    _inherit = 'library.book.loan'
    
    expected_return_date = fields.Date('Due for', required = True)
    
    