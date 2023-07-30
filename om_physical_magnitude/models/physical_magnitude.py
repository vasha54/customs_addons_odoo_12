# -*- coding: utf-8 -*-
from odoo import models, fields, api
from . import  functions

class PhysicalMagnitude(models.Model):
    _name = 'physical.magnitude'
    _description = 'Physical magnitude Record'
    _sql_constraints = [ ('uniq_slug', 'unique(slug_name)', "There is already a physical quantity with a similar name"),]
    
    name = fields.Char(string='Name', required=True, track_visibility='always')
    slug_name = fields.Char(string='Slug name',compute='_compute_slug',store=True,compute_sudo=False)
    count_units = fields.Integer(String='Count unit mesaurements',compute='compute_count_units')
    name_main_unit = fields.Char(string='Main unit name',compute='compute_main_units')
    
    
    @api.depends('name')
    def _compute_slug(self):
        for pm in self.filtered('name'):
            pm.slug_name = functions.generateSLUG(pm.name)
    
    @api.multi
    def compute_count_units(self):
        for rec in self:
            units = self.env['unit.measurement'].search([('physical_magnitude_id', '=', rec.id)])
            rec.count_units = len(units)
            
    @api.multi
    def compute_main_units(self):
        for rec in self:
            unit = self.env['unit.measurement'].search([('physical_magnitude_id', '=', rec.id)],limit=1)
            if unit :
                unit = unit[0]
                rec.name_main_unit = unit.name+' ('+unit.acronym+')'
            else:
                rec.name_main_unit = 'There is no defined'
    
    