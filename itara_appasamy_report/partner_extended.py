# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api
from _dbus_bindings import String
import random
from odoo.exceptions import ValidationError

class supplier_type(models.Model):
    _name = 'supplier.type'

    name = fields.Char(string = 'Name')
    code = fields.Char(string = 'Code')

class hod_type(models.Model):
    _name = 'hod.type'

    name = fields.Char(string = 'Name')
    code = fields.Char(string = 'Code')

# class sub_division(models.Model):
#     _name ='sub.division'
#     _description  ='Sub Division'
#
#     name = fields.Char(string='Subdivision',required=True)
#     subdivision_code = fields.Char(string = 'Code')

class grade_master(models.Model):
    _name ='grade.master'
    _description ='Grade'

    name = fields.Char(string='Grade',required=True)
    grade_code = fields.Char(string = 'Code')

class speciality_master(models.Model):
    _name ='speciality.master'
    _description ='Speciality Master'

    name = fields.Char(string='Speciality',required=True)
    speciality_code = fields.Char(string = 'Code')

class city_master(models.Model):
    _name ='city.master'
    _description ='City Master'

    name = fields.Char(string='City',required=True)

class district_master(models.Model):
    _name ='district.master'
    _description ='District Master'

    name = fields.Char(string='District',required=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True,default=lambda self: self.env['res.company']._company_default_get('area.master'))
    district_code = fields.Char(string = 'District Code')


class area_master(models.Model):
    _name ='area.master'
    _description ='Area Master'

    name = fields.Char(string='Area',required=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True,default=lambda self: self.env['res.company']._company_default_get('area.master'))
    area_code = fields.Char(string = 'Area Code')


ADDRESS_FIELDS = ('street', 'street2', 'zip', 'area_id','district_id', 'state_id', 'country_id')

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string='Email')
    cst = fields.Char(string = 'CST')
    ecc_no = fields.Char(string = 'ECC No')
    range = fields.Char(string = 'Range Division')
    service_tax = fields.Char(string = 'Service Tax')
    central_excise = fields.Char(string = 'Central Excise')
    commodity_code = fields.Char(string = 'Commodity Code as per VAT')
    # subdivision_id = fields.Many2one('sub.division',string='Subdivision Type')
    grade_id = fields.Many2one('grade.master',string = 'Grade Type')
    dl_no = fields.Char(string='DL No 1',required=True)
    dl_no_2 = fields.Char(string='DL No 2',required=True)
    mca_no =fields.Char(string ='MCIA No')
    supplier_type_id = fields.Many2one('supplier.type' , string = 'Supplier Type')
    traiff_no = fields.Char(string='Tariff No')
    st_code = fields.Char(string='ST Code')
    type_1 = fields.Selection([('regular','Regular'),('one_time','One Time')],string='Customer Type',default="regular")
#    sub_division = fields.Char(string="Sub Division")
    speciality_id= fields.Many2one('speciality.master',string='Speciality')
    area_id = fields.Many2one('area.master',string="Area", required=True)
    district_id = fields.Many2one('district.master',string="District", required=True)
    date =  fields.Date('Date',default=fields.Date.context_today)
    hod_id = fields.Many2one('hod.type',string='Department')
    branch_id = fields.Many2one('res.partner.branch', string="Branch Name", required=True)
    zone_id = fields.Many2one('res.partner.zone', string="Zone")
    city_id = fields.Many2one('city.master',string="City")



    _sql_constraints = [
        ('partner_unique', 'unique(name)', 'Name must be Unique!'),
    ]

    @api.multi
    def onchange_section_id(self,section_id):
        vals = {}
        user = []
        if section_id:
            sec = self.env['crm.case.section'].browse(section_id)
            for sec_line in sec.member_ids:
                user.append(sec_line.id)
        domain = [('id','=', user)]
        vals = {'domain': {'user_id' : domain}, 'value' : {'user_id' : False}}
        return vals

class res_partner_branch(models.Model):
    _name = "res.partner.branch"

    name = fields.Char(string="Branch Name")

class res_partner_zone(models.Model):
    _name = "res.partner.zone"

    name = fields.Char(string="Zone Name")
