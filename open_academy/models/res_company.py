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

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    @api.multi
    def update_phone_number(self, new_number):
        self.ensure_one()
        company_as_superuser = self.sudo()
        company_as_superuser.phone = new_number