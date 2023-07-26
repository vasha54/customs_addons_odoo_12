# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StudentStudent(models.Model):
    _name = 'student.student'
    #_inherit = 'mail.thread'
    _description = 'Student Record'
    
    name = fields.Char(string='Name', required=True, track_visibility='always')
    age = fields.Integer(string='Age',track_visibility='onchange')
    photo = fields.Binary(string='Image')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'),('others', 'Others')], string='Gender')
    student_dob = fields.Date(string="Date of Birth")
    student_blood_group = fields.Selection( [('A+', 'A+ve'), ('B+', 'B+ve'), 
                                          ('O+', 'O+ve'), ('AB+', 'AB+ve'),('A-', 'A-ve'), 
                                          ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
                                        string='Blood Group')
    nationality = fields.Many2one('res.country', string='Nationality')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'),   ('cancel', 'Cancelled'), ], required=True, default='draft')
    
    @api.multi
    def button_done(self):   
        for rec in self:       
            rec.write({'state': 'done'})
    
    @api.multi
    def button_cancel(self):   
        for rec in self:       
            rec.write({'state': 'cancel'})
            
    @api.multi
    def button_reset(self):
        for rec in self:       
            rec.state='draft'
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'This Name has already been taken!'),
    ]