"""
Create and push a new configuration and tokenizer for the Llama v2 7b model trained on The Pile dataset to the Hugging Face Hub.
This script loads the configuration of the Llama v2 7b model, modifies it by setting the number of key-value attention heads to 8
and the vocabulary size to 49152, and pushes the new configuration to the Hub under the name "llama-v2-7b-the-pile" in the "HuggingFaceBR4".
It also loads the tokenizer from the local path "/fsx/loubna/starcoder-tokenizer/tokenizer-pile", and pushes it to the Hub.
Then you could use "HuggingFaceBR4/llama-v2-7b-the-pile" as a model name to load the model and tokenizer from the Hub.

Note: This script is for the purpose of creating a new configuration and tokenizer for the Llama v2 7b model trained on The Pile dataset.
If there is already a configuration and tokenizer for this model on the Hub, you could still call this script but it will replace the existing
configuration and tokenizer.

Usage: python create_hf_config_llama2_the_pile.py
"""
from transformers import AutoConfig, AutoTokenizer

config = AutoConfig.from_pretrained("meta-llama/Llama-2-7b-hf")
config.num_key_value_heads = 8
config.vocab_size = 49152
config.push_to_hub("HuggingFaceBR4/llama-v2-7b-the-pile", private=True)

tokenizer = AutoTokenizer.from_pretrained("/fsx/loubna/starcoder-tokenizer/tokenizer-pile")
tokenizer.push_to_hub("HuggingFaceBR4/llama-v2-7b-the-pile", private=True)
