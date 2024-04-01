from fpdf import FPDF


class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Sales Report', align='C', ln=True)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, align='L', ln=True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()


def generate_sales_report(orders):
    pdf = PDFReport()
    pdf.add_page()

    pdf.chapter_title('Completed Orders')

    for order in orders:
        order_details = f"Customer Name: {order['customer_name']}\nStatus: {order['status']}\nDate: " \
                        f"{order['created_at']}\nProduct: ${order['product_id']}\nQuantity: ${order['quantity']}\n" \
                        f"Total Sum: {order['total_price']}"
        pdf.chapter_body(order_details)

    return pdf
