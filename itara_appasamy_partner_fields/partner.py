import json
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang

from odoo.exceptions import UserError, RedirectWarning, ValidationError

import odoo.addons.decimal_precision as dp


class res_partner(models.Model):
    _inherit = "res.partner"
    
    @api.onchange('section_id')
    def onchange_section_id(self):
        user = []
        if self.section_id:
            sec = self.env['crm.team'].browse(self.section_id.id)
            for sec_line in sec.member_ids:
                user.append(sec_line.id)
        domain = [('id','=', user)]
        vals = {'domain': {'user_id' : domain}, 'value' : {'user_id' : False}}
        return vals

    sub_division_id = fields.Many2one("res.partner.sub.division", index=True, ondelete='cascade')
    designation_id = fields.Many2one("res.partner.designation", index=True, ondelete='cascade')
    grade_type = fields.Many2one("res.partner.grade", string="Grade Type")
    buyer_dl = fields.Char(string="DL No 1")
    buyer_dl2 = fields.Char(string="DL No 2")
    buyer_mci = fields.Char(string="MCI No")
    pan = fields.Char(string="PAN")
    partner_type = fields.Selection([('regular', 'Regular'),('onetime', 'One Time')], string="Customer Type")
    site_code = fields.Char(string="Site Code")
    section_id = fields.Many2one('crm.team', "Sales Team")
    group_customer_no = fields.Char(string="Group Customer Number")
    category = fields.Char(string="Category", required=True)
    customer_creation_date = fields.Date(string="Customer Creation Date")

class res_partner_grade(models.Model):
    _name = "res.partner.grade"

    name = fields.Char(string="Grade Name")
    grade_code = fields.Char(string="Grade Code")

class res_partner_sub_division(models.Model):
    _name = "res.partner.sub.division"

    name = fields.Char(string="Sub Division Name")
    sub_division_code = fields.Char(string="Sub Division Code")

class res_partner_designation(models.Model):
    _name = "res.partner.designation"

    name = fields.Char(string="Designation Name")
    designation_code = fields.Char(string="Designation Code")


