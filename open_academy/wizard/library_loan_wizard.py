# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 All Rights Reserved
#
# Created on Feb 23, 2017
#
# @author: kerbrose (Khaled Said)
# kerbrose  __hotmail__
###############################################

from odoo import api, models, fields

class LibraryLoanWizard(models.TransientModel):
    _name = 'library.loan.wizard'
    
    book_ids = fields.Many2many('library.book', 'Books')
    
    member_id = fields.Many2one('library.member', 'Member')
    
    @api.multi
    def record_loans(self):
        for wizard in self:
            member = wizard.member_id
            books = wizard.book_ids
            loan = self.env['library.book.loan']
            for book in wizard.book_ids:
                loan.create({'member_id': member.id, 'book_id': book.id})
    
    @api.multi
    def record_borrows(self):
        self.ensure_one()
        member = self.member_id
        books = self.book_ids
        member.borrow_books(books)
        member_ids = self.mapped('member_id').ids
        action = { 'type': 'ir.action.act_window',
                   'name': 'Borrower',
                   'res_model': 'library.member',
                   'domain': [('id', '=', member_ids)],
                   'view_mode': 'form,tree',
                   }
        return action

