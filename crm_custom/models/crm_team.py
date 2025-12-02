# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    # Trường tùy chỉnh cho Sales Team
    team_target = fields.Monetary(
        string='Mục tiêu Đội',
        currency_field='company_currency_id',
        help='Mục tiêu doanh số của đội trong kỳ'
    )
    
    current_period_revenue = fields.Monetary(
        string='Doanh thu Kỳ hiện tại',
        currency_field='company_currency_id',
        compute='_compute_period_revenue',
        help='Doanh thu thực tế của đội trong kỳ hiện tại'
    )
    
    company_currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        string='Company Currency',
        readonly=True
    )
    
    target_achievement_rate = fields.Float(
        string='Tỷ lệ Đạt Mục tiêu (%)',
        compute='_compute_target_achievement',
        help='Tỷ lệ đạt mục tiêu của đội'
    )
    
    active_leads_count = fields.Integer(
        string='Số Lead Đang hoạt động',
        compute='_compute_team_stats',
        help='Số lượng lead đang hoạt động của đội'
    )
    
    active_opportunities_count = fields.Integer(
        string='Số Cơ hội Đang hoạt động',
        compute='_compute_team_stats',
        help='Số lượng cơ hội đang hoạt động của đội'
    )
    
    @api.depends('member_ids', 'member_ids.sale_order_ids')
    def _compute_period_revenue(self):
        """Tính doanh thu kỳ hiện tại của đội"""
        for team in self:
            # Lấy tất cả đơn hàng của thành viên đội trong tháng hiện tại
            current_month = fields.Date.today().replace(day=1)
            orders = self.env['sale.order'].search([
                ('user_id', 'in', team.member_ids.ids),
                ('date_order', '>=', current_month),
                ('state', 'in', ['sale', 'done'])
            ])
            team.current_period_revenue = sum(orders.mapped('amount_total'))
    
    @api.depends('team_target', 'current_period_revenue')
    def _compute_target_achievement(self):
        """Tính tỷ lệ đạt mục tiêu"""
        for team in self:
            if team.team_target > 0:
                team.target_achievement_rate = (team.current_period_revenue / team.team_target) * 100
            else:
                team.target_achievement_rate = 0.0
    
    @api.depends('member_ids')
    def _compute_team_stats(self):
        """Tính thống kê lead và cơ hội của đội"""
        for team in self:
            leads = self.env['crm.lead'].search([
                ('team_id', '=', team.id),
                ('active', '=', True)
            ])
            
            team.active_leads_count = len(leads.filtered(lambda l: l.type == 'lead'))
            team.active_opportunities_count = len(leads.filtered(lambda l: l.type == 'opportunity'))

