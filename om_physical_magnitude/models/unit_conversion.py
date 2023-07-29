# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UnitConversion(models.Model):
    _name = 'unit.conversion'
    _description = 'Unit Conversion Record'
    
    
    unitA_id = fields.Many2one('unit.measurement', string='Unit A',ondelete='cascade', required=True,index=True)
    unitB_id = fields.Many2one('unit.measurement', string='Unit B',ondelete='cascade', required=True,index=True)
    conversion_one_A_to_B = fields.Float( string='A unit of A is equivalent to B',digits = (12,6))
    conversion_one_B_to_A = fields.Float( string='A unit of B is equivalent to A',
                                         compute='_compute_conversion',store=True,compute_sudo=False,
                                         digits = (12,6))
    
    
    @api.depends('conversion_one_A_to_B')
    def _compute_conversion(self):
        for rec in self.filtered('conversion_one_A_to_B'):
            rec.conversion_one_B_to_A = float(1.0000)/rec.conversion_one_A_to_B
            
    @api.constrains('unitA_id','unitB_id')
    def check_existance_conversion(self):
        combA = self.env['unit.conversion'].search([('id', '!=', self.id),
                                                    ('unitA_id','=',self.unitA_id.id),
                                                    ('unitB_id','=',self.unitB_id.id)])
        combB = self.env['unit.conversion'].search([('id', '!=', self.id),
                                                    ('unitB_id','=',self.unitA_id.id),
                                                    ('unitA_id','=',self.unitB_id.id)])
        if len(combA) > 0 or len(combB):
            raise models.ValidationError('This conversion already exists')
        
        if self.unitA_id.physical_magnitude_id.id != self.unitB_id.physical_magnitude_id.id:
            raise models.ValidationError('It is not possible to establish conversion between measurement units of different physical magnitudes')
            
    
    @api.constrains('conversion_one_A_to_B')
    def check_value(self) :
        if self.conversion_one_A_to_B == 0:
            raise models.ValidationError('The value must be greater than zero.')
        
    