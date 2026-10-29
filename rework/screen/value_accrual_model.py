"""Value accrual model for the Singha Lemon Soda project (task T12, 20 October 2026, revision 2).

Standard library only. Deterministic: no random draws and no clock.
Run with:  python -I value_accrual_model.py
Reads (this folder): project_valuation_results.json, can_cost_model_results.json
Writes:              value_accrual_model_results.json (this folder)

What the model does. It takes the project cash flows of project_valuation.py (200,000 cubes a
year at steady state, year 1 at half volume, five years, no terminal value, year-0 outlay equal
to one year of fixed cost, 10 percent discount rate) and adds:
  (a) Thai corporate income tax at 20 percent on the incremental profit, with the year-0 outlay
      capitalised and depreciated straight line over five years; three treatments of a loss year;
  (b) netting against the Singha Lemon Soda can: each cube bought by an existing can buyer
      displaces one can, at the can's contribution before aluminium;
  (c) incremental net profit, its share of Singha Corporation net profit (year by year and
      cumulative), and dividends through Boon Rawd Brewery at the stated ownership and payout;
  (d) equity value uplift by two methods: the NPV, and P/E multiples of listed peers applied to
      steady-state incremental net profit;
  (e) return on invested capital against a cost of capital built as the Bank of Thailand policy
      rate plus a stated premium;
  (f) the cube volume at which incremental net profit reaches 0.1, 0.5 and 1 percent of Singha
      Corporation net profit, and the break points for cannibalisation, volume, fixed cost and
      contribution per cube;
  (g) how a stated switch share in the pilot maps to displaced cans, and the review level it implies.

Three contribution bases are run.
  after_excise (LEAD): cube contribution after the same chain as the can (VAT, retailer and
      distributor margins, excise): planning price 15 THB times the can's net-to-listing ratio,
      less the cube cost of 4.09 THB (DERIVED; record 70 headline, 3.94). It is on the same basis
      as the can contribution of 4.127 THB, so the cannibalisation netting compares like with like.
  before_excise (sensitivity, deck basis): ex-factory 9.00 less cost 4.09 = 4.91 THB, before excise
      (project_valuation.py, the basis of the current deck and submission figures). It reproduces
      the deck's pre-tax numbers. At a cannibalised share above zero it nets this before-excise cube
      against the can's AFTER-excise contribution, which is the scenario in which the cube is outside
      the excise and the can is inside it. The excise classification of the cube is not determined, so
      the rows are labelled with that scenario wherever they are quoted; they are not "both before excise".
  before_excise_chain (team record only): both products on the can's invoice before excise: cube
      invoice at the 15 THB planning price less cost 4.09; can invoice less the non-aluminium variable
      cost. This is the run with both products before excise; it is compared with the deck-basis rows
      in before_excise_comparison.
The can contribution of 4.127 THB is before aluminium, so the loss from a displaced can is an upper bound
and every cannibalisation break point is pulled down by it. The cube contribution excludes binder and flavour
(not priced), so it is an upper bound too, which pulls every break point up. The two are not sized, so the
cannibalisation break points are approximate and are not described as conservative.

Every input is listed in INPUTS with a tier and a status. A figure with no saved page is
UNVERIFIED. Tiers follow rework/SOURCING_POLICY.md and Appendix A. A primary-origin page that was read
through a page summary and not in full is tiered S (Appendix A reserves P for text read in full).
"""

import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PV_PATH = os.path.join(HERE, "project_valuation_results.json")
CAN_PATH = os.path.join(HERE, "can_cost_model_results.json")
OUT_PATH = os.path.join(HERE, "value_accrual_model_results.json")


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


PV = load(PV_PATH)
CAN = load(CAN_PATH)

# ---- Upstream figures (read from the results files) -------------------------------------

UE = PV["unit_economics"]
C_BEFORE = PV["summary"]["base_case"]["contribution_per_cube_thb"]        # 4.91 (before excise)
COST_BASE = UE["base_cost_thb"]                                           # 4.09
EX_FACTORY = UE["ex_factory_thb_per_cube"]                                # 9.00
SHELF = UE["shelf_thb"]                                                   # 15.00
NPV_PRE_PV = PV["summary"]["base_case"]["npv_at_fixed_500000_thb"]        # 880,796 (pre-tax)

C_CAN = CAN["aluminium"]["contribution_pre_aluminium_thb_per_can"]        # 4.127 (after excise)
CAN_NET_AFTER_EXCISE = CAN["aluminium"]["net_after_excise_thb_per_can"]   # 7.393
CAN_LISTING = CAN["aluminium"]["listing_price_basis_thb_per_can"]         # 13.8025
CAN_VAR_COST = CAN["variable_cost_excl_aluminium_mid_thb"]                # 3.266

assert abs(C_BEFORE - 4.91) < 1e-9, C_BEFORE
assert abs(COST_BASE - 4.09) < 1e-9, COST_BASE
assert abs(EX_FACTORY - 9.0) < 1e-9, EX_FACTORY
assert abs(SHELF - 15.0) < 1e-9, SHELF
assert abs(C_CAN - 4.127) < 1e-9, C_CAN

CHAIN_RATIO = CAN_NET_AFTER_EXCISE / CAN_LISTING                         # about 0.5356
C_AFTER = SHELF * CHAIN_RATIO - COST_BASE                                 # about 3.94 (DERIVED)
assert 3.9 < C_AFTER < 4.0, C_AFTER

# The can's price chain (rework/screen/singha_internal_estimates.py, INPUTS vat, retail_margin,
# distributor_margin, excise_ad_valorem; central values). Reproduced here so the reconciliation of the
# 3.65 and 3.94 figures is computed, not typed. The assertions below fail if the chain does not give the
# can's 7.393 net.
VAT = 0.07                                  # P, Revenue Department (T9 raw file)
RETAIL_MARGIN = 0.216                       # S, PROXY (Big C group gross margin, all categories)
DIST_MARGIN = 0.15                          # ASSUMPTION (unsourced band 10 to 20 percent)
EXCISE = 0.14                               # P as saved (Gazette item 02.02); base not read, ASSUMPTION


def invoice(price):
    """Maker invoice before excise: price / (1 + VAT) x (1 - retail margin) x (1 - distributor margin)."""
    return price / (1.0 + VAT) * (1.0 - RETAIL_MARGIN) * (1.0 - DIST_MARGIN)


INV_CAN = invoice(CAN_LISTING)
INV_CUBE = invoice(SHELF)
assert abs(INV_CAN * (1.0 - EXCISE) - CAN_NET_AFTER_EXCISE) < 1e-3, (INV_CAN * (1.0 - EXCISE), CAN_NET_AFTER_EXCISE)
assert abs(INV_CUBE * (1.0 - EXCISE) - COST_BASE - C_AFTER) < 1e-3, (INV_CUBE * (1.0 - EXCISE) - COST_BASE, C_AFTER)
C_CUBE_INV = INV_CUBE - COST_BASE                                         # cube, before excise, can's chain
C_CAN_INV = INV_CAN - CAN_VAR_COST                                        # can, before excise, before aluminium
assert abs((INV_CAN * (1.0 - EXCISE) - CAN_VAR_COST) - C_CAN) < 1e-3

# (key, cube contribution, can contribution, note)
BASES = (
    ("after_excise", C_AFTER, C_CAN,
     "Lead. Cube and can both after excise. Consistent."),
    ("before_excise", C_BEFORE, C_CAN,
     "Deck basis (ex-factory 9.00). At a cannibalised share of 0 the can does not enter. At a share above 0 it nets a "
     "before-excise cube against the can's after-excise contribution, which is the scenario in which the cube is outside "
     "the excise and the can is inside it (the cube's excise classification is not determined). Those rows are flagged "
     "cube_outside_excise_can_inside_row and must carry that label wherever they are quoted."),
    ("before_excise_chain", C_CUBE_INV, C_CAN_INV,
     "Team record only. Cube and can both on the can's invoice before excise. Used to compare with the deck-basis rows."),
)
LEAD_BASES = BASES[:2]
CUBE_OUTSIDE_EXCISE_SCENARIO = {"before_excise"}

# ---- Scenario and policy inputs --------------------------------------------------------

TAX = 0.20                                  # Revenue Department, CIT 20 percent (page summary, S)
RAMP = [0.5, 1.0, 1.0, 1.0, 1.0]            # year 1 at half volume (ASSUMPTION; project_valuation)
HORIZON = len(RAMP)
DEP_YEARS = 5                               # straight-line depreciation of year-0 outlay (ASSUMPTION)

POLICY_RATE = 0.01                          # BOT press release 31/2026, MPC Decision 4/2026, 26 Aug 2026 (page summary, S)
PREMIUMS = [0.07, 0.09, 0.11]               # premium over the policy rate (ASSUMPTION)
RATES = [round(POLICY_RATE + p, 6) for p in PREMIUMS]     # 8, 10 and 12 percent
RATE_BASE = RATES[1]                        # 10 percent, kept from project_valuation.py
assert [round(r, 4) for r in RATES] == [0.08, 0.10, 0.12], RATES

VOLUMES = {"low": 50000, "base": 200000, "high": 1000000}   # cubes a year (ASSUMPTION)
FIXED_BASE = 500000                         # THB a year (ASSUMPTION grid)
FIXED_GRID = [250000, 500000, 1000000, 2000000]
CANNIB = [0.0, 0.25, 0.5, 1.0]              # share of cube buyers who would otherwise buy a can
CAN_PER_CUBE = 1.0                          # one can displaced per cube bought by a switcher (ASSUMPTION)
DISPLACEMENT_FACTORS = [0.5, 1.0, 1.5]      # cans lost per cube bought by a stated switcher (illustrative range)

NP_GROUP_2025 = 3085e6                      # Singha Corporation net profit 2025 (S, MGR Online 23 May 2026)
NP_GROUP_2024 = 3135e6                      # Singha Corporation net profit 2024 (S, same article)
REV_2025 = 3892e6                           # Singha Corporation total revenue 2025 (S)
REV_2024 = 3950e6                           # Singha Corporation total revenue 2024 (S)
NP_BOONRAWD_2022 = 5793e6                   # Boon Rawd Brewery net profit 2022 (S, Thaiger; latest year found)

OWN_PARENT = 1.0                            # Boon Rawd Brewery share of Singha Corporation (UNVERIFIED; 100 percent assumed)
PAYOUT_BASE = 1.0                           # share of incremental net profit paid out (ASSUMPTION; no policy found)
PAYOUT_ALT = 0.5
PARENT_TAX_FULL_EXCL = 0.0                  # only if holding >= 25 percent, 3-month rule and proviso hold (all UNVERIFIED)
PARENT_TAX_HALF_EXCL = TAX * 0.5            # half excluded and taxed at 20 percent: effective 10 percent of gross
HOLDER_PAYOUT = 1.0                         # share of the dividend Boon Rawd passes to its holders (ASSUMPTION)
HOLDER_WHT = 0.10                           # 10 percent rate for Thai individuals on separate taxation (RD 6045, page summary, S; illustrative)
HOLDER_STAKE_ILLUSTRATIVE = [0.10, 1.0]     # stake of an ultimate holder in Boon Rawd (UNVERIFIED; illustrative only)

PE = {                                      # trailing P/E, aggregator, read 20 October 2026 (S)
    "Thai Beverage PCL (SGX Y92)": 10.87,
    "Ichitan Group PCL (SET ICHI)": 13.65,
    "Osotspa PCL (SET OSP)": 13.67,
    "Carabao Group PCL (SET CBG)": 24.10,
}
PE_FWD = {
    "Thai Beverage PCL (SGX Y92)": 9.76,
    "Ichitan Group PCL (SET ICHI)": 13.21,
    "Osotspa PCL (SET OSP)": 13.09,
    "Carabao Group PCL (SET CBG)": 16.55,
}
_pv = sorted(PE.values())
PE_MIN, PE_MAX = _pv[0], _pv[-1]
PE_MEDIAN = (_pv[1] + _pv[2]) / 2.0         # median of four = mean of the middle two

SCALE_SHARES = [0.001, 0.005, 0.01]         # 0.1, 0.5 and 1 percent of the reference net profit

PAGE_NOTE = "primary-origin page read through a page summary, not in full, so tiered S under Appendix A"

INPUTS = [
    {"key": "tax", "label": "Thai corporate income tax rate", "value": TAX, "unit": "fraction",
     "tier": "S", "status": "SOURCED",
     "source": "Revenue Department English site, Corporate Income Tax page, last updated 23.11.2020, 20 percent on net profit (accounting periods 2015); https://www.rd.go.th/english/6044.html; read 20 October 2026 (" + PAGE_NOTE + "); saved: rework/raw/diligence_2026-10-20/T12/revenue_dept_corporate_income_tax_and_dividend_rule_2026-10-20.md. Forvis Mazars (S, 20 Jan 2021) agrees"},
    {"key": "c_after", "label": "Cube contribution, after-excise basis (lead)", "value": round(C_AFTER, 4), "unit": "THB per cube",
     "tier": "DERIVED on PROXY and ASSUMPTION inputs", "status": "DERIVED",
     "source": "Planning price 15 times can net-to-listing ratio 7.393 / 13.8025 (can_cost_model_results.json), less cube cost 4.09; record rework/70 section 2.11 gives 3.94. Inputs: listing prices (S), VAT 7 percent (P), retailer margin (PROXY, group gross margins), distributor margin 10 to 20 percent (ASSUMPTION, unsourced), excise 14 percent (rate P as saved, base not read, ASSUMPTION), pouch and print costs of the cube (ASSUMPTION). Excludes binder and flavour (not priced), so an upper bound by those items"},
    {"key": "c_before", "label": "Cube contribution, before-excise basis (sensitivity, deck basis)", "value": C_BEFORE, "unit": "THB per cube",
     "tier": "DERIVED", "status": "DERIVED",
     "source": "rework/screen/project_valuation_results.json summary.base_case (ex-factory 9.00, 60 percent of the 15 THB planning price, less cost 4.09; before excise); the basis of the current deck and submission figures"},
    {"key": "c_cube_inv", "label": "Cube contribution, before excise on the can's invoice chain (team record)", "value": round(C_CUBE_INV, 4), "unit": "THB per cube",
     "tier": "DERIVED on PROXY and ASSUMPTION inputs", "status": "DERIVED",
     "source": "Invoice at the 15 THB planning price through VAT 7 percent, retailer margin 21.6 percent and distributor margin 15 percent (9.34), less cost 4.09"},
    {"key": "cost_base", "label": "Cube cost per cube, six-cube pack", "value": COST_BASE, "unit": "THB per cube",
     "tier": "DERIVED", "status": "DERIVED",
     "source": "rework/screen/project_valuation_results.json unit_economics.base_cost_thb"},
    {"key": "shelf", "label": "Planning shelf price per cube", "value": SHELF, "unit": "THB per cube",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "project_valuation_results.json unit_economics.shelf_thb (cube not priced; reference 330 mL cans, record 68d)"},
    {"key": "c_can", "label": "Singha Lemon Soda can contribution before aluminium (after excise)", "value": C_CAN, "unit": "THB per can",
     "tier": "DERIVED on PROXY and ASSUMPTION inputs", "status": "DERIVED",
     "source": "rework/screen/can_cost_model_results.json aluminium.contribution_pre_aluminium_thb_per_can. Inputs: listing price 13.80 THB (mean of four online prices, S), VAT (P), retailer margin (PROXY), distributor margin (ASSUMPTION, unsourced), excise (rate P as saved, base not read), non-aluminium cost (PROXY, US 2024 conversion cost, and ASSUMPTION bounds). An upper bound on lost contribution because the aluminium cost avoided is not netted; no aluminium price used; record rework/70"},
    {"key": "c_can_inv", "label": "Can contribution before aluminium and before excise (team record)", "value": round(C_CAN_INV, 4), "unit": "THB per can",
     "tier": "DERIVED on PROXY and ASSUMPTION inputs", "status": "DERIVED",
     "source": "Can invoice at 13.80 THB through the same chain (8.60) less the non-aluminium variable cost 3.266"},
    {"key": "vat", "label": "Value added tax rate (price chain)", "value": VAT, "unit": "fraction",
     "tier": "P", "status": "SOURCED",
     "source": "Revenue Department, rd.go.th/59.html, 7 percent, as saved in rework/raw/diligence_2026-10-20/T9/rd_vat_7_percent_2026.md (carried from singha_internal_estimates.py)"},
    {"key": "retail_margin", "label": "Retailer margin (price chain)", "value": RETAIL_MARGIN, "unit": "fraction",
     "tier": "S", "status": "PROXY",
     "source": "Big C group gross margin, all categories, FY2025 (stockanalysis, S); not beverage-specific"},
    {"key": "dist_margin", "label": "Distributor margin (price chain)", "value": DIST_MARGIN, "unit": "fraction",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "Unsourced band of 10 to 20 percent, central 15 percent (singha_internal_estimates.py)"},
    {"key": "excise", "label": "Excise rate (price chain)", "value": EXCISE, "unit": "fraction",
     "tier": "P as saved", "status": "SOURCED; base ASSUMPTION",
     "source": "Royal Gazette 2560, excise item 02.02, 14 percent ad valorem (rework/raw/gazette_sugar_drink_excise_primary_2560_A095_111.md, read from page images); base not read; applied to the ex-VAT invoice by assumption; whether a dissolvable cube falls under the item is not determined"},
    {"key": "np_2025", "label": "Singha Corporation net profit, 2025", "value": NP_GROUP_2025, "unit": "THB",
     "tier": "S", "status": "SOURCED",
     "source": "MGR Online, 23 May 2026, 2568 BE label printed; saved in rework/raw/diligence_2026-10-20/T12/mgronline_9690000048712_2026-05-23_extract.md; no source named in the article; not checked against a filing. Single-company figure, not consolidated group profit"},
    {"key": "np_2024", "label": "Singha Corporation net profit, 2024", "value": NP_GROUP_2024, "unit": "THB",
     "tier": "S", "status": "SOURCED",
     "source": "MGR Online, 23 May 2026, 2567 BE label printed; same extract"},
    {"key": "rev_2025", "label": "Singha Corporation total revenue, 2025", "value": REV_2025, "unit": "THB",
     "tier": "S", "status": "SOURCED",
     "source": "MGR Online, 23 May 2026, 2568 BE label printed; same extract"},
    {"key": "rev_2024", "label": "Singha Corporation total revenue, 2024", "value": REV_2024, "unit": "THB",
     "tier": "S", "status": "SOURCED",
     "source": "MGR Online, 23 May 2026, 2567 BE label printed; same extract"},
    {"key": "np_boonrawd_2022", "label": "Boon Rawd Brewery net profit, 2022 (latest year found)", "value": NP_BOONRAWD_2022, "unit": "THB",
     "tier": "S", "status": "PROXY",
     "source": "Thaiger, 18 April 2025 (as recorded in T6/07), https://thethaiger.com/th/news/1389992/, year 2565 BE; saved: rework/raw/diligence_2026-10-20/T12/thaiger_1389992_group_financials_2026-10-20.md; a larger denominator from a different year (2022 stands in for 2025); no filing cited; single-company figure"},
    {"key": "np_2023", "label": "Singha Corporation and Boon Rawd net profit, 2023; consolidated group profit", "value": None, "unit": "THB",
     "tier": "UNVERIFIED", "status": "UNVERIFIED",
     "source": "Not found on any page reached; the web search budget for the turn is used up and Creden and DBD amounts are behind a login or a 404. Statements for 2564 to 2568 BE are listed as filed on the Creden page. Consolidated group profit was not found at all"},
    {"key": "booking_entity", "label": "Entity that books the project profit", "value": "Singha Corporation", "unit": "text",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "The profit is earned by the group company that sells the cube. The model books it in Singha Corporation as a stated assumption. Creden gives Singha Corporation the TSIC code 64202 (holding company), and Thai Wikipedia describes it as the holding company for the Boon Rawd group, so a selling subsidiary is possible. Group profit after 20 percent tax is the same wherever it is booked"},
    {"key": "own_parent", "label": "Boon Rawd Brewery share of Singha Corporation", "value": OWN_PARENT, "unit": "fraction",
     "tier": "UNVERIFIED", "status": "UNVERIFIED",
     "source": "Not found in the sources read (Singha Corporation About page, footer 2014: 'important subsidiary'; Thai Wikipedia: Singha Corporation is the holding company for the group's businesses; Boon Rawd group page does not list Singha Corporation; Creden shareholders behind a login); 100 percent used as an upper bound for the parent"},
    {"key": "payout", "label": "Payout of incremental net profit by Singha Corporation (base)", "value": PAYOUT_BASE, "unit": "fraction",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "No dividend policy found for Singha Corporation or Boon Rawd (both unlisted). Creden shows Singha Corporation equity of about THB 19.5 billion against registered capital of THB 4.86 billion, which suggests retention in the past, so 100 percent is a high case; 50 percent alternative shown"},
    {"key": "parent_tax_full", "label": "Parent tax on dividend from Singha Corporation, full exclusion", "value": PARENT_TAX_FULL_EXCL, "unit": "fraction",
     "tier": "S", "status": "CONDITIONAL",
     "source": "RD page 6044 (" + PAGE_NOTE + "): full exclusion where the recipient owns at least 25 percent of the distributing company's capital, shares held 3 months before and 3 months after, and the distributing company holds no interest in the recipient. All three conditions are UNVERIFIED here (ownership not found), so 0 is a conditional value"},
    {"key": "parent_tax_half", "label": "Parent tax on dividend from Singha Corporation, half exclusion", "value": PARENT_TAX_HALF_EXCL, "unit": "fraction",
     "tier": "S", "status": "DERIVED",
     "source": "RD page 6044 (" + PAGE_NOTE + "): one-half of inter-company dividends excluded; the remaining half taxed at 20 percent, so 10 percent of gross"},
    {"key": "holder_payout", "label": "Share of Boon Rawd's dividend receipt passed to its holders", "value": HOLDER_PAYOUT, "unit": "fraction",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "Boon Rawd's own dividend policy not found; 100 percent is an upper bound"},
    {"key": "holder_wht", "label": "Holder-level tax on dividends (illustrative)", "value": HOLDER_WHT, "unit": "fraction",
     "tier": "S", "status": "ASSUMPTION",
     "source": "RD page 6045 (last updated 21.03.2024; " + PAGE_NOTE + "): 10 percent withheld at source on dividends where a Thai individual takes the separate-taxation option; whether the holders are Thai individuals and which option they take is not known. Corporate dividend withholding (10 percent in the RD page 6044 table) is not modelled"},
    {"key": "pe_peers", "label": "Peer trailing P/E (median of four)", "value": round(PE_MEDIAN, 3), "unit": "times",
     "tier": "S", "status": "SOURCED",
     "source": "stockanalysis.com statistics pages, read 20 October 2026, prices as of 19 October 2026: Y92 10.87, ICHI 13.65, OSP 13.67, CBG 24.10; saved in rework/raw/diligence_2026-10-20/T12/peer_pe_stockanalysis_2026-10-20.md; aggregator"},
    {"key": "pe_serm_suk", "label": "Serm Suk trailing P/E", "value": None, "unit": "times",
     "tier": "UNVERIFIED", "status": "UNVERIFIED",
     "source": "stockanalysis SSC statistics URL returned HTTP 404 on 20 October 2026; not read"},
    {"key": "policy_rate", "label": "Bank of Thailand policy rate", "value": POLICY_RATE, "unit": "fraction",
     "tier": "S", "status": "SOURCED",
     "source": "BOT press release No. 31/2026, MPC Decision 4/2026, 26 August 2026: policy rate maintained at 1.00 percent; https://www.bot.or.th/en/news-and-media/news/mpc/news-20260826-KsecaE98.html; read 20 October 2026 (" + PAGE_NOTE + "; a second fetch asked for the verbatim text returned a summary that gives the same decision); saved: rework/raw/diligence_2026-10-20/T12/bot_policy_rate_press_release_31_2026_2026-10-20.md. Trading Economics (S) agrees, saved in tradingeconomics_thailand_interest_rate_2026-10-20.md"},
    {"key": "premium", "label": "Premium over the policy rate (cost of capital = policy rate + premium)", "value": PREMIUMS, "unit": "fraction",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "Team choice: 7, 9 and 11 percentage points, giving 8, 10 and 12 percent. The 10 percent base was set in the earlier project_valuation.py and is kept; the premium of 9 points is back-solved to it and is not sourced. The sourced policy rate supplies 1 of the 10 points"},
    {"key": "rates", "label": "Cost of capital and discount rate", "value": RATES, "unit": "per year",
     "tier": "DERIVED", "status": "DERIVED",
     "source": "Policy rate 1.00 percent (S) plus the premium (ASSUMPTION)"},
    {"key": "cannib", "label": "Cannibalisation shares of cube buyers", "value": CANNIB, "unit": "fraction",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "Task scenario set (0, 25, 50, 100 percent); one displaced can per cube bought by a switcher (ASSUMPTION)"},
    {"key": "displacement_factor", "label": "Cans lost per cube bought by a buyer who says they switched", "value": 1.0, "unit": "cans per cube",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "One cube is one 330 mL serve, the size of one can; a buyer who says they switched may still buy cans, so the true factor may be lower, and a buyer who does not say so may still switch, so it may be higher. 0.5 and 1.5 are shown as an illustrative range"},
    {"key": "fixed_base", "label": "Annual fixed cash cost (base)", "value": FIXED_BASE, "unit": "THB per year",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "project_valuation.py FIXED_GRID; not sourced"},
    {"key": "vol_base", "label": "Cube volume at steady state (base)", "value": VOLUMES["base"], "unit": "cubes per year",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "project_valuation.py VOLUMES; no volume basis in the record"},
    {"key": "dep", "label": "Depreciation of year-0 setup outlay", "value": DEP_YEARS, "unit": "years",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "Straight line over five years; capitalised setup outlay"},
    {"key": "loss_tax", "label": "Tax treatment of a loss year", "value": "same-year credit (base); carry-forward and no relief shown", "unit": "text",
     "tier": "ASSUMPTION", "status": "ASSUMPTION",
     "source": "The base takes tax as 20 percent of the net incremental profit, so a loss year gives a credit, as if the cube and the can were booked in one taxpayer. Thai companies file separately, so a credit works only against the booking company's own taxable profit; the carry-forward case (loss set against later profit inside the five years, ASSUMPTION; the carry-forward rule was not read) and the no-relief case (loss never used) bound the effect"},
]


# ---- Cash flows -------------------------------------------------------------------------

def flows(c, volume, s, fixed, cc=None):
    """Per-year series for t = 0..HORIZON. s is the cannibalised share of cube buyers; cc the can contribution."""
    cc = C_CAN if cc is None else cc
    years = range(HORIZON + 1)
    q = [0.0] + [volume * r for r in RAMP]                     # cubes sold in year t
    cube = [c * q[t] for t in years]                           # cube contribution
    loss = [s * CAN_PER_CUBE * cc * q[t] for t in years]       # can contribution lost
    fx = [0.0] + [fixed] * HORIZON                             # annual fixed cash cost
    dep = [0.0] + [fixed / DEP_YEARS] * HORIZON                # depreciation of the setup
    ebitda = [cube[t] - loss[t] - fx[t] for t in years]
    ebit = [ebitda[t] - dep[t] for t in years]
    tax = [TAX * ebit[t] for t in years]                       # negative = credit (same-year offset)
    np_ = [ebit[t] - tax[t] for t in years]
    cf_after = [(-fixed if t == 0 else np_[t] + dep[t]) for t in years]
    cf_pre = [(-fixed if t == 0 else ebitda[t]) for t in years]
    return {"q": q, "cube": cube, "loss": loss, "ebitda": ebitda, "dep": dep, "ebit": ebit,
            "tax": tax, "np": np_, "cf_after": cf_after, "cf_pre": cf_pre}


def cash_after_tax_variant(c, volume, s, fixed, cc, mode):
    """After-tax cash flow under a loss-year treatment: same_year, carry_forward or no_relief."""
    fl = flows(c, volume, s, fixed, cc)
    pool = 0.0
    cf = [-fixed]
    for t in range(1, HORIZON + 1):
        e = fl["ebit"][t]
        if mode == "same_year":
            tax = TAX * e
        elif mode == "no_relief":
            tax = TAX * max(e, 0.0)
        elif mode == "carry_forward":
            if e < 0:
                pool += -e
                tax = 0.0
            else:
                use = min(pool, e)
                pool -= use
                tax = TAX * (e - use)
        else:
            raise ValueError(mode)
        cf.append(e - tax + fl["dep"][t])
    return cf


def npv(cf, rate):
    return sum(cf[t] / (1.0 + rate) ** t for t in range(len(cf)))


def npv_of(c, volume, s, fixed, rate, basis, cc=None):
    fl = flows(c, volume, s, fixed, cc)
    return npv(fl["cf_after"] if basis == "after" else fl["cf_pre"], rate)


def cumulative(cf):
    out, run = [], 0.0
    for x in cf:
        run += x
        out.append(run)
    return out


def payback_year(cf, rate=None):
    """First year-end at which the cumulative (discounted if rate given) cash flow is >= 0; linear within the year."""
    series = cf if rate is None else [cf[t] / (1.0 + rate) ** t for t in range(len(cf))]
    cum = cumulative(series)
    for t in range(1, len(cum)):
        if cum[t] >= 0 > cum[t - 1]:
            step = series[t]
            return round((t - 1) + (-cum[t - 1] / step), 2) if step != 0 else float(t)
    return None


def summary_for(c, volume, s, fixed, rate=RATE_BASE, cc=None):
    fl = flows(c, volume, s, fixed, cc)
    np_ = fl["np"]
    steady_np = np_[2]                                          # first full-volume year
    cum_np = sum(np_[1:])
    cum_group = HORIZON * NP_GROUP_2025
    npv_after = npv(fl["cf_after"], rate)
    npv_pre = npv(fl["cf_pre"], rate)
    roic = [np_[t] / fixed for t in range(1, HORIZON + 1)]
    div = [max(0.0, PAYOUT_BASE * np_[t]) if t >= 1 else 0.0 for t in range(HORIZON + 1)]
    parent_receipt = [OWN_PARENT * d * (1.0 - PARENT_TAX_FULL_EXCL) for d in div]
    parent_receipt_alt = [OWN_PARENT * d * (1.0 - PARENT_TAX_HALF_EXCL) for d in div]
    holder = {str(stake): [stake * HOLDER_PAYOUT * r for r in parent_receipt] for stake in HOLDER_STAKE_ILLUSTRATIVE}
    holder_after_wht = {str(stake): [stake * HOLDER_PAYOUT * r * (1.0 - HOLDER_WHT) for r in parent_receipt]
                        for stake in HOLDER_STAKE_ILLUSTRATIVE}
    pe_uplift = {"min": PE_MIN * steady_np, "median": PE_MEDIAN * steady_np, "max": PE_MAX * steady_np}
    return {
        "contribution_thb_per_cube": round(c, 4),
        "cubes_per_year": volume,
        "cannibalised_share": s,
        "fixed_cost_thb_per_year": fixed,
        "after_tax_cash_flow_thb": [round(x, 2) for x in fl["cf_after"]],
        "cumulative_after_tax_cash_flow_thb": [round(x, 2) for x in cumulative(fl["cf_after"])],
        "payback_year_undiscounted": payback_year(fl["cf_after"]),
        "payback_year_discounted_at_base_rate": payback_year(fl["cf_after"], rate),
        "pre_tax_cash_flow_thb": [round(x, 2) for x in fl["cf_pre"]],
        "incremental_profit_before_tax_thb": [round(x, 2) for x in fl["ebit"]],
        "incremental_net_profit_thb": [round(x, 2) for x in np_],
        "share_of_singha_np_2025_by_year": [round(x / NP_GROUP_2025, 8) for x in np_],
        "share_of_singha_np_2025_cumulative_y1_5": round(cum_np / cum_group, 8),
        "steady_state_net_profit_thb": round(steady_np, 2),
        "steady_state_share_of_np_2025": round(steady_np / NP_GROUP_2025, 8),
        "steady_state_share_of_boonrawd_np_2022_proxy": round(steady_np / NP_BOONRAWD_2022, 8),
        "npv_after_tax_thb": {str(r): round(npv(fl["cf_after"], r), 2) for r in RATES},
        "npv_pre_tax_thb": {str(r): round(npv(fl["cf_pre"], r), 2) for r in RATES},
        "npv_after_tax_at_base_rate_thb": round(npv_after, 2),
        "npv_pre_tax_at_base_rate_thb": round(npv_pre, 2),
        "npv_after_tax_as_share_of_np_2025": round(npv_after / NP_GROUP_2025, 8),
        "npv_pre_tax_as_share_of_np_2025": round(npv_pre / NP_GROUP_2025, 8),
        "dividend_declared_thb_by_year": [round(x, 2) for x in div],
        "dividend_received_by_boon_rawd_thb_by_year": [round(x, 2) for x in parent_receipt],
        "dividend_received_by_boon_rawd_half_exclusion_thb_by_year": [round(x, 2) for x in parent_receipt_alt],
        "dividend_received_by_boon_rawd_total_y1_5_thb": round(sum(parent_receipt), 2),
        "dividend_received_by_boon_rawd_half_exclusion_total_y1_5_thb": round(sum(parent_receipt_alt), 2),
        "cumulative_net_profit_y1_5_thb": round(sum(np_[1:]), 2),
        "dividend_to_holder_by_stake_before_holder_tax_thb_by_year": {k: [round(x, 2) for x in v] for k, v in holder.items()},
        "dividend_to_holder_by_stake_after_10pct_withholding_thb_by_year": {k: [round(x, 2) for x in v] for k, v in holder_after_wht.items()},
        "pe_equity_uplift_thb": {k: round(v, 2) for k, v in pe_uplift.items()},
        "npv_equity_uplift_thb": round(npv_after, 2),
        "roic_by_year": [round(x, 6) for x in roic],
        "roic_average_y1_5": round(sum(roic) / len(roic), 6),
        "roic_steady_state": round(steady_np / fixed, 6),
        "roic_steady_state_minus_hurdle_by_rate": {str(r): round(steady_np / fixed - r, 6) for r in RATES},
        "invested_capital_thb": fixed,
    }


# ---- Break points and scale (closed form: NPV is linear in s, in volume, in contribution and in fixed cost) ---

def zero_in_s(c, volume, fixed, rate, basis, cc=None):
    a = npv_of(c, volume, 0.0, fixed, rate, basis, cc)
    b = npv_of(c, volume, 1.0, fixed, rate, basis, cc) - a
    if b == 0:
        return None
    s_star = -a / b
    return {"raw": round(s_star, 6), "inside_0_to_1": (0.0 <= s_star <= 1.0)}


def zero_in_volume(c, s, fixed, rate, basis, cc=None):
    a0 = npv_of(c, 0.0, s, fixed, rate, basis, cc)
    a1 = npv_of(c, 1.0, s, fixed, rate, basis, cc)
    slope = a1 - a0
    if slope <= 0:
        return {"cubes_per_year": None, "positive": False}
    v_star = -a0 / slope
    return {"cubes_per_year": round(v_star, 1), "positive": v_star > 0}


def zero_in_fixed(c, volume, s, rate, basis, cc=None):
    """Largest annual fixed cost (and equal year-0 setup outlay) at which NPV is zero."""
    a0 = npv_of(c, volume, s, 0.0, rate, basis, cc)
    a1 = npv_of(c, volume, s, 1.0, rate, basis, cc)
    slope = a1 - a0
    if slope >= 0:
        return None
    f_star = -a0 / slope
    return round(f_star, 0) if f_star > 0 else None


def zero_in_contribution(volume, s, fixed, rate, basis, cc=None):
    """Cube contribution per cube at which the NPV is zero (the NPV is linear in the cube contribution)."""
    a0 = npv_of(0.0, volume, s, fixed, rate, basis, cc)
    a1 = npv_of(1.0, volume, s, fixed, rate, basis, cc)
    slope = a1 - a0
    if slope <= 0:
        return None
    return round(-a0 / slope, 4)


def volume_for_share(c, s, fixed, share, denom, cc=None):
    """Steady-state cubes a year at which incremental net profit equals share of the reference net profit."""
    cc = C_CAN if cc is None else cc
    margin = c - s * CAN_PER_CUBE * cc
    if margin <= 0:
        return None
    ebit_needed = share * denom / (1.0 - TAX)
    return (ebit_needed + fixed + fixed / DEP_YEARS) / margin


def per_cube_zero_share(c, cc=None):
    """Cannibalised share at which the cube's own contribution equals the can's (per cube)."""
    cc = C_CAN if cc is None else cc
    s_star = c / (CAN_PER_CUBE * cc)
    return {"raw": round(s_star, 6), "inside_0_to_1": (0.0 <= s_star <= 1.0)}


def s_for_roic(c, volume, fixed, hurdle, cc=None):
    """Cannibalised share at which steady-state ROIC (year-2 net profit / setup outlay) equals the hurdle."""
    cc = C_CAN if cc is None else cc
    need_ebit = hurdle * fixed / (1.0 - TAX) + fixed + fixed / DEP_YEARS
    s_star = (c - need_ebit / volume) / (CAN_PER_CUBE * cc)
    return {"raw": round(s_star, 6), "inside_0_to_1": (0.0 <= s_star <= 1.0)}


# ---- Checks ----------------------------------------------------------------------------

CHECKS = {}
base_pre = npv_of(C_BEFORE, VOLUMES["base"], 0.0, FIXED_BASE, RATE_BASE, "pre")
CHECKS["pre_tax_npv_matches_project_valuation"] = abs(base_pre - NPV_PRE_PV) < 1.0
CHECKS["pre_tax_npv_before_excise_basis"] = round(base_pre, 2)
CHECKS["pre_tax_npv_project_valuation"] = NPV_PRE_PV
assert CHECKS["pre_tax_npv_matches_project_valuation"], (base_pre, NPV_PRE_PV)

# Pre-tax, before-excise grid reproduces the deck's Appendix B (all 12 cells, three rates).
_grid_ok = True
for row in PV["scenario_results"]:
    for r in RATES:
        mine = npv_of(C_BEFORE, row["cubes_per_year"], 0.0, row["fixed_cost_thb_per_year"], r, "pre")
        if abs(mine - row["npv_thb"][str(r)]) > 1.0:
            _grid_ok = False
CHECKS["pre_tax_grid_reproduces_project_valuation_12_cells_3_rates"] = _grid_ok
assert _grid_ok

# Pre-tax break-even volumes and maximum fixed cost reproduce the deck.
_be_ok = True
for row in PV["break_even_by_fixed_cost"]:
    mine = zero_in_volume(C_BEFORE, 0.0, row["fixed_cost_thb_per_year"], RATE_BASE, "pre")["cubes_per_year"]
    if abs(mine - row["npv_zero_cubes_per_year"]["0.1"]) > 1.0:
        _be_ok = False
CHECKS["pre_tax_break_even_volumes_reproduce_project_valuation"] = _be_ok
assert _be_ok
_mf = zero_in_fixed(C_BEFORE, VOLUMES["base"], 0.0, RATE_BASE, "pre")
CHECKS["pre_tax_max_fixed_cost_base_reproduces_project_valuation"] = abs(_mf - PV["max_fixed_cost_by_scenario_thb_per_year"]["base"]["0.1"]) < 1.0
assert CHECKS["pre_tax_max_fixed_cost_base_reproduces_project_valuation"], _mf

# Pre-tax sensitivity table reproduces project_valuation (the stated contribution is rounded to 4 decimals,
# which moves the maximum fixed cost by up to about THB 5, so the tolerance is THB 10)
_sens_ok = True
for row in PV["sensitivities"]:
    mine = zero_in_fixed(row["contribution_per_cube_thb"], VOLUMES["base"], 0.0, RATE_BASE, "pre")
    if mine is None or abs(mine - row["max_fixed_cost_thb_per_year_base_volume_10pct"]) > 10.0:
        _sens_ok = False
CHECKS["pre_tax_sensitivity_max_fixed_cost_reproduces_project_valuation"] = _sens_ok
assert _sens_ok

# Cash identity: after-tax cash flow equals net profit plus depreciation (years 1 to 5)
_fl = flows(C_BEFORE, VOLUMES["base"], 0.0, FIXED_BASE)
CHECKS["cash_identity_ok"] = all(abs(_fl["cf_after"][t] - (_fl["np"][t] + _fl["dep"][t])) < 1e-6
                                 for t in range(1, HORIZON + 1))
assert CHECKS["cash_identity_ok"]

# The same-year variant equals the base after-tax flow in every lead case
_tv_ok = True
for _bk, _c, _cc, _n in BASES:
    for _s in CANNIB:
        _a = cash_after_tax_variant(_c, VOLUMES["base"], _s, FIXED_BASE, _cc, "same_year")
        _b = flows(_c, VOLUMES["base"], _s, FIXED_BASE, _cc)["cf_after"]
        if any(abs(x - y) > 1e-6 for x, y in zip(_a, _b)):
            _tv_ok = False
CHECKS["tax_variant_same_year_equals_base_flow"] = _tv_ok
assert _tv_ok

# Steady-state scale check: the volume formula returns the threshold profit
_v = volume_for_share(C_BEFORE, 0.0, FIXED_BASE, 0.001, NP_GROUP_2025)
_fl2 = flows(C_BEFORE, _v, 0.0, FIXED_BASE)
CHECKS["scale_formula_roundtrip_ok"] = abs(_fl2["np"][2] - 0.001 * NP_GROUP_2025) < 1.0
assert CHECKS["scale_formula_roundtrip_ok"], (_fl2["np"][2], 0.001 * NP_GROUP_2025)

# Break points are exact zeros of the NPV
for _bk, _c, _cc, _n in BASES:
    _s = zero_in_s(_c, VOLUMES["base"], FIXED_BASE, RATE_BASE, "after", _cc)["raw"]
    # raw is rounded to 6 decimals, so the residual NPV is a few THB at most
    assert abs(npv_of(_c, VOLUMES["base"], _s, FIXED_BASE, RATE_BASE, "after", _cc)) < 10.0, (_bk, _s)
    _f = zero_in_fixed(_c, VOLUMES["base"], 0.0, RATE_BASE, "after", _cc)
    assert abs(npv_of(_c, VOLUMES["base"], 0.0, _f, RATE_BASE, "after", _cc)) < 1.0, (_bk, _f)
    _h = s_for_roic(_c, VOLUMES["base"], FIXED_BASE, RATE_BASE, _cc)["raw"]
    _np2 = flows(_c, VOLUMES["base"], _h, FIXED_BASE, _cc)["np"][2]
    assert abs(_np2 / FIXED_BASE - RATE_BASE) < 1e-5, (_bk, _h, _np2)
    _k = zero_in_contribution(VOLUMES["base"], 0.0, FIXED_BASE, RATE_BASE, "after", _cc)
    # _k is rounded to 4 decimals; a THB 0.00005 move in contribution moves the NPV by about THB 25
    assert abs(npv_of(_k, VOLUMES["base"], 0.0, FIXED_BASE, RATE_BASE, "after", _cc)) < 100.0, (_bk, _k)
CHECKS["break_points_are_exact_zeros"] = True
CHECKS["cost_of_capital_equals_policy_rate_plus_premium"] = all(
    abs(r - (POLICY_RATE + p)) < 1e-12 for r, p in zip(RATES, PREMIUMS))
assert CHECKS["cost_of_capital_equals_policy_rate_plus_premium"]
CHECKS["price_chain_reproduces_can_net_7_393"] = abs(INV_CAN * (1.0 - EXCISE) - CAN_NET_AFTER_EXCISE) < 1e-3
CHECKS["price_chain_reproduces_cube_contribution_3_94"] = abs(INV_CUBE * (1.0 - EXCISE) - COST_BASE - C_AFTER) < 1e-3


# ---- Reconciliation of the excise sensitivity (3.65) with the chain contribution (3.94) --------

EXCISE_EXFACTORY = EX_FACTORY * EXCISE                       # 1.26 on the 9.00 ex-factory price
C_EXCISE_ON_EXFACTORY = C_BEFORE - EXCISE_EXFACTORY          # 3.65 (submission 05 line 103)
EXCISE_CHAIN = INV_CUBE * EXCISE                             # excise on the chain invoice
_diff = C_AFTER - C_EXCISE_ON_EXFACTORY
_diff_formula = (INV_CUBE - EX_FACTORY) * (1.0 - EXCISE)
assert abs(C_EXCISE_ON_EXFACTORY - 3.65) < 0.005, C_EXCISE_ON_EXFACTORY
assert abs(_diff - _diff_formula) < 1e-3, (_diff, _diff_formula)
RECON = {
    "shelf_price_thb": SHELF,
    "ex_factory_assumed_60pct_of_shelf_thb": EX_FACTORY,
    "invoice_from_the_cans_chain_thb": round(INV_CUBE, 4),
    "invoice_as_share_of_shelf": round(INV_CUBE / SHELF, 4),
    "excise_on_ex_factory_14pct_thb": round(EXCISE_EXFACTORY, 4),
    "excise_on_chain_invoice_14pct_thb": round(EXCISE_CHAIN, 4),
    "contribution_excise_on_ex_factory_thb": round(C_EXCISE_ON_EXFACTORY, 4),
    "contribution_chain_after_excise_thb": round(C_AFTER, 4),
    "difference_thb": round(_diff, 4),
    "difference_explained_thb": round(_diff_formula, 4),
    "reading": "Both take 14 percent excise off an invoice. Line 103 of submission 05 takes it off the assumed ex-factory price of THB 9.00 (60 percent of the shelf price); the chain takes it off the invoice of THB 9.34 that VAT 7 percent, the retailer margin of 21.6 percent and the distributor margin of 15 percent leave from the same THB 15 shelf price. The THB 0.29 gap is the difference between the two invoices (THB 0.34) after excise.",
    "max_fixed_cost_pre_tax_thb_by_contribution": {
        "3.65": zero_in_fixed(C_EXCISE_ON_EXFACTORY, VOLUMES["base"], 0.0, RATE_BASE, "pre"),
        "3.94": zero_in_fixed(C_AFTER, VOLUMES["base"], 0.0, RATE_BASE, "pre"),
    },
}


# ---- Scenario grids ---------------------------------------------------------------------

GRID = []
for basis_key, c, cc, _note in LEAD_BASES:
    for vol_key in ("low", "base", "high"):
        for s in CANNIB:
            row = summary_for(c, VOLUMES[vol_key], s, FIXED_BASE, cc=cc)
            row["basis"] = basis_key
            row["volume_scenario"] = vol_key
            row["cube_outside_excise_can_inside_row"] = (basis_key in CUBE_OUTSIDE_EXCISE_SCENARIO and s > 0)
            GRID.append(row)

FIXED_GRID_ROWS = []
for basis_key, c, cc, _note in LEAD_BASES:
    for f in FIXED_GRID:
        for s in (0.0, 0.5):
            row = summary_for(c, VOLUMES["base"], s, f, cc=cc)
            row["basis"] = basis_key
            row["fixed_cost_thb_per_year"] = f
            row["cube_outside_excise_can_inside_row"] = (basis_key in CUBE_OUTSIDE_EXCISE_SCENARIO and s > 0)
            FIXED_GRID_ROWS.append(row)

# Replacement grid for the deck's Appendix B and submission 05 (after tax, 10 percent, 0 percent cannibalisation)
REPLACEMENT_GRID = {}
for basis_key, c, cc, _note in LEAD_BASES:
    REPLACEMENT_GRID[basis_key] = {
        "npv_after_tax_thb_by_volume_and_fixed_cost": {
            vk: {str(f): round(npv_of(c, VOLUMES[vk], 0.0, f, RATE_BASE, "after"), 0) for f in FIXED_GRID}
            for vk in ("low", "base", "high")},
        "npv_pre_tax_thb_by_volume_and_fixed_cost": {
            vk: {str(f): round(npv_of(c, VOLUMES[vk], 0.0, f, RATE_BASE, "pre"), 0) for f in FIXED_GRID}
            for vk in ("low", "base", "high")},
        "max_fixed_cost_after_tax_thb_by_volume": {
            vk: zero_in_fixed(c, VOLUMES[vk], 0.0, RATE_BASE, "after") for vk in ("low", "base", "high")},
        "max_fixed_cost_pre_tax_thb_by_volume": {
            vk: zero_in_fixed(c, VOLUMES[vk], 0.0, RATE_BASE, "pre") for vk in ("low", "base", "high")},
        "break_even_cubes_after_tax_by_fixed_cost": {
            str(f): zero_in_volume(c, 0.0, f, RATE_BASE, "after")["cubes_per_year"] for f in FIXED_GRID},
        "break_even_cubes_pre_tax_by_fixed_cost": {
            str(f): zero_in_volume(c, 0.0, f, RATE_BASE, "pre")["cubes_per_year"] for f in FIXED_GRID},
        "npv_after_tax_thb_at_500k_by_cubes": {
            str(v): round(npv_of(c, v, 0.0, FIXED_BASE, RATE_BASE, "after"), 0) for v in (50000, 200000, 500000, 1000000)},
        "npv_pre_tax_thb_at_500k_by_cubes": {
            str(v): round(npv_of(c, v, 0.0, FIXED_BASE, RATE_BASE, "pre"), 0) for v in (50000, 200000, 500000, 1000000)},
    }

# Sensitivity table of submission 05 (lines 93 to 108) re-run on the lead basis, after tax, at base volume,
# 10 percent, 0 percent cannibalisation. Cost rows shift the lead contribution by the same THB delta as the
# pre-tax table; the shelf rows re-price through the can's chain; the ex-factory share rows and the excise row are
# replaced by the chain itself and are not re-run.
_SHELF_RE = re.compile(r"^Shelf price (\d+) THB")
SENS_AFTER = []
for row in PV["sensitivities"]:
    name = row["change"]
    if name.startswith("Dose 0.9"):
        continue                                           # superseded design; not in submission 05
    m = _SHELF_RE.match(name)
    entry = {"change": name, "pre_tax_before_excise_contribution_thb": row["contribution_per_cube_thb"],
             "pre_tax_before_excise_max_fixed_cost_thb": row["max_fixed_cost_thb_per_year_base_volume_10pct"]}
    if name.startswith("Ex-factory share") or name.startswith("Excise 14%"):
        entry["lead_basis"] = "not re-run: replaced by the can's chain (invoice 62.3 percent of shelf, excise 14 percent of the invoice)"
        entry["contribution_after_excise_thb"] = None
        entry["max_fixed_cost_after_tax_thb"] = None
    else:
        if m:
            c_new = int(m.group(1)) * CHAIN_RATIO - COST_BASE
        elif name.startswith("Base"):
            c_new = C_AFTER
        else:
            c_new = C_AFTER + row["delta_vs_base_thb"]
        entry["lead_basis"] = "re-run"
        entry["contribution_after_excise_thb"] = round(c_new, 4)
        entry["max_fixed_cost_after_tax_thb"] = zero_in_fixed(c_new, VOLUMES["base"], 0.0, RATE_BASE, "after")
        entry["max_fixed_cost_pre_tax_thb"] = zero_in_fixed(c_new, VOLUMES["base"], 0.0, RATE_BASE, "pre")
    SENS_AFTER.append(entry)

# Payout alternative (dividend timing only; NPV unchanged)
PAYOUT_ALT_ROWS = []
for basis_key, c, cc, _note in LEAD_BASES:
    for s in CANNIB:
        fl = flows(c, VOLUMES["base"], s, FIXED_BASE, cc)
        div_alt = [max(0.0, PAYOUT_ALT * x) if t >= 1 else 0.0 for t, x in enumerate(fl["np"])]
        PAYOUT_ALT_ROWS.append({
            "basis": basis_key,
            "cannibalised_share": s,
            "payout": PAYOUT_ALT,
            "dividend_declared_thb_by_year": [round(x, 2) for x in div_alt],
            "dividend_received_by_boon_rawd_half_exclusion_thb_by_year": [round(OWN_PARENT * x * (1.0 - PARENT_TAX_HALF_EXCL), 2) for x in div_alt],
            "cube_outside_excise_can_inside_row": (basis_key in CUBE_OUTSIDE_EXCISE_SCENARIO and s > 0),
        })

# ---- Tax treatment of a loss year ---------------------------------------------------------

TAX_LOSS = {}
for basis_key, c, cc, _note in BASES:
    rows = {}
    for s in CANNIB:
        npvs = {mode: round(npv(cash_after_tax_variant(c, VOLUMES["base"], s, FIXED_BASE, cc, mode), RATE_BASE), 2)
                for mode in ("same_year", "carry_forward", "no_relief")}
        rows[str(s)] = {
            "npv_after_tax_thb": npvs,
            "carry_forward_minus_same_year_thb": round(npvs["carry_forward"] - npvs["same_year"], 2),
            "no_relief_minus_same_year_thb": round(npvs["no_relief"] - npvs["same_year"], 2),
            "cube_outside_excise_can_inside_row": (basis_key in CUBE_OUTSIDE_EXCISE_SCENARIO and s > 0),
        }
    TAX_LOSS[basis_key] = rows
_y1 = flows(C_AFTER, VOLUMES["base"], 0.0, FIXED_BASE)
TAX_LOSS_YEAR1 = {
    "year1_profit_before_tax_thb_after_excise_0pct": round(_y1["ebit"][1], 2),
    "year1_tax_credit_thb_after_excise_0pct": round(-_y1["tax"][1], 2),
    "note": "The year-1 loss gives a same-year credit in the base. Under carry-forward the loss is set against the year-2 and year-3 profit; under no relief it is lost.",
}

# ---- Break points and scale summary ------------------------------------------------------

BREAK = {}
for basis_key, c, cc, note in BASES:
    BREAK[basis_key] = {
        "basis_note": note,
        "per_cube_cannibalised_share_where_cube_equals_can": per_cube_zero_share(c, cc),
        "npv_zero_cannibalised_share_after_tax_base_volume_fixed_500k_10pct": zero_in_s(c, VOLUMES["base"], FIXED_BASE, RATE_BASE, "after", cc),
        "npv_zero_cannibalised_share_pre_tax_base_volume_fixed_500k_10pct": zero_in_s(c, VOLUMES["base"], FIXED_BASE, RATE_BASE, "pre", cc),
        "npv_zero_cannibalised_share_after_tax_by_rate": {str(r): zero_in_s(c, VOLUMES["base"], FIXED_BASE, r, "after", cc) for r in RATES},
        "npv_zero_cannibalised_share_after_tax_by_volume": {str(v): zero_in_s(c, v, FIXED_BASE, RATE_BASE, "after", cc) for v in VOLUMES.values()},
        "npv_zero_cubes_per_year_after_tax_by_share": {str(s): zero_in_volume(c, s, FIXED_BASE, RATE_BASE, "after", cc) for s in CANNIB},
        "npv_zero_cubes_per_year_pre_tax_by_share": {str(s): zero_in_volume(c, s, FIXED_BASE, RATE_BASE, "pre", cc) for s in CANNIB},
        "max_fixed_cost_after_tax_base_volume_by_share": {str(s): zero_in_fixed(c, VOLUMES["base"], s, RATE_BASE, "after", cc) for s in CANNIB},
        "max_fixed_cost_pre_tax_base_volume_by_share": {str(s): zero_in_fixed(c, VOLUMES["base"], s, RATE_BASE, "pre", cc) for s in CANNIB},
        "npv_zero_contribution_per_cube_after_tax_base_volume_fixed_500k_10pct_by_share": {
            str(s): zero_in_contribution(VOLUMES["base"], s, FIXED_BASE, RATE_BASE, "after", cc) for s in CANNIB},
        "npv_zero_contribution_per_cube_pre_tax_base_volume_fixed_500k_10pct_by_share": {
            str(s): zero_in_contribution(VOLUMES["base"], s, FIXED_BASE, RATE_BASE, "pre", cc) for s in CANNIB},
        "cannibalised_share_where_steady_roic_equals_hurdle": {str(r): s_for_roic(c, VOLUMES["base"], FIXED_BASE, r, cc) for r in RATES},
        "scale_cubes_per_year_for_share_of_singha_np_2025_steady_state": {
            str(share): {str(s): (None if volume_for_share(c, s, FIXED_BASE, share, NP_GROUP_2025, cc) is None
                                  else round(volume_for_share(c, s, FIXED_BASE, share, NP_GROUP_2025, cc), 0))
                         for s in CANNIB}
            for share in SCALE_SHARES},
        "scale_cubes_per_year_for_share_of_boonrawd_np_2022_proxy_steady_state": {
            str(share): {str(s): (None if volume_for_share(c, s, FIXED_BASE, share, NP_BOONRAWD_2022, cc) is None
                                  else round(volume_for_share(c, s, FIXED_BASE, share, NP_BOONRAWD_2022, cc), 0))
                         for s in CANNIB}
            for share in SCALE_SHARES},
    }

_k_lead = BREAK["after_excise"]["npv_zero_contribution_per_cube_after_tax_base_volume_fixed_500k_10pct_by_share"]["0.0"]
_dist = C_AFTER - _k_lead
CONTRIBUTION_MARGIN = {
    "lead_contribution_thb": round(C_AFTER, 4),
    "npv_zero_contribution_thb_0pct_after_tax": _k_lead,
    "distance_thb": round(_dist, 4),
    "distance_pct_of_lead_contribution": round(100.0 * _dist / C_AFTER, 2),
    "reading": ("With no cannibalisation the NPV is zero at a contribution of about THB %.2f a cube, THB %.2f (%.1f percent) below the "
                "lead contribution of THB %.2f. The unpriced binder and flavour, the assumed pouch, print and processing costs and "
                "the excise base each move the contribution by that much or more, so the sign of the headline NPV is not robust."
                % (_k_lead, _dist, 100.0 * _dist / C_AFTER, C_AFTER)),
    "excise_sensitivity_3_65_is_above_break_even_by_thb": round(C_EXCISE_ON_EXFACTORY - _k_lead, 4),
}

# ---- Deck-basis before-excise rows against the run with both products before excise ----------

_cmp = {}
for _s in CANNIB:
    _d = summary_for(C_BEFORE, VOLUMES["base"], _s, FIXED_BASE, cc=C_CAN)["npv_after_tax_at_base_rate_thb"]
    _c2 = summary_for(C_CUBE_INV, VOLUMES["base"], _s, FIXED_BASE, cc=C_CAN_INV)["npv_after_tax_at_base_rate_thb"]
    _cmp[str(_s)] = {"npv_after_tax_deck_basis_cube_before_excise_can_after_excise_thb": _d,
                     "npv_after_tax_both_before_excise_chain_thb": _c2,
                     "difference_thb": round(_d - _c2, 2)}
BEFORE_EXCISE_COMPARISON = {
    "by_cannibalised_share": _cmp,
    "break_even_share_deck_basis": BREAK["before_excise"]["npv_zero_cannibalised_share_after_tax_base_volume_fixed_500k_10pct"]["raw"],
    "break_even_share_both_before_excise_chain": BREAK["before_excise_chain"]["npv_zero_cannibalised_share_after_tax_base_volume_fixed_500k_10pct"]["raw"],
    "reading": ("The deck-basis rows (cube before excise at 4.91, can after excise at 4.127) are the scenario in which only the can bears excise. "
                "Against the run with both products before excise on the can's invoice chain (cube 5.25, can 5.33) the break-even share is %.1f "
                "against %.1f percent. At a share of 25 percent the deck-basis NPV is THB %.2f million lower; at 50 and 100 percent it is THB %.2f "
                "and %.2f million less negative. The deck-basis figures are therefore a close read at 25 percent and flatter the NPV at 50 and 100 percent."
                % (100.0 * BREAK["before_excise"]["npv_zero_cannibalised_share_after_tax_base_volume_fixed_500k_10pct"]["raw"],
                   100.0 * BREAK["before_excise_chain"]["npv_zero_cannibalised_share_after_tax_base_volume_fixed_500k_10pct"]["raw"],
                   abs(_cmp["0.25"]["difference_thb"]) / 1e6, _cmp["0.5"]["difference_thb"] / 1e6, _cmp["1.0"]["difference_thb"] / 1e6)),
}

# ---- Review level for the pilot's cannibalisation question ---------------------------------

_S_STAR = BREAK["after_excise"]["npv_zero_cannibalised_share_after_tax_base_volume_fixed_500k_10pct"]["raw"]
_REVIEW_LEVEL = math.floor(_S_STAR * 100.0) / 100.0                    # rounded down to a whole percent
_a50 = summary_for(C_AFTER, VOLUMES["base"], 0.5, FIXED_BASE)
_a_rev = summary_for(C_AFTER, VOLUMES["base"], _REVIEW_LEVEL, FIXED_BASE)
REVIEW = {
    "basis": "after_excise (lead); 200,000 cubes a year; THB 500,000 fixed cost; 10 percent; after tax",
    "break_even_displaced_cans_per_cube": round(_S_STAR * CAN_PER_CUBE, 6),
    "mapping": "displaced cans per cube = stated switch share x cans lost per cube bought by a switcher (displacement factor). The model sets the factor to 1 (ASSUMPTION), so the model's cannibalised share equals the stated share.",
    "stated_switch_share_where_npv_is_zero_by_displacement_factor": {
        str(d): round(_S_STAR * CAN_PER_CUBE / d, 4) for d in DISPLACEMENT_FACTORS},
    "proposed_review_level_stated_switch_share": _REVIEW_LEVEL,
    "proposed_review_level_basis": "The break-even of about 7.5 percent rounded down to a whole percent. DERIVED on ASSUMPTION inputs. It moves with volume, contribution and the displacement factor, so it is re-read from the model with the pilot's own measured values.",
    "npv_after_tax_at_proposed_review_level_thb": _a_rev["npv_after_tax_at_base_rate_thb"],
    "old_trigger_stated_switch_share": 0.5,
    "npv_after_tax_at_old_trigger_thb": _a50["npv_after_tax_at_base_rate_thb"],
    "cubes_per_year_for_npv_zero_at_old_trigger": BREAK["after_excise"]["npv_zero_cubes_per_year_after_tax_by_share"]["0.5"]["cubes_per_year"],
    "break_even_share_by_steady_volume": {
        str(v): BREAK["after_excise"]["npv_zero_cannibalised_share_after_tax_by_volume"][str(v)] for v in VOLUMES.values()},
    "reading": ("The old trigger of 50 percent stated switchers lies far above the break-even: at 200,000 cubes a year the NPV is already "
                "minus THB %.2f million there, and the volume at which it returns to zero is about %s cubes a year. At 50,000 cubes a year "
                "the NPV is negative even with no cannibalisation, so the break-even share is below zero."
                % (abs(_a50["npv_after_tax_at_base_rate_thb"]) / 1e6,
                   "{:,.0f}".format(BREAK["after_excise"]["npv_zero_cubes_per_year_after_tax_by_share"]["0.5"]["cubes_per_year"]))),
}

# ---- Figures elsewhere in the proposal that depend on the contribution basis ----------------

_CPA = PV["acquisition_cross_check"]["cpa_thb_per_first_purchase"]
_POUCH_HIGH = [s for s in PV["sensitivities"] if s["change"].startswith("Pouch 2.70")][0]
assert abs(_CPA / C_BEFORE - PV["acquisition_cross_check"]["cubes_to_recover_cpa_at_base_contribution"]) < 0.1
assert abs((C_BEFORE + _POUCH_HIGH["delta_vs_base_thb"]) - _POUCH_HIGH["contribution_per_cube_thb"]) < 1e-9
DEPENDENT = {
    "cubes_to_recover_paid_click_cost_per_first_purchase": {
        "cost_per_first_purchase_thb": _CPA,
        "before_excise": round(_CPA / C_BEFORE, 1),
        "after_excise": round(_CPA / C_AFTER, 1),
        "note": "Submission 04 line 38 and submission 05 line 110 quote 234 cubes at 4.91",
    },
    "stop_rule_contribution_floor_thb_per_cube": {
        "before_excise_high_pouch_case": _POUCH_HIGH["contribution_per_cube_thb"],
        "pouch_cost_increase_thb": -_POUCH_HIGH["delta_vs_base_thb"],
        "after_excise_same_cost_increase": round(C_AFTER + _POUCH_HIGH["delta_vs_base_thb"], 4),
        "note": "Deck slides 11 and 13 and submission 06 set a floor of 3.51 (4.91 less 1.40 for a 2.70 THB pouch). The same 1.40 cost rise on the after-excise basis leaves the floor at the value shown",
    },
}

# ---- Denominator note ------------------------------------------------------------------------

DENOMINATORS = {
    "singha_corporation_np_2025_thb": NP_GROUP_2025,
    "boon_rawd_np_2022_thb": NP_BOONRAWD_2022,
    "boon_rawd_2022_over_singha_corporation_2025": round(NP_BOONRAWD_2022 / NP_GROUP_2025, 3),
    "note": "Both denominators are single-company press figures, not consolidated group profit, which was not found. Boon Rawd Brewery's 2022 net profit was about 1.9 times Singha Corporation's 2025 net profit, so a wider profit base would make every share smaller. Singha Corporation's profit includes dividends from group companies, so the two companies' profits cannot be added.",
}


# ---- Phrase-ready figures for the written text (so the record quotes the file, not memory) ---

def mil(x, nd=2):
    v = round(abs(x) / 1e6, nd)
    s = ("%." + str(nd) + "f") % v
    return ("minus " + s) if x < 0 else s


def pct(x, nd=1):
    return ("%." + str(nd) + "f") % (100.0 * x)


def thousands(x):
    return "{:,.0f}".format(x)


def build_text_figures():
    out = {}
    for bk, c, cc, _note in BASES:
        base = {str(s): summary_for(c, VOLUMES["base"], s, FIXED_BASE, cc=cc) for s in CANNIB}
        out[bk] = {
            "npv_after_tax_million_by_share": {k: mil(v["npv_after_tax_at_base_rate_thb"]) for k, v in base.items()},
            "npv_pre_tax_million_by_share": {k: mil(v["npv_pre_tax_at_base_rate_thb"]) for k, v in base.items()},
            "steady_net_profit_thousand_by_share": {k: thousands(v["steady_state_net_profit_thb"]) for k, v in base.items()},
            "steady_share_pct_of_np_2025_by_share": {k: pct(v["steady_state_share_of_np_2025"], 4) for k, v in base.items()},
            "npv_after_tax_share_pct_of_np_2025": pct(base["0.0"]["npv_after_tax_as_share_of_np_2025"], 4),
            "npv_pre_tax_share_pct_of_np_2025": pct(base["0.0"]["npv_pre_tax_as_share_of_np_2025"], 4),
            "break_even_share_after_tax_pct": pct(BREAK[bk]["npv_zero_cannibalised_share_after_tax_base_volume_fixed_500k_10pct"]["raw"]),
            "break_even_cubes_after_tax_0pct": thousands(BREAK[bk]["npv_zero_cubes_per_year_after_tax_by_share"]["0.0"]["cubes_per_year"]),
            "max_fixed_cost_after_tax_base": thousands(BREAK[bk]["max_fixed_cost_after_tax_base_volume_by_share"]["0.0"]),
            "scale_0p1pct_cubes": thousands(BREAK[bk]["scale_cubes_per_year_for_share_of_singha_np_2025_steady_state"]["0.001"]["0.0"]),
            "scale_0p5pct_cubes": thousands(BREAK[bk]["scale_cubes_per_year_for_share_of_singha_np_2025_steady_state"]["0.005"]["0.0"]),
            "scale_1pct_cubes": thousands(BREAK[bk]["scale_cubes_per_year_for_share_of_singha_np_2025_steady_state"]["0.01"]["0.0"]),
            "roic_steady_pct_0": pct(base["0.0"]["roic_steady_state"]),
            "roic_hurdle_share_pct_by_rate": {str(r): pct(BREAK[bk]["cannibalised_share_where_steady_roic_equals_hurdle"][str(r)]["raw"]) for r in RATES},
            "npv_zero_contribution_0pct_after_tax": BREAK[bk]["npv_zero_contribution_per_cube_after_tax_base_volume_fixed_500k_10pct_by_share"]["0.0"],
            "cube_outside_excise_can_inside_at_positive_share": bk in CUBE_OUTSIDE_EXCISE_SCENARIO,
        }
    return out


RESULT = {
    "model": "Singha Lemon Soda value accrual to Singha Corporation and Boon Rawd Brewery, desk model (revision 2, 20 October 2026)",
    "scope_note": "Model output for the proposal. Not a valuation opinion. Singha Corporation is unlisted; peer multiples are listed companies. The model books the project profit in Singha Corporation as an assumption.",
    "method": {
        "cash_flow_year_t": "after-tax: (EBITDA_t minus depreciation_t) times (1 minus 20 percent) plus depreciation_t, t = 1..5; year 0 = minus setup outlay",
        "ebitda_t": "cubes_t times contribution, minus cannibalised share times can contribution times cubes_t, minus fixed cost",
        "depreciation": "setup outlay (equal to one year's fixed cost) straight line over five years",
        "tax": "20 percent of the net incremental profit before tax, as if the cube and the can were booked in one taxpayer; a loss year gives a same-year credit in the base. Carry-forward and no-relief variants are in tax_loss_treatment",
        "share_of_np": "incremental net profit divided by Singha Corporation net profit 2025 (3,085 million), held flat",
        "dividends": "payout times positive incremental net profit; received by Boon Rawd at the stated ownership (100 percent assumed); passed to holders at the stated share",
        "pe_uplift": "peer trailing P/E times steady-state (year 2) incremental net profit; no terminal value in the project, so this overstates a five-year stream",
        "npv_uplift": "after-tax NPV at the base rate",
        "cost_of_capital": "Bank of Thailand policy rate 1.00 percent (S) plus a premium of 7, 9 and 11 points (ASSUMPTION): 8, 10 and 12 percent; the 10 percent base was kept from the earlier model",
        "roic": "steady-state (year 2) incremental net profit divided by the invested capital (setup outlay); upper bound, no working capital; compared with the cost of capital",
        "scale": "steady-state cubes a year at which incremental net profit equals the stated share of the reference net profit",
        "break_points": "NPV is linear in the cannibalised share, in volume, in fixed cost and in the contribution per cube, so the zero points are closed form",
        "bias": "The can contribution is before aluminium (loss overstated, which lowers the cannibalisation break points); the cube contribution excludes binder and flavour (value overstated, which raises them). The two are not sized, so the net direction is not known",
        "before_excise_scenario": "The before_excise basis nets a before-excise cube (4.91) against the can's after-excise contribution (4.127) when the cannibalised share is above zero. That is the scenario in which the cube is outside the excise and the can is inside it; rows are flagged cube_outside_excise_can_inside_row and carry that label. before_excise_chain is the run with both products before excise, compared in before_excise_comparison.",
    },
    "inputs": INPUTS,
    "contribution_bases": {
        "after_excise_thb": round(C_AFTER, 4),
        "before_excise_thb": C_BEFORE,
        "before_excise_chain_cube_thb": round(C_CUBE_INV, 4),
        "can_contribution_before_aluminium_after_excise_thb": C_CAN,
        "can_contribution_before_aluminium_before_excise_thb": round(C_CAN_INV, 4),
        "chain_ratio_can_net_to_listing": round(CHAIN_RATIO, 6),
        "note": "The after-excise basis is the lead because the can contribution is after excise and the cannibalisation netting must compare like with like. The before-excise basis (4.91) is the basis of the current deck and submission figures; at a cannibalised share above 0 it is the scenario in which the cube is outside the excise and the can is inside it. Excise classification and base of the cube are not verified.",
    },
    "contribution_reconciliation_3_65_vs_3_94": RECON,
    "contribution_margin_of_safety": CONTRIBUTION_MARGIN,
    "before_excise_comparison": BEFORE_EXCISE_COMPARISON,
    "checks": CHECKS,
    "base_case": {bk: {str(s): summary_for(c, VOLUMES["base"], s, FIXED_BASE, cc=cc) for s in CANNIB}
                  for bk, c, cc, _n in BASES},
    "tax_loss_treatment": TAX_LOSS,
    "tax_loss_year1": TAX_LOSS_YEAR1,
    "payout_alternative_50pct": PAYOUT_ALT_ROWS,
    "scenario_grid": GRID,
    "fixed_cost_rows": FIXED_GRID_ROWS,
    "replacement_grid_for_deck_appendix_b_and_submission_05": REPLACEMENT_GRID,
    "sensitivity_table_of_submission_05_on_lead_basis": SENS_AFTER,
    "break_points": BREAK,
    "pilot_review_level": REVIEW,
    "denominators": DENOMINATORS,
    "peer_pe": {"trailing": PE, "forward": PE_FWD, "min": PE_MIN, "median": round(PE_MEDIAN, 3), "max": PE_MAX},
    "dependent_figures_elsewhere_in_proposal": DEPENDENT,
    "text_figures": build_text_figures(),
    "unverified": [
        "Boon Rawd Brewery share of Singha Corporation (100 percent assumed).",
        "Shareholders of Boon Rawd Brewery and their stakes.",
        "Dividend policy and payout of Singha Corporation and Boon Rawd.",
        "Entity that books the project profit (Singha Corporation assumed).",
        "Singha Corporation and Boon Rawd net profit and revenue for 2023 (not found); Boon Rawd 2023 to 2025 (not found); consolidated group profit (not found).",
        "Serm Suk P/E (page 404).",
        "Corporate dividend withholding (10 percent in the RD table; credit and exemption treatment not read) and the holder type for holder-level tax.",
        "Excise base and classification of the cube (14 percent ad valorem, base not read).",
        "Premium over the policy rate (ASSUMPTION); the 10 percent base is kept from the earlier model.",
        "Carry-forward rule for tax losses (not read); the carry-forward variant is an ASSUMPTION.",
        "Displacement factor of a stated switcher (1 assumed).",
    ],
}


def main():
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(RESULT, fh, indent=2, sort_keys=True)
        fh.write("\n")
    b = RESULT["base_case"]
    print("written:", OUT_PATH)
    print("checks:", {k: v for k, v in CHECKS.items() if isinstance(v, bool)})
    for basis in ("after_excise", "before_excise", "before_excise_chain"):
        for s in ("0.0", "0.25", "0.5", "1.0"):
            r = b[basis][s]
            print(basis, "s=", s,
                  "NPV after tax 10%:", r["npv_after_tax_at_base_rate_thb"],
                  "pre-tax:", r["npv_pre_tax_at_base_rate_thb"],
                  "steady NP:", r["steady_state_net_profit_thb"],
                  "steady share:", r["steady_state_share_of_np_2025"])
    print("break-even share after tax:", {k: v["npv_zero_cannibalised_share_after_tax_base_volume_fixed_500k_10pct"]["raw"]
                                         for k, v in BREAK.items()})
    print("contribution break-even:", CONTRIBUTION_MARGIN["npv_zero_contribution_thb_0pct_after_tax"],
          "distance:", CONTRIBUTION_MARGIN["distance_thb"], CONTRIBUTION_MARGIN["distance_pct_of_lead_contribution"])
    print("reconciliation:", RECON["contribution_excise_on_ex_factory_thb"], RECON["contribution_chain_after_excise_thb"],
          RECON["difference_thb"], RECON["invoice_from_the_cans_chain_thb"])
    print("tax loss treatment (after excise, 0 percent):", TAX_LOSS["after_excise"]["0.0"])
    print("review:", REVIEW["proposed_review_level_stated_switch_share"],
          REVIEW["stated_switch_share_where_npv_is_zero_by_displacement_factor"])


if __name__ == "__main__":
    main()
