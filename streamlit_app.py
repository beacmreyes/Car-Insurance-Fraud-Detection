# general libraries
import pickle
import pandas as pd

# model deployment
import streamlit as st
from datetime import datetime

# read model and holdout data
model = pickle.load(open('lr_tk.pkl', 'rb'))


html_temp = """
<div style="background:#025246 ;padding:10px">
<h2 style="color:white;text-align:center;"> Car Insurance Fraud Detection ML App </h2>
</div>
"""
st.markdown(html_temp, unsafe_allow_html = True)
import streamlit as st
from datetime import datetime

def main():
    st.markdown("<h2 style='text-align: center; color: #333;'>Policy Holder</h2>", unsafe_allow_html=True)
    Sex = st.selectbox("Sex", ["","Male","Female"])
    MaritalStatus = st.selectbox("Marital Status", ["","Single","Married","Divorced","Widow"])
    AgeOfPolicyHolder = st.number_input("Age", min_value=0, max_value=150)
    AddressChangeClaim = st.selectbox("Address Change - Claim", ["","no change","under 6 months","1 year","2 to 3 years","4 to 8 years"])
    DriverRating = st.selectbox("Driver Rating", [None,1,2,3,4])

    st.markdown("<h2 style='text-align: center; color: #333;'>Policy Details</h2>", unsafe_allow_html=True)
    PolicyDate = st.date_input("Policy Start Date", datetime.now())
    BasePolicy = st.selectbox("Base Policy", ["","All Perils","Collision","Liability"])
    Deductible = st.number_input("Deductible", min_value=0)
    NumberOfCars = st.selectbox("Number of Cars", ["","1 vehicle","2 vehicles","3 to 4","5 to 8","more than 8"])    
    AgentType = st.selectbox("Agent Type", ["","Internal","External"])
    RepNumber = st.selectbox("Rep Number", [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
    NumberOfSuppliments = st.selectbox("Number of Supliments", ["none","1 to 2","3 to 5","more than 5"])
    ClaimDate = st.date_input("Date Claimed", datetime.now())
    PastNumberOfClaims = st.selectbox("Past Number of Claims", ["none",1,"2 to 4","more than 4"])

    st.markdown("<h2 style='text-align: center; color: #333;'>Vehicle</h2>", unsafe_allow_html=True)
    VehicleCategory = st.selectbox("Vehicle Category", ["","Sedan","Sport","Utility"])
    Make = st.selectbox("Make", ["","Accura","BMW","Chevrolet","Dodge","Ferrari","Ford","Honda","Jaguar","Lexus","Mazda","Mecedes","Mercury","Nisson","Pontiac","Porche","Saab","Saturn","Toyota","VW"])
    VehiclePrice = st.selectbox("Vehicle Price", ["","less than 20,000","20,000 to 29,000","30,000 to 39,000","40,000 to 59,000","60,000 to 69,000","more than 69,000"])
    AgeOfVehicle = st.selectbox("Age of Vehicle", ["","new","2 years","3 years","4 years","5 years","6 years","7 years","more than 7"])

    st.markdown("<h2 style='text-align: center; color: #333;'>Accident</h2>", unsafe_allow_html=True)
    AccidentDate = st.date_input("Date of Accident", datetime.now())
    AccidentArea = st.selectbox("Accident Area", ["","Rural","Urban"])
    Fault = st.selectbox("Fault", ["","Policy Holder","Third Party"])
    PoliceReportFiled = st.selectbox("Police Report Filed", ["","Yes","No"])
    WitnessPresent = st.selectbox("Witness Present", ["","Yes","No"])



    # output = predict_if_fraud(choice)
    if st.button("Predict"):
        Year = AccidentDate.year
        Month = AccidentDate.strftime("%b")
        WeekOfMonth = (AccidentDate.day - 1) // 7 + 1
        DayOfWeek = AccidentDate.strftime("%A")
        DaysPolicyAccident =  (AccidentDate - PolicyDate).days

        if DaysPolicyAccident  <= 0:
            DaysPolicyAccident = 'none'

        elif  DaysPolicyAccident <= 7:
            DaysPolicyAccident = '1 to 7'

        elif  DaysPolicyAccident <= 15:
            DaysPolicyAccident = '8 to 15'

        elif  DaysPolicyAccident <= 30:
            DaysPolicyAccident = '15 to 30'
        else:
            DaysPolicyAccident ='more than 30'
        
        MonthClaimed = ClaimDate.strftime("%b")
        WeekOfMonthClaimed = (ClaimDate.day - 1) // 7 + 1
        DayOfWeekClaimed = ClaimDate.strftime("%A")
        DaysPolicyClaim =  (ClaimDate - PolicyDate).days
        if DaysPolicyClaim  <= 0:
            DaysPolicyClaim = 'none'

        elif  DaysPolicyClaim <= 7:
            DaysPolicyClaim = '1 to 7'

        elif  DaysPolicyClaim <= 15:
            DaysPolicyClaim = '8 to 15'

        elif  DaysPolicyClaim <= 30:
            DaysPolicyClaim = '15 to 30'
        else:
            DaysPolicyClaim ='more than 30'
        
        compiled_values = [Month , WeekOfMonth , DayOfWeek , Make , AccidentArea , DayOfWeekClaimed , MonthClaimed , WeekOfMonthClaimed ,
            Sex , MaritalStatus , Fault , VehicleCategory , VehiclePrice , RepNumber , Deductible , DriverRating ,
                DaysPolicyAccident , DaysPolicyClaim , PastNumberOfClaims , AgeOfVehicle , AgeOfPolicyHolder ,
                PoliceReportFiled , WitnessPresent , AgentType , NumberOfSuppliments , AddressChangeClaim , NumberOfCars , Year , BasePolicy
            ]

        columns = ["Month" , "WeekOfMonth" , "DayOfWeek" , "Make" , "AccidentArea" , "DayOfWeekClaimed" , "MonthClaimed" , "WeekOfMonthClaimed" ,
                    "Sex" , "MaritalStatus" , "Fault" , "VehicleCategory" , "VehiclePrice" , "RepNumber" , "Deductible" , "DriverRating" , "Days:Policy-Accident" ,
                    "Days:Policy-Claim" , "PastNumberOfClaims" , "AgeOfVehicle" , "AgeOfPolicyHolder" , "PoliceReportFiled" , "WitnessPresent" , "AgentType" , 
                    "NumberOfSuppliments" , "AddressChange-Claim" , "NumberOfCars" , "Year" , "BasePolicy"]
        df_final = pd.DataFrame([compiled_values], columns = columns)

        df_final_orig_columns = df_final.columns.tolist()
        to_drop3 = []
        for col in df_final_orig_columns:
            if df_final[col].dtype == 'O':
                dummies = pd.get_dummies(df_final[col], prefix=col, drop_first=False)
                df_final = pd.concat([df_final, dummies], axis=1)
                to_drop3.append(col)
        df_final = df_final.drop(to_drop3, axis=1)


        complete_features = ["WeekOfMonth" , "WeekOfMonthClaimed" , "RepNumber" , "Deductible" , "DriverRating" , "Year" , "Month_Apr" , 
                            "Month_Aug" , "Month_Dec" , "Month_Feb" , "Month_Jan" , "Month_Jul" , "Month_Jun" , "Month_Mar" , "Month_May" ,
                            "Month_Nov" , "Month_Oct" , "Month_Sep" , "DayOfWeek_Friday" , "DayOfWeek_Monday" , "DayOfWeek_Saturday" , "DayOfWeek_Sunday" ,
                            "DayOfWeek_Thursday" , "DayOfWeek_Tuesday" , "DayOfWeek_Wednesday" , "Make_Accura" , "Make_BMW" , "Make_Chevrolet" , "Make_Dodge" , 
                            "Make_Ferrari" , "Make_Ford" , "Make_Honda" , "Make_Jaguar" , "Make_Lexus" , "Make_Mazda" , "Make_Mecedes" , "Make_Mercury" ,
                            "Make_Nisson" , "Make_Pontiac" , "Make_Porche" , "Make_Saab" , "Make_Saturn" , "Make_Toyota" , "Make_VW" , "AccidentArea_Rural" ,
                            "AccidentArea_Urban" , "DayOfWeekClaimed_Friday" , "DayOfWeekClaimed_Monday" , "DayOfWeekClaimed_Saturday" ,
                            "DayOfWeekClaimed_Sunday" , "DayOfWeekClaimed_Thursday" , "DayOfWeekClaimed_Tuesday" , "DayOfWeekClaimed_Wednesday" ,
                            "MonthClaimed_Apr" , "MonthClaimed_Aug" , "MonthClaimed_Dec" , "MonthClaimed_Feb" , "MonthClaimed_Jan" , "MonthClaimed_Jul" , 
                            "MonthClaimed_Jun" , "MonthClaimed_Mar" , "MonthClaimed_May" , "MonthClaimed_Nov" , "MonthClaimed_Oct" , "MonthClaimed_Sep" ,
                            "Sex_Female" , "Sex_Male" , "MaritalStatus_Divorced" , "MaritalStatus_Married" , "MaritalStatus_Single" , "MaritalStatus_Widow" ,
                            "Fault_Policy Holder" , "Fault_Third Party" , "VehicleCategory_Sedan" , "VehicleCategory_Sport" , "VehicleCategory_Utility" ,
                            "VehiclePrice_20,000 to 29,000" , "VehiclePrice_30,000 to 39,000" , "VehiclePrice_40,000 to 59,000" , "VehiclePrice_60,000 to 69,000" , 
                            "VehiclePrice_less than 20,000" , "VehiclePrice_more than 69,000" , "Days:Policy-Accident_1 to 7" , "Days:Policy-Accident_15 to 30" , 
                            "Days:Policy-Accident_8 to 15" , "Days:Policy-Accident_more than 30" , "Days:Policy-Accident_none" , "Days:Policy-Claim_15 to 30" ,
                            "Days:Policy-Claim_8 to 15" , "Days:Policy-Claim_more than 30" , "PastNumberOfClaims_1" , "PastNumberOfClaims_2 to 4" , "PastNumberOfClaims_more than 4" , 
                            "PastNumberOfClaims_none" , "AgeOfVehicle_2 years" , "AgeOfVehicle_3 years" , "AgeOfVehicle_4 years" , "AgeOfVehicle_5 years" , "AgeOfVehicle_6 years" , "AgeOfVehicle_7 years" , 
                            "AgeOfVehicle_more than 7" , "AgeOfVehicle_new" , "AgeOfPolicyHolder_16 to 17" , "AgeOfPolicyHolder_18 to 20" , "AgeOfPolicyHolder_21 to 25" , "AgeOfPolicyHolder_26 to 30" , "AgeOfPolicyHolder_31 to 35" ,
                            "AgeOfPolicyHolder_36 to 40" , "AgeOfPolicyHolder_41 to 50" , "AgeOfPolicyHolder_51 to 65" , "AgeOfPolicyHolder_over 65" , "PoliceReportFiled_No" , "PoliceReportFiled_Yes" , "WitnessPresent_No" , "WitnessPresent_Yes" ,
                            "AgentType_External" , "AgentType_Internal" , "NumberOfSuppliments_1 to 2" , "NumberOfSuppliments_3 to 5" , "NumberOfSuppliments_more than 5" , "NumberOfSuppliments_none" , "AddressChange-Claim_1 year" , "AddressChange-Claim_2 to 3 years" ,
                            "AddressChange-Claim_4 to 8 years" , "AddressChange-Claim_no change" , "AddressChange-Claim_under 6 months" , "NumberOfCars_1 vehicle" , 
                            "NumberOfCars_2 vehicles" , "NumberOfCars_3 to 4" , "NumberOfCars_5 to 8" , 
                            "NumberOfCars_more than 8" , "BasePolicy_All Perils" , 
                            "BasePolicy_Collision" , "BasePolicy_Liability"
                                ]
    

        missing_features = list(set(complete_features) - set(df_final.columns.tolist()))

        
        for f in missing_features:
            df_final[f] = False

        df_final = df_final[complete_features]


        output = model.predict(df_final)

        if output:
            st.error('This transaction may be FRAUDULENT', icon="🚨")
        else:
            st.success('This transaction is approved!', icon="✅")
 
if __name__ == "__main__":
    main()
