# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 All Rights Reserved
#
# Created on Feb 22, 2017
#
# @author: kerbrose (Khaled Said)
# @contact: kerbrose  ==> hotmail  ==> com
#####################################

class LibraryMember(models.Model):
    _inherit = 'library.member'
    
    loan_duration = fields.Integer('Loan Duration', default=15, required = Trues)