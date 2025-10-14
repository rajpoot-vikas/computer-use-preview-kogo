

EXTRACTION_PROMPT_V1 = """
You are a precise document extraction agent. Extract the following fields from the tax bill document. Return values exactly as they appear in the document.

EXTRACTION FIELDS:

1. ParcelNumber - The parcel/property identifier as printed (e.g., "BLOCK 286 LOT 5", "10-24-307-004")
    - Also known as: Parcel Number, Parcel No., Parcel #, Parcel ID, APN, PIN, Tax ID, GEO ID, MAP NO, Map/Parcel, Schedule No., AIN, Account No., Account Number, Bill Number (only if used by the jurisdiction as the parcel identifier)

    - Capture rules:
        - Use the parcel identifier explicitly printed for the selected record (same row/box/coupon as the chosen TotalDue/DueDate for that line).
        - Prefer identifiers labeled or positioned as the primary parcel ID for the tax line. If multiple identifiers are present, priority:
            1) Parcel Number / PIN / APN / AIN / Tax ID / Geo ID / Map-Parcel
            2) Schedule No. / Account No. (only if clearly used as the parcel identifier for this bill and no separate parcel/PIN/APN is provided)
            3) Bill/Statement Number only if the bill explicitly uses it as the parcel identifier and no other parcel-like ID is present.
        - Accept any printed form: digits, letters, hyphens, slashes, dots, spaces, block/lot/qual formats (e.g., "BLOCK 286 LOT 5", "123-A-45.00", "10 24 307 004 0000").
        - Strip label text but preserve the value exactly (e.g., "PIN: 10-24-307-004-0000" => "10-24-307-004-0000", "Parcel # 123-456" => "123-456").
        - Preserve leading zeros and internal punctuation; do not normalize, reformat, or infer characters (no O↔0 or I↔1 corrections).
        - If the jurisdiction prints the parcel as components (e.g., "BLOCK 286", "LOT 5", optional "QUAL C0001") and no single combined ID appears, concatenate the components in printed order separated by single spaces (e.g., "BLOCK 286 LOT 5 QUAL C0001").
        - If the document lists multiple parcels/rows, return the identifier tied to the selected line/coupon only. If the applicable line cannot be determined unambiguously, return null.
        - Use the human-readable text printed on the bill; ignore barcodes/QR codes unless their human-readable value is printed.

    - Exclusions:
        - Do not return owner names, situs/mailing addresses, legal descriptions, subdivision/plat names, tax district/levy codes, control numbers, receipt/payment IDs, confirmation numbers, cashier/session IDs.
        - Do not return account-level or multi-parcel identifiers when they cannot be tied unambiguously to the selected line.
        - Do not return Bill/Statement/Invoice numbers if a separate parcel/PIN/APN/Tax ID is present.

    - Normalization:
        - Return exactly as printed (preserve casing, spacing, hyphens, slashes, periods).
        - Trim leading/trailing whitespace and remove label prefixes only (e.g., "APN:", "PIN", "Parcel #").
        - If the value wraps across lines, join wrapped lines with a single space.

    - Examples:
        - "Parcel Number: 10-24-307-004-0000" => "10-24-307-004-0000"
        - "PIN 10 24 307 004 0000" => "10 24 307 004 0000"
        - "MAP NO 123-A-45.00" => "123-A-45.00"
        - "BLOCK 286 LOT 5" => "BLOCK 286 LOT 5"
        - "AIN: 1234-567-890" => "1234-567-890"

    - If not visible or ambiguous after applying these rules, return null.

2. TaxYear - The four-digit levy year the tax applies to (e.g., "2025")

    - Also known as: Tax Year, Levy Year, Tax Period, Fiscal Year (FY), Year Ending, Assessment Year (AY), TY, AY

    - Capture rules:
        - Use the year explicitly labeled for the selected ParcelNumber/Installment line or its header section.
        - Priority when multiple labels exist: "Levy Year" > "Tax Year" > "Tax Period/Fiscal Year" > "Year Ending".
        - Ranges/periods:
            - If shown as a span/range (e.g., "2023-2024", "FY 2023/24", "Tax Period: 07/01/2023–06/30/2024"), return the starting year ("2023").
            - If explicitly labeled "Year Ending" or "Year Ended" (e.g., "Year Ending 06/30/2024"), return the ending year ("2024").
        - Phrases like "2023 PAY 2024", "Payable 2024", "Pay in 2024": return the levy/tax year ("2023").
        - When multiple years appear on the document, select the one tied to the same line/box/section as the chosen TotalDue/DueDate for the selected record; if not unambiguously tied, return null.
        - Exclude non-tax years: due/discount/delinquent dates, bill/print/statement dates, receipt/payment dates, penalty schedules, ordinance/statute years, and website/version years.

    - Normalization:
        - Return exactly four digits (YYYY).
        - If printed as a two-digit year within a tax/fiscal period label (e.g., "’23-’24", "FY 23/24"), convert the starting part to "2023". If ambiguity remains, return null.
        - Strip surrounding text while preserving the year (e.g., "TY 2024" => "2024").

    - Examples:
        - "Tax Year 2024" => "2024"
        - "Levy Year: 2023 Pay 2024" => "2023"
        - "FY 2023–2024" => "2023"
        - "Tax Period: 07/01/2023 – 06/30/2024" => "2023"
        - "Year Ending 06/30/2024" => "2024"
        - "Bill Date 01/15/2024" => null

    - If not visible or ambiguous after applying these rules, return null.

3. InstallmentNumber - The installment indicator for the selected bill/line (use the value exactly as printed)

    - Also known as: Installment, Installment No., Inst. No., Inst., Coupon, Stub, Half, Half-Year, Payment, Period, Quarter, Q1/Q2/Q3/Q4, Spring, Fall, Summer, Winter, A/B (coupon letters)

    - Examples: "1", "01", "1 of 2", "1st", "First", "1st Half", "Second Half", "First Installment", "Q2", "Spring", "Coupon A", "Full Year", "Annual", "Full Payment"

    - Capture rules:
        - Use the installment text explicitly printed for the selected ParcelNumber and TaxYear, tied to the same row/box/section as the selected amounts (e.g., BaseAmount/TotalDue) for that line.
        - Prefer the label nearest to or within the same coupon/line as the chosen TotalDue and DueDate. Do not infer from dates or amounts alone.
        - Accept any printed form: numerals (1, 01), ordinals/words (1st, First), halves (1st Half, Second Half), seasons (Spring/Fall, Summer/Winter), quarters (Q1–Q4), periods (Period 1), letters (A/B), or combined payment indicators ("Full Year", "Annual", "Full Payment"). Return exactly as shown (preserve casing, spacing, and punctuation).
        - If multiple installments are shown and the applicable line cannot be tied unambiguously to the selected record, return null.
        - Exclude payment-plan installments, delinquency schedules, or account-level notices not specific to the tax installment line.

    - If not visible or ambiguous after applying these rules, return null.

4. BaseAmount - The base tax amount for the selected record before penalties, interest, fees, discounts, or credits

    - Also known as: Base Amount, Base Tax, Tax Amount, Principal, Original Amount, Bill Amount, Base Levy, Ad Valorem Tax, Real Estate Tax, Current Tax (before P&I/fees)

    - Capture rules:
        - Use the amount explicitly labeled as base for the selected ParcelNumber, TaxYear, and InstallmentNumber.
        - Prefer installment-specific base labels (e.g., "1st Half Tax", "First Installment Tax", "Second Half Tax", "2nd Installment Tax").
        - If both full-year and installment base amounts are printed, select the one matching the InstallmentNumber. Do not prorate or divide. No calculations for this field.
        - If multiple line items are shown, use the printed subtotal labeled as base (e.g., "Base Tax", "Tax Amount") that excludes penalties/interest/fees for the selected line/row.

    - If not visible or ambiguous after applying these rules, return null.


5. AlreadyAmount - Amount already paid for the selected bill/line (e.g., "0.00")
    - Also known as: Amount Paid, Paid, Payments, Paid to Date, Previously Paid, Total Payments, Prior Payments, Payment(s) Made
    - Capture rules:
      - Use the value explicitly labeled as paid/previously paid for the selected ParcelNumber, TaxYear, and InstallmentNumber.
      - Prefer installment-specific paid amounts. If both full-year and installment paid amounts are printed, use the one matching the InstallmentNumber. Do not prorate or divide.
      - If multiple payment lines appear, use the printed subtotal/total labeled as paid for the selected line/row. Do not sum individual lines yourself.
      - Exclude credits, discounts, refunds, overpayments, and any “Amount Due”, “Total Due”, “Balance Due”, “Net Due”, “Pay This Amount”, or similar.
      - If shown in parentheses or with a minus sign, output as a negative number (e.g., "(12.34)" => "-12.34").
      - If only an account-level or multi-parcel/multi-year paid amount is shown and it cannot be tied unambiguously to the selected record, return null.
    - If not visible or ambiguous after applying these rules, return null.


6. PenaltyAndInterest - Penalty + Interest (P&I)
    - If a combined "Penalty & Interest" (P&I) is printed for the selected ParcelNumber, TaxYear, and InstallmentNumber, use it.
    - Otherwise compute: PenaltyAndInterest = Penalty + Interest + Fees using printed amounts for the selected record only (no proration).
    - Prefer installment-specific values; if only account-level/multi-year and not clearly tied to the selected record, return null.
    - Exclude base tax, discounts, credits, and any "Total/Amount Due" lines.
    - Respect negatives/parentheses as printed; if none of the components are visible, return null.

7. Fee - Any additional fees for the selected record only (exclude base tax, penalty, and interest)
    - Also known as: Fee, Fees, Service Fee, Processing Fee, Convenience Fee, Online Convenience Fee, E-Check Fee, ACH Fee, Credit/Debit Card Fee, Transaction Fee, Administrative/Admin Fee, Service Charge, Surcharge, Collection Fee, Lien Fee, Recording/Release Fee, Publication/Advertising Fee, Certified Mail/Postage Fee, Returned Check/NSF Fee, Duplicate Bill/Print Fee, Handling/Delivery Fee, Cost

    - Capture rules:
      - Use the amount explicitly labeled as a fee/charge for the selected ParcelNumber, TaxYear, and InstallmentNumber.
      - Prefer installment-specific fee amounts; if both full-year and installment fees are printed, use the one matching the InstallmentNumber. Do not prorate or divide.
      - If a single “Fees” subtotal/total is printed for the selected record, use it.
      - Otherwise compute Fee as the sum of all line items that are fees/charges for the selected record only (no proration). Do not include base tax, penalty, interest, discounts, credits, or any “Total/Amount Due” lines.
      - Exclude items labeled Penalty or Interest (e.g., “Penalty”, “Interest”, “P&I”), and exclude “Late Fee” if it represents penalty/interest rather than a separate administrative fee.
      - Exclude optional payment-processor checkout fees unless they are printed on the bill for the selected record.
      - Exclude account-level, multi-parcel, or multi-year fees that cannot be tied unambiguously to the selected record.
      - If only a combined “Penalty & Interest” or “Penalty, Interest & Fees” total is shown without a separate fee amount, set Fee to null.
      - Respect negatives/parentheses as printed (e.g., "(2.50)" => "-2.50").

    - If not visible or ambiguous after applying these rules, return null.


8. TotalDue - Total amount due for the selected record (use the printed due amount as-is)
    - Also known as: Total Due, Amount Due, Balance Due, Total Amount Due, Pay This Amount, Amount to Pay, Net Amount Due, Balance
    - Capture rules:
      - Use the amount explicitly labeled as due for the selected ParcelNumber, TaxYear, and InstallmentNumber.
      - Prefer installment-specific due amounts; if both full-year and installment due amounts are printed, select the one matching the InstallmentNumber. Do not prorate or compute.
      - If multiple amounts are shown by date (e.g., “If paid by [date]”, “After [date]”), select the amount tied to the primary/face due date (not a discount date and not a delinquent/after date). If only a single due amount is printed, use it.
      - If a due amount is printed per line/row, use the subtotal/total labeled as due for the selected line/row only. Do not sum individual items yourself.
      - Exclude totals that combine multiple parcels, multiple years, or multiple installments when they cannot be tied unambiguously to the selected record.
      - Exclude optional payment-processor checkout fees not printed on the bill.
      - Respect negatives/parentheses as printed (e.g., “(12.34)” => “-12.34”).
      - If not visible or ambiguous after applying these rules, return null.

9. DueDate - Payment due date in MM/DD/YYYY format (for the selected TotalDue)
    - Also known as: Due Date, Pay By, Pay On or Before, Installment Due, Due
    - Capture rules:
      - Use the due date printed for the selected ParcelNumber, TaxYear, and InstallmentNumber that corresponds to the TotalDue selected above.
      - Prefer the primary/face due date (not an early-payment discount date and not a delinquent/after date). If the bill ties specific amounts to dates, select the date linked to the chosen TotalDue.
      - If multiple installments/lines are present, use the due date for the selected line/InstallmentNumber only.
      - Exclude delinquency/penalty start dates unless explicitly labeled as the due date for the selected amount.
      - Extract the date only if a complete MM/DD/YYYY is printed; if missing, partial, text-only (e.g., “Due upon receipt”), or ambiguous, return null.

10. PaidDate - Payment date in MM/DD/YYYY for the selected record (null if not paid)

    - Also known as: Paid Date, Payment Date, Date Paid, Date of Payment, Payment Received, Received Date, Receipt Date, Posted/Posting Date, Processed Date, Cleared Date, ACH Date, EFT Date

    - Capture rules:
      - Use the payment date printed for the selected ParcelNumber, TaxYear, and InstallmentNumber that corresponds to the AlreadyAmount selected above.
      - Prefer installment-specific payment/receipt entries; exclude account-level or multi-year dates that cannot be tied unambiguously to the selected record.
      - If multiple payment entries are shown for the selected record, use the most recent payment date that contributes to the printed AlreadyAmount subtotal/total for that line/row. Do not compute sums; rely on the bill’s labeled paid subtotal/total. If no subtotal is shown and attribution is ambiguous, return null.
      - Exclude non-payment dates: due/discount dates, delinquent/penalty start dates, statement/print dates, assessment dates, postmark dates, authorization/submitted/initiated dates, and generic “as of” dates unless explicitly labeled as payment posted/received.
      - If both an initiation/authorization date and a posted/received/processed date are shown, use the posted/received/processed date.
      - If a reversal/void/refund fully offsets payments (net paid = 0) for the selected record, return null; otherwise use the latest net payment date.
      - If only a status indicator (e.g., “PAID”) appears with no date, return null.
      - If multiple installments/lines are present, use the date tied to the selected InstallmentNumber/line only.

    - Formatting:
      - Return the date as MM/DD/YYYY with leading zeros.
      - If printed as M/D/YY or MM/DD/YY, convert to MM/DD/20YY.
      - If any part of the date (month/day/year) is missing or not fully numeric, return null.


11. Comments - Any comments or notes on the bill (null if none)

    - Also known as: Comments, Notes, Note, Message, Messages, Remarks, Memo, Alert, Important Message, Important Information, Special Instructions, Account Message, Notice

    - Capture rules:
        - Capture the free-text comment(s) printed for the selected ParcelNumber, TaxYear, and InstallmentNumber.
        - Prefer comments explicitly labeled as one of the above or placed in a “Comments/Notes/Message/Important Notice” box or column for the selected line/installment.
        - If both a general account-level comment and an installment/line-specific comment are present, use the installment-specific text. If only a general account-level comment clearly refers to this parcel/year, capture it.
        - If multiple qualifying comments exist for the selected record, concatenate them in printed order separated by " | ".
        - Preserve wording, capitalization, and punctuation exactly as printed; trim leading/trailing whitespace. Do not add labels or dates.
        - If the only visible text is a placeholder such as "None", "N/A", "-", or the field is blank, return null.

    - Exclude:
        - Payment instructions, mailing addresses, detachable stub text, website/portal directions, office hours, statutory citations, generic disclaimers, barcode/scan lines, and boilerplate not specific to the selected record.
        - Amounts/figures (totals, due amounts, penalties, interest, schedules) unless they are part of a sentence that is itself a comment about the selected record.
        - Multi-parcel or multi-year notices that cannot be tied unambiguously to the selected record.
        - Standalone stamps/words such as "PAID", "VOID", or "DUPLICATE" without explanatory text.

    - If not visible or ambiguous after applying these rules, return null.




FORMATTING RULES:
- Extract amounts as plain numbers with two decimals, no currency symbols or commas (e.g., "4256.60" not "$4,256.60")
- Extract dates in MM/DD/YYYY format
- Extract text fields exactly as they appear
- If a field is empty or blank, use null
- If a field is not visible, use null

OUTPUT FORMAT:
Return ONLY valid JSON with no additional text, markdown, or commentary:

{{
    "ParcelNumber": "value or null",
    "TaxYear": "value or null",
    "InstallmentNumber": "value or null",
    "BaseAmount": "value or null",
    "AlreadyAmount": "value or null",
    "PenaltyAndInterest": "value or null",
    "Fee": "value or null",
    "TotalDue": "value or null",
    "DueDate": "value or null",
    "PaidDate": "value or null",
    "Comments": "value or null"
}}

DOCUMENT TEXT:
{documentText}
"""




EXTRACTION_PROMPT_V2_SCOPED = """
You are a precise extraction agent. Extract the fields below from a tax bill document.

Targeting filters (may be empty):
- parcelNumber: "{parcelNumber}"
- taxYear: "{taxYear}"
- installment: "{installment}"

Selection rules:
- If one or more filters are provided (non-empty), select the single coupon/line whose printed values match those filters:
    - ParcelNumber: match the printed parcel identifier (after removing label text like "PIN:", "Parcel #"); preserve punctuation and leading zeros.
    - TaxYear: match the levy/tax year as defined below.
    - InstallmentNumber: match the printed installment label exactly as shown (e.g., "1st Half", "Q2", "Full Year").
- If a provided filter is not printed on the page (e.g., parcel/year/installment not present), ignore that filter and continue with remaining filters.
- If no line matches the provided filters, or multiple lines match and it’s ambiguous, proceed with normal selection (choose one consistent line per standard rules) and return null for fields that aren’t visible.

EXTRACTION FIELDS:

1. ParcelNumber — Printed parcel identifier (Parcel/APN/PIN/AIN/Tax ID/Geo ID/Map-Parcel; Schedule/Account No. only if used as parcel ID). Strip label text only; keep punctuation/spacing/leading zeros. If components (BLOCK/LOT/QUAL) appear without a single ID, join with single spaces in order.

2. TaxYear — Levy year (YYYY). Prefer: Levy Year > Tax Year > Fiscal/Tax Period (use starting year) > Year Ending (use ending year). Interpret “2023 PAY 2024” as 2023. Exclude non-tax dates.

3. InstallmentNumber — Installment indicator exactly as printed (e.g., 1, 1st, First Half, Q2, Spring, Coupon A, Full Year). Use the label in the same line/coupon as TotalDue.

4. BaseAmount — Base tax before penalties/interest/fees/discounts/credits for the selected installment. Use printed subtotal/label only; do not compute or divide.

5. AlreadyAmount — Amount already paid for the selected installment. Respect negatives/parentheses.

6. PenaltyAndInterest — If a combined P&I is printed for the selected installment, use it; else sum printed Penalty + Interest + Fees for that installment (no proration). Respect negatives/parentheses.

7. Fee — Sum of printed fees/charges (exclude base/penalty/interest/discounts/credits). If only a combined “P&I” or “Penalty, Interest & Fees” is shown with no separate fee, return null.

8. TotalDue — Amount due for the selected installment. Choose the primary/face due amount (not discount or “after” amounts).

9. DueDate — Due date corresponding to the chosen TotalDue. Must be MM/DD/YYYY; convert M/D/YY or MM/DD/YY to MM/DD/20YY.

10. PaidDate — Most recent payment posted/received date contributing to AlreadyAmount for the selected installment. Format MM/DD/YYYY; convert M/D/YY or MM/DD/YY to MM/DD/20YY. If only “PAID” with no date, return null.

11. Comments — Free-text comments specific to the selected line/installment. If multiple, join with " | ". Exclude generic instructions/boilerplate.

FORMATTING RULES:
- Amounts: plain numbers with two decimals, no currency symbols or commas (e.g., 4256.60).
- Dates: MM/DD/YYYY.
- Text: preserve as printed (casing, punctuation, spacing).
- If a field is empty, not visible, or ambiguous, use null.

OUTPUT FORMAT:
Return ONLY valid JSON with no extra text:

{{
    "ParcelNumber": "value or null",
    "TaxYear": "value or null",
    "InstallmentNumber": "value or null",
    "BaseAmount": "value or null",
    "AlreadyAmount": "value or null",
    "PenaltyAndInterest": "value or null",
    "Fee": "value or null",
    "TotalDue": "value or null",
    "DueDate": "value or null",
    "PaidDate": "value or null",
    "Comments": "value or null"
}}

DOCUMENT TEXT:
{documentText}
"""


EXTRACTION_PROMPT_V2 = """
You are a precise document extraction agent. Extract the following fields from the tax bill document. Return values exactly as they appear in the document.

EXTRACTION FIELDS:

1. ParcelNumber - The parcel/property identifier as printed (e.g., "BLOCK 286 LOT 5", "10-24-307-004")
    - Also known as: Parcel Number, Parcel No., Parcel #, Parcel ID, APN, PIN, Tax ID, GEO ID, MAP NO, Map/Parcel, Schedule No., AIN, Account No., Account Number, Bill Number (only if used by the jurisdiction as the parcel identifier)

    - Capture rules:
        - Use the parcel identifier explicitly printed for the selected record (same row/box/coupon as the chosen TotalDue/DueDate for that line).
        - Prefer identifiers labeled or positioned as the primary parcel ID for the tax line. If multiple identifiers are present, priority:
            1) Parcel Number / PIN / APN / AIN / Tax ID / Geo ID / Map-Parcel
            2) Schedule No. / Account No. (only if clearly used as the parcel identifier for this bill and no separate parcel/PIN/APN is provided)
            3) Bill/Statement Number only if the bill explicitly uses it as the parcel identifier and no other parcel-like ID is present.
        - Accept any printed form: digits, letters, hyphens, slashes, dots, spaces, block/lot/qual formats (e.g., "BLOCK 286 LOT 5", "123-A-45.00", "10 24 307 004 0000").
        - Strip label text but preserve the value exactly (e.g., "PIN: 10-24-307-004-0000" => "10-24-307-004-0000", "Parcel # 123-456" => "123-456").
        - Preserve leading zeros and internal punctuation; do not normalize, reformat, or infer characters (no O↔0 or I↔1 corrections).
        - If the jurisdiction prints the parcel as components (e.g., "BLOCK 286", "LOT 5", optional "QUAL C0001") and no single combined ID appears, concatenate the components in printed order separated by single spaces (e.g., "BLOCK 286 LOT 5 QUAL C0001").
        - If the document lists multiple parcels/rows, return the identifier tied to the selected line/coupon only. If the applicable line cannot be determined unambiguously, return null.
        - Use the human-readable text printed on the bill; ignore barcodes/QR codes unless their human-readable value is printed.

    - Exclusions:
        - Do not return owner names, situs/mailing addresses, legal descriptions, subdivision/plat names, tax district/levy codes, control numbers, receipt/payment IDs, confirmation numbers, cashier/session IDs.
        - Do not return account-level or multi-parcel identifiers when they cannot be tied unambiguously to the selected line.
        - Do not return Bill/Statement/Invoice numbers if a separate parcel/PIN/APN/Tax ID is present.

    - Normalization:
        - Return exactly as printed (preserve casing, spacing, hyphens, slashes, periods).
        - Trim leading/trailing whitespace and remove label prefixes only (e.g., "APN:", "PIN", "Parcel #").
        - If the value wraps across lines, join wrapped lines with a single space.

    - Examples:
        - "Parcel Number: 10-24-307-004-0000" => "10-24-307-004-0000"
        - "PIN 10 24 307 004 0000" => "10 24 307 004 0000"
        - "MAP NO 123-A-45.00" => "123-A-45.00"
        - "BLOCK 286 LOT 5" => "BLOCK 286 LOT 5"
        - "AIN: 1234-567-890" => "1234-567-890"

    - If not visible or ambiguous after applying these rules, return null.

2. TaxYear - The four-digit levy year the tax applies to (e.g., "2025")

    - Also known as: Tax Year, Levy Year, Tax Period, Fiscal Year (FY), Year Ending, Assessment Year (AY), TY, AY

    - Capture rules:
        - Use the year explicitly labeled for the selected ParcelNumber/Installment line or its header section.
        - Priority when multiple labels exist: "Levy Year" > "Tax Year" > "Tax Period/Fiscal Year" > "Year Ending".
        - Ranges/periods:
            - If shown as a span/range (e.g., "2023-2024", "FY 2023/24", "Tax Period: 07/01/2023–06/30/2024"), return the starting year ("2023").
            - If explicitly labeled "Year Ending" or "Year Ended" (e.g., "Year Ending 06/30/2024"), return the ending year ("2024").
        - Phrases like "2023 PAY 2024", "Payable 2024", "Pay in 2024": return the levy/tax year ("2023").
        - When multiple years appear on the document, select the one tied to the same line/box/section as the chosen TotalDue/DueDate for the selected record; if not unambiguously tied, return null.
        - Exclude non-tax years: due/discount/delinquent dates, bill/print/statement dates, receipt/payment dates, penalty schedules, ordinance/statute years, and website/version years.

    - Normalization:
        - Return exactly four digits (YYYY).
        - If printed as a two-digit year within a tax/fiscal period label (e.g., "’23-’24", "FY 23/24"), convert the starting part to "2023". If ambiguity remains, return null.
        - Strip surrounding text while preserving the year (e.g., "TY 2024" => "2024").

    - Examples:
        - "Tax Year 2024" => "2024"
        - "Levy Year: 2023 Pay 2024" => "2023"
        - "FY 2023–2024" => "2023"
        - "Tax Period: 07/01/2023 – 06/30/2024" => "2023"
        - "Year Ending 06/30/2024" => "2024"
        - "Bill Date 01/15/2024" => null

    - If not visible or ambiguous after applying these rules, return null.

3. InstallmentNumber - The installment indicator for the selected bill/line (use the value exactly as printed)

    - Also known as: Installment, Installment No., Inst. No., Inst., Coupon, Stub, Half, Half-Year, Payment, Period, Quarter, Q1/Q2/Q3/Q4, Spring, Fall, Summer, Winter, A/B (coupon letters)

    - Examples: "1", "01", "1 of 2", "1st", "First", "1st Half", "Second Half", "First Installment", "Q2", "Spring", "Coupon A", "Full Year", "Annual", "Full Payment"

    - Capture rules:
        - Use the installment text explicitly printed for the selected ParcelNumber and TaxYear, tied to the same row/box/section as the selected amounts (e.g., BaseAmount/TotalDue) for that line.
        - Prefer the label nearest to or within the same coupon/line as the chosen TotalDue and DueDate. Do not infer from dates or amounts alone.
        - Accept any printed form: numerals (1, 01), ordinals/words (1st, First), halves (1st Half, Second Half), seasons (Spring/Fall, Summer/Winter), quarters (Q1–Q4), periods (Period 1), letters (A/B), or combined payment indicators ("Full Year", "Annual", "Full Payment"). Return exactly as shown (preserve casing, spacing, and punctuation).
        - If multiple installments are shown and the applicable line cannot be tied unambiguously to the selected record, return null.
        - Exclude payment-plan installments, delinquency schedules, or account-level notices not specific to the tax installment line.

    - If not visible or ambiguous after applying these rules, return null.

4. BaseAmount - The base tax amount for the selected record before penalties, interest, fees, discounts, or credits

    - Also known as: Base Amount, Base Tax, Tax Amount, Principal, Original Amount, Bill Amount, Base Levy, Ad Valorem Tax, Real Estate Tax, Current Tax (before P&I/fees)

    - Capture rules:
        - Use the amount explicitly labeled as base for the selected ParcelNumber, TaxYear, and InstallmentNumber.
        - Prefer installment-specific base labels (e.g., "1st Half Tax", "First Installment Tax", "Second Half Tax", "2nd Installment Tax").
        - If both full-year and installment base amounts are printed, select the one matching the InstallmentNumber. Do not prorate or divide. No calculations for this field.
        - If multiple line items are shown, use the printed subtotal labeled as base (e.g., "Base Tax", "Tax Amount") that excludes penalties/interest/fees for the selected line/row.

    - If not visible or ambiguous after applying these rules, return null.


5. AlreadyAmount - Amount already paid for the selected bill/line (e.g., "0.00")
    - Also known as: Amount Paid, Paid, Payments, Paid to Date, Previously Paid, Total Payments, Prior Payments, Payment(s) Made
    - Capture rules:
      - Use the value explicitly labeled as paid/previously paid for the selected ParcelNumber, TaxYear, and InstallmentNumber.
      - Prefer installment-specific paid amounts. If both full-year and installment paid amounts are printed, use the one matching the InstallmentNumber. Do not prorate or divide.
      - If multiple payment lines appear, use the printed subtotal/total labeled as paid for the selected line/row. Do not sum individual lines yourself.
      - Exclude credits, discounts, refunds, overpayments, and any “Amount Due”, “Total Due”, “Balance Due”, “Net Due”, “Pay This Amount”, or similar.
      - If shown in parentheses or with a minus sign, output as a negative number (e.g., "(12.34)" => "-12.34").
      - If only an account-level or multi-parcel/multi-year paid amount is shown and it cannot be tied unambiguously to the selected record, return null.
    - If not visible or ambiguous after applying these rules, return null.


6. PenaltyAndInterest - Penalty + Interest (P&I)
    - If a combined "Penalty & Interest" (P&I) is printed for the selected ParcelNumber, TaxYear, and InstallmentNumber, use it.
    - Otherwise compute: PenaltyAndInterest = Penalty + Interest + Fees using printed amounts for the selected record only (no proration).
    - Prefer installment-specific values; if only account-level/multi-year and not clearly tied to the selected record, return null.
    - Exclude base tax, discounts, credits, and any "Total/Amount Due" lines.
    - Respect negatives/parentheses as printed; if none of the components are visible, return null.

7. Fee - Any additional fees for the selected record only (exclude base tax, penalty, and interest)
    - Also known as: Fee, Fees, Service Fee, Processing Fee, Convenience Fee, Online Convenience Fee, E-Check Fee, ACH Fee, Credit/Debit Card Fee, Transaction Fee, Administrative/Admin Fee, Service Charge, Surcharge, Collection Fee, Lien Fee, Recording/Release Fee, Publication/Advertising Fee, Certified Mail/Postage Fee, Returned Check/NSF Fee, Duplicate Bill/Print Fee, Handling/Delivery Fee, Cost

    - Capture rules:
      - Use the amount explicitly labeled as a fee/charge for the selected ParcelNumber, TaxYear, and InstallmentNumber.
      - Prefer installment-specific fee amounts; if both full-year and installment fees are printed, use the one matching the InstallmentNumber. Do not prorate or divide.
      - If a single “Fees” subtotal/total is printed for the selected record, use it.
      - Otherwise compute Fee as the sum of all line items that are fees/charges for the selected record only (no proration). Do not include base tax, penalty, interest, discounts, credits, or any “Total/Amount Due” lines.
      - Exclude items labeled Penalty or Interest (e.g., “Penalty”, “Interest”, “P&I”), and exclude “Late Fee” if it represents penalty/interest rather than a separate administrative fee.
      - Exclude optional payment-processor checkout fees unless they are printed on the bill for the selected record.
      - Exclude account-level, multi-parcel, or multi-year fees that cannot be tied unambiguously to the selected record.
      - If only a combined “Penalty & Interest” or “Penalty, Interest & Fees” total is shown without a separate fee amount, set Fee to null.
      - Respect negatives/parentheses as printed (e.g., "(2.50)" => "-2.50").

    - If not visible or ambiguous after applying these rules, return null.


8. TotalDue - Total amount due for the selected record (use the printed due amount as-is)
    - Also known as: Total Due, Amount Due, Balance Due, Total Amount Due, Pay This Amount, Amount to Pay, Net Amount Due, Balance
    - Capture rules:
      - Use the amount explicitly labeled as due for the selected ParcelNumber, TaxYear, and InstallmentNumber.
      - Prefer installment-specific due amounts; if both full-year and installment due amounts are printed, select the one matching the InstallmentNumber. Do not prorate or compute.
      - If multiple amounts are shown by date (e.g., “If paid by [date]”, “After [date]”), select the amount tied to the primary/face due date (not a discount date and not a delinquent/after date). If only a single due amount is printed, use it.
      - If a due amount is printed per line/row, use the subtotal/total labeled as due for the selected line/row only. Do not sum individual items yourself.
      - Exclude totals that combine multiple parcels, multiple years, or multiple installments when they cannot be tied unambiguously to the selected record.
      - Exclude optional payment-processor checkout fees not printed on the bill.
      - Respect negatives/parentheses as printed (e.g., “(12.34)” => “-12.34”).
      - If not visible or ambiguous after applying these rules, return null.

9. DueDate - Payment due date in MM/DD/YYYY format (for the selected TotalDue)
    - Also known as: Due Date, Pay By, Pay On or Before, Installment Due, Due
    - Capture rules:
      - Use the due date printed for the selected ParcelNumber, TaxYear, and InstallmentNumber that corresponds to the TotalDue selected above.
      - Prefer the primary/face due date (not an early-payment discount date and not a delinquent/after date). If the bill ties specific amounts to dates, select the date linked to the chosen TotalDue.
      - If multiple installments/lines are present, use the due date for the selected line/InstallmentNumber only.
      - Exclude delinquency/penalty start dates unless explicitly labeled as the due date for the selected amount.
      - Extract the date only if a complete MM/DD/YYYY is printed; if missing, partial, text-only (e.g., “Due upon receipt”), or ambiguous, return null.

10. PaidDate - Payment date in MM/DD/YYYY for the selected record (null if not paid)

    - Also known as: Paid Date, Payment Date, Date Paid, Date of Payment, Payment Received, Received Date, Receipt Date, Posted/Posting Date, Processed Date, Cleared Date, ACH Date, EFT Date

    - Capture rules:
      - Use the payment date printed for the selected ParcelNumber, TaxYear, and InstallmentNumber that corresponds to the AlreadyAmount selected above.
      - Prefer installment-specific payment/receipt entries; exclude account-level or multi-year dates that cannot be tied unambiguously to the selected record.
      - If multiple payment entries are shown for the selected record, use the most recent payment date that contributes to the printed AlreadyAmount subtotal/total for that line/row. Do not compute sums; rely on the bill’s labeled paid subtotal/total. If no subtotal is shown and attribution is ambiguous, return null.
      - Exclude non-payment dates: due/discount dates, delinquent/penalty start dates, statement/print dates, assessment dates, postmark dates, authorization/submitted/initiated dates, and generic “as of” dates unless explicitly labeled as payment posted/received.
      - If both an initiation/authorization date and a posted/received/processed date are shown, use the posted/received/processed date.
      - If a reversal/void/refund fully offsets payments (net paid = 0) for the selected record, return null; otherwise use the latest net payment date.
      - If only a status indicator (e.g., “PAID”) appears with no date, return null.
      - If multiple installments/lines are present, use the date tied to the selected InstallmentNumber/line only.

    - Formatting:
      - Return the date as MM/DD/YYYY with leading zeros.
      - If printed as M/D/YY or MM/DD/YY, convert to MM/DD/20YY.
      - If any part of the date (month/day/year) is missing or not fully numeric, return null.


11. Comments - Any comments or notes on the bill (null if none)

    - Also known as: Comments, Notes, Note, Message, Messages, Remarks, Memo, Alert, Important Message, Important Information, Special Instructions, Account Message, Notice

    - Capture rules:
        - Capture the free-text comment(s) printed for the selected ParcelNumber, TaxYear, and InstallmentNumber.
        - Prefer comments explicitly labeled as one of the above or placed in a “Comments/Notes/Message/Important Notice” box or column for the selected line/installment.
        - If both a general account-level comment and an installment/line-specific comment are present, use the installment-specific text. If only a general account-level comment clearly refers to this parcel/year, capture it.
        - If multiple qualifying comments exist for the selected record, concatenate them in printed order separated by " | ".
        - Preserve wording, capitalization, and punctuation exactly as printed; trim leading/trailing whitespace. Do not add labels or dates.
        - If the only visible text is a placeholder such as "None", "N/A", "-", or the field is blank, return null.

    - Exclude:
        - Payment instructions, mailing addresses, detachable stub text, website/portal directions, office hours, statutory citations, generic disclaimers, barcode/scan lines, and boilerplate not specific to the selected record.
        - Amounts/figures (totals, due amounts, penalties, interest, schedules) unless they are part of a sentence that is itself a comment about the selected record.
        - Multi-parcel or multi-year notices that cannot be tied unambiguously to the selected record.
        - Standalone stamps/words such as "PAID", "VOID", or "DUPLICATE" without explanatory text.

    - If not visible or ambiguous after applying these rules, return null.




FORMATTING RULES:
- Extract amounts as plain numbers with two decimals, no currency symbols or commas (e.g., "4256.60" not "$4,256.60")
- Extract dates in MM/DD/YYYY format
- Extract text fields exactly as they appear
- If a field is empty or blank, use null
- If a field is not visible, use null

OUTPUT FORMAT:
Return ONLY valid JSON with no additional text, markdown, or commentary:

{{
    "ParcelNumber": "value or null",
    "TaxYear": "value or null",
    "InstallmentNumber": "value or null",
    "BaseAmount": "value or null",
    "AlreadyAmount": "value or null",
    "PenaltyAndInterest": "value or null",
    "Fee": "value or null",
    "TotalDue": "value or null",
    "DueDate": "value or null",
    "PaidDate": "value or null",
    "Comments": "value or null"
}}

DOCUMENT TEXT:
{documentText}
"""




EXTRACTION_PROMPT_V3 = """ 
You are a **precise and rule-based tax bill extraction agent**.  
Extract the requested fields **exactly as printed** in the tax bill document.  
Do **not infer, reformat, calculate, or guess** unless a specific rule authorizes it.

---

## CORE PRINCIPLES


1. **Targeting filters (may be empty)**
    - parcelNumber: "{parcelNumber}"
    - taxYear: "{taxYear}"
    - installment: "{installment}"
    - If a provided filter is not printed on the page (e.g., parcel/year/installment not present), ignore that filter and continue with remaining filters.


2. **Scope & Selection**
   - Extract values **only** for the record corresponding to the intended **ParcelNumber** and **TaxYear** (and Installment if specified).
   - If multiple parcels, years, or installments appear, select the record that best matches these parameters.  
   - If multiple possible matches or ambiguous associations exist, return `null`.

3. **Precision**
   - Use **only printed text** visible in the document (ignore barcodes, metadata, or inferred values).
   - **Preserve all characters** (hyphens, slashes, spacing, casing) as printed.
   - Remove **label prefixes** (e.g., “PIN:”, “Parcel #”, “Tax Year:”) but not the value itself.

4. **Normalization**
   - Amounts: plain numbers with two decimals (no `$`, commas, or text).
     - e.g., `$4,256.60` → `4256.60`
   - Dates: always in `MM/DD/YYYY`
     - Convert `M/D/YY` → `MM/DD/20YY`
     - If incomplete or ambiguous, return `null`.
   - Text fields: preserve wording, punctuation, and casing.
   - If a value is blank, missing, or not visible, return `null`.

5. **Output Format**
   - Return **only valid JSON**, with field names and values (no comments, no extra text):
     ```json
     {
       "ParcelNumber": "...",
       "TaxYear": "...",
       "InstallmentNumber": "...",
       "BaseAmount": "...",
       "AlreadyAmount": "...",
       "PenaltyAndInterest": "...",
       "Fee": "...",
       "TotalDue": "...",
       "DueDate": "...",
       "PaidDate": "...",
       "Comments": "..."
     }
     ```

---

## FIELD-SPECIFIC INSTRUCTIONS

### 1. ParcelNumber
**Also known as:** Parcel Number, Parcel No., Parcel ID, PIN, APN, AIN, Tax ID, GEO ID, Account No., Schedule No., Bill No. (only if it functions as the parcel ID).

**Rules:**
- Select the identifier directly tied to the chosen **TotalDue/DueDate line**.
- Priority:  
  1. Parcel/PIN/APN/AIN/Tax ID/GEO ID  
  2. Schedule No. or Account No. (only if no primary parcel ID exists)  
  3. Bill/Statement No. (only if used as the parcel ID)
- Preserve **exact formatting** (e.g., “BLOCK 286 LOT 5 QUAL C0001”).
- If components (BLOCK/LOT/QUAL) appear separately, join them with spaces.
- Exclude owner names, addresses, descriptions, or unrelated IDs.

**Examples:**
- `PIN 10 24 307 004 0000` → `"10 24 307 004 0000"`
- `MAP NO 123-A-45.00` → `"123-A-45.00"`
- `BLOCK 286 LOT 5` → `"BLOCK 286 LOT 5"`

---

### 2. TaxYear
**Also known as:** Tax Year, Levy Year, Fiscal Year, Assessment Year, AY, TY, Year Ending.

**Rules:**
- Use the year labeled near the selected **parcel line** or header.  
- If shown as a range, return:
  - Start year for “2023–2024”, “FY 23/24”, etc. → `2023`
  - End year for “Year Ending 06/30/2024” → `2024`
- For “2023 Pay 2024” or “Payable 2024” → `2023`
- Return exactly 4 digits. If unclear which year applies → `null`.

---

### 3. InstallmentNumber
**Also known as:** Installment, Half, Coupon, Period, Quarter, Payment, Q1–Q4, Spring/Fall, A/B.

**Rules:**
- Use the printed label tied to the selected **TotalDue/DueDate line**.
- Preserve exact text (e.g., “1st Half”, “Coupon A”, “Full Year”).
- Do not infer from dates or partial numbering.
- If multiple installments shown and unclear which applies → `null`.

---

### 4. BaseAmount
**Also known as:** Base Amount, Base Tax, Tax Amount, Principal, Original Amount.

**Rules:**
- Extract the explicitly printed base amount for the chosen record.
- Prefer labels such as “Base Tax” or “1st Half Tax”.
- Do **not compute or divide**; use exactly what’s printed.
- Exclude totals or multi-parcel/multi-year aggregates.

---

### 5. AlreadyAmount
**Also known as:** Paid, Amount Paid, Payments, Paid to Date, Previously Paid.

**Rules:**
- Use the printed paid/previously paid value tied to the selected record.
- Convert parentheses `(12.34)` to `-12.34`.
- Exclude credits, discounts, or unrelated balances.
- Use installment-specific values only; otherwise return `null`.

---

### 6. PenaltyAndInterest
**Rules:**
- Use the printed “Penalty & Interest (P&I)” amount for the selected record.  
- If printed separately, sum **Penalty + Interest + Fees** (for that record only).
- Exclude base tax and unrelated charges.
- If none or ambiguous → `null`.

---

### 7. Fee
**Also known as:** Fee, Service Fee, Processing Fee, Convenience Fee, etc.

**Rules:**
- Capture explicitly labeled fees only.
- Exclude penalties, interest, or optional payment-processor fees.
- If printed as a combined “Penalty, Interest & Fees” with no separation → `null`.

---

### 8. TotalDue
**Also known as:** Total Due, Amount Due, Pay This Amount, Balance Due, Net Amount Due.

**Rules:**
- Use the amount labeled “Due” tied to the chosen line.
- Prefer the **face/primary due amount**, not discount or delinquent amounts.
- Convert parentheses to negatives if shown.  
- Exclude totals for multiple parcels or years.

---

### 9. DueDate
**Also known as:** Due Date, Pay By, Pay On or Before.

**Rules:**
- Extract the date associated with the chosen **TotalDue**.
- Prefer the main/face due date (not discount or late dates).
- Only output if a full numeric date (MM/DD/YYYY) is printed.

---

### 10. PaidDate
**Also known as:** Paid Date, Payment Date, Receipt Date, Date Posted.

**Rules:**
- Use the latest posted/processed date associated with the printed **AlreadyAmount**.
- Exclude authorization/submitted dates or non-payment references.
- Convert to `MM/DD/YYYY` if possible; else `null`.

---

### 11. Comments
**Also known as:** Notes, Messages, Remarks, Important Information, Alerts.

**Rules:**
- Capture any free-text message specific to the selected parcel/year/installment.
- Concatenate multiple with `" | "`.
- Exclude generic disclaimers, addresses, or payment instructions.
- Return `null` for placeholders like “N/A” or “None”.

---

## FINAL REQUIREMENTS

- **Never** include explanations, reasoning, or markdown.  
- **Never** output extra text outside JSON.  
- **If uncertain**, prefer `null` over assumption.

---

DOCUMENT TEXT:
{documentText}

"""



