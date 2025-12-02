# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Trường tùy chỉnh cho Lead
    lead_score = fields.Integer(
        string='Điểm Lead',
        default=0,
        help='Điểm số đánh giá chất lượng lead (0-100)'
    )
    
    lead_source_detail = fields.Char(
        string='Chi tiết Nguồn Lead',
        help='Thông tin chi tiết về nguồn lead'
    )
    
    industry_type = fields.Selection([
        ('technology', 'Công nghệ'),
        ('finance', 'Tài chính'),
        ('healthcare', 'Y tế'),
        ('education', 'Giáo dục'),
        ('retail', 'Bán lẻ'),
        ('manufacturing', 'Sản xuất'),
        ('other', 'Khác'),
    ], string='Loại Ngành', default='other')
    
    expected_close_date = fields.Date(
        string='Ngày Đóng Dự kiến',
        help='Ngày dự kiến đóng deal'
    )
    
    probability_custom = fields.Float(
        string='Xác suất Thắng (%)',
        default=10.0,
        help='Xác suất thắng deal (tính bằng phần trăm)'
    )
    
    competitor_info = fields.Text(
        string='Thông tin Đối thủ',
        help='Thông tin về các đối thủ cạnh tranh'
    )
    
    decision_maker = fields.Char(
        string='Người Quyết định',
        help='Tên người có quyền quyết định mua hàng'
    )
    
    budget_confirmed = fields.Boolean(
        string='Ngân sách Đã Xác nhận',
        default=False,
        help='Đánh dấu nếu ngân sách đã được xác nhận'
    )
    
    # Trường computed
    lead_quality = fields.Selection([
        ('hot', 'Nóng'),
        ('warm', 'Ấm'),
        ('cold', 'Lạnh'),
    ], string='Chất lượng Lead', compute='_compute_lead_quality', store=True)
    
    days_in_stage = fields.Integer(
        string='Số Ngày trong Giai đoạn',
        compute='_compute_days_in_stage',
        help='Số ngày lead đã ở trong giai đoạn hiện tại'
    )
    
    # Ràng buộc và validation
    @api.constrains('lead_score')
    def _check_lead_score(self):
        """Kiểm tra điểm lead trong khoảng 0-100"""
        for record in self:
            if record.lead_score < 0 or record.lead_score > 100:
                raise ValidationError('Điểm lead phải nằm trong khoảng 0-100!')
    
    @api.constrains('probability_custom')
    def _check_probability(self):
        """Kiểm tra xác suất trong khoảng 0-100"""
        for record in self:
            if record.probability_custom < 0 or record.probability_custom > 100:
                raise ValidationError('Xác suất phải nằm trong khoảng 0-100%!')
    
    @api.depends('lead_score')
    def _compute_lead_quality(self):
        """Tính toán chất lượng lead dựa trên điểm số"""
        for record in self:
            if record.lead_score >= 70:
                record.lead_quality = 'hot'
            elif record.lead_score >= 40:
                record.lead_quality = 'warm'
            else:
                record.lead_quality = 'cold'
    
    @api.depends('date_last_stage_update', 'stage_id')
    def _compute_days_in_stage(self):
        """Tính số ngày lead đã ở trong giai đoạn hiện tại"""
        today = fields.Date.today()
        for record in self:
            if record.date_last_stage_update:
                delta = today - record.date_last_stage_update
                record.days_in_stage = delta.days
            else:
                record.days_in_stage = 0
    
    def action_calculate_lead_score(self):
        """Tính toán điểm lead tự động dựa trên các tiêu chí"""
        self.ensure_one()
        score = 0
        
        # Điểm cho ngân sách đã xác nhận
        if self.budget_confirmed:
            score += 30
        
        # Điểm cho xác suất
        score += self.probability_custom * 0.5
        
        # Điểm cho người quyết định
        if self.decision_maker:
            score += 20
        
        # Điểm cho ngày đóng dự kiến (càng gần càng tốt)
        if self.expected_close_date:
            today = fields.Date.today()
            days_until_close = (self.expected_close_date - today).days
            if 0 <= days_until_close <= 30:
                score += 20
            elif 31 <= days_until_close <= 60:
                score += 10
        
        # Giới hạn điểm tối đa là 100
        self.lead_score = min(score, 100)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Điểm lead đã được tính toán: {self.lead_score}',
                'type': 'success',
                'sticky': False,
            }
        }

