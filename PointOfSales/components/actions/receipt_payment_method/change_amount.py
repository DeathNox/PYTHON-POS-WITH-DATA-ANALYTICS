import unittest
from unittest.mock import patch, MagicMock
import customtkinter as ctk
import tkinter as tk
from PointOfSales.components.actions.receipt_payment_method.modal_cash_payment import show_cash_payment_modal

class TestShowCashPaymentModal(unittest.TestCase):

    @patch('PointOfSales.components.actions.receipt_payment_method.modal_cash_payment.db')
    @patch('PointOfSales.components.actions.receipt_payment_method.modal_cash_payment.mycursor')
    def test_show_cash_payment_modal(self, mock_db, mock_cursor):
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        orders_total = 100.0
        show_cash_payment_modal(orders_total)

        # Get the modal window
        modal = root.winfo_children()[0]
        self.assertEqual(modal.title(), "Cash Payment")

        # Check the total amount label
        total_amount_label = modal.nametowidget('.!ctktoplevel.!ctkframe.!ctkframe.!ctklabel2')
        self.assertEqual(total_amount_label.cget("text"), "PHP 100.00")

        # Simulate entering amount received
        amount_received_entry = modal.nametowidget('.!ctktoplevel.!ctkframe.!ctkframe.!ctkentry')
        amount_received_entry.insert(0, "150.00")
        amount_received_entry.event_generate('<Return>')

        # Check the change amount label
        change_amount_lbl = modal.nametowidget('.!ctktoplevel.!ctkframe.!ctkframe.!ctklabel3')
        self.assertEqual(change_amount_lbl.cget("text"), "50.00")

        # Simulate clicking the confirm payment button
        confirm_payment_btn = modal.nametowidget('.!ctktoplevel.!ctkframe.!ctkframe.!ctkbutton2')
        confirm_payment_btn.invoke()

   

        root.destroy()

if __name__ == '__main__':
    unittest.main()