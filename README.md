# Flask Invoice Generator

A self-hosted invoicing tool for small businesses and freelancers. Fill out a form, preview the generated PDF in your browser, then download it or email it directly to the client — all without touching a third-party service.

## Features

- **PDF generation** — professional invoices built programmatically with ReportLab: custom typography, accent colors, itemized labor and materials, and auto-calculated totals
- **Client database** — persistent SQLite store with full CRUD; add, edit, or delete clients via modal dialogs without leaving the page
- **Live preview** — invoices render in an embedded browser PDF viewer before you commit, so you can catch mistakes without wasting an invoice number
- **Email delivery** — sends the PDF as an attachment via Gmail SMTP with a single click; no invoice number is consumed until the invoice is actually downloaded or sent
- **Draft persistence** — the form saves your in-progress work to `sessionStorage` so navigating back from the preview restores exactly what you had
- **Business setup flow** — first-run wizard prompts for company name, address, and phone; all of that info is stamped onto every invoice automatically

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python · Flask |
| PDF generation | ReportLab |
| Database | SQLite (via Python's built-in `sqlite3`) |
| Email | `smtplib` / `EmailMessage` over Gmail SMTP SSL |
| Frontend | Jinja2 templates · Vanilla JS (Fetch API) · Custom CSS |
| Config | python-dotenv |

No frontend framework, no ORM, no external PDF service — just the standard library and a few focused packages.

## Getting Started

**1. Clone and install**

```bash
git clone <repo-url>
cd flaskInvoice
pip install -r requirements.txt
```

**2. Configure email** *(optional — only needed to send invoices by email)*

Create a `.env` file in the project root:

```
EMAIL_USER=your_gmail_address@gmail.com
EMAIL_PASS=your_gmail_app_password
```

Gmail requires an [App Password](https://support.google.com/accounts/answer/185833), not your regular account password. If you skip this step, invoices can still be downloaded as PDFs.

**3. Run**

```bash
python app.py
```

Open `http://localhost:5000`. On first launch you will be walked through a one-time setup to enter your business information.

## How It Works

1. Select or create a client, fill in the work description, materials, and pricing, then click **Generate Invoice**.
2. The server builds the PDF in memory and issues a short-lived token tied to that invoice.
3. The preview page loads the PDF directly in the browser using that token.
4. Clicking **Download** or **Email** finalizes the invoice and increments the invoice counter. Navigating away without doing either discards it, keeping your numbering clean.
