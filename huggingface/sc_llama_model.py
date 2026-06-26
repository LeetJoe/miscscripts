import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

def extract_embeddings(tsv_path, model_name, output_path, batch_size=32):
    # 1. Load TSV and sort by ID to ensure strict matrix indexing
    df = pd.read_csv(tsv_path, sep='\t')
    df = df.sort_values(by='id').reset_index(drop=True)
    names = df['name'].tolist()
    
    # 2. Initialize LLaMA Tokenizer and Base Model
    print(f"Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # CRITICAL: Configure Left-Padding
    tokenizer.padding_side = "left"
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    # Load model in half-precision (FP16/BF16) to save VRAM
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        torch_dtype=torch.float16, 
        device_map="auto"
    )
    model.eval()
    
    all_embeddings = []
    
    # 3. Batch processing
    print(f"Extracting embeddings from {tsv_path}...")
    for i in tqdm(range(0, len(names), batch_size)):
        batch_names = names[i:i + batch_size]
        
        # Append EOS token to the end of each text string as per Method 1
        batch_texts = [f"{text}{tokenizer.eos_token}" for text in batch_names]
        
        # Tokenize with Left-Padding
        inputs = tokenizer(
            batch_texts, 
            padding=True, 
            return_tensors="pt"
        ).to(device)
        
        with torch.no_grad():
            outputs = model(**inputs, output_hidden_states=True)
            # Shape: [batch_size, seq_len, hidden_dim]
            last_hidden_states = outputs.last_hidden_state
            
            # Since we used left-padding, the actual text ends exactly at the last index (-1)
            # Grab the last token's hidden state for the whole batch
            batch_embeddings = last_hidden_states[:, -1, :].cpu()
            all_embeddings.append(batch_embeddings)
    # 4. Concatenate and save as a single tensor matrix [Num_Elements, Hidden_Dim]
    embedding_matrix = torch.cat(all_embeddings, dim=0)
    torch.save(embedding_matrix, output_path)
    print(f"Successfully saved tensor of shape {embedding_matrix.shape} to {output_path}\n")

# --- Execution ---
if __name__ == "__main__":
    # Replace with your local path or official HuggingFace path (e.g., "meta-llama/Meta-Llama-3-8B")
    MODEL_PATH = "meta-llama/Meta-Llama-3-8B" 
    
    extract_embeddings("entities.tsv", MODEL_PATH, "entity_llama_embeddings.pt")
    extract_embeddings("relations.tsv", MODEL_PATH, "relation_llama_embeddings.pt")
