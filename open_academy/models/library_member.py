# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 All Rights Reserved
#
# Created on Feb 20, 2017
#
# @author: kerbrose (Khaled Said)
# @contact: kerbrose  ==> hotmail  ==> com
#####################################

from odoo import api, models, fields

class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner':'partner_id'}
    
    partner_id = fields.Many2one('res.partner',
                             ondelete= 'cascade'
                             )

    date_start = fields.Date('Member Since')
    
    date_end = fields.Date('Termination Date')
    
    member_number = fields.Char()