# -*- coding: utf-8 -*-
from odoo import models, fields, api

class UnitMeasurment(models.Model):
    _name = 'unit.measurement'
    _description = 'Unit Measurment Record'
    _sql_constraints = [ ('uniq_acronym', 'unique(acronym)', "There is already a unit of measurement with a similar acronym"),]
    
    name = fields.Char(string='Name', required=True, track_visibility='always')
    acronym = fields.Char(string='Acronym', required=True, track_visibility='always')
    physical_magnitude_id = fields.Many2one('physical.magnitude', string='Physical magnitude',ondelete='cascade', required=True)
    main_magnitude = fields.Boolean(string='Main unit of magnitude',default=False)
    
    @api.constrains('main_magnitude')
    def _change_main_magnitude (self):
        if self.main_magnitude:
            units = self.env['unit.measurement'].search([('id', '!=', self.id),('physical_magnitude_id','=',self.physical_magnitude_id.id)])
            for unit in units:
                unit.main_magnitude = False
    