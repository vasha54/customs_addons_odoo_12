# -*- coding: utf-8 -*-
from odoo import models, fields, api


class UnitMeasurment(models.Model):
    """Class that represents in the database schema the entity in charge of
    storing the measurement units. The following data is stored for each unit
    of measure:
     - Name
     - Physical magnitude to which it is associated
     - Whether or not it will be the main unit of the physical magnitude to
     which it is associated
     - Acronym of the unit that must be unique
    """
    _name = 'unit.measurement'
    _description = 'Unit Measurment Record'
    
    
    _sql_constraints = [ 
                        ('uniq_acronym', 
                         'unique(acronym)', 
                         "There is already a unit of measurement with a similar"
                         " acronym")
                        ]
    
    
    name = fields.Char(string='Name',
                       required=True,
                       track_visibility='always')
    acronym = fields.Char(string='Acronym',
                          required=True,
                          track_visibility='always')
    physical_magnitude_id = fields.Many2one('physical.magnitude',
                                            string='Physical magnitude',
                                            ondelete='cascade',
                                            required=True)
    main_magnitude = fields.Boolean(string='Main unit of magnitude',
                                    default=False)
    
    
    @api.constrains('main_magnitude')
    def _change_main_magnitude (self):
        """Method in charge of when a measurement unit is selected as the main 
        unit of the physical magnitude to which it is associated, change the 
        value of the main_magnitude field to False to the rest of the units 
        associated with the same physical magnitude.
        """
        entity_um = self.env['unit.measurement']
        if self.main_magnitude and entity_um:
            units = entity_um.search(
                [
                    ('id', '!=', self.id),
                    ('physical_magnitude_id','=',self.physical_magnitude_id.id)
                ])
            for unit in units:
                unit.main_magnitude = False
    