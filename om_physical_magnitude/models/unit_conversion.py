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
    
    # def check_existance(self, cr, uid, ids, context=None):
    #     self_obj = self.browse(cr, uid, ids[0], context=context)
    #     field1 = self_obj.unitA_id
    #     field2 = self_obj.unitB_id
    #     search_idsA = self.search(cr, uid, [('unitA_id', '=', field1),('unitB_id', '=' , field2)], context=context)
    #     search_idsB = self.search(cr, uid, [('unitB_id', '=', field1),('unitA_id', '=' , field2)], context=context)
    #     res = True
    #     if len(search_ids) > 1 or len(search_idsB) > 1:
    #         res = False
    #     return res
    
    # @api.multi
    # def name(self):
    #     result = []
    #     for conversion in self:
    #         unitA = conversion.unitA.mapped('name')
    #         unitB = conversion.unitB.mapped('name')
    #         name = '%s (%s)' % (unitA, ' - '.join(unitB))
    #         result.append((conversion.id, name))
    #     return result
    
    # _constraints = [(check_existance,'Unit conversion already exist', ['unitA_id','unitB_id'])]
