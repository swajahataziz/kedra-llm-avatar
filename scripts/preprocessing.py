import csv
import re
import pandas as pd

# Percorso del file CSV
input_csv_file = './data/input/Book3.csv'
output_csv_file = './data/output/train3.csv'
output_json_file = './data/output/train.json'
output_jsonl_file = './data/output/train.jsonl'
output_txt_file = './data/output/train.txt'

# Funzione per applicare le trasformazioni al testo
def anonymize_text(text):
    pattern = r'[A-Z0-9]+\s[A-Z\s]+\b'
    replacement = 'Assistant'
    updated_text = re.sub(pattern, replacement, text)
    return updated_text

def clean_text(text):
    pattern = r"\(\s*\d+m\s*\d+s\s*\)"
    replacement = ''
    updated_text = re.sub(pattern, replacement, text)
    pattern = r"\(\s*\d+s\s*\)"
    updated_text = re.sub(pattern, replacement, updated_text)
    return updated_text

def extract_agent_visitor(text):
    pattern = r"(Assistant|Visitor):\s*(.*?)(?=\s*(?:Assistant|Visitor):|$)"
    matches = re.findall(pattern, text)
    agents = []
    visitors = []
    previous = ""
    for match in matches:
        if match[0] == "Assistant":
            if previous == "Assistant":
                if len(agents) > 0:
                    agents[-1] = agents[-1] + " " + match[1]
                else:
                    agents.append(match[1])
            else:
                agents.append(match[1])
        else:
            if previous == "Visitor":
                if len(agents) > 0:
                    visitors[-1] = visitors[-1] + " " + match[1]
                else:
                    visitors.append(match[1])
            else:
                visitors.append(match[1])
        previous = match[0]

    data = []
    max_len = max(len(agents), len(visitors))
    for i in range(max_len):
        data.append({"Assistant": agents[i] if i < len(agents) else None,
                     "Human": visitors[i] if i < len(visitors) else None})
    return pd.DataFrame(data)

def remove_start(text):
    pattern = r'(Chat Started:).+\(.[0-9]s.\)\s'
    replacement = ''
    updated_text = re.sub(pattern, replacement, text)
    return updated_text

def main():
    # Apertura del file CSV
    df = pd.read_csv(input_csv_file, sep=";")

    # Applicazione delle trasformazioni alla colonna "Body"
    df['Body'] = df['Body'].apply(anonymize_text)
    df['Body'] = df['Body'].apply(remove_start)
    df['Body'] = df['Body'].apply(clean_text)

    # new_df = df["Body"].apply(extract_agent_visitor)
    #
    # # Concatena i DataFrame risultanti
    # result_df = pd.concat(new_df.tolist(), ignore_index=True)
    #
    # result_df = result_df.dropna(subset=["Assistant", "Human"])
    #
    # result_df = result_df[['Assistant', 'Human']]
    #
    # ## Salvataggio del DataFrame trasformato in un nuovo file JSON
    # content = ''
    # for index, row in result_df.iterrows():
    #     content += f"Assistant: {row['Assistant']}\nHuman: {row['Human']}\n"
    #
    # with open(output_txt_file, 'w') as file:
    #     file.write(content)

    result_df = df[["Case: Call Reason Detail", "Body"]]

    # Salvataggio del DataFrame trasformato in un nuovo file CSV
    result_df.to_csv(output_csv_file, sep=';', index=False)
    print("Trasformazione completata. Il file CSV di output è stato creato.")

    # # Salvataggio del DataFrame trasformato in un nuovo file JSON
    # result_df[["Assistant", "Human"]].to_json(output_json_file, orient="records")
    #
    # # Salvataggio del DataFrame trasformato in un nuovo file JSONL
    # result_df[["Assistant", "Human"]].to_json(output_jsonl_file, orient="records", lines=True)

if __name__ == "__main__":
    main()