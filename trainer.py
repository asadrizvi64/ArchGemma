# Import necessary libraries
from peft import LoraConfig
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import transformers
from trl import SFTTrainer
from tqdm import tqdm
from datasets import Dataset

hf_token = "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"

data= "./converted_data.json"
with open(data, 'r') as file:
    data = json.load(file)

lora_config = LoraConfig(
    r=8,
    target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
    task_type="CAUSAL_LM",
)

model_id = "google/gemma-2b"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token)
model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map={"": 0}, token=hf_token)


def formatting_func(examples):  
    texts = []

    for example in tqdm(examples):
        text = f"Instruction: {example['Q']} \n Output: {example['A']}<eos>"
        texts.append(text)

    return texts

def formatting_func2(examples):  
    texts = []

    for example in tqdm(examples["text"]):
        texts.append(example)
    
    return texts

formatted_data = formatting_func(data)
dataset = Dataset.from_dict({"text": formatted_data})

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=transformers.TrainingArguments(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        num_train_epochs=5,
        learning_rate=2e-5,
        fp16=False,
        logging_steps=200,
        output_dir="outputs",
        optim="paged_adamw_8bit"
    ),
    peft_config=lora_config,
    formatting_func=formatting_func2,
)

trainer.train()

# Save the model
trainer.save_model('./Model')

# # ### Loading and Using the Fine-Tuned Model

# model_id = "./Model"
# bnb_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.bfloat16
# )

# tokenizer = AutoTokenizer.from_pretrained(model_id)
# model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map={"": 0})
