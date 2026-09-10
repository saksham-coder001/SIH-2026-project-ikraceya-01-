"""
persona_scripts.py — persona-tailored explanations for each rule result.

Consumer framing emphasizes rights / what's missing as a buyer.
Seller framing emphasizes the legal obligation and what to fix.

Each entry has a {status} placeholder filled in by get_script() below.
"""

RULE_SCRIPTS = {
    "SCOPE-3": {
        "consumer": "This package is small enough (10 g/mL or less) that sellers aren't legally required to show the usual label details on it.",
        "seller": "This package qualifies for the tiny-package exemption (Rule 26) — the standard Chapter II declarations are not mandatory here.",
    },
    "DECL-1": {
        "consumer": "You have a right to know who made or packed this product and where to reach them. Status: {status}.",
        "seller": "You're legally required to display the manufacturer/packer's name and address (Rule 6(1)(a)). Status: {status}.",
    },
    "DECL-3": {
        "consumer": "The package should clearly state how much product is actually inside. Status: {status}.",
        "seller": "Net quantity declaration is mandatory (Rule 6(1)(c)). Status: {status}.",
    },
    "DECL-4": {
        "consumer": "You're entitled to know when this was made or packed, so you can judge freshness. Status: {status}.",
        "seller": "Month & year of manufacture/packing must be declared (Rule 6(1)(d)). Status: {status}.",
    },
    "DECL-5": {
        "consumer": "The price you should pay (MRP) must be printed clearly on the pack. Status: {status}.",
        "seller": "Retail Sale Price (MRP) declaration is mandatory (Rule 6(1)(e)). Status: {status}.",
    },
    "DECL-7": {
        "consumer": "You should have a way to contact the company if something's wrong with this product. Status: {status}.",
        "seller": "Consumer care contact details (phone/email) are mandatory (Rule 6(2)). Status: {status}.",
    },
    "MRP-FORMAT": {
        "consumer": "The listed price should already include all taxes — you shouldn't be charged extra at checkout. Status: {status}.",
        "seller": "MRP must be declared as inclusive of all taxes (Rule 2(m)). Status: {status}.",
    },
    "QTY-3": {
        "consumer": "The quantity on the pack should be an exact number — watch out for vague words like 'approximately'. Status: {status}.",
        "seller": "Quantity declarations must not use misleading qualifiers like 'about' or 'approximately' (Rule 12(6)). Status: {status}.",
    },
    "QTY-6": {
        "consumer": "Quantities should be given in standard units, not vague grouping words like 'dozen' or 'gross'. Status: {status}.",
        "seller": "Quantity must not be expressed using words like dozen/score/gross (Rule 13(4)). Status: {status}.",
    },
    "FONT-CHECK": {
        "consumer": "Label text should be large and clear enough to read easily — this needs a physical check, not just a photo.",
        "seller": "Numeral height/contrast rules (Rule 7) require a physical measurement — not verifiable from a photo alone.",
    },
    "MPE-CHECK": {
        "consumer": "Whether the pack actually contains the full declared quantity needs a real weighing check, not a photo.",
        "seller": "Maximum Permissible Error verification requires lab measurement of actual fill quantity — not automatable from an image.",
    },
    "PRICE-REVISION": {
        "consumer": "If the price was ever revised, that should be documented properly by the seller — not something a photo can confirm.",
        "seller": "Price-revision compliance (Rule 18(3)) requires checking against your own revision notices — not verifiable from the label alone.",
    },
    "PENALTIES": {
        "consumer": "Penalties are decided by an inspecting officer after violations are confirmed — not something this scan can determine.",
        "seller": "Penalty determination (Rule 32) is an enforcement action taken by an officer, not an automated check.",
    },
}


def get_script(rule_id: str, persona: str, status: str, fallback_description: str) -> str:
    """
    Return the persona-specific explanation for a rule, with {status} filled
    in. Falls back to the generic rule-engine description if no script is
    defined for this rule_id (keeps things working even for future rules
    added to rule_definitions.json without a script yet written).
    """
    scripts = RULE_SCRIPTS.get(rule_id)
    if not scripts:
        return fallback_description

    template = scripts.get(persona, scripts.get("consumer"))
    if "{status}" in template:
        return template.format(status=status)
    return template