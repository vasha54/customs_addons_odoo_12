# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
from odoo.modules import get_module_resource
from . import  functions

import base64


class PhysicalMagnitude(models.Model):
    """Class that represents in the database schema the entity in charge of 
    storing the physical magnitudes. The following data is recorded for each 
    physical magnitude:
     - Name
     - Icon that represents the magnitude
     
     In addition to each physical magnitude, the number of measurement units 
     associated with it is determined, as well as the main unit of the 
     magnitude. In the same way, a unique alphanumeric key (slug) is determined
     from the name of the quantity in order to avoid physical quantities with
     similar names.  
    """

    _name = 'physical.magnitude'
    _description = 'Physical magnitude Record'
    
    _sql_constraints = [ 
                        ('uniq_slug',
                         'unique(slug_name)',
                         "There is already a physical quantity with a similar "
                         "name")
                        ]
    
    name = fields.Char(string='Name',
                       required=True,
                       track_visibility='always')
    icon = fields.Binary("Icon")
    slug_name = fields.Char(string='Slug name',
                            compute='_compute_slug',
                            store=True,
                            compute_sudo=False)
    count_units = fields.Integer(String='Count unit mesaurements',
                                 compute='_compute_count_units')
    name_main_unit = fields.Char(string='Main unit name',
                                 compute='_compute_main_units')
    
    
    @api.depends('name')
    def _compute_slug(self):
        """Method in charge of assigning the value of slug to a physical 
        magnitude from its name.
        """
        for pm in self.filtered('name'):
            pm.slug_name = functions.generateSLUG(pm.name)
    
    @api.multi
    def _compute_count_units(self):
        """Method in charge of determining the number of measurement units 
        associated with the physical magnitude
        """
        entity_um = None
        entity_um = self.env['unit.measurement']
        for rec in self:
            units =[]
            if entity_um != None:
                units = entity_um.search([('physical_magnitude_id','=',rec.id)])
            rec.count_units = len(units)
            
    @api.multi
    def _compute_main_units(self):
        """Method in charge of determining the main unit of measurement of the 
        physical magnitude in case it is defined.
        """
        entity_um = None
        entity_um = self.env['unit.measurement']
        for rec in self:
            
            filters = [
                ('physical_magnitude_id','=',rec.id),
                ('main_magnitude','=',True)
                ]
            
            units = entity_um.search(filters,limit=1)
            
            if units and  len(units) > 0 :
                unit = units[0]
                rec.name_main_unit = unit.name+' ('+unit.acronym+')'
            else:
                rec.name_main_unit = 'There is no defined'
                
    @api.multi
    def write(self, vals):
        """Redefining the write method so that in the event that the physical 
        magnitude has not been defined an icon, one is assigned by default

        Args:
            vals (dict): Dictionary with the values that define the physical 
            magnitude

        Returns:
            PhysicalMagnitude: instance of Physical Magnitude from the values 
            passed by parameters. 
        """
        res = super(PhysicalMagnitude, self).write(vals)
        if not self.icon:
            self.icon = self._get_default_icon_value()
        return res
    
    
    @api.multi
    def show_units_measurements(self):
        """Method in charge of displaying a tree-type view that shows the 
        measurement units associated with this physical magnitude.

        Returns:
            dict: Dictionary with the values to visualize the data
        """
        return {
            'name': self.name+'\'s units of measurement',
            'domain': [('physical_magnitude_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'unit.measurement',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }
        
    @api.multi
    def add_units_measurements(self):
        """Method in charge of displaying a form to record a unit of measure 
        associated with the physical magnitude

        Returns:
            dict: Dictionary with the values to visualize the data
        """
        return {
            'name': 'Add unit of measurement',
            'view_type': 'form',
            'res_model': 'unit.measurement',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window'
        }
    
                
    @api.model
    def _get_default_icon_value(self):
        """Method in charge of creating a default icon for those physical
        magnitudes that were not defined for it

        Returns:
            Image: Default icon image
        """
        icon = None
        img_path = get_module_resource(
            'om_physical_magnitude',
            'static/img',
            'logo.png') 
        
        if img_path:
            with open(img_path, 'rb') as f:
                icon = f.read()
        
        if icon:
            icon = tools.image_colorize(icon) 
        return tools.image_resize_image_big(base64.b64encode(icon))
    
    @api.model
    def create(self, vals):
        """Redefining the create method so that in the event that the physical
        magnitude has not been defined an icon, one is assigned by default

        Args:
            vals (dict): Dictionary with the values that define the physical 
            magnitude

        Returns:
            PhysicalMagnitude: instance of Physical Magnitude from the values 
            passed by parameters. 
        """
        if not vals.get('icon'):
            vals['icon'] = self._get_default_icon_value()
        return super(PhysicalMagnitude, self).create(vals)  