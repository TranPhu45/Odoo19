# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Trường tùy chỉnh cho Partner/Contact
    customer_segment = fields.Selection([
        ('enterprise', 'Doanh nghiệp'),
        ('sme', 'Doanh nghiệp vừa và nhỏ'),
        ('startup', 'Khởi nghiệp'),
        ('individual', 'Cá nhân'),
    ], string='Phân khúc Khách hàng', default='sme')
    
    customer_lifetime_value = fields.Monetary(
        string='Giá trị Vòng đời Khách hàng',
        currency_field='company_currency_id',
        compute='_compute_customer_lifetime_value',
        help='Tổng giá trị khách hàng mang lại trong suốt thời gian hợp tác'
    )
    
    company_currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        string='Company Currency',
        readonly=True
    )
    
    first_contact_date = fields.Date(
        string='Ngày Liên hệ Đầu tiên',
        help='Ngày đầu tiên liên hệ với khách hàng này'
    )
    
    last_purchase_date = fields.Date(
        string='Ngày Mua Hàng Cuối',
        compute='_compute_last_purchase_date',
        help='Ngày mua hàng gần nhất'
    )
    
    total_opportunities = fields.Integer(
        string='Tổng số Cơ hội',
        compute='_compute_opportunity_stats',
        help='Tổng số cơ hội liên quan đến khách hàng này'
    )
    
    won_opportunities = fields.Integer(
        string='Cơ hội Thắng',
        compute='_compute_opportunity_stats',
        help='Số cơ hội đã thắng'
    )
    
    lost_opportunities = fields.Integer(
        string='Cơ hội Thua',
        compute='_compute_opportunity_stats',
        help='Số cơ hội đã thua'
    )
    
    win_rate = fields.Float(
        string='Tỷ lệ Thắng (%)',
        compute='_compute_opportunity_stats',
        help='Tỷ lệ thắng cơ hội (tính bằng phần trăm)'
    )
    
    preferred_contact_method = fields.Selection([
        ('email', 'Email'),
        ('phone', 'Điện thoại'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('in_person', 'Gặp trực tiếp'),
    ], string='Phương thức Liên hệ Ưa thích', default='email')
    
    notes = fields.Text(
        string='Ghi chú',
        help='Ghi chú bổ sung về khách hàng'
    )
    
    @api.depends('sale_order_ids', 'sale_order_ids.amount_total')
    def _compute_customer_lifetime_value(self):
        """Tính giá trị vòng đời khách hàng từ các đơn hàng"""
        for partner in self:
            orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ['sale', 'done'])
            ])
            partner.customer_lifetime_value = sum(orders.mapped('amount_total'))
    
    @api.depends('sale_order_ids', 'sale_order_ids.date_order')
    def _compute_last_purchase_date(self):
        """Tính ngày mua hàng cuối cùng"""
        for partner in self:
            orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ['sale', 'done'])
            ], order='date_order desc', limit=1)
            partner.last_purchase_date = orders.date_order if orders else False
    
    @api.depends('opportunity_ids')
    def _compute_opportunity_stats(self):
        """Tính thống kê cơ hội cho khách hàng"""
        for partner in self:
            opportunities = self.env['crm.lead'].search([
                ('partner_id', '=', partner.id),
                ('type', '=', 'opportunity')
            ])
            
            partner.total_opportunities = len(opportunities)
            partner.won_opportunities = len(opportunities.filtered(lambda o: o.probability == 100))
            partner.lost_opportunities = len(opportunities.filtered(lambda o: o.probability == 0))
            
            if partner.total_opportunities > 0:
                partner.win_rate = (partner.won_opportunities / partner.total_opportunities) * 100
            else:
                partner.win_rate = 0.0

