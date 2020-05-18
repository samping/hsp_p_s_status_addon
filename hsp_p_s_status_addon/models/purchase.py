from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging


_logger = logging.getLogger(__name__)


class purchase_order(models.Model):
    _inherit = "purchase.order"

    hsp_move_status = fields.Selection([('no','未收货'),('part_ship','部分收货'),('shipped','全部收货')],string='发收情况',default='no',compute='_compute_hsp_move_status')
    hsp_invoice_status = fields.Selection([('no','未收发票'),('invoiced','已收发票')],string='发票情况',default='no',compute='_compute_hsp_invoice_status')
    hsp_payment_status = fields.Selection([('no','未完成付款'),('part_payment','部分付款'),('paymented','已付款')],string='付款情况',default='no',compute='_compute_hsp_payment_status')

    hsp_invoice_date = fields.Date(string='发票日期')
    hsp_invoice_ref = fields.Char(string='发票参考')

    def _compute_hsp_move_status(self):
        for purchase in self:
            tem_qty = 0
            tem_qty_received = 0
            for line in purchase.order_line:
                tem_qty = tem_qty + line.product_qty
                tem_qty_received = tem_qty_received + line.qty_received
            if tem_qty_received == 0 :
                purchase.hsp_move_status = 'no'
            elif tem_qty_received < tem_qty:
                purchase.hsp_move_status = 'part_ship'
            elif tem_qty_received == tem_qty:
                purchase.hsp_move_status = 'shipped'

    def _compute_hsp_payment_status(self):
        for purchase in self:
            for line in purchase.order_line:
                tem_qty = 0
                tem_qty_invoiced = 0
                for line in purchase.order_line:
                    tem_qty = tem_qty + line.product_qty
                    tem_qty_invoiced = tem_qty_invoiced + line.qty_invoiced
                if tem_qty_invoiced < tem_qty:
                    purchase.hsp_payment_status = 'no'
                elif tem_qty_invoiced == tem_qty:
                    purchase.hsp_payment_status = 'paymented'
                    invoice_ids = self.env['account.invoice'].sudo().search([('origin','=',purchase.name)])
                    for invoice in invoice_ids:
                        if invoice.state == 'open' or invoice.state == 'in_payment':
                            purchase.hsp_payment_status = 'no'

    def _compute_hsp_invoice_status(self):
        for purchase in self:
            if purchase.hsp_invoice_date:
                purchase.hsp_invoice_status='invoiced'
            else:
                purchase.hsp_invoice_status='no'

# class purchase_order_line(models.Model):
#     _inherit = "purchase.order.line"

#     hsp_payment_status = 