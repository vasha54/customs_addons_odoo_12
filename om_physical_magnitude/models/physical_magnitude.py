# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
from odoo.modules import get_module_resource
import base64
from . import  functions

class PhysicalMagnitude(models.Model):
    _name = 'physical.magnitude'
    _description = 'Physical magnitude Record'
    _sql_constraints = [ ('uniq_slug', 'unique(slug_name)', "There is already a physical quantity with a similar name"),]
    
    name = fields.Char(string='Name', required=True, track_visibility='always')
    slug_name = fields.Char(string='Slug name',compute='_compute_slug',store=True,compute_sudo=False)
    count_units = fields.Integer(String='Count unit mesaurements',compute='compute_count_units')
    name_main_unit = fields.Char(string='Main unit name',compute='compute_main_units')
    icon = fields.Binary("Icon")
    
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
            unit = self.env['unit.measurement'].search([('physical_magnitude_id', '=', rec.id),('main_magnitude','=',True)],limit=1)
            if unit :
                unit = unit[0]
                rec.name_main_unit = unit.name+' ('+unit.acronym+')'
            else:
                rec.name_main_unit = 'There is no defined'
                
    @api.multi
    def write(self, vals):
        res = super(PhysicalMagnitude, self).write(vals)
        if not self.icon:
            self.icon = self._get_default_icon_value()
        return res
                
    @api.model
    def _get_default_icon_value(self):
        icon = False
        img_path = get_module_resource('om_physical_magnitude', 'static/img', 'logo.png') # your default image path
        if img_path:
            with open(img_path, 'rb') as f: # read the image from the path
                icon = f.read()
        if icon: # if the file type is .jpg then you don't need this whole if condition.
            icon = tools.image_colorize(icon) 
        return tools.image_resize_image_big(base64.b64encode(icon))
    
    @api.model
    def create(self, vals):
        if not vals.get('icon'):
            vals['icon'] = self._get_default_icon_value()
        return super(PhysicalMagnitude, self).create(vals)
    
    