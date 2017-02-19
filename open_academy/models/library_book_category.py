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

class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _parent_store = True
    
    name = fields.Char('Category')
    
    child_ids = fields.One2many('library.book.category',
                                'parent_id',
                                string = 'Child Categories')
    
    parent_id = fields.Many2one('library.book.category',
                                string = 'Parent Category',
                                ondelete = 'restrict',
                                index = True
                                )
    
    parent_left = fields.Integer(index = True)
    
    parent_right = fields.Integer(index = True)
    
    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')