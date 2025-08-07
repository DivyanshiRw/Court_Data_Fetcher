# app.py
import streamlit as st
from scraper import fetch_case_details
from config import DEBUG

# ---------------------- Streamlit Page Config ----------------------
st.set_page_config(
    page_title="Delhi High Court Case Search",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------- Title & Instructions ----------------------
st.title("🧾 Delhi High Court Case Search")
st.markdown("Enter the case details to fetch current case status and documents.")

# ---------------------- Input Form ----------------------
with st.form(key="case_form"):
    case_type = st.selectbox("Case Type", [
        "ADMIN.REPORT","ARB.A.","ARB. A. (COMM.)","ARB.P.","BAIL APPLN.",
                "CA","CA (COMM.IPD‑CR)","C.A.(COMM.IPD‑GI)","C.A.(COMM.IPD‑PAT)","C.A.(COMM.IPD‑PV)",
                "C.A.(COMM.IPD‑TM)","CAVEAT(CO.)","CC(ARB.)","CCP(CO.)","CCP(REF)","CEAC",
                "CEAR","CHAT.A.C.","CHAT.A.REF","CMI","CM(M)","CM(M)-IPD","C.O.","CO.APP.",
                "CO.APPL.(C)","CO.APPL.(M)","CO.A(SB)","C.O.(COMM.IPD‑CR)","C.O.(COMM.IPD‑GI)",
                "C.O.(COMM.IPD‑PAT)","C.O.(COMM.IPD‑TM)","CO.EX.","CONT.APP.(C)","CONT.CAS(C)",
                "CONT.CAS.(CRL)","CO.PET.","C.REF.(O)","CRL.A.","CRL.L.P.","CRL.M.C.","CRL.M.(CO.)",
                "CRL.M.I.","CRL.O.","CRL.O.(CO.)","CRL.REF.","CRL.REV.P.","CRL.REV.P.(MAT.)",
                "CRL.REV.P.(NDPS)","CRL.REV.P.(NI)","C.R.P.","CRP‑IPD","C.RULE","CS(COMM)","CS(OS)",
                "GP","CUSAA","CUS.A.C.","CUS.A.R.","CUSTOM A.","DEATH SENTENCE REF.","DEMO",
                "EDC","EDR","EFA(COMM)","EFA(OS)","EFA(OS) (COMM)","EFA(OS) (IPD)","EL.PET.","ETR",
                "EX.F.A.","EX.P.","EX.S.A.","FAO","FAO (COMM)","FAO-IPD","FAO(OS)","FAO(OS) (COMM)",
                "FAO(OS)(IPD)","GCAC","GCAR","GTA","GTC","GTR","I.A.","I.P.A.","ITA","ITC","ITR",
                "ITSA","LA.APP.","LPA","MAC.APP.","MAT.","MAT.APP.","MAT.APP.(F.C.)","MAT.CASE",
                "MAT.REF.","MISC. APPEAL(PMLA)","OA","OCJA","O.M.P.","O.M.P. (COMM)","O.M.P. (CONT.)",
                "O.M.P. (E)","O.M.P. (E) (COMM.)","O.M.P.(EFA)(COMM.)","O.M.P. (ENF.) (COMM.)",
                "O.M.P.(I)","O.M.P. (I) (COMM.)","O.M.P. (J) (COMM.)","O.M.P. (MISC.)",
                "O.M.P.(MISC.)(COMM.)","O.M.P.(T)","O.M.P. (T) (COMM.)","O.REF.","RC.REV.","RC.S.A.",
                "RERA APPEAL","REVIEW PET.","RFA","RFA(COMM)","RFA-IPD","RFA(OS)","RFA(OS)(COMM)",
                "RFA(OS)(IPD)","RSA","SCA","SDR","SERTA","ST.APPL.","STC","ST.REF.","SUR.T.REF.",
                "TEST.CAS.","TR.P.(C)","TR.P.(C.)","TR.P.(CRL.)","VAT APPEAL","W.P.(C)",
                "W.P.(C)-IPD","WP(C)(IPD)","W.P.(CRL)","WTA","WTC","WTR"
    ], help="Start typing to filter case types")
    
    case_number = st.text_input("Case Number", placeholder="Enter Case Number (e.g., 1234)")
    filing_year = st.text_input("Filing Year", placeholder="Enter Filing Year (e.g., 2024)")
    
    submit_button = st.form_submit_button(label="🔍 Search Case Status")

# ---------------------- Results Section ----------------------
if submit_button:
    if not (case_type and case_number and filing_year):
        st.warning("⚠️ Please fill in all fields.")
    else:
        with st.spinner("Fetching case details..."):
            result, message = fetch_case_details(case_type, case_number, filing_year)

        if result:
            st.success("✅ Case details fetched successfully!")

            st.markdown("## ⚖️ Case Status Result")
            
            # Plain Table Format
            st.markdown("""
            <table>
                <thead>
                    <tr>
                        <th style="text-align: left;">Field</th>
                        <th style="text-align: left;">Details</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>👥 Parties' Names</td>
                        <td>{parties}</td>
                    </tr>
                    <tr>
                        <td>📅 Filing Date</td>
                        <td>{filing_date}</td>
                    </tr>
                    <tr>
                        <td>🔔 Next Hearing Date</td>
                        <td>{next_hearing}</td>
                    </tr>
                    <tr>
                        <td>📄 Order</td>
                        <td>{download_button}</td>
                    </tr>
                </tbody>
            </table>
            """.format(
                parties=result["parties"],
                filing_date=result["filing_date"],
                next_hearing=result["next_hearing"],
                download_button=(
                    f"<a href='{result['pdf_link']}' target='_blank'>Download PDF</a>"
                    if result["pdf_link"]
                    else "Not Available"
                )
            ), unsafe_allow_html=True)

            

        else:
            st.error(message)
