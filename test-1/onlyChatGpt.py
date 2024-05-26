import pandas as pd
import openai
import json

# Function to read CSV file
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# Function to generate checklist using OpenAI's GPT-4
def generate_checklist(chapter, working_product, standards):
    standards_list = "\n".join([f"{standard_id}: {description}" for standard_id, description in standards.items()])
    prompt = f"""
    You are a consultant specializing in compliance and security, assisting in the release of a new product. Your task is to create comprehensive checklists that ensure adherence to various standards, specifically from the ISO and SPICE frameworks, provided in a CSV format. Each checklist should focus on fulfilling the auditing requirements for these standards.

    Chapter: {chapter}
    Working Product: {working_product}
    Standards:
    {standards_list}

    For these standards, develop a checklist that answers the following questions:

    What actions must be taken to comply with the standards' requirements?
    What documentation or evidence is needed to demonstrate compliance?
    What processes or procedures should be implemented to ensure ongoing compliance?
    How should compliance be monitored and maintained over time?

    Ensure that the checklists are detailed, actionable, and aligned with best practices for compliance and security. The goal is to facilitate a smooth and thorough auditing process in the future.

    The checklist should be returned in a JSON format and must include the IDs of the standards used for each checkpoint.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a consultant specializing in compliance and security."},
            {"role": "user", "content": prompt}
        ]
    )
    
    checklist = response['choices'][0]['message']['content']
    return checklist

# Function to structure output in the required JSON format
def structure_output(df):
    grouped = df.groupby(['Chapter', 'Working product'])
    output = []

    for (chapter, working_product), group in grouped:
        standards = dict(zip(group['StandardsID'], group['Description']))
        checklist = generate_checklist(chapter, working_product, standards)
        
        output.append({
            "Chapter": chapter,
            "Working product": working_product,
            "Checklist": checklist,
            "StandardsID": list(standards.keys())
        })
    return output

# Main function
def main(file_path):
    df = read_csv(file_path)
    structured_data = structure_output(df)
    
    # Convert structured data to JSON
    json_output = json.dumps(structured_data, indent=4)
    
    return json_output

# Example usage
file_path = '/Users/carlos/Desktop/Tesis/Template/rag-templates/datasets/SWArchtitecture-classification.csv'  # Replace with the actual path to your CSV file
json_output = main(file_path)
print(json_output)
