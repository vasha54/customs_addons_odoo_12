# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UnitConversion(models.Model):
    """Class in charge of representing in the database schema the entity in 
    charge of storing the conversions between the units that belong to the same 
    physical magnitude. For each conversion is stored:
    - The two measurement units involved in the conversion (let's call them 
     unit A and unit B)
    - The value that represents a unit of A converted to unit B.
    
    In the same way, the value of converting a unit of B into the unit A is 
    stored and calculated. 
    """
    _name = 'unit.conversion'
    _description = 'Unit Conversion Record'
    
    
    unitA_id = fields.Many2one('unit.measurement',
                               string='Unit A',
                               ondelete='cascade',
                               required=True,
                               index=True)
    unitB_id = fields.Many2one('unit.measurement',
                               string='Unit B',
                               ondelete='cascade',
                               required=True,
                               index=True)
    conversion_one_A_to_B = fields.Float(string='A unit of A is equivalent to B',
                                         digits = (12,6))
    conversion_one_B_to_A = fields.Float(string='A unit of B is equivalent to A',
                                         compute='_compute_conversion',
                                         store=True,
                                         compute_sudo=False,
                                         digits = (12,6))
    
    
    @api.depends('conversion_one_A_to_B')
    def _compute_conversion(self):
        """Method in charge of calculating for the conversion how much a unit 
        of B is equivalent to A from knowing what a unit of A is equivalent to 
        in B.
        """
        for rec in self.filtered('conversion_one_A_to_B'):
            rec.conversion_one_B_to_A = float(1.0000)/rec.conversion_one_A_to_B
            
    
    @api.constrains('unitA_id','unitB_id')
    def _check_existance_conversion(self):
        """Method in charge of checking whether or not there is a conversion 
        between the units

        Raises:
            models.ValidationError: If the conversion between the units already 
            exists, it throws an exception notifying the error. 
        """
        entity_um = self.env['unit.conversion']
        
        if entity_um != None:
            combA = entity_um.search([('id','!=',self.id),
                                      ('unitA_id','=',self.unitA_id.id),
                                      ('unitB_id','=',self.unitB_id.id)])
            
            combB = entity_um.search([('id','!=',self.id),
                                      ('unitB_id','=',self.unitA_id.id),
                                      ('unitA_id','=',self.unitB_id.id)])
            if len(combA) > 0 or len(combB):
                raise models.ValidationError('This conversion already exists')
    

    @api.constrains('unitA_id','unitB_id')
    def _check_conversion_between_units_same_magnitude(self):
        """Method in charge of verifying that the conversion is carried out 
        between two units associated with the same physical magnitude.

        Raises:
            models.ValidationError: If the conversion is between two units of 
            different physical magnitudes, it throws an exception notifying 
            the error.
        """
        
        id_magnitude_unit_a = self.unitA_id.physical_magnitude_id.id
        id_magnitude_unit_b = self.unitB_id.physical_magnitude_id.id
        
        if id_magnitude_unit_a != id_magnitude_unit_b:
            raise models.ValidationError("It is not possible to establish "
                                         "conversion between measurement units "
                                         "of different physical magnitudes")
            
 
    @api.constrains('unitA_id','unitB_id')  
    def _check_conversion_between_units_different(self):
        """Method in charge of verifying that the conversion is carried out 
        between two units that are different from each other.

        Raises:
            models.ValidationError: If the conversion is done with the same 
            unit, an exception is thrown notifying the error
        """
        id_unit_a = self.unitA_id.id
        id_unit_b = self.unitB_id.id
        
        if id_unit_a == id_unit_b:
            raise models.ValidationError("It is not possible to establish "
                                         "conversion between the same "
                                         "measurement units")
 
    
    @api.constrains('conversion_one_A_to_B')
    def _check_value_conversion_a_to_b(self) :
        """Method in charge of checking that the value of the conversion from 
        unit A to unit B is greater than zero.

        Raises:
            models.ValidationError: If the value is greater than zero it 
            throws an exception notifying the error
        """
        if self.conversion_one_A_to_B <= 0:
            raise models.ValidationError('The value must be greater than zero.')
        
    