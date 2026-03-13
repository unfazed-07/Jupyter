import streamlit as st
def calculate_old_tax_regime(taxable_income):
    slabs=[
        (300000, 0),
        (600000, 0.05),
        (900000, 0.1),
        (1200000, 0.15),
        (1500000, 0.2),
        (float('inf'), 0.3)
    ]

    prev_slab=0
    tax=0

    for limit, rate in slabs:
        if taxable_income>limit:
            tax+=(limit-prev_slab)*rate
            prev_slab=limit
        else:
            tax+=(taxable_income-prev_slab)*rate
            break
    return tax*1.04 #Cess Included



def  calculate_new_tax_regime(taxable_income):
    slabs=[
        (400000,0),
        (800000,0.05),
        (1200000,0.1),
        (1600000,0.15),
        (2000000,0.2),
        (float('inf'), 0.3)
    ]

    prev_slab=0
    tax=0

    for limit, rate in slabs:
        if taxable_income>limit:
            tax+=(limit-prev_slab)*rate
            prev_slab=limit
        else:
            tax+=(taxable_income-prev_slab)*rate
            break
    return tax*1.04 #Cess Included
    
def epf_deduction(CTC):
    base_sal=0.4*CTC
    epf=.12*base_sal
    return epf

def take_home_salary(CTC, regime):
    standard_deduction=75000 if regime=='new regime' else 50000
    professional_tax=2500 #2500 is considered for professional tax, though it vaies by states, i have taken its avergae or rough estimate
    taxable_income=CTC-standard_deduction
    if regime=='new regime':
        income_tax=calculate_new_tax_regime(taxable_income)
    else:
        income_tax=calculate_old_tax_regime(taxable_income)
    epf_ded=epf_deduction(CTC)
    net_salary= CTC  -  income_tax  -  epf_ded  -  professional_tax
    return {
        "CTC": f"₹{CTC}",
        "Taxable Income":f"₹{taxable_income:.2f}",
        "Income Tax":f"₹{income_tax:.2f} (estimated)",
        "EPF deduction":f"₹{epf_ded:.2f}",
        "Professional Tax":f"₹{professional_tax:.2f}",
        "Net Take-Home(Yearly)":f"₹{round(net_salary,2)}",
        "Net Take-Home(Monthly)":f"₹{round(net_salary/12,2)}"
    }
with st.container():
    st.title("India Salery Tax Calcurlator")
    #Input of salery
    salary=st.number_input("Enter Your annual CTC (₹):", min_value=0, step=10000)
    #Tab creation
    if salary>0:
        if st.button("View Breakdown"):

            tab1, tab2 =st.tabs(["New Regime", "Old Regime"])
            with tab1:
                st.header("Breakdown (New Regime)")
                breakdown=take_home_salary(salary, 'new regime')
                for k, v in breakdown.items():
                    st.write(f"{k}: {v}")
            with tab2:
                st.header("Breakdown (Old Regime)")
                breakdown=take_home_salary(salary, "old regime")
                for k, v in breakdown.items():
                    st.write(f"{k}: {v}")
    else:
        st.warning("Please enter your Annual CTC.")