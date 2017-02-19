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

class LibraryBook(models.Model):
    _name = 'library.book' # this is the unique id for the model
    _description = 'Library Book' # this is a human readable name
    _order = 'date_release desc, name' 
    _rec_name = 'short_name'  # Alternative field to use as name, used by osv’s name_get() (default: 'name')
    
    author_ids = fields.Many2many('res.partner', string='Authors')
    
    cost_price = fields.Float('Book Cost', dp.get_precision('Book Price'))
    
    cover = fields.Binary('Book Cover')
    
    currency_id = fields.Many2one('res.currency', string='Currency')
    
    date_release = fields.Date('Release Date')
    
    description = fields.Html(string='Description', # optional:
                              sanitize=True,
                              strip_style=False,
                              translate=False,)
    
    date_updated = fields.Datetime('Last Updated')
    
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

    reader_rating = fields.Float( 'Reader Average Rating',
                                  (14, 4), # Optional precision (total, decimals),
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
        for record in self:
            result.append(
                (record.id, u"%s (%s)" % (record.name, record.date_release)
                 ))
        return result
