# -*- coding: utf-8 -*-
from odoo import models, fields, api
from . import  functions

class PhysicalMagnitude(models.Model):
    _name = 'physical.magnitude'
    _description = 'Physical magnitude Record'
    _sql_constraints = [ ('uniq_slug', 'unique(slug_name)', "There is already a physical quantity with a similar name"),]
    
    name = fields.Char(string='Name', required=True, track_visibility='always')
    slug_name = fields.Char(string='Slug name',compute='_compute_slug',store=True,compute_sudo=False)
    count_units = fields.Integer(String='Count unit mesaurements',compute='compute_units',store=False,compute_sudo=False)
    
    @api.depends('name')
    def _compute_slug(self):
        for pm in self.filtered('name'):
            pm.slug_name = functions.generateSLUG(pm.name)
    
    @api.one
    def compute_units(self):
        #units = self.env['unit.measurement'].search([('physical_magnitude_id', '=', self)])
        return len([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21])
    
    