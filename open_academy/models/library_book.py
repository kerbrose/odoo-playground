# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 All Rights Reserved
#
# Created on Feb 1, 2017
#
# @author: kerbrose
#####################################

from odoo import api, models, fields
from odoo.addons import decimal_precision as dp
from odoo.fields import Date as fDate
from datetime import timedelta as td

class LibraryBook(models.Model):
    _name = 'library.book' # this is the unique id for the model
    _description = 'Library Book' # this is a human readable name
    _inherit = ['base.archive']
    _order = 'date_release desc, name' 
    _rec_name = 'short_name'  # Alternative field to use as name, used by osv’s name_get() (default: 'name')
    _sql_constraints = [('name_uniq',
                         'UNIQUE (name)',
                         'Book title must be unique.')
]
    age_days = fields.Float(string = 'Days Since Release',
                            compute = '_compute_age',
                            inverse = '_inverse_age',
                            search = '_search_age',
                            store = False,
                            compute_sudo= False,
                            )
    
    author_ids = fields.Many2many('res.partner', string='Authors')
    
    cost_price = fields.Float('Book Cost', dp.get_precision('Book Price'))
    
    cover = fields.Binary('Book Cover')
    
    currency_id = fields.Many2one('res.currency', string='Currency')
    
    date_release = fields.Date('Release Date')
    
    date_updated = fields.Datetime('Last Updated')
    
    description = fields.Html(string='Description', # optional:
                              sanitize=True,
                              strip_style=False,
                              translate=False,)
    
    isbn = fields.Char('ISBN')
    
    manager_remarks = fields.Text('Manager Remarks')
    
    name = fields.Char('Title', required=True)
    
    notes = fields.Text('Internal Notes')
    
    out_of_print = fields.Boolean('Out of Print?')
    
    pages = fields.Integer( string='Number of Pages',
                            default=0,
                            help='Total book pages count',
                            groups='base.group_user',
                            states={'cancel': [('readonly', True)]},
                            copy=True,
                            index=False,
                            readonly=False,
                            required=False,
                            company_dependent=False,)
    
    publisher_id = fields.Many2one('res.partner',
                                  string = 'Publisher',
                                  # optional
                                  ondelete = 'set null',
                                  context = {},
                                  domain = [],
                                  )

    publisher_city = fields.Char('Publisher City',
                                 related = 'publisher_id.city')
    
    reader_rating = fields.Float( 'Reader Average Rating',
                                  (14, 4), # Optional precision (total, decimals),
                                  )
    
    ref_doc_id = fields.Reference(selection = '_referencable_models',
                                  string='Reference Document'
                                  )

    retail_price = fields.Monetary('Retail Price',
                                   currency_field = 'currency_id', # Optional
                                   )
    
    short_name = fields.Char(string='Short Title',
                             size=100, # For Char only
                             translate=False, # also for Text fields
                             )
    
    state = fields.Selection([('draft', 'Not Available'), 
                              ('available', 'Available'), 
                              ('lost', 'Lost')],
                             'State')


    @api.multi
    def name_get(self):
        result = []
        for book in self:
            authors = book.author_ids.mapped('name')
            name = u'%s (%s)' % (book.title, u', '.join(authors))
            result.append((book.id, name))
        return result

    @api.constrains('date_release')
    def _check_release_date(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the past')

    @api.depends
    def _compute_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            delta = (fDate.from_string(book.date_release - today))
            book.age_days = delta.days

    def _inverse_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            d = td(days=book.age_days) - today
            book.date_release = fDate.to_string(d)

    def _search_age(self, operator, value):
        today = fDate.from_string(fDate.today())
        value_days = td(days=value)
        value_date = fDate.to_string(today - value_days)
        return [('date_release', operator, value_date)]
    
    @api.model
    def _referencable_models(self):
        models = self.env['res.request.link'].search([])
        return [(x.object, x.name) for x in models]

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed =  [('draft', 'available'),
                    ('available', 'borrowed'),
                    ('borrowed', 'available'),
                    ('available', 'lost'),
                    ('lost', 'available')]
        return (old_state, new_state) in allowed
    
    @api.multi
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                continue
    
    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        if not self.user_has_groups('library.group_library_manager'):
            if 'manager_remarks' in values:
                raise exceptions.UserError( 'You are not allowed to modify', 'manager_remarks')
        return super(LibraryBook, self).create(values)
    
    @api.multi
    def write(self, values):
        if not self.user_has_groups('library.group_library_manager'):
            if 'manager_remarks' in values:
                raise exceptions.UserError('You are not allowed to modify', 'manager_remarks')
        return super(LibraryBook, self).write(values)
    
    @api.model
    def fields_get(self, allfields=None, write_access=True, attributes=None):
        fields = super(LibraryBook, self).fields_get(
            allfields=allfields,
            write_access=write_access,
            attributes=attributes
            )
        if not self.user_has_groups('library.group_library_manager'):
            if 'manager_remarks' in fields:
                fields['manager_remarks']['readonly'] = True

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()
        if not(name == '' and operator == 'ilike'):
            args += ['|', '|',
                     ('name', operator, name),
                     ('isbn', operator, name),
                     ('author_ids.name', operator, name)
                     ]
        return super(LibraryBook, self)._name_search( name='',
                                                      args=args,
                                                      operator='ilike',
                                                      limit=limit,
                                                      name_get_uid=name_get_uid)
        


