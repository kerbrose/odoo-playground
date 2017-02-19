# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 All Rights Reserved
#
# Created on Feb 19, 2017
#
# @author: kerbrose (Khaled Said)
# @contact: kerbrose  ==> hotmail  ==> com
#####################################

from odoo import api, models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    book_ids = fields.One2many('library.book', 'publisher_id',
                               string = 'Published Books')
    
    book_ids = fields.Many2many( 'library.book',
                                 string='Authored Books',
                                 # relation='library_book_res_partner_rel'  # optional
                                 )