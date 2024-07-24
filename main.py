import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize-matplotlib
# Load the data from the CSV file
@st.cache
def load_data(file_path):
    data = pd.read_csv(file_path, encoding='cp949')
    return data

# Calculate the proportion of elementary school-aged children
def calculate_proportion(data, region):
    region_data = data[data['행정구역'].str.contains(region)]
    total_population = region_data['2024년06월_계_총인구수'].astype(int).sum()
    elem_school_ages = ['2024년06월_계_6세', '2024년06월_계_7세', '2024년06월_계_8세', 
                        '2024년06월_계_9세', '2024년06월_계_10세', '2024년06월_계_11세']
    elem_population = region_data[elem_school_ages].astype(int).sum(axis=1).sum()
    
    return total_population, elem_population

# Streamlit app
def main():
    st.title("Elementary School Age Population Proportion by Region")
    
    # Load data
    file_path = 'path/to/your/file.csv'  # Replace with the correct file path
    data = load_data(file_path)
    
    # User input for region
    region = st.text_input("Enter the region:")
    
    if region:
        total_population, elem_population = calculate_proportion(data, region)
        
        if total_population == 0:
            st.write("No data available for the specified region.")
        else:
            elem_percentage = (elem_population / total_population) * 100
            other_population = total_population - elem_population
            
            # Create pie chart
            labels = ['Elementary School Age', 'Other Ages']
            sizes = [elem_population, other_population]
            colors = ['#ff9999','#66b3ff']
            explode = (0.1, 0)
            
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90)
            ax1.axis('equal')
            
            st.pyplot(fig1)
            st.write(f"Total Population: {total_population:,}")
            st.write(f"Elementary School Age Population: {elem_population:,}")
            st.write(f"Elementary School Age Percentage: {elem_percentage:.2f}%")

if __name__ == "__main__":
    main()
